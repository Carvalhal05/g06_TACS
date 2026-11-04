# Test instances

All instances come from the SmartWatch product line of the main example ([Example.md](Example.md)), so the presentation can focus on one domain. They differ in the size of the feature model and in the selection request. Together they cover the instance kinds asked for in Annex A of the assignment: a tiny one checkable by hand, one with a known unique solution, several solutions, no solution, and the largest size we target.

The problem object models of these instances are in [Part2/instances.py](../Part2/instances.py), and the T1 outputs with every clause and solution in [Part2/generated/T1_report.md](../Part2/generated/T1_report.md).

| # | Feature model | Request | Role | n (variables) | m (clauses) | M (solutions) | Rounds | n + m + 1 |
|---|---|---|---|---|---|---|---|---|
| I1 | MiniWatch (4 features) | digitalOnly | tiny, checkable by hand | 4 | 8 | 1 | 3 | 13 |
| I2 | SmartWatch, Part I version (7 features) | onlyGPS | known unique solution | 7 | 15 | 1 | 8 | 23 |
| I3 | SmartWatch (11 features) | onlyGPS | **main example**, several solutions | 11 | 20 | 8 | 12 | 32 |
| I4 | SmartWatch (11 features) | fullDigital | largest size, unique solution, most rounds | 11 | 23 | 1 | 35 | 35 |
| I5 | SmartWatch (11 features) | analogWithGPS | no solution | 11 | 20 | 0 | 1 (see I5) | 32 |

How the numbers were obtained:

- **m** follows the mapping rules of the Problem DSL concept table (Batory, 2005): one clause for the root, the "child implies parent" clause once per child, the "parent implies child" clause for mandatory features, one "at least one member" clause per group, pairwise "at most one" clauses for Xor groups, one clause per cross-tree constraint and one unit clause per `FeatureChoice`.
- **M** was obtained by brute force over all 2^n assignments. This is the classical baseline of Part II.
- **Rounds** = ⌊π/4 · √(N/M)⌋ with N = 2^n (Boyer et al., 1998). The formula is undefined when M = 0; T1 then uses 1 round (see I5).
- **n + m + 1** is the number of qubits if the oracle uses one ancilla per clause plus one output qubit, as in the party planning oracle of the course slides. Only I1 stays under the ~20 qubits of the assignment with that construction, so T2 has to use fewer ancillas.

## I1 · MiniWatch, digitalOnly

The display part of the SmartWatch alone:

```
watch (root)
└── display (mandatory)
      └── Xor { analog, digital }
```

Request: REQUIRED digital. Clauses: watch · (¬watch ∨ display) · (¬display ∨ watch) · (¬display ∨ analog ∨ digital) · (¬analog ∨ display) · (¬digital ∨ display) · (¬analog ∨ ¬digital) · digital.

Unique solution: **watch, display, digital**. With 4 variables the whole truth table has 16 rows and can be checked by hand. Without the request there are 2 solutions (analog or digital).

## I2 · SmartWatch (Part I version), onlyGPS

The 7-feature model handed in for Part I: the model of [Example.md](Example.md) without battery, temperature, steps and weather. Request: REQUIRED gps, EXCLUDED heartrate.

Unique solution: **watch, display, digital, sensors, gps**.

## I3 · SmartWatch, onlyGPS (main example)

Described in full in [Example.md](Example.md). Request: REQUIRED gps, EXCLUDED heartrate. Eight solutions: watch, display, digital, battery, sensors, gps, plus any combination of temperature, steps and weather.

## I4 · SmartWatch, fullDigital

Same feature model as I3. Request: REQUIRED gps, temperature, steps and weather; EXCLUDED heartrate.

Unique solution: **watch, display, digital, battery, temperature, steps, weather, sensors, gps**. With M = 1 out of 2048 states it needs the most Grover rounds (35).

## I5 · SmartWatch, analogWithGPS

Same feature model as I3. Request: REQUIRED analog, REQUIRED gps.

No solution: gps requires digital, and the Xor group of display forbids analog and digital together. Here `knownSolutions = 0` and the rounds formula is undefined. T1 sets `rounds = 1`: with no solution the oracle marks nothing, so every round leaves the uniform superposition unchanged and the number of rounds does not change the result. 1 is the smallest value allowed by the OCL rule `PositiveExecutionParams` (`rounds > 0`). The run must measure no valid configuration.

## References

- D. Batory, "Feature models, grammars, and propositional formulas", SPLC 2005, LNCS 3714, pp. 7–20.
- M. Boyer, G. Brassard, P. Høyer, A. Tapp, "Tight bounds on quantum searching", Fortschritte der Physik 46, 1998.
