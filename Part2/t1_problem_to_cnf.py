"""T1 (model-to-model): Problem DSL model (feature model + selection request) -> Solution DSL model (CNF).

Input : a B-UML object model conforming to Problem_DSL (Part I), with one FeatureModel.
Output: a B-UML object model conforming to Solution_DSL (Part I): one CnfFormula with its
        Variables, Clauses, Literals and SolverConfig, plus a trace that says which rule and
        which source elements produced each clause.

References for the rules (each rule below cites the one it implements):
  [B05] D. Batory, "Feature models, grammars, and propositional formulas", SPLC 2005, LNCS 3714, pp. 7-20.
  [T07] S. Thaker, D. Batory, D. Kitchin, W. Cook, "Safe composition of product lines", GPCE 2007,
        pp. 95-104, Figure 2 (p. 96).
  [BBHT98] M. Boyer, G. Brassard, P. Hoyer, A. Tapp, "Tight bounds on quantum searching",
        Fortschritte der Physik 46, 1998.
  [S] J. Pascoal Faria, J. Cunha, "Quantum computing: a brief introduction", TACS 2026/27 slides
      (definition of CNF; X => Y written as (not X or Y)).

Solver choices are not fixed here: `shots` is a parameter of the transformation and the number of
Grover rounds is derived from the number of solutions found by the classical baseline. Both are
stored in the SolverConfig of the output model, where T2 reads them.
"""

from besser.BUML.metamodel.object import ObjectModel

import metamodels as mm
from metamodels import attr, linked, objects_of
import baseline
import checks


class T1Error(Exception):
    """The input model does not satisfy the Problem DSL invariants, or the request is ambiguous."""


def transform(problem_model, shots=1024, request_name=None):
    """Run T1. Returns (solution ObjectModel, trace).

    trace: list of dicts {clause, text, rule, source, ref}, one per clause, in clause order.
    request_name: the SelectionRequest to encode; may be omitted when the model has 0 or 1 requests.
    """
    violations = checks.check_problem_model(problem_model)
    if violations:
        raise T1Error(f"input violates Problem DSL invariants: {violations}")

    (fm,) = objects_of(problem_model, mm.FeatureModel)
    request = _select_request(fm, request_name)

    # ---- Variables: one Boolean variable per feature [B05, sec. 3: "a variable of the formula is a
    # token, the name of a non-terminal, or the name of a pattern", i.e. one per feature].
    # Index (= qubit position): depth-first pre-order of the feature tree from the root, children in
    # alphabetical order of id. Deterministic, and each parent comes before its children.
    order = _preorder(linked(fm, "root")[0])
    fid = {f: attr(f, "id") for f in order}
    variables = {f: mm.Variable(f"v_{fid[f]}").attributes(name=fid[f], index=i).build()
                 for i, f in enumerate(order)}

    clauses = []      # list of (literals, rule, source, ref); literals = [(feature, isNegated)]

    def add(literals, rule, source, ref):
        # An identical clause adds nothing to a conjunction, so it is written only once.
        if frozenset(literals) not in {frozenset(lits) for lits, *_ in clauses}:
            clauses.append((literals, rule, source, ref))

    root = order[0]
    # R1 Root: the root is in every product. [B05, sec. 3 "Mapping Grammars": the predicate root = true;
    # T07, p. 96: "the formula that selects the root feature"]. Clause: (root).
    add([(root, False)], "R1 root", fid[root], "B05 sec. 3; T07 p. 96")

    for f in order:
        parents = linked(f, "parent")
        if parents:
            p = parents[0]
            # R2 Mandatory feature: parent => child [B05, sec. 3, formula (2): P <=> t;
            # T07 Fig. 2 "and": S <=> A]. The "=>" half: (not P or C).
            if attr(f, "isMandatory"):
                add([(p, True), (f, False)], "R2 mandatory: parent implies child", f"{fid[f]} (mandatory)",
                    "B05 sec. 3 (2); T07 Fig. 2")
            # R3 Child implies parent, for every non-root feature (optional, mandatory or group member):
            # [B05, sec. 3, formula (3): "if t2 is selected, Q is also selected"; the "<=" half of (2)
            # and of r <=> (P1 or ... or Pn); T07 Fig. 2: B => S]. Clause: (not C or P).
            add([(f, True), (p, False)], "R3 child implies parent", fid[f], "B05 sec. 3 (2),(3); T07 Fig. 2")

        for g in sorted(linked(f, "groups"), key=lambda g: g.name_):
            members = sorted(linked(g, "members"), key=lambda x: order.index(x))
            kind = g.classifier.name
            # R4 Group, at least one member when the parent is selected:
            # [B05, sec. 3 "Mapping Productions": r <=> (P1 or ... or Pn) for r+ ;
            # T07 Fig. 2 "or" S <=> A or B or C, and "alternative" (S <=> A or B or C) and atmost1(A,B,C)].
            # The "=>" half: (not P or M1 or ... or Mk); the "<=" half is R3 of each member.
            add([(f, True)] + [(x, False) for x in members], f"R4 {kind}: at least one member",
                f"{g.name_} ({', '.join(fid[x] for x in members)})", "B05 sec. 3; T07 Fig. 2")
            # R5 Xor, at most one member: atmost1(M1..Mk) [T07 Fig. 2 "alternative (choose1)";
            # B05 sec. 3 choose1]. "At most one is true" holds exactly when no two are true together,
            # so it is one clause per pair: (not Mi or not Mj).
            if kind == "Xor":
                for i, a in enumerate(members):
                    for b in members[i + 1:]:
                        add([(a, True), (b, True)], "R5 Xor: at most one member",
                            f"{g.name_} ({fid[a]}, {fid[b]})", "T07 Fig. 2; B05 sec. 3")

    requires_first = lambda c: (not mm.is_a(c, mm.RequiresConstraint), c.name_)
    for c in sorted(linked(fm, "constraints"), key=requires_first):
        a, b = linked(c, "source")[0], linked(c, "target")[0]
        if mm.is_a(c, mm.RequiresConstraint):
            # R6 "A requires B": A => B [B05, sec. 3, "non-grammar constraints": "inclusion" constraints are
            # propositional formulas conjoined onto the grammar's formula]. Clause: (not A or B).
            add([(a, True), (b, False)], "R6 requires", f"{c.name_} ({fid[a]} requires {fid[b]})", "B05 sec. 3")
        else:
            # R7 "A excludes B": not (A and B) [B05, sec. 3, "non-grammar constraints": "exclusion"].
            # Clause: (not A or not B).
            add([(a, True), (b, True)], "R7 excludes", f"{c.name_} ({fid[a]} excludes {fid[b]})", "B05 sec. 3")

    if request is not None:
        choices = sorted(linked(request, "choices"), key=lambda ch: order.index(linked(ch, "feature")[0]))
        for ch in choices:
            x = linked(ch, "feature")[0]
            # R8 Selection request: features selected (REQUIRED) or deselected (EXCLUDED) by the user
            # are fixed as assumptions [B05, sec. 4: "Assumptions are features that are manually selected
            # by users"]. Unit clause (X) for REQUIRED, (not X) for EXCLUDED.
            negated = attr(ch, "type") == "EXCLUDED"
            add([(x, negated)], f"R8 {attr(ch, 'type')}", f"{ch.name_} ({attr(ch, 'type')} {fid[x]})", "B05 sec. 4")

    # ---- Build the Solution DSL objects
    name = attr(fm, "name") + (f"_{attr(request, 'name')}" if request is not None else "")
    cnf = mm.CnfFormula("cnf").attributes(name=name).build()
    cnf.variables = set(variables.values())
    objects = [cnf, *variables.values()]
    trace = []
    for k, (lits, rule, source, ref) in enumerate(clauses, start=1):
        cl = mm.Clause(f"c{k}").attributes(id=f"c{k}").build()
        cl.cnfformula = cnf
        objects.append(cl)
        for j, (f, neg) in enumerate(lits, start=1):
            lit = mm.Literal(f"l{k}_{j}").attributes(isNegated=neg).build()
            lit.clause = cl
            lit.target = variables[f]
            objects.append(lit)
        text = " ∨ ".join(("¬" if neg else "") + fid[f] for f, neg in lits)
        trace.append({"clause": f"c{k}", "text": text, "rule": rule, "source": source, "ref": ref})

    # ---- SolverConfig: knownSolutions from the classical baseline run on the CNF built so far,
    # rounds derived from it [BBHT98].
    cnf_only = ObjectModel(name=f"{name}_cnf", objects=set(objects))
    m_solutions = len(baseline.cnf_solutions(cnf_only))
    rounds = baseline.grover_rounds(len(order), m_solutions)
    cfg = mm.SolverConfig("cfg").attributes(rounds=rounds, shots=shots, knownSolutions=m_solutions).build()
    cnf.solverconfig = cfg
    model = ObjectModel(name=f"{name}_solution", objects=set(objects) | {cfg})

    violations = checks.check_solution_model(model)
    if violations:
        raise T1Error(f"output violates Solution DSL invariants: {violations}")
    return model, trace


def _select_request(fm, request_name):
    requests = linked(fm, "requests")
    if request_name is not None:
        found = [r for r in requests if attr(r, "name") == request_name]
        if not found:
            raise T1Error(f"no SelectionRequest named {request_name!r}")
        return found[0]
    if len(requests) > 1:
        raise T1Error("the feature model has several SelectionRequests; pass request_name")
    return requests[0] if requests else None


def _preorder(root):
    out = [root]
    for child in sorted(linked(root, "children"), key=lambda c: attr(c, "id")):
        out += _preorder(child)
    return out
