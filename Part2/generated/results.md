# Results of the chain and validation against the classical baseline

Written by `run_all.py`; do not edit by hand. Measured values change slightly from run to run
(sampling noise).

M is counted by brute force over the 2ⁿ assignments directly on the feature model, without the
CNF of T1 (classical baseline, independent of T1 and T2). P measured is the share of shots that
gave a valid configuration; P theoretical is sin²((2k+1)θ) with sin²θ = M/2ⁿ (Boyer et al., 1998).
Result is OK when (1) the solutions of the T1 CNF are exactly the baseline configurations,
(2) SolverConfig.knownSolutions = M, (3) P measured is within 3σ of P theoretical (binomial
sampling noise), and (4) if M > 0, the most frequent measurement is a valid configuration.

## Results in domain terms

### I1 · MiniWatch, digitalOnly (tiny, checkable by hand)

- Product line: MiniWatch. Request "digitalOnly": a product with Digital.
- Answer, a valid product: Watch, Display, Digital.
- Features left out: Analog.

### I2 · SmartWatch Part I version (7 features), onlyGPS (unique solution)

- Product line: SmartWatch7. Request "onlyGPS": a product with GPS; without Heartrate.
- Answer, a valid product: Watch, Display, Digital, Sensors, GPS.
- Features left out: Analog, Heartrate.

### I3 · SmartWatch (11 features), onlyGPS (main example, several solutions)

- Product line: SmartWatch. Request "onlyGPS": a product with GPS; without Heartrate.
- Answer, a valid product: Watch, Display, Digital, Battery, Temperature, Weather, Sensors, GPS.
- Features left out: Analog, StepsDistance, Heartrate.
- It is one of 8 valid products; the run measured 8 of them (listed below).

### I4 · SmartWatch (11 features), fullDigital (largest, unique solution)

- Product line: SmartWatch. Request "fullDigital": a product with GPS, StepsDistance, Temperature, Weather; without Heartrate.
- Answer, a valid product: Watch, Display, Digital, Battery, StepsDistance, Temperature, Weather, Sensors, GPS.
- Features left out: Analog, Heartrate.

### I5 · SmartWatch (11 features), analogWithGPS (no solution)

- Product line: SmartWatch. Request "analogWithGPS": a product with Analog, GPS.
- Answer: no product of this product line satisfies the request (none of the 1024 measurements is a valid configuration).

## Validation against the classical baseline

| Instance | n | Qubits (search + counter + output) | M | Rounds k | P measured | P theoretical | Solutions found | Oracle calls per shot | Brute-force evaluations | Result |
|---|---|---|---|---|---|---|---|---|---|---|
| I1 | 4 | 8 (4 + 3 + 1) | 1 | 3 | 0.969 | 0.961 | 1 of 1 | 3 | 16 | OK |
| I2 | 7 | 12 (7 + 4 + 1) | 1 | 8 | 0.997 | 0.996 | 1 of 1 | 8 | 128 | OK |
| I3 | 11 | 17 (11 + 5 + 1) | 8 | 12 | 1.000 | 1.000 | 8 of 8 | 12 | 2048 | OK |
| I4 | 11 | 17 (11 + 5 + 1) | 1 | 35 | 1.000 | 1.000 | 1 of 1 | 35 | 2048 | OK |
| I5 | 11 | 17 (11 + 5 + 1) | 0 | 1 | 0.000 | 0.000 | 0 of 0 | 1 | 2048 | OK |

### I1 · MiniWatch, digitalOnly (tiny, checkable by hand)

| Quantity | Value |
|---|---|
| Variables n / clauses m / states N | 4 / 8 / 16 |
| Solutions M (classical brute force on the feature model) | 1 (SolverConfig.knownSolutions = 1) |
| Grover rounds k / shots | 3 / 1024 |
| Success probability, measured | 0.969 (992 of 1024 shots) |
| Success probability, theoretical sin²((2k+1)θ) | 0.961 |
| Distinct valid configurations measured | 1 of 1 |
| Check: solutions of the T1 CNF = baseline configurations | yes |
| Check: SolverConfig.knownSolutions = M | yes |
| Check: measured success within 3σ of the theoretical one | yes |
| Check: most frequent measurement is a valid configuration (when M > 0) | yes |
| Oracle calls: per shot / total | 3 / 3072 |
| Classical brute force: formula evaluations | 16 |
| Most frequent bitstring | `1011` (992 shots): Digital, Display, Watch — valid |

Valid configurations measured (shots):

- Digital, Display, Watch (992)

Generated code: `I1/qiskit_circuit.py` · counts: `I1/counts.json` · simulation time: 7.7 s

### I2 · SmartWatch Part I version (7 features), onlyGPS (unique solution)

| Quantity | Value |
|---|---|
| Variables n / clauses m / states N | 7 / 15 / 128 |
| Solutions M (classical brute force on the feature model) | 1 (SolverConfig.knownSolutions = 1) |
| Grover rounds k / shots | 8 / 1024 |
| Success probability, measured | 0.997 (1021 of 1024 shots) |
| Success probability, theoretical sin²((2k+1)θ) | 0.996 |
| Distinct valid configurations measured | 1 of 1 |
| Check: solutions of the T1 CNF = baseline configurations | yes |
| Check: SolverConfig.knownSolutions = M | yes |
| Check: measured success within 3σ of the theoretical one | yes |
| Check: most frequent measurement is a valid configuration (when M > 0) | yes |
| Oracle calls: per shot / total | 8 / 8192 |
| Classical brute force: formula evaluations | 128 |
| Most frequent bitstring | `0111011` (1021 shots): Digital, Display, GPS, Sensors, Watch — valid |

Valid configurations measured (shots):

- Digital, Display, GPS, Sensors, Watch (1021)

Generated code: `I2/qiskit_circuit.py` · counts: `I2/counts.json` · simulation time: 0.4 s

### I3 · SmartWatch (11 features), onlyGPS (main example, several solutions)

| Quantity | Value |
|---|---|
| Variables n / clauses m / states N | 11 / 20 / 2048 |
| Solutions M (classical brute force on the feature model) | 8 (SolverConfig.knownSolutions = 8) |
| Grover rounds k / shots | 12 / 1024 |
| Success probability, measured | 1.000 (1024 of 1024 shots) |
| Success probability, theoretical sin²((2k+1)θ) | 1.000 |
| Distinct valid configurations measured | 8 of 8 |
| Check: solutions of the T1 CNF = baseline configurations | yes |
| Check: SolverConfig.knownSolutions = M | yes |
| Check: measured success within 3σ of the theoretical one | yes |
| Check: most frequent measurement is a valid configuration (when M > 0) | yes |
| Oracle calls: per shot / total | 12 / 12288 |
| Classical brute force: formula evaluations | 2048 |
| Most frequent bitstring | `01111011011` (145 shots): Battery, Digital, Display, GPS, Sensors, Temperature, Watch, Weather — valid |

Valid configurations measured (shots):

- Battery, Digital, Display, GPS, Sensors, Temperature, Watch, Weather (145)
- Battery, Digital, Display, GPS, Sensors, Watch (136)
- Battery, Digital, Display, GPS, Sensors, StepsDistance, Temperature, Watch (135)
- Battery, Digital, Display, GPS, Sensors, Temperature, Watch (133)
- Battery, Digital, Display, GPS, Sensors, StepsDistance, Watch (131)
- Battery, Digital, Display, GPS, Sensors, StepsDistance, Watch, Weather (122)
- Battery, Digital, Display, GPS, Sensors, Watch, Weather (119)
- Battery, Digital, Display, GPS, Sensors, StepsDistance, Temperature, Watch, Weather (103)

Generated code: `I3/qiskit_circuit.py` · counts: `I3/counts.json` · simulation time: 1.9 s

### I4 · SmartWatch (11 features), fullDigital (largest, unique solution)

| Quantity | Value |
|---|---|
| Variables n / clauses m / states N | 11 / 23 / 2048 |
| Solutions M (classical brute force on the feature model) | 1 (SolverConfig.knownSolutions = 1) |
| Grover rounds k / shots | 35 / 1024 |
| Success probability, measured | 1.000 (1024 of 1024 shots) |
| Success probability, theoretical sin²((2k+1)θ) | 1.000 |
| Distinct valid configurations measured | 1 of 1 |
| Check: solutions of the T1 CNF = baseline configurations | yes |
| Check: SolverConfig.knownSolutions = M | yes |
| Check: measured success within 3σ of the theoretical one | yes |
| Check: most frequent measurement is a valid configuration (when M > 0) | yes |
| Oracle calls: per shot / total | 35 / 35840 |
| Classical brute force: formula evaluations | 2048 |
| Most frequent bitstring | `01111111011` (1024 shots): Battery, Digital, Display, GPS, Sensors, StepsDistance, Temperature, Watch, Weather — valid |

Valid configurations measured (shots):

- Battery, Digital, Display, GPS, Sensors, StepsDistance, Temperature, Watch, Weather (1024)

Generated code: `I4/qiskit_circuit.py` · counts: `I4/counts.json` · simulation time: 4.2 s

### I5 · SmartWatch (11 features), analogWithGPS (no solution)

| Quantity | Value |
|---|---|
| Variables n / clauses m / states N | 11 / 20 / 2048 |
| Solutions M (classical brute force on the feature model) | 0 (SolverConfig.knownSolutions = 0) |
| Grover rounds k / shots | 1 / 1024 |
| Success probability, measured | 0.000 (0 of 1024 shots) |
| Success probability, theoretical sin²((2k+1)θ) | 0.000 |
| Distinct valid configurations measured | 0 of 0 |
| Check: solutions of the T1 CNF = baseline configurations | yes |
| Check: SolverConfig.knownSolutions = M | yes |
| Check: measured success within 3σ of the theoretical one | yes |
| Check: most frequent measurement is a valid configuration (when M > 0) | yes |
| Oracle calls: per shot / total | 1 / 1024 |
| Classical brute force: formula evaluations | 2048 |
| Most frequent bitstring | `10110001101` (4 shots): Analog, Digital, Heartrate, Sensors, Watch, Weather — not valid |

No valid configuration was measured: the request cannot be satisfied.

Generated code: `I5/qiskit_circuit.py` · counts: `I5/counts.json` · simulation time: 0.4 s
