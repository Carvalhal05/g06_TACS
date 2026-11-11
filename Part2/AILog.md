# LLM Usage Log — Part II

This table logs every session where an LLM was used for the second part of the project. All outputs were reviewed by the group before being used in the deliverables.

## Part II Sessions

| # | Member | Model | Approximate content of the conversation | What we obtained |
|---|---|---|---|---|
| 1 | Ana | Claude / Gemini | Asked for a conceptual breakdown of Part II requirements, clarifying the transition from Part I models to executable quantum code via T1, T2, and T3 (BESSER Qiskit generator). | A clear step-by-step roadmap of Part II: what the M2M transformations (T1 and T2) need to achieve, how solver configurations (`SolverConfig`) bridge the models, and how validation against a classical brute-force baseline works. |
| 2 | Ana | Claude / Gemini | Asked for guidance on structuring the T2 transformation (`t2_cnf_to_quantum.py`), specifically how to implement the clause counter, oracle synthesis, and uncomputation step in BESSER, while noting that T1 was developed by a teammate. | Architectural guidance on implementing the binary clause counter using ancilla qubits, phase kickback via an output qubit in $\ket{-}$, and safe uncomputation logic to prevent unwanted entanglement. |
| 3 | Ana | Claude / Gemini | Asked for assistance in designing unit tests (`test_part2.py`) | Test cases covering invariant checks, (T1/T2/T3) transformation correctness, matching solution counts between CNF formulas and feature model semantics|
| 4 | Ana | Claude / Gemini | Asked for a review of the generated execution pipeline (`run_all.py`) and documentation to ensure all assignment criteria for Part II were fully met. | Final review and refinement of the automated end-to-end execution script, ensuring it successfully processes instances I1 through I5 and outputs structured validation reports (`results.md`). |
| 5 | João | Claude (Fable 5.2) | Asked for a review of the repository against the assignment. | List of what was done (T1, baseline, validation) and what was missing (T2, Qiskit generation, runs, report). |
| 6 | João | Claude (Fable 5.2) | Asked for a corrected T2, tested on the five instances. | New `t2_cnf_to_quantum.py`, `run_all.py` (whole chain in one command) and 5 tests. |
| 7 | João | Claude (Fable 5.2) | Asked which references the T2 code uses. | Table of the five references and what we still had to check ourselves. |
| 8 | João | Claude Fable 5.2 | Gave the repository and the assignment and asked for help writing the Part II report in LaTeX. | A first draft in IEEE format built from the repository: table of the T1 rules (R1 to R8) with their references, description of the T2 circuit, results table for I1 to I5 and a list of limitations. The group then rewrote the text in its own words. |