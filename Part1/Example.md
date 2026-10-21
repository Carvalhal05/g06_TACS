# Example: SmartWatch feature model

Hand-built example for Part I of the TACS project. 

The model has 7 features, so the CNF has 7 variables and the Grover circuit needs 7 search qubits, below the Class B limit of 12.

## 1. The feature model

```
relogio (root)                    watch
├── mostrador (mandatory)         display
│     └── Xor { analogico, digital }
└── sensores (optional)           sensors
      └── Or { gps, cardio }

r1: gps requires digital
e1: analogico excludes cardio
```

A watch always has a display, which is either analog or digital (Xor). It may have sensors and, if it does, it has GPS, a heart rate sensor (cardio) or both (Or). GPS needs a digital display, and the analog display does not support the heart rate sensor.

The example covers every construct of the Problem DSL: root, mandatory and optional features, an Xor group, an Or group, a requires constraint, an excludes constraint and a selection request with both REQUIRED and EXCLUDED choices.

## 2. Problem object model

Attributes (`id`, `name`, `isMandatory`, `type`) are values stored in the object. Associations (`root`, `features`, `children`, `parent`, `groups`, `group`, `members`, `source`, `target`, `choices`, `feature`) are links to other objects.

| Object | Class | Attributes and links |
|---|---|---|
| fm | FeatureModel | name="SmartWatch", root=relogio, features={relogio, mostrador, analogico, digital, sensores, gps, cardio} |
| relogio | Feature | id="relogio", name="Relógio", isMandatory=false, children={mostrador, sensores} |
| mostrador | Feature | id="mostrador", name="Mostrador", isMandatory=true, parent=relogio, children={analogico, digital}, groups={xor1} |
| analogico | Feature | id="analogico", name="Analógico", isMandatory=false, parent=mostrador, group=xor1 |
| digital | Feature | id="digital", name="Digital", isMandatory=false, parent=mostrador, group=xor1 |
| sensores | Feature | id="sensores", name="Sensores", isMandatory=false, parent=relogio, children={gps, cardio}, groups={or1} |
| gps | Feature | id="gps", name="GPS", isMandatory=false, parent=sensores, group=or1 |
| cardio | Feature | id="cardio", name="Cardio", isMandatory=false, parent=sensores, group=or1 |
| xor1 | Xor | parent=mostrador, members={analogico, digital} |
| or1 | Or | parent=sensores, members={gps, cardio} |
| r1 | RequiresConstraint | source=gps, target=digital |
| e1 | ExcludesConstraint | source=analogico, target=cardio |
| sr1 | SelectionRequest | name="soGPS", choices={ch1, ch2} |
| ch1 | FeatureChoice | type=REQUIRED, feature=gps |
| ch2 | FeatureChoice | type=EXCLUDED, feature=cardio |

## 3. Solution object model (request "soGPS")

### 3.1 Formula

```
cnf : CnfFormula   name="SmartWatch_soGPS"
                   variables={v_relogio, ..., v_cardio}
                   clauses={c1, ..., c15}
                   solverconfig=cfg
```

### 3.2 Variables

Each feature becomes one Variable. The `index` is the position of its qubit in the circuit.

| Object | name | index |
|---|---|---|
| v_relogio | relogio | 0 |
| v_mostrador | mostrador | 1 |
| v_analogico | analogico | 2 |
| v_digital | digital | 3 |
| v_sensores | sensores | 4 |
| v_gps | gps | 5 |
| v_cardio | cardio | 6 |

### 3.3 Clauses

Each row is one Clause object and each term is one Literal object. The rule "child implies parent" (¬C ∨ P) is produced both by optional features and by group members, so duplicated clauses appear only once.

| id | Clause | Origin |
|---|---|---|
| c1 | relogio | root is always selected |
| c2 | ¬mostrador ∨ relogio | child implies parent |
| c3 | ¬relogio ∨ mostrador | mostrador is mandatory |
| c4 | ¬analogico ∨ mostrador | child implies parent |
| c5 | ¬digital ∨ mostrador | child implies parent |
| c6 | ¬mostrador ∨ analogico ∨ digital | xor1: at least one member |
| c7 | ¬analogico ∨ ¬digital | xor1: at most one member |
| c8 | ¬sensores ∨ relogio | child implies parent |
| c9 | ¬gps ∨ sensores | child implies parent |
| c10 | ¬cardio ∨ sensores | child implies parent |
| c11 | ¬sensores ∨ gps ∨ cardio | or1: at least one member |
| c12 | ¬gps ∨ digital | r1 (requires) |
| c13 | ¬analogico ∨ ¬cardio | e1 (excludes) |
| c14 | gps | ch1 (REQUIRED) |
| c15 | ¬cardio | ch2 (EXCLUDED) |

Example of one clause written as objects (c12 ( ¬gps ∨ digital)):

```
c12  : Clause    id="c12"   literals={l12a, l12b}
l12a : Literal   isNegated=true    target=v_gps
l12b : Literal   isNegated=false   target=v_digital
```

### 3.4 Solver configuration

```
cfg : SolverConfig   knownSolutions=1   rounds=8   shots=1024
```

The number of Grover rounds is ⌊π/4 · √(N/M)⌋, with N = 2^7 = 128 states and M = 1 solution, which gives 8.

### 3.5 Expected result

A single valid configuration: **relogio, mostrador, digital, sensores, gps**.

## 4. Other requests on the same feature model

To cover the cases asked in the assignment (several solutions, one solution, no solution), only the SelectionRequest changes. The first 13 clauses stay the same and only the clauses coming from the choices change.

| Request | Choices | Clauses | Solutions | rounds |
|---|---|---|---|---|
| soGPS | gps REQUIRED, cardio EXCLUDED | 15 | 1 | 8 |
| comGPS | gps REQUIRED | 14 | 2 | 6 |
| gpsAnalogico | gps REQUIRED, analogico REQUIRED | 15 | 0 | n/a |

- **comGPS:** without c15, cardio is free, so there are 2 solutions (with and without cardio). knownSolutions=2 and rounds = ⌊π/4 · √(128/2)⌋ = 6.
- **gpsAnalogico:** c14 = gps and c15 = analogico. GPS requires digital (c12) and the Xor forbids analog and digital together (c7), so there is no valid configuration. No number of rounds makes sense here: Grover should not find any marked state, and the measured results should look uniformly random.
