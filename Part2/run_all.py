"""The whole chain for every test instance, with one command:

    python run_all.py [shots] [instance ...]      e.g.  python run_all.py        (all, 1024 shots)
                                                        python run_all.py 2048 I1 I3

For each instance of instances.py:
  1. T1: Problem DSL model -> Solution DSL model (CNF + SolverConfig)      t1_problem_to_cnf.py
  2. T2: Solution DSL model -> BESSER quantum circuit model (Grover)        t2_cnf_to_quantum.py
  3. T3: BESSER's Qiskit generator writes generated/<instance>/qiskit_circuit.py
  4. the generated script is run as it is (Aer simulator); its counts are saved to counts.json
  5. validation: the counts are decoded into features and compared with the classical baseline
  6. the answer is written in domain terms: the product (features selected and left out) that
     answers the selection request, or that no product can satisfy it

Results: generated/results.md.
"""

import contextlib
import io
import json
import runpy
import sys
import time

from besser.generators.qiskit.qiskit_generator import QiskitGenerator

import metamodels as mm
from metamodels import attr, linked, objects_of
import baseline
import instances
import run_t1
import t1_problem_to_cnf as t1
import t2_cnf_to_quantum as t2
import validation

OUT = run_t1.OUT


def run_instance(inst, problem, request, shots):
    """T1 -> T2 -> T3 -> execution -> validation for one instance. Returns (results, layout, seconds, domain_answer)."""
    solution, _trace = t1.transform(problem, shots=shots, request_name=request)
    circuit, layout = t2.transform(solution)

    (cfg,) = objects_of(solution, mm.SolverConfig)
    folder = OUT / inst
    folder.mkdir(parents=True, exist_ok=True)
    quiet = io.StringIO()
    with contextlib.redirect_stdout(quiet):
        # T3 The number of shots is read from the SolverConfig of the model.
        QiskitGenerator(circuit, output_dir=str(folder), shots=attr(cfg, "shots")).generate()

    # Run the generated script unchanged and take the counts it computes. What it prints (the
    # circuit drawing and the raw counts) goes to run_output.txt.
    start = time.time()
    printed = io.StringIO()
    with contextlib.redirect_stdout(printed):
        scope = runpy.run_path(str(folder / "qiskit_circuit.py"))
    seconds = time.time() - start
    (folder / "run_output.txt").write_text(printed.getvalue(), encoding="utf-8")
    counts = dict(scope["counts"])
    (folder / "counts.json").write_text(json.dumps(counts, indent=1, sort_keys=True), encoding="utf-8")

    results = validation.validate(solution, counts, problem, request)
    return results, layout, seconds, domain_answer(problem, request, solution, results)


def domain_answer(problem, request, solution, r):
    """The result of the run in domain terms (product line, request, product), read from the models.

    Measured bit i -> Variable with index i (Solution DSL) -> Feature with that id (Problem DSL).
    The features are listed in the order of the feature tree (the variable order of T1).
    """
    (fm,) = objects_of(problem, mm.FeatureModel)
    name = {attr(f, "id"): attr(f, "name") for f in linked(fm, "features")}
    lines = [f"Product line: {attr(fm, 'name')}. No selection request: any valid product."]
    requests = [q for q in linked(fm, "requests") if attr(q, "name") == request] if request else []
    if requests:
        (req,) = requests
        asked = {"REQUIRED": [], "EXCLUDED": []}
        for ch in linked(req, "choices"):
            asked[attr(ch, "type")].append(name[attr(linked(ch, "feature")[0], "id")])
        wish = "; ".join(f"{label} {', '.join(sorted(feats))}" for label, feats in
                         (("with", asked["REQUIRED"]), ("without", asked["EXCLUDED"])) if feats)
        lines = [f"Product line: {attr(fm, 'name')}. Request \"{request}\": a product {wish}."]

    variables, _clauses = baseline.read_cnf(solution)          # feature ids, in qubit order
    if r["baselineSolutions"] == 0:
        lines.append("Answer: no product of this product line satisfies the request "
                     f"(none of the {r['shots']} measurements is a valid configuration).")
    elif r["mostFrequent"] is None:
        lines.append("Answer: no measurement was made (the run produced no counts).")
    elif not r["mostFrequent"][3]:
        lines.append("Answer: the most frequent measurement is not a valid product (the run failed).")
    else:
        chosen = validation.decode(r["mostFrequent"][0], variables)
        lines.append("Answer, a valid product: " + ", ".join(name[v] for v in variables if v in chosen) + ".")
        lines.append("Features left out: " + (", ".join(name[v] for v in variables if v not in chosen) or "none") + ".")
        if r["baselineSolutions"] > 1:
            lines.append(f"It is one of {r['baselineSolutions']} valid products; the run measured "
                         f"{r['foundSolutions']} of them (listed below).")
    return lines


def main(argv):
    shots = int(argv[0]) if argv and argv[0].isdigit() else 1024
    wanted = [a for a in argv if not a.isdigit()]
    all_instances = instances.all_instances()
    unknown = [w for w in wanted if w not in all_instances]
    if unknown:
        sys.exit(f"unknown instance(s) {unknown}; available: {list(all_instances)}")

    run_t1.run(shots)                       # T1 outputs as B-UML files + T1_report.md
    summary = ["| Instance | n | Qubits (search + counter + output) | M | Rounds k | P measured | P theoretical "
               "| Solutions found | Oracle calls per shot | Brute-force evaluations | Result |",
               "|---|---|---|---|---|---|---|---|---|---|---|"]
    sections = []
    domain = []                             # the answers in domain terms, one block per instance
    for inst, (desc, problem, request) in all_instances.items():
        if wanted and inst not in wanted:
            continue
        r, layout, seconds, answer = run_instance(inst, problem, request, shots)
        domain += [f"### {inst} · {desc}", "", *[f"- {line}" for line in answer], ""]
        qubits = len(layout["search"]) + len(layout["counter"]) + 1
        ok = r["passed"]
        summary.append(
            f"| {inst} | {r['variables']} | {qubits} ({len(layout['search'])} + {len(layout['counter'])} + 1) "
            f"| {r['baselineSolutions']} | {r['rounds']} | {r['measuredSuccess']:.3f} | {r['theoreticalSuccess']:.3f} "
            f"| {r['foundSolutions']} of {r['baselineSolutions']} | {r['oracleCallsPerShot']} "
            f"| {r['classicalEvaluations']} | {'OK' if ok else 'FAILED'} |")
        sec = [validation.report(f"{inst} · {desc}", r).rstrip(), ""]
        if r["solutionsByShots"]:
            sec += ["Valid configurations measured (shots):", ""]
            sec += [f"- {', '.join(terms)} ({c})" for terms, c in r["solutionsByShots"]]
        else:
            sec += ["No valid configuration was measured: the request cannot be satisfied."
                    if r["baselineSolutions"] == 0 else "No valid configuration was measured."]
        sec += ["", f"Generated code: `{inst}/qiskit_circuit.py` · counts: `{inst}/counts.json` · "
                    f"simulation time: {seconds:.1f} s", ""]
        sections.append("\n".join(sec))

    text = "\n".join([
        "# Results of the chain and validation against the classical baseline", "",
        "Written by `run_all.py`; do not edit by hand. Measured values change slightly from run to run",
        "(sampling noise).", "",
        "M is counted by brute force over the 2ⁿ assignments directly on the feature model, without the",
        "CNF of T1 (classical baseline, independent of T1 and T2). P measured is the share of shots that",
        "gave a valid configuration; P theoretical is sin²((2k+1)θ) with sin²θ = M/2ⁿ (Boyer et al., 1998).",
        "Result is OK when (1) the solutions of the T1 CNF are exactly the baseline configurations,",
        "(2) SolverConfig.knownSolutions = M, (3) P measured is within 3σ of P theoretical (binomial",
        "sampling noise), and (4) if M > 0, the most frequent measurement is a valid configuration.", "",
        "## Results in domain terms", "", *domain,
        "## Validation against the classical baseline", "",
        *summary, "", *sections])
    (OUT / "results.md").write_text(text, encoding="utf-8")
    print(text)
    print(f"written to {OUT / 'results.md'}")
    return 0 if all("FAILED" not in row for row in summary) else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main(sys.argv[1:]))