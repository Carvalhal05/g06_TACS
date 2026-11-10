# Results of the chain and validation against the classical baseline

Written by `run_all.py`; do not edit by hand. Measured values change slightly from run to run
(sampling noise).

M is counted by brute force over the 2ⁿ assignments (classical baseline). P measured is the share
of shots that gave a valid configuration; P theoretical is sin²((2k+1)θ) with sin²θ = M/2ⁿ
(Boyer et al., 1998). Result is OK when every measured valid configuration is a baseline
solution and, if there are solutions, the most frequent measurement is one of them.

| Instance | n | Qubits (search + counter + output) | M | Rounds k | P measured | P theoretical | Solutions found | Oracle calls per shot | Brute-force evaluations | Result |
|---|---|---|---|---|---|---|---|---|---|---|
| I1 | 4 | 8 (4 + 3 + 1) | 1 | 3 | 0.981 | 0.961 | 1 of 1 | 3 | 16 | OK |
| I2 | 7 | 12 (7 + 4 + 1) | 1 | 8 | 0.995 | 0.996 | 1 of 1 | 8 | 128 | OK |
| I3 | 11 | 17 (11 + 5 + 1) | 8 | 12 | 1.000 | 1.000 | 8 of 8 | 12 | 2048 | OK |
| I4 | 11 | 17 (11 + 5 + 1) | 1 | 35 | 1.000 | 1.000 | 1 of 1 | 35 | 2048 | OK |
| I5 | 11 | 17 (11 + 5 + 1) | 0 | 1 | 0.000 | 0.000 | 0 of 0 | 1 | 2048 | OK |

### I1 · MiniWatch, digitalOnly (tiny, checkable by hand)

| Quantity | Value |
|---|---|
| Variables n / clauses m / states N | 4 / 8 / 16 |
| Solutions M (classical brute force) | 1 (SolverConfig.knownSolutions = 1) |
| Grover rounds k / shots | 3 / 1024 |
| Success probability, measured | 0.981 (1005 of 1024 shots) |
| Success probability, theoretical sin²((2k+1)θ) | 0.961 |
| Distinct valid configurations measured | 1 of 1 |
| Every measured valid configuration is a baseline solution | True |
| Oracle calls: per shot / total | 3 / 3072 |
| Classical brute force: formula evaluations | 16 |
| Most frequent bitstring | `1011` (1005 shots): Digital, Display, Watch — valid |

Valid configurations measured (shots):

- Digital, Display, Watch (1005)

Generated code: `I1/qiskit_circuit.py` · counts: `I1/counts.json` · simulation time: 0.6 s

### I2 · SmartWatch Part I version (7 features), onlyGPS (unique solution)

| Quantity | Value |
|---|---|
| Variables n / clauses m / states N | 7 / 15 / 128 |
| Solutions M (classical brute force) | 1 (SolverConfig.knownSolutions = 1) |
| Grover rounds k / shots | 8 / 1024 |
| Success probability, measured | 0.995 (1019 of 1024 shots) |
| Success probability, theoretical sin²((2k+1)θ) | 0.996 |
| Distinct valid configurations measured | 1 of 1 |
| Every measured valid configuration is a baseline solution | True |
| Oracle calls: per shot / total | 8 / 8192 |
| Classical brute force: formula evaluations | 128 |
| Most frequent bitstring | `0111011` (1019 shots): Digital, Display, GPS, Sensors, Watch — valid |

Valid configurations measured (shots):

- Digital, Display, GPS, Sensors, Watch (1019)

Generated code: `I2/qiskit_circuit.py` · counts: `I2/counts.json` · simulation time: 0.1 s

### I3 · SmartWatch (11 features), onlyGPS (main example, several solutions)

| Quantity | Value |
|---|---|
| Variables n / clauses m / states N | 11 / 20 / 2048 |
| Solutions M (classical brute force) | 8 (SolverConfig.knownSolutions = 8) |
| Grover rounds k / shots | 12 / 1024 |
| Success probability, measured | 1.000 (1024 of 1024 shots) |
| Success probability, theoretical sin²((2k+1)θ) | 1.000 |
| Distinct valid configurations measured | 8 of 8 |
| Every measured valid configuration is a baseline solution | True |
| Oracle calls: per shot / total | 12 / 12288 |
| Classical brute force: formula evaluations | 2048 |
| Most frequent bitstring | `01110011011` (144 shots): Battery, Digital, Display, GPS, Sensors, Watch, Weather — valid |

Valid configurations measured (shots):

- Battery, Digital, Display, GPS, Sensors, Watch, Weather (144)
- Battery, Digital, Display, GPS, Sensors, Temperature, Watch (140)
- Battery, Digital, Display, GPS, Sensors, StepsDistance, Temperature, Watch, Weather (139)
- Battery, Digital, Display, GPS, Sensors, Watch (130)
- Battery, Digital, Display, GPS, Sensors, Temperature, Watch, Weather (126)
- Battery, Digital, Display, GPS, Sensors, StepsDistance, Temperature, Watch (120)
- Battery, Digital, Display, GPS, Sensors, StepsDistance, Watch (119)
- Battery, Digital, Display, GPS, Sensors, StepsDistance, Watch, Weather (106)

Generated code: `I3/qiskit_circuit.py` · counts: `I3/counts.json` · simulation time: 0.3 s

### I4 · SmartWatch (11 features), fullDigital (largest, unique solution)

| Quantity | Value |
|---|---|
| Variables n / clauses m / states N | 11 / 23 / 2048 |
| Solutions M (classical brute force) | 1 (SolverConfig.knownSolutions = 1) |
| Grover rounds k / shots | 35 / 1024 |
| Success probability, measured | 1.000 (1024 of 1024 shots) |
| Success probability, theoretical sin²((2k+1)θ) | 1.000 |
| Distinct valid configurations measured | 1 of 1 |
| Every measured valid configuration is a baseline solution | True |
| Oracle calls: per shot / total | 35 / 35840 |
| Classical brute force: formula evaluations | 2048 |
| Most frequent bitstring | `01111111011` (1024 shots): Battery, Digital, Display, GPS, Sensors, StepsDistance, Temperature, Watch, Weather — valid |

Valid configurations measured (shots):

- Battery, Digital, Display, GPS, Sensors, StepsDistance, Temperature, Watch, Weather (1024)

Generated code: `I4/qiskit_circuit.py` · counts: `I4/counts.json` · simulation time: 0.8 s

### I5 · SmartWatch (11 features), analogWithGPS (no solution)

| Quantity | Value |
|---|---|
| Variables n / clauses m / states N | 11 / 20 / 2048 |
| Solutions M (classical brute force) | 0 (SolverConfig.knownSolutions = 0) |
| Grover rounds k / shots | 1 / 1024 |
| Success probability, measured | 0.000 (0 of 1024 shots) |
| Success probability, theoretical sin²((2k+1)θ) | 0.000 |
| Distinct valid configurations measured | 0 of 0 |
| Every measured valid configuration is a baseline solution | True |
| Oracle calls: per shot / total | 1 / 1024 |
| Classical brute force: formula evaluations | 2048 |
| Most frequent bitstring | `00101001011` (5 shots): Digital, Display, Sensors, Temperature, Watch — not valid |

No valid configuration was measured: the request cannot be satisfied.

Generated code: `I5/qiskit_circuit.py` · counts: `I5/counts.json` · simulation time: 0.1 s
