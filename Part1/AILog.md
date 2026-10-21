# LLM Usage Log

This table logs every session where an LLM was used for the first part of the project. All outputs were reviewed by the group before being used in the deliverables.

## Part 1 Sessions

| # | Member | Model | Approximate content of the conversation | What we obtained |
|---|---|---|---|---|
| 1 | João | Opus 5.5 | Asked for a review of our Part I draft (Word document and diagrams) against the assignment. | Gap analysis: group features (Or/Xor members) had no clear owner, no traceability from CNF clauses back to the feature model, mismatches between the concept table and the class diagram, missing deliverables (object models, OCL, report, this log). Flagged the qubit limit as a risk. Suggested references (Batory 2005, Benavides et al. 2010, Kang et al. 1990). |
| 2 | João | Opus 5.5 | Asked For a general explanation about OCLs. |  Interactive step by step guide ("OCL do Feature Model"): what OCL is, its basic building blocks, review of our draft rules, mismatches between our diagrams and tables, the constraints for the Problem DSL and Solution DSL (each with a plain-language reading, an example that violates it and why it matters for T1/T2), how to add them in the BESSER web editor, and how to test them by breaking an object model on purpose. It also showed that BOCL has no `closure`, `oclIsUndefined()` or `including`, so those rules were rewritten.  |
| 3 | João | Opus 5.5 | Asked which OCL rules were still missing and whether any should be removed. | Added `ChildrenWithinModel`, `NonEmptyId`, `NonEmptyName` and `NonEmptyVariableName`. Removed "requires and excludes on the same pair", with the reasoning that OCL checks well-formedness and whether a model has a solution is answered by Grover (models with no solution must stay valid). |
| 4 | João | Opus 5.5 | Asked for corrections to the Problem DSL and Solution DSL concept tables in our document. | Minor grammatical corrections and a few changes to specific rules. |
| 5 | João | Opus 5.5 | Asked for validity for examples. | Candidate instances (car, mobile phone, watch, World Cup group draw, table seating), with solution counts, clause counts and Grover rounds checked by brute force. Suggested car, mobile phone and watch as the three main candidates. |
| 6 | João | Opus 5.5 | Asked for help structuring the report (LaTeX skeleton for the report to be written). | LaTeX skeleton with the header (course, FEUP and our names) and the concept tables already in place. The report text itself was written by us. |
| 7 | João | Opus 5.5 | Asked for further help with the formulation and correctness of our already semi-developed watch example. | Review and completion of the watch feature model, the matching CNF object model and `SolverConfig`.|
| 8 | João | Opus 5.5 | Asked for the .md skeleton for this log. |  A draft of this table, which we then reviewed and rewrote row by row. |
| 9 | João | Opus 5.5 | Asked for help creating a figure for the report showing how each Problem DSL element is mapped to the Solution DSL. | The desired figure used in the report. |
| 10 | Ana | | *(add Ana's sessions here, if any)* | |

