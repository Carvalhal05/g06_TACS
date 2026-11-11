# LLM Usage Log — Part II

This table logs every session where an LLM was used for the second part of the project. All outputs were reviewed by the group before being used in the deliverables.

## Part II 

### Log

| # | Member | Model | Approximate content of the conversation | What we obtained |
|---|---|---|---|---|
| 1 | Ana | Claude 3.5 / Gemini | Asked for a conceptual breakdown of Part II requirements, clarifying the transition from Part I models to executable quantum code via T1, T2, and T3 (BESSER Qiskit generator). | A clear step-by-step roadmap of Part II: what the M2M transformations (T1 and T2) need to achieve, how solver configurations (`SolverConfig`) bridge the models, and how validation against a classical brute-force baseline works. |
| 2 | Ana | Claude 3.5 / Gemini | Asked for guidance on structuring the T2 transformation (`t2_cnf_to_quantum.py`), specifically how to implement the clause counter, oracle synthesis, and uncomputation step in BESSER, while noting that T1 was developed by a teammate. | Architectural guidance on implementing the binary clause counter using ancilla qubits, phase kickback via an output qubit in $\ket{-}$, and safe uncomputation logic to prevent unwanted entanglement. |
| 3 | Ana | Claude 3,5 / Gemini | Asked for assistance in designing unit tests (`test_part2.py`) | Test cases covering invariant checks, (T1/T2/T3) transformation correctness, matching solution counts between CNF formulas and feature model semantics|
| 4 | Ana | Claude 3.5 / Gemini | Asked for a review of the generated execution pipeline (`run_all.py`) and documentation to ensure all assignment criteria for Part II were fully met. | Final review and refinement of the automated end-to-end execution script, ensuring it successfully processes instances I1 through I5 and outputs structured validation reports (`results.md`). |
| 5 | João | Claude (Fable 5.2) | Asked for a review of the repository against the assignment. | List of what was done (T1, baseline, validation) and what was missing (T2, Qiskit generation, runs, report). |
| 6 | João | Claude (Fable 5.2) | Asked for a corrected T2, tested on the five instances. | New `t2_cnf_to_quantum.py`, `run_all.py` (whole chain in one command) and 5 tests. |
| 7 | João | Claude (Fable 5.2) | Asked which references the T2 code uses. | Table of the five references and what we still had to check ourselves. |
| 8 | João | Claude Fable 5.2 | Gave the repository and the assignment and asked for help writing the Part II report in LaTeX. | A first draft in IEEE format built from the repository: table of the T1 rules (R1 to R8) with their references, description of the T2 circuit, results table for I1 to I5 and a list of limitations. The group then rewrote the text in its own words. |
| 9 | Rodrigo | Opus 5.5 (Claude Code) | Ran a strict code-quality review of Part2/ and a check of the repository against the assignment (draft v0.7), using Claude Code as an assistant to surface issues. Directed the work item by item, deciding what to fix and implementing each point as its own commit: the validation, the qubit count in T1_report.md, the design decisions in the README, and the bonus of mapping the answer back to the Problem DSL. | Review: identified that two of the validation checks could never fail (see below), that the qubit column of T1_report.md disagreed with results.md, that the README no longer listed the design decisions the Part I log refers to, and that the generated script prints only the counts (7.2), which is now justified in the README. Code: validation.py now uses the feature model as the baseline, with four checks (CNF = baseline configurations, knownSolutions = M, measured success within 3σ of the theoretical one, most frequent measurement valid). run_t1.py reports the real T2 qubit count. New answer_to_problem.py builds the answer as a Problem DSL model (a SelectionRequest that fixes every feature). Six new tests (27 in total), and generated/ was regenerated with run_all.py. Design choices made by the author: the 3σ tolerance with a 0.01 floor, and representing the answer as a complete SelectionRequest. |

### What was wrong and how detected/fixed 

- The first version of the control pattern of the oracle had the wrong sign
convention: it used controls on the positive literals and anti-controls on the
negated ones. A clause is false when every positive literal is 0 and every
negated literal is 1, so the controls must be the other way round. We detected
it with `test_oracle_marks_exactly_the_baseline_solutions`, which runs the
oracle on every basis state and compares the output with `baseline.satisfies`.
We fixed the control pattern in `_count_violated`.

- The first version of `validation.decode` read bit `i` as character `i` of the
measured bitstring. That is wrong because Qiskit is little-endian: qubit 0 is
the rightmost character, so bit `i` is character `-1-i`. We detected it with
`test_decode_uses_qiskit_bit_order`, which checks the known I1 product (`1011`
→ Watch, Display, Digital), and fixed it in `validation.decode`.

- The first suggestion for the number of Grover rounds when there are no
solutions ($M = 0$) was `rounds = 0`. That violates our OCL invariant
`PositiveExecutionParams` (rounds > 0), and a circuit with zero oracle calls is
not a Grover circuit. We detected it with `test_no_solution_instance` and fixed
it by using `rounds = 1` when $M = 0$ (the oracle marks nothing, so the
distribution is unchanged), documenting the choice in the report's limitations.

- The validation written in an earlier LLM session (Part I log, session 17)
compared the CNF of T1 with its own solutions: the measured configurations were
counted as valid with `baseline.satisfies` on the same clauses that gave the
expected solutions, and `knownSolutions` was computed by the same function. So
`allFoundAreBaselineSolutions` and `knownSolutions == baselineSolutions` were
always true, and a wrong T1 would still pass. The LLM pointed it out while
reviewing the code in session 9; no test had caught it. We fixed it by validating against
`baseline.feature_model_configurations`, which does not use the CNF, and added
`test_a_wrong_cnf_is_caught` (a CNF where the Xor of I1 became an Or) and
`test_a_wrong_oracle_is_caught` (uniform counts) to show that the checks can fail.

- The qubit column of `T1_report.md` was `n + m + 1` (one ancilla per clause),
from before T2 existed. T2 uses a counter, so the two reports gave different
qubit counts for the same instance (I3: 32 and 17). We detected it by comparing
`T1_report.md` with `results.md` and fixed it in `run_t1.py`.

- The first version of the bonus wrote the answer model to
`generated/<instance>/answer_model.py` with BESSER's code builder. The files
could not be loaded: the builder writes the Problem DSL association
`parent/children` as a Python variable with that name (`SyntaxError`). We
detected it by reloading the generated file. We now build and check the answer
model in memory (Problem DSL invariants and a T1 round trip) and do not write
it, since renaming the association would change the Part I metamodel.

- The first version of `test_a_wrong_cnf_is_caught` picked the clause to remove
with a condition that made no sense and depended on how BESSER unlinks objects.
It was noticed before the test was first run, and replaced with a
CNF built by T1 from a modified feature model (Xor replaced by Or).



### Critical reflection

- The LLM was useful in three roles: explaining BESSER and Qiskit, drafting the
first version of the code, and proposing tests. It was not useful as a source of
truth.

- It got quantum formulations wrong in ways that are easy to miss. The bit order
of Qiskit is the opposite of the intuitive one; the number of Grover rounds when
there are no solutions divides by zero. None of these errors is visible by
reading the code — they only show up against a baseline. This is why every
claim in the chain is checked by a test or by `baseline.py`.

- It was useful for structure, not for correctness. The roadmap, the list of tests
and the first draft of the report saved time, but every value, every rule and
every reference was checked against the assignment, the papers and the baseline.

- The group is responsible for everything submitted. Every member can explain any
part of the project.