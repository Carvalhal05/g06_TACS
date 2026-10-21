# Test instances

Problem instances collected during the domain analysis (assignment §6.1 and Annex A). They will be the test cases of Part II.

Annex A asks for a tiny instance checkable by hand, a medium one with a known solution, one near the size limit, one with several solutions and, where possible, one with none. Because a `FeatureModel` can own several `SelectionRequest`s, some instances reuse the same feature model with a different request.

| # | Feature model | Request | Role | n (variables) | m (clauses) | M (solutions) | Rounds |
|---|---|---|---|---|---|---|---|
| I1 | SmartWatch | onlyGPS | tiny, checkable by hand ([Example.md](Example.md)) | 7 | 15 | 1 | 8 |
| I2 | SmartWatch | withSensors | several solutions | 7 | 14 | 3 | 5 |
| I3 | SmartWatch | analogWithGPS | no solution | 7 | 15 | 0 | — |
| I4 | MobilePhone | cameraPhone | medium, known solution, taken from the literature | 10 | 22 | 1 | 25 |
| I5 | Laptop | linuxTouch | at the Class B limit of 12 search qubits (OCL `QubitLimit`), several solutions | 12 | 29 | 2 | 35 |

How the numbers were obtained:

- **m** follows the mapping rules of the Problem DSL concept table (Batory, 2005). Identical "child implies parent" clauses are counted once, as in Example.md. Unit clauses for the root and for each `FeatureChoice` are included.
- **M** was obtained by brute force over all 2^n assignments. This is the classical baseline we will compare against in Part II.
- **Rounds** = ⌊π/4 · √(N/M)⌋ with N = 2^n (Boyer et al., 1998). It is undefined when M = 0 (see I3).

## SmartWatch (I1, I2, I3)

The feature model is the one in [Example.md](Example.md):

```
watch (root)
├── display (mandatory)
│     └── Xor { analog, digital }
└── sensors (optional)
      └── Or { gps, heartrate }

gps requires digital
analog excludes heartrate
```

Without any choice, the product line has 5 valid configurations.

**I1 · onlyGPS**: REQUIRED gps, EXCLUDED heartrate.
- Unique solution: watch, display, digital, sensors, gps.

**I2 · withSensors**: REQUIRED sensors. There are 3 solutions:
- watch, display, digital, sensors, gps
- watch, display, digital, sensors, heartrate
- watch, display, digital, sensors, gps, heartrate

Every solution has `digital`. With `gps`, `digital` is forced by the requires constraint. With `heartrate`, `analog` is ruled out by the excludes constraint.

**I3 · analogWithGPS**: REQUIRED analog, REQUIRED gps.
- No solution: gps requires digital, and the Xor group forbids analog and digital together.
- Here `knownSolutions = 0` and the rounds formula is undefined. The OCL rule `PositiveExecutionParams` still requires `rounds > 0`, so the number of rounds for this case has to be decided in Part II.

## MobilePhone (I4)

This is the mobile phone feature model used as a running example by Benavides et al. (2010):

```
mobilePhone (root)
├── calls (mandatory)
├── gps (optional)
├── screen (mandatory)
│     └── Xor { basic, color, highResolution }
└── media (optional)
      └── Or { camera, mp3 }

camera requires highResolution
gps excludes basic
```

Without any choice, the product line has 14 valid configurations.

**I4 · cameraPhone**: REQUIRED camera, REQUIRED gps, EXCLUDED mp3.
- Unique solution: mobilePhone, calls, gps, screen, highResolution, media, camera.

## Laptop (I5)

This is our own example, sized at the 12-variable limit:

```
laptop (root)
├── cpu (mandatory)
│     └── Xor { intel, amd, arm }
├── os (mandatory)
│     └── Xor { windows, linux, macos }
└── extras (optional)
      └── Or { touchscreen, stylus }

macos requires arm
macos excludes touchscreen
```

Without any choice, the product line has 26 valid configurations.

**I5 · linuxTouch**: REQUIRED linux, REQUIRED touchscreen, EXCLUDED stylus, EXCLUDED amd. There are 2 solutions:
- laptop, cpu, intel, os, linux, extras, touchscreen
- laptop, cpu, arm, os, linux, extras, touchscreen

## Qubit budget

n is the number of search qubits. The total also includes the oracle's ancillas, which depend on how T2 builds the oracle (Part II).

As a reference point, an oracle with one ancilla per clause plus one output qubit would need n + m + 1 qubits:

| Instance | Total qubits |
|---|---|
| I1 | 23 |
| I2 | 22 |
| I3 | 23 |
| I4 | 33 |
| I5 | 42 |

All of these are above the ~20 qubits of §7.3, so the ancilla count is a point to address in T2.

## References

- D. Batory, "Feature models, grammars, and propositional formulas", SPLC 2005, LNCS 3714, pp. 7–20.
- D. Benavides, S. Segura, A. Ruiz-Cortés, "Automated analysis of feature models 20 years later: A literature review", Information Systems 35(6), 2010, pp. 615–636.
- M. Boyer, G. Brassard, P. Høyer, A. Tapp, "Tight bounds on quantum searching", Fortschritte der Physik 46, 1998.
