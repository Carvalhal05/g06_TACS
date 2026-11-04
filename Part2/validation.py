"""Validation: compare the measurements of a Grover run with the classical baseline.

Input: the Solution DSL model produced by T1 (with its SolverConfig), optionally the Problem DSL
model (for feature names), and the counts of the quantum run in Qiskit format
(`result.get_counts()`: {bitstring: number of shots}).

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


def validate(solution_model, counts, problem_model=None):
    """Compare `counts` with the classical baseline. Returns a dict of results (see `report`)."""
    names, clauses = baseline.read_cnf(solution_model)
    (cfg,) = objects_of(solution_model, mm.SolverConfig)
    n, k = len(names), attr(cfg, "rounds")
    expected = baseline.cnf_solutions(solution_model)          # classical baseline
    m = len(expected)

    shots = sum(counts.values())
    found = {}                                                  # valid configuration -> shots
    for key, c in counts.items():
        config = decode(key, names)
        bits = tuple(name in config for name in names)
        if baseline.satisfies(bits, clauses):
            found[config] = found.get(config, 0) + c
    valid_shots = sum(found.values())
    measured = valid_shots / shots if shots else 0.0
    theoretical = baseline.success_probability(n, m, k)

    feature_name = {}
    if problem_model is not None:
        feature_name = {attr(f, "id"): attr(f, "name") for f in objects_of(problem_model, mm.Feature)}

    def terms(config):
        return sorted(feature_name.get(x, x) for x in config)

    best = max(counts, key=counts.get) if counts else None
    return {
        "variables": n, "clauses": len(clauses), "states": 2 ** n,
        "knownSolutions": attr(cfg, "knownSolutions"), "baselineSolutions": m,
        "rounds": k, "shots": shots,
        "validShots": valid_shots, "measuredSuccess": measured, "theoreticalSuccess": theoretical,
        "foundSolutions": len(found), "allFoundAreBaselineSolutions": set(found) <= expected,
        "missingSolutions": [terms(s) for s in expected - set(found)],
        "mostFrequent": (best, counts[best], terms(decode(best, names)),
                         decode(best, names) in expected) if best else None,
        "solutionsByShots": sorted(((terms(s), c) for s, c in found.items()), key=lambda t: -t[1]),
        # oracle calls: Grover applies the oracle k times per shot; brute force evaluates the formula
        # on all N assignments to know M.
        "oracleCallsPerShot": k, "oracleCallsTotal": k * shots,
        "expectedOracleCallsPerSolution": (k / theoretical) if theoretical > 0 else None,
        "classicalEvaluations": 2 ** n,
    }


def report(instance, r):
    """Markdown summary of the results of `validate`."""
    lines = [
        f"### {instance}",
        "",
        "| Quantity | Value |",
        "|---|---|",
        f"| Variables n / clauses m / states N | {r['variables']} / {r['clauses']} / {r['states']} |",
        f"| Solutions M (classical brute force) | {r['baselineSolutions']} "
        f"(SolverConfig.knownSolutions = {r['knownSolutions']}) |",
        f"| Grover rounds k / shots | {r['rounds']} / {r['shots']} |",
        f"| Success probability, measured | {r['measuredSuccess']:.3f} ({r['validShots']} of {r['shots']} shots) |",
        f"| Success probability, theoretical sin²((2k+1)θ) | {r['theoreticalSuccess']:.3f} |",
        f"| Distinct valid configurations measured | {r['foundSolutions']} of {r['baselineSolutions']} |",
        f"| Every measured valid configuration is a baseline solution | {r['allFoundAreBaselineSolutions']} |",
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
    _desc, problem, _request = instances.all_instances()[inst]
    (generated,) = OUT.glob(f"{inst}_*.py")       # the T1 output that T2 used
    with open(path, encoding="utf-8") as fh:
        print(report(inst, validate(load_solution_model(generated), json.load(fh), problem)))
