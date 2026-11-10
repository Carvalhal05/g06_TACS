"""T2 (model-to-model): Solution DSL model (CNF + SolverConfig) -> BESSER quantum circuit model (Grover).

Input : a B-UML object model conforming to Solution_DSL (Part I): one CnfFormula with its
        Variables, Clauses, Literals and SolverConfig (the output of T1).
Output: a besser.BUML.metamodel.quantum.QuantumCircuit, the input of BESSER's Qiskit generator (T3),
        plus a layout that says what each qubit is.

Circuit (n variables, K clauses with two or more literals, c = ceil(log2(K + 1)) counter qubits):

    q[0 .. n-1]      search qubits; q[i] is the Variable with index i
    q[n .. n+c-1]    counter of violated clauses (ancillas, start and end in |0>)
    q[n+c]           output qubit, kept in |-> (phase kickback)
    c[0 .. n-1]      classical bits; search qubit i is measured into bit i

    H on every search qubit; X, H on the output qubit;
    `rounds` times: oracle, diffuser;
    measurement of the search qubits.

The oracle and the diffuser are sub-circuits (FunctionGate), defined once and applied `rounds` times.

References (each rule below cites the one it implements):
  [G96]    L. K. Grover, "A fast quantum mechanical algorithm for database search", STOC 1996.
  [NC]     M. A. Nielsen, I. L. Chuang, "Quantum Computation and Quantum Information", 10th
           anniversary ed., 2010, sec. 6.1 (oracle, Grover iteration) and sec. 4.3 (controlled operations).
  [BBHT98] M. Boyer, G. Brassard, P. Hoyer, A. Tapp, "Tight bounds on quantum searching",
           Fortschritte der Physik 46, 1998 (number of rounds; computed in T1, read here).
  [AJP22]  A. Alasow, P. Jin, M. Perkowski, "Quantum algorithm for variant maximum satisfiability",
           Entropy 24(11), 1615, 2022 (oracle with a counter of clauses instead of one ancilla per clause).
  [S]      J. Pascoal Faria, J. Cunha, "Quantum computing: a brief introduction", TACS 2026/27 slides
           (party planning oracle: compute the clauses, mark, uncompute).

Nothing about how to solve is fixed here: the number of rounds is read from SolverConfig.rounds.
SolverConfig.shots is not part of the circuit; the generator takes it (see run_all.py).
"""

import math

from besser.BUML.metamodel.quantum import (
    QuantumCircuit, QuantumRegister, ClassicalRegister, ControlState,
    HadamardGate, PauliXGate, FunctionGate, Measurement,
)

import metamodels as mm
from metamodels import attr, objects_of
import baseline


class T2Error(Exception):
    """The input model is not a well-formed Solution DSL model."""


def transform(solution_model):
    """Run T2. Returns (QuantumCircuit, layout).

    layout: dict with the qubit roles, {"search": [...], "counter": [...], "output": int,
            "variables": [name of Variable i, ...], "unit_clauses": [...], "counted_clauses": [...]}.
    """
    configs = objects_of(solution_model, mm.SolverConfig)
    if len(objects_of(solution_model, mm.CnfFormula)) != 1 or len(configs) != 1:
        raise T2Error("T2 needs exactly one CnfFormula with its SolverConfig")
    (cnf,) = objects_of(solution_model, mm.CnfFormula)
    rounds = attr(configs[0], "rounds")

    # Variables in index order and clauses in id order (c1, c2, ...), as written by T1.
    # clauses: [(clause id, [(variable index, isNegated), ...])]
    names, clauses = baseline.read_cnf(solution_model)
    n = len(names)

    # ---- R1 Unit clauses need no ancilla. A clause with one literal is true exactly when its
    # variable has one fixed value, so the search qubit itself controls the marking gate: a control
    # for (X), an anti-control for (not X) [NC sec. 4.3, controlled operations conditioned on 0 or 1].
    unit = {}                 # variable index -> isNegated
    contradiction = False     # (X) and (not X) both present: no assignment satisfies the formula
    counted = []              # clauses with two or more literals
    for cid, lits in clauses:
        if len(lits) == 1:
            (i, neg), = lits
            contradiction |= unit.setdefault(i, neg) != neg
        else:
            counted.append((cid, lits))

    # ---- R2 Counter register. Instead of one ancilla per clause [S], the oracle counts the violated
    # clauses in a binary counter and marks the states whose count is 0 [AJP22]. K clauses need
    # ceil(log2(K + 1)) qubits to hold the values 0..K.
    c = math.ceil(math.log2(len(counted) + 1))
    search = list(range(n))
    counter = list(range(n, n + c))
    output = n + c
    total = n + c + 1

    # One quantum register "q" and one classical register "c": BESSER's Qiskit generator addresses
    # the qubits of every operation as q[i] and the measured bits as c[i].
    circuit = QuantumCircuit(name=f"{attr(cnf, 'name')}_grover")
    circuit.add_qreg(QuantumRegister("q", total))
    circuit.add_creg(ClassicalRegister("c", n))

    oracle = FunctionGate("oracle", list(range(total)),
                          gates=_oracle(counted, unit, contradiction, counter, output))
    diffuser = FunctionGate("diffuser", list(range(total)), gates=_diffuser(search, output))

    # ---- R3 Initial state [G96; NC sec. 6.1.2]: uniform superposition of the 2^n assignments
    # (H on every search qubit). The output qubit is put in |-> = H X |0>, so that an X applied to it
    # multiplies the state by -1 (phase kickback) [NC sec. 6.1.1].
    for q in search:
        circuit.add_operation(HadamardGate(q))
    circuit.add_operation(PauliXGate(output))
    circuit.add_operation(HadamardGate(output))

    # ---- R4 Grover iteration, repeated SolverConfig.rounds times [G96; NC sec. 6.1.2, Fig. 6.1].
    # The value of `rounds` follows [BBHT98] and comes from the model (computed by T1).
    for _ in range(rounds):
        circuit.add_operation(oracle)
        circuit.add_operation(diffuser)

    # ---- R5 Measurement: search qubit i (Variable i) into classical bit i. Qiskit prints bit 0 on
    # the right, so Variable i is character -1-i of each measured bitstring (see validation.decode).
    for q in search:
        circuit.add_operation(Measurement(q, q))

    layout = {"search": search, "counter": counter, "output": output, "variables": names,
              "unit_clauses": [cid for cid, lits in clauses if len(lits) == 1],
              "counted_clauses": [cid for cid, _ in counted]}
    return circuit, layout


def _mcx(target, controls):
    """X on `target` controlled by `controls`: a list of (qubit, required value)."""
    if not controls:
        return PauliXGate(target)
    return PauliXGate(target, control_qubits=[q for q, _ in controls],
                      control_states=[ControlState.CONTROL if value else ControlState.ANTI_CONTROL
                                      for _, value in controls])


def _count_violated(counted, counter):
    """Gates that add 1 to the counter for each violated clause."""
    gates = []
    for _cid, lits in counted:
        # ---- R6 A clause is false for exactly one combination of its variables: every positive
        # literal's variable is 0 and every negated literal's variable is 1 (De Morgan; a clause is
        # "true when at least one of its literals is true" [S]). That combination is the control
        # pattern: anti-control for X, control for (not X).
        violated = [(i, neg) for i, neg in lits]
        # ---- R7 Controlled increment [AJP22; NC sec. 4.3]: bit j of the counter flips when all
        # lower bits are 1 (ripple carry), from the highest bit down so that each step reads the
        # lower bits before they change.
        for j in reversed(range(len(counter))):
            gates.append(_mcx(counter[j], violated + [(b, True) for b in counter[:j]]))
    return gates


def _oracle(counted, unit, contradiction, counter, output):
    """Phase oracle: multiplies by -1 the assignments that satisfy every clause [NC sec. 6.1.1]."""
    gates = _count_violated(counted, counter)                       # compute
    # ---- R8 Mark: flip the output qubit when no clause is violated, i.e. the counter is 0
    # (anti-controls) and every unit clause holds (R1). With the output in |-> this is the factor -1
    # on the solutions [NC sec. 6.1.1]. If two unit clauses contradict each other there is no
    # solution and nothing is marked.
    if not contradiction:
        gates.append(_mcx(output, [(i, not neg) for i, neg in sorted(unit.items())]
                          + [(b, False) for b in counter]))
    # ---- R9 Uncompute: the same gates in reverse order return the counter to |0>, so that it is
    # not entangled with the search qubits (every multi-controlled X is its own inverse)
    # [NC sec. 6.1.1; S].
    gates += reversed(_count_violated(counted, counter))
    return gates


def _diffuser(search, output):
    """Inversion about the mean, H^n (2|0><0| - I) H^n [G96; NC sec. 6.1.2].

    The conditional phase shift is done with the output qubit, as in the oracle: an X on it,
    anti-controlled by every search qubit, multiplies |0...0> by -1. That is (I - 2|0><0|), which
    equals (2|0><0| - I) up to a global phase of -1 that no measurement can see.
    """
    return ([HadamardGate(q) for q in search]
            + [_mcx(output, [(q, False) for q in search])]
            + [HadamardGate(q) for q in search])
