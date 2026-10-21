# Example: SmartWatch feature model

Hand-built example for Part I of the TACS project. 

The model has 7 features, so the CNF has 7 variables and the Grover circuit needs 7 search qubits, below the Class B limit of 12.

## 1. The feature model

```
watch (root)
├── display (mandatory)
│     └── Xor { analog, digital }
└── sensors (optional)
      └── Or { gps, heartRate }

r1: gps requires digital
e1: analog excludes heartRate
```

A watch always has a display, which is either analog or digital (Xor). It may have sensors and, if it does, it has GPS, a heart rate sensor or both (Or). GPS needs a digital display, and the analog display does not support the heart rate sensor.

The example covers every construct of the Problem DSL: root, mandatory and optional features, an Xor group, an Or group, a requires constraint, an excludes constraint and a selection request with both REQUIRED and EXCLUDED choices.

## 2. Problem object model

Attributes (`id`, `name`, `isMandatory`, `type`) are values stored in the object. Associations (`root`, `features`, `children`, `parent`, `groups`, `group`, `members`, `source`, `target`, `choices`, `feature`) are links to other objects.

| Object | Class | Attributes and links |
|---|---|---|
| fm | FeatureModel | name="SmartWatch", root=watch, features={watch, display, analog, digital, sensors, gps, heartRate} |
| watch | Feature | id="watch", name="Watch", isMandatory=false, children={display, sensors} |
| display | Feature | id="display", name="Display", isMandatory=true, parent=watch, children={analog, digital}, groups={xor1} |
| analog | Feature | id="analog", name="Analog", isMandatory=false, parent=display, group=xor1 |
| digital | Feature | id="digital", name="Digital", isMandatory=false, parent=display, group=xor1 |
| sensors | Feature | id="sensors", name="Sensors", isMandatory=false, parent=watch, children={gps, heartRate}, groups={or1} |
| gps | Feature | id="gps", name="GPS", isMandatory=false, parent=sensors, group=or1 |
| heartRate | Feature | id="heartrate", name="Heartrate", isMandatory=false, parent=sensors, group=or1 |
| xor1 | Xor | parent=display, members={analog, digital} |
| or1 | Or | parent=sensors, members={gps, heartRate} |
| r1 | RequiresConstraint | source=gps, target=digital |
| e1 | ExcludesConstraint | source=analog, target=heartRate |
| sr1 | SelectionRequest | name="soGPS", choices={ch1, ch2} |
| ch1 | FeatureChoice | type=REQUIRED, feature=gps |
| ch2 | FeatureChoice | type=EXCLUDED, feature=heartRate |

## 3. Solution object model

### 3.1 Formula

```
cnf : CnfFormula   name="SmartWatch_soGPS"
                   variables={v_watch, ..., v_heartRate}
                   clauses={c1, ..., c15}
                   solverconfig=cfg
```

### 3.2 Variables

Each feature becomes one Variable. The `index` is the position of its qubit in the circuit.

| Object | name | index |
|---|---|---|
| v_watch | watch | 0 |
| v_display | display | 1 |
| v_analog | analog | 2 |
| v_digital | digital | 3 |
| v_sensors | sensors | 4 |
| v_gps | gps | 5 |
| v_heartRate | heartRate | 6 |

### 3.3 Clauses

Each row is one Clause object and each term is one Literal object. The rule "child implies parent" (¬C ∨ P) is produced both by optional features and by group members, so duplicated clauses appear only once.

| id | Clause | Origin |
|---|---|---|
| c1 | watch | root is always selected |
| c2 | ¬display ∨ watch | child implies parent |
| c3 | ¬watch ∨ display | display is mandatory |
| c4 | ¬analog ∨ display | child implies parent |
| c5 | ¬digital ∨ display | child implies parent |
| c6 | ¬display ∨ analog ∨ digital | xor1: at least one member |
| c7 | ¬analog ∨ ¬digital | xor1: at most one member |
| c8 | ¬sensors ∨ watch | child implies parent |
| c9 | ¬gps ∨ sensors | child implies parent |
| c10 | ¬heartRate ∨ sensors | child implies parent |
| c11 | ¬sensors ∨ gps ∨ heartRate | or1: at least one member |
| c12 | ¬gps ∨ digital | r1 (requires) |
| c13 | ¬analog ∨ ¬heartRate | e1 (excludes) |
| c14 | gps | ch1 (REQUIRED) |
| c15 | ¬heartRate | ch2 (EXCLUDED) |

Example of one clause written as objects (c12 ( ¬gps ∨ digital)):

```
c12  : Clause    id="c12"   literals={l12_1, l12_2}
l12_1 : Literal   isNegated=true    target=v_gps
l12_2 : Literal   isNegated=false   target=v_digital
```

### 3.4 Solver configuration

```
cfg : SolverConfig   knownSolutions=1   rounds=8   shots=1024
```

The number of Grover rounds is ⌊π/4 · √(N/M)⌋, with N = 2^7 = 128 states and M = 1 solution, which gives 8.

### 3.5 Expected result

A single valid configuration: **watch, display, digital, sensors, gps**.

## Object Models

### Object Problem model

<img width="908" height="505" alt="objectProblem" src="https://github.com/user-attachments/assets/faee1c37-fde4-4928-a4d8-cb1b01111ccd" />


### Object Solution model

<img width="1197" height="846" alt="objectDomain" src="https://github.com/user-attachments/assets/0c1fc612-8c20-4b1d-afde-7a8789e26eea" />


