## TACS — Grupo G6

| Up number | Name| Email |
|---|---|---|
| 202305274 | Ana Carolina Copolecchia Carvalhal | up202305274@edu.fe.up.pt |
| 202306063 | João Gonçalves Taveira | up202306063@edu.fe.up.pt |
| 202305891 | Rodrigo Jorge do Rego Rocha | up202305891@edu.fe.up.pt |
| 202109775 | André Pinto de Sousa | up202109775@edu.fe.up.pt |

Problem B1: product configuration from a feature model (SAT / CNF, Grover search). Stack: BESSER.

## Part I deliverables

| Deliverable | Where |
|---|---|
| Concept list, Problem DSL (with mapping to the Solution DSL and references) | [Part1/images/problem_dsl_table.png](Part1/images/problem_dsl_table.png) |
| Concept list, Solution DSL | [Part1/images/solution_dsl_table.png](Part1/images/solution_dsl_table.png) |
| Problem DSL metamodel with OCL | [Part1/tacs262_assignment_project-4.py](Part1/tacs262_assignment_project-4.py) (model `Problem_DSL`), [Part1/images/problemDSL.png](Part1/images/problemDSL.png) |
| Solution DSL metamodel with OCL | [Part1/tacs262_assignment_project-4.py](Part1/tacs262_assignment_project-4.py) (model `Solution_DSL`), [Part1/images/SolutionDSL.png](Part1/images/SolutionDSL.png) |
| Hand-built example object models (SmartWatch, 11 features) | [Part1/Example.md](Part1/Example.md), [Part1/tacs262_assignment_project-4.py](Part1/tacs262_assignment_project-4.py) (models `Object_Problema_Diagram` and `Object_Solution_Diagram`) |
| Object model images (earlier 7-feature version) | [Part1/images/objectProblem.png](Part1/images/objectProblem.png), [Part1/images/objectSolution.png](Part1/images/objectSolution.png) |
| BESSER project (can be imported into the BESSER web editor; object models still in the earlier 7-feature version) | [Part1/TACS262_Assignment-15.json](Part1/TACS262_Assignment-15.json) |
| Test instances (SmartWatch family) | [Part1/Instances.md](Part1/Instances.md) |
| Report | [Part1/ReportPart1.pdf](Part1/ReportPart1.pdf) |
| LLM usage log | [Part1/AILog.md](Part1/AILog.md) |

## Part II deliverables

How to run, design decisions and references: [Part2/README.md](Part2/README.md).

| Deliverable | Where |
|---|---|
| T1 (Problem DSL → Solution DSL, model-to-model) | [Part2/t1_problem_to_cnf.py](Part2/t1_problem_to_cnf.py) |
| T2 (Solution DSL → BESSER quantum model, model-to-model) | [Part2/t2_cnf_to_quantum.py](Part2/t2_cnf_to_quantum.py) |
| Single command for the whole chain (T1 → T2 → T3 → Aer → validation), used to generate everything in `generated/` | [Part2/run_all.py](Part2/run_all.py) |
| T1 & T2 outputs and generated Qiskit code for test instances | [Part2/generated/](Part2/generated) |
| Clause-by-clause trace of T1 and the classical baseline for every instance | [Part2/generated/T1_report.md](Part2/generated/T1_report.md) |
 Results in domain terms and validation against the classical baseline for every instance | [Part2/generated/results.md](Part2/generated/results.md) |
| Classical baseline (brute force) | [Part2/baseline.py](Part2/baseline.py) |
| Validation of quantum results against the baseline | [Part2/validation.py](Part2/validation.py) |
| OCL invariants checked on T1's input and output | [Part2/checks.py](Part2/checks.py) |
| Tests | [Part2/test_part2.py](Part2/test_part2.py) |
| Report | [Part2/ReportPart2.pdf](Part2/ReportPart2.pdf) |
| LLM usage log | [Part2/AILog.md](Part2/AILog.md) |
