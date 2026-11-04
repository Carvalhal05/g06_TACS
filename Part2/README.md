# Part II · T1, classical baseline and validation

This folder holds T1 (Problem DSL → Solution DSL), the classical baseline and the validation of
the quantum results against it. T2 (Solution DSL → BESSER quantum model), the Qiskit generation and
the runs are not here.

## How to run

Requires Python 3.11 or later and `pip install besser` (tested with BESSER 8.8.0). Run from this folder:

```
python run_t1.py                      # T1 + baseline on I1-I5 -> generated/
python -m unittest test_part2 -v      # 16 tests
python validation.py I3 counts.json   # compare a Qiskit run of I3 with the baseline
```

| File | What it does |
|---|---|
| [metamodels.py](metamodels.py) | Loads both metamodels and the hand-built example from [Part1/tacs262_assignment_project-4.py](../Part1/tacs262_assignment_project-4.py), so Part II uses exactly the Part I metamodels. |
| [checks.py](checks.py) | The 36 OCL invariants of both metamodels, as Python checks with the same names (see [OCL checks](#ocl-checks)). |
| [t1_problem_to_cnf.py](t1_problem_to_cnf.py) | **T1**: feature model + selection request → CnfFormula with Variables, Clauses, Literals and SolverConfig. |
| [baseline.py](baseline.py) | **Classical baseline**: brute force over all 2ⁿ assignments, plus the Grover round count and success probability. |
| [instances.py](instances.py) | Problem DSL object models of the test instances I1–I5 of [Part1/Instances.md](../Part1/Instances.md). |
| [run_t1.py](run_t1.py) | Runs T1 and the baseline on every instance and writes `generated/`. |
| [validation.py](validation.py) | **Validation**: decodes the counts of a Grover run into features and compares them with the baseline. |
| [test_part2.py](test_part2.py) | Tests of all of the above. |
| [generated/](generated) | T1 outputs as B-UML files (written by BESSER's code builder, input for T2) and [T1_report.md](generated/T1_report.md). Do not edit by hand. |

## T1 rules

Each rule is implemented, with its reference, in [t1_problem_to_cnf.py](t1_problem_to_cnf.py), and
[generated/T1_report.md](generated/T1_report.md) lists the rule and source elements of every clause
of every instance. P is a parent feature, C a child, M₁…Mₖ the members of a group.

| Rule | Problem DSL element | Clauses | Reference |
|---|---|---|---|
| — | Feature | one Variable | [B05] §3 |
| R1 | FeatureModel root | (root) | [B05] §3 "Mapping Grammars" (root = true); [T07] p. 96 |
| R2 | Feature with isMandatory = true | (¬P ∨ C) | [B05] §3 formula (2) P ⇔ t; [T07] Fig. 2 "and" |
| R3 | every non-root Feature | (¬C ∨ P) | [B05] §3 formulas (2), (3); [T07] Fig. 2 |
| R4 | Or / Xor group | (¬P ∨ M₁ ∨ … ∨ Mₖ) | [B05] §3 "Mapping Productions"; [T07] Fig. 2 "or", "alternative" |
| R5 | Xor group | (¬Mᵢ ∨ ¬Mⱼ) for each pair | [T07] Fig. 2 atmost1; [B05] §3 choose1 |
| R6 | RequiresConstraint A → B | (¬A ∨ B) | [B05] §3, "non-grammar constraints" (conjoined to the formula) |
| R7 | ExcludesConstraint A, B | (¬A ∨ ¬B) | [B05] §3, "non-grammar constraints" |
| R8 | FeatureChoice REQUIRED / EXCLUDED | (X) / (¬X) | [B05] §4 (user selections as LTMS assumptions) |

R3 is generated once per child even though optional features, mandatory features and group members
all imply it. Together, R3 and R4 give the "⇔" of [B05]/[T07]. Identical clauses are written only once.

## Decisions taken in Part II (to be reviewed by the group)

| Decision | Choice | Why |
|---|---|---|
| Variable index (= qubit) | Depth-first pre-order of the feature tree from the root; children in alphabetical order of `id` | Deterministic (B-UML links are unordered), and each parent comes before its children. The hand-built example numbered the variables by hand, so T1's indices differ from it. The clauses are the same. |
| Clause order and ids | Rules in the order of the tree walk, then requires, excludes, choices; ids c1…cm | Same clauses as the hand-built example (checked by a test); only the numbering differs. |
| `shots` | Parameter of T1 (`transform(..., shots=1024)`, `run_t1.py [shots]`), stored in SolverConfig | Solver choices are not hard-coded in the transformation; T2 reads them from the model. |
| `rounds` | ⌊π/4 · √(2ⁿ/M)⌋ [BBHT98], M from the classical baseline | Same formula as Part I (Example.md, Instances.md). |
| `rounds` when M = 0 (I5) | 1 | With no solution the oracle marks nothing, so every round leaves the uniform superposition unchanged and the number of rounds does not matter. 1 is the smallest value allowed by the OCL rule `PositiveExecutionParams` (rounds > 0). The run must then measure no valid configuration. |
| Classical baseline | Brute force over the 2ⁿ assignments, computed twice: on the CNF, and directly on the feature model without the CNF | Exact for n ≤ 12 (`QubitLimit`). The second computation checks T1 itself: for every instance both give the same configurations. |
| Input checking | T1 refuses an input that breaks a Problem DSL invariant and checks its output against the Solution DSL invariants | The transformation is only defined for well-formed models. |

## For T2 and the runs

- The input of T2 is a Solution DSL model: either a file in `generated/` (load it with
  `run_t1.load_solution_model(path)`) or the result of `t1_problem_to_cnf.transform(problem_model)`.
- Variable `index` i is search qubit i. `SolverConfig.rounds` and `SolverConfig.shots` are the
  Grover parameters.
- For `validation.py`, measure search qubit i into classical bit i, so that Qiskit's bitstring has
  Variable 0 as its rightmost character. If there are several classical registers, the search
  register must be the first one. Save `result.get_counts()` as JSON and run
  `python validation.py <instance> counts.json`. The report gives the measured and theoretical
  success probability, the distinct valid configurations found, the most frequent configuration in
  feature names and the oracle calls (k per shot, k · shots in total) against the 2ⁿ evaluations of
  brute force.
- Qubit budget: with one ancilla per clause plus an output qubit, the instances need n + m + 1 =
  13, 23, 32, 35 and 32 qubits. Only I1 fits in about 20 qubits, so T2 has to reuse ancillas or
  use fewer of them.

The validation was tested with counts sampled from the ideal Grover distribution (sin²((2k+1)θ)),
not with a quantum run; the real counts come from the code generated by T2/T3.

## OCL checks

BESSER's OCL parser accepts all 36 constraints of Part I. The BESSER OCL evaluator (`bocl` 1.0.4)
cannot evaluate most of them: it raises Python syntax errors on `implies`, `oclIsTypeOf` and
`forAll`, resolves `isUnique(id)` to Python's built-in `id`, and reports `ContigousIndexes` as false
for indices 0…10. [checks.py](checks.py) therefore implements each invariant in Python under its OCL
name; a test checks that every OCL constraint of both metamodels has a check.

## References

- [B05] D. Batory, "Feature models, grammars, and propositional formulas", SPLC 2005, LNCS 3714, pp. 7–20.
- [T07] S. Thaker, D. Batory, D. Kitchin, W. Cook, "Safe composition of product lines", GPCE 2007, pp. 95–104.
- [BBHT98] M. Boyer, G. Brassard, P. Høyer, A. Tapp, "Tight bounds on quantum searching", Fortschritte der Physik 46, 1998.
- [S] J. Pascoal Faria, J. Cunha, "Quantum computing: a brief introduction", TACS 2026/27 slides, 2026 (CNF).
