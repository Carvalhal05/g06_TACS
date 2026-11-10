# Part II 

This folder contains the complete implementation of the Part II chain: **T1** (Problem DSL → Solution DSL), **T2** (Solution DSL → Quantum Circuit DSL), **T3** (BESSER Qiskit code generation), Aer simulation, classical baseline comparison, and validation.

## Setup & How to Run

Requires Python 3.12. Set up your virtual environment and install the required dependencies by running:

```
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install besser==8.8.0
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

## References

- [B05] D. Batory, "Feature models, grammars, and propositional formulas", SPLC 2005, LNCS 3714, pp. 7–20.
- [T07] S. Thaker, D. Batory, D. Kitchin, W. Cook, "Safe composition of product lines", GPCE 2007, pp. 95–104.
- [BBHT98] M. Boyer, G. Brassard, P. Høyer, A. Tapp, "Tight bounds on quantum searching", Fortschritte der Physik 46, 1998.
- [S] J. Pascoal Faria, J. Cunha, "Quantum computing: a brief introduction", TACS 2026/27 slides, 2026 (CNF).
