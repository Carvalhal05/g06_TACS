# Part II 

This folder contains the complete implementation of the Part II chain: **T1** (Problem DSL → Solution DSL), **T2** (Solution DSL → Quantum Circuit DSL), **T3** (BESSER Qiskit code generation), Aer simulation, classical baseline comparison, and validation.

## Setup & How to Run

Requires Python 3.12. Set up your virtual environment and install the required dependencies by running:

```
cd Part2
python3.12 -m venv .venv
source .venv/bin/activate
git clone https://github.com/jacomecunha/BESSER.git
python -m pip install -e ./BESSER
python -m pip install qiskit==2.6.2 qiskit-aer==0.18.2
```

Once installed, run the commands from this folder:

```
python run_t1.py                      # Run T1 + baseline on instances I1–I5 -> generated/
python -m unittest test_part2 -v      # Run unit tests
python run_all.py                     # Run end-to-end chain (T1 → T2 → T3 → Aer Simulation)
```

## Project Structure

| File | Description |
|---|---|
| `metamodels.py` | Loads metamodels and the Part I hand-built example. |
| `checks.py` | Implementation of OCL invariants in Python. |
| `t1_problem_to_cnf.py` | **T1 Transformation**: Feature model + request → CNF formula. |
| `t2_cnf_to_quantum.py` | **T2 Transformation**: CNF formula + SolverConfig → Grover quantum circuit. |
| `baseline.py` | Classical brute-force baseline ($2^n$ states), Grover rounds, and success probability. |
| `instances.py` | Test instances I1–I5. |
| `run_t1.py` | Executes T1 across all instances and builds `generated/`. |
| `run_all.py` | Executes the full end-to-end chain (T1 → T2 → T3 → Qiskit Aer simulation → Validation). |
| `validation.py` | **Validation**: decodes Grover simulation counts and compares them with the baseline. |
| `test_part2.py` | Unit tests for the pipeline. |
| `generated/` | Generated B-UML models, T1 report, execution logs, and Qiskit circuits (do not edit manually). |
| `AILog.md` | LLM usage log for Part II. |
| `ReportPart2.pdf` | Group report for Part II. |

## Design decisions (to be reviewed by the group)

| Decision | Choice | Why |
|---|---|---|
| Variable index (= qubit) | Depth-first pre-order of the feature tree from the root; children in alphabetical order of `id` | Deterministic (B-UML links are unordered), and each parent comes before its children. The hand-built example of Part I numbered the variables by hand, so T1's indices differ from it; the clauses are the same (checked by a test). |
| Clause order and ids | Rules in the order of the tree walk, then requires, excludes, choices; ids `c1…cm`; identical clauses written once | Same clauses as the hand-built example; only the numbering differs. |
| `shots` | Parameter of T1 (`transform(..., shots=1024)`, `run_all.py [shots]`), stored in `SolverConfig`; T3 reads it from there | Solver choices are not hard-coded in the transformations. |
| `rounds` | ⌊π/4 · √(2ⁿ/M)⌋ [Boyer et al. 1998], M from the classical baseline | Same formula as in Part I (Example.md, Instances.md). |
| `rounds` when M = 0 (I5) | 1 | With no solution the oracle marks nothing, so every round leaves the uniform superposition unchanged and the number of rounds does not matter. 1 is the smallest value allowed by the OCL rule `PositiveExecutionParams` (rounds > 0). |
| Oracle ancillas | A binary counter of violated clauses (⌈log₂(K+1)⌉ qubits) instead of one ancilla per clause [Alasow et al. 2022]; unit clauses act directly as controls on the search qubits | With one ancilla per clause the instances would need n + m + 1 = 13, 23, 32, 35 and 32 qubits; with the counter they need at most 17. |
| Classical baseline | Brute force over the 2ⁿ assignments, computed twice: on the CNF, and directly on the feature model without the CNF | Exact for n ≤ 12 (`QubitLimit`). The second computation is independent of T1, so it checks T1 itself. |
| Input checking | T1 refuses an input that breaks a Problem DSL invariant and checks its output against the Solution DSL invariants | The transformation is only defined for well-formed models. |
| Answer in domain terms | The generated `qiskit_circuit.py` prints the circuit and the counts; `run_all.py` decodes the counts into features using only the models (bit i → Variable i → Feature with that id) and writes the answer to `generated/results.md` | Generated code must not be edited by hand, and BESSER's Qiskit generator writes only the circuit and its execution, so the decoding cannot be placed inside the generated script. |
