"""Validation: compare the measurements of a Grover run with the classical baseline.

Input: the Solution DSL model produced by T1 (with its SolverConfig), the Problem DSL model and the
name of its selection request, and the counts of the quantum run in Qiskit format
(`result.get_counts()`: {bitstring: number of shots}).

The baseline is computed on the feature model itself (`baseline.feature_model_configurations`),
without the CNF produced by T1, so it is independent of both transformations:
  - the CNF of T1 must have exactly the baseline configurations as solutions (checks T1);
  - SolverConfig.knownSolutions must equal the number of baseline configurations;
  - the share of shots that are baseline configurations must match the theoretical success
    probability within sampling noise, and the most frequent measurement must be a baseline
    configuration (checks T2 and the generated code).
Without a problem model, the baseline falls back to the CNF and the first check is not possible.

Bit order: Qiskit writes bitstrings with qubit 0 on the right. The search qubit of Variable i must be
measured into classical bit i, so character -1-i of the key is the value of Variable i. If the
circuit has more than one classical register, the search register must be the first one (its bits
are the rightmost group of the key).

Decoding uses only the models: bit i -> Variable with index i -> its name (the feature id) -> the
Feature with that id in the problem model.

Usage from the command line, with the counts saved as JSON:
    python validation.py I3 counts_I3.json
"""

import json
import sys

import metamodels as mm
from metamodels import attr, linked, objects_of
import baseline


def decode(bitstring, variable_names):
    """Assignment encoded by a Qiskit bitstring, as the frozenset of names of true variables."""
    bits = bitstring.replace(" ", "")[::-1][:len(variable_names)]
    return frozenset(name for name, b in zip(variable_names, bits) if b == "1")


def within_sampling_noise(measured, theoretical, shots):
    """True if `measured` is within 3 standard deviations of a binomial(shots, theoretical) share.

    A floor of 0.01 covers theoretical probabilities of exactly 0 or 1, where the deviation is 0.
    """
    sigma = (theoretical * (1 - theoretical) / shots) ** 0.5 if shots else 0.0
    return abs(measured - theoretical) <= max(3 * sigma, 0.01)


def validate(solution_model, counts, problem_model=None, request_name=None):
    """Compare `counts` with the classical baseline. Returns a dict of results (see `report`)."""
    names, clauses = baseline.read_cnf(solution_model)
    (cfg,) = objects_of(solution_model, mm.SolverConfig)
    n, k = len(names), attr(cfg, "rounds")
    cnf_solutions = baseline.cnf_solutions(solution_model)
    if problem_model is not None:       # classical baseline, independent of T1 and T2
        expected = baseline.feature_model_configurations(problem_model, request_name)
    else:
        expected = cnf_solutions
    m = len(expected)

    shots = sum(counts.values())
    found = {}                                                  # valid configuration -> shots
    for key, c in counts.items():
        config = decode(key, names)
        if config in expected:
            found[config] = found.get(config, 0) + c
    valid_shots = sum(found.values())
    measured = valid_shots / shots if shots else 0.0
    theoretical = baseline.success_probability(n, m, k)
    best = max(counts, key=counts.get) if counts else None
    best_is_valid = best is not None and decode(best, names) in expected

    checks = {
        "cnfMatchesBaseline": cnf_solutions == expected,
        "knownSolutionsMatchBaseline": attr(cfg, "knownSolutions") == m,
        "successWithinSamplingNoise": within_sampling_noise(measured, theoretical, shots),
        "mostFrequentIsValid": best_is_valid if m > 0 else True,
    }

    feature_name = {}
    if problem_model is not None:
        feature_name = {attr(f, "id"): attr(f, "name") for f in objects_of(problem_model, mm.Feature)}

    def terms(config):
        return sorted(feature_name.get(x, x) for x in config)

    return {
        "variables": n, "clauses": len(clauses), "states": 2 ** n,
        "knownSolutions": attr(cfg, "knownSolutions"), "baselineSolutions": m,
        "baselineSource": "feature model" if problem_model is not None else "CNF",
        "rounds": k, "shots": shots,
        "validShots": valid_shots, "measuredSuccess": measured, "theoreticalSuccess": theoretical,
        "foundSolutions": len(found),
        "checks": checks, "passed": all(checks.values()),
        "missingSolutions": [terms(s) for s in expected - set(found)],
        "mostFrequent": (best, counts[best], terms(decode(best, names)), best_is_valid) if best else None,
        "solutionsByShots": sorted(((terms(s), c) for s, c in found.items()), key=lambda t: -t[1]),
        # oracle calls: Grover applies the oracle k times per shot; brute force evaluates the formula
        # on all N assignments to know M.
        "oracleCallsPerShot": k, "oracleCallsTotal": k * shots,
        "expectedOracleCallsPerSolution": (k / theoretical) if theoretical > 0 else None,
        "classicalEvaluations": 2 ** n,
    }


CHECK_LABELS = {
    "cnfMatchesBaseline": "solutions of the T1 CNF = baseline configurations",
    "knownSolutionsMatchBaseline": "SolverConfig.knownSolutions = M",
    "successWithinSamplingNoise": "measured success within 3σ of the theoretical one",
    "mostFrequentIsValid": "most frequent measurement is a valid configuration (when M > 0)",
}


def report(instance, r):
    """Markdown summary of the results of `validate`."""
    lines = [
        f"### {instance}",
        "",
        "| Quantity | Value |",
        "|---|---|",
        f"| Variables n / clauses m / states N | {r['variables']} / {r['clauses']} / {r['states']} |",
        f"| Solutions M (classical brute force on the {r['baselineSource']}) | {r['baselineSolutions']} "
        f"(SolverConfig.knownSolutions = {r['knownSolutions']}) |",
        f"| Grover rounds k / shots | {r['rounds']} / {r['shots']} |",
        f"| Success probability, measured | {r['measuredSuccess']:.3f} ({r['validShots']} of {r['shots']} shots) |",
        f"| Success probability, theoretical sin²((2k+1)θ) | {r['theoreticalSuccess']:.3f} |",
        f"| Distinct valid configurations measured | {r['foundSolutions']} of {r['baselineSolutions']} |",
        *[f"| Check: {CHECK_LABELS[name]} | {'yes' if ok else 'NO'} |" for name, ok in r["checks"].items()],
        f"| Oracle calls: per shot / total | {r['oracleCallsPerShot']} / {r['oracleCallsTotal']} |",
        f"| Classical brute force: formula evaluations | {r['classicalEvaluations']} |",
    ]
    if r["mostFrequent"]:
        key, c, terms, ok = r["mostFrequent"]
        lines.append(f"| Most frequent bitstring | `{key}` ({c} shots): {', '.join(terms) or '(none)'}"
                     f" — {'valid' if ok else 'not valid'} |")
    if r["missingSolutions"]:
        lines.append(f"| Baseline solutions never measured | {len(r['missingSolutions'])} |")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    import instances
    from run_t1 import OUT, load_solution_model
    if len(sys.argv) != 3:
        sys.exit("usage: python validation.py <instance id, e.g. I3> <counts.json>")
    inst, path = sys.argv[1], sys.argv[2]
    _desc, problem, request = instances.all_instances()[inst]
    (generated,) = OUT.glob(f"{inst}_*.py")       # the T1 output that T2 used
    with open(path, encoding="utf-8") as fh:
        print(report(inst, validate(load_solution_model(generated), json.load(fh), problem, request)))
