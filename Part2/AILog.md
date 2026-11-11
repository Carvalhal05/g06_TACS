# LLM Usage Log — Part II

This table logs every session where an LLM was used for the second part of the project. All outputs were reviewed by the group before being used in the deliverables.

## Part II Sessions

| # | Member | Model | Approximate content of the conversation | What we obtained |
|---|---|---|---|---|
| 1 | Ana | Claude / Gemini | Asked for a conceptual breakdown of Part II requirements, clarifying the transition from Part I models to executable quantum code via T1, T2, and T3 (BESSER Qiskit generator). | A clear step-by-step roadmap of Part II: what the M2M transformations (T1 and T2) need to achieve, how solver configurations (`SolverConfig`) bridge the models, and how validation against a classical brute-force baseline works. |
| 2 | Ana | Claude / Gemini | Asked for guidance on structuring the T2 transformation (`t2_cnf_to_quantum.py`), specifically how to implement the clause counter, oracle synthesis, and uncomputation step in BESSER, while noting that T1 was developed by a teammate. | Architectural guidance on implementing the binary clause counter using ancilla qubits, phase kickback via an output qubit in $\ket{-}$, and safe uncomputation logic to prevent unwanted entanglement. |
| 3 | Ana | Claude / Gemini | Asked for assistance in designing unit tests (`test_part2.py`) | Test cases covering invariant checks, (T1/T2/T3) transformation correctness, matching solution counts between CNF formulas and feature model semantics|
| 4 | Ana | Claude / Gemini | Asked for a review of the generated execution pipeline (`run_all.py`) and documentation to ensure all assignment criteria for Part II were fully met. | Final review and refinement of the automated end-to-end execution script, ensuring it successfully processes instances I1 through I5 and outputs structured validation reports (`results.md`). |