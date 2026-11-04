"""The OCL invariants of both metamodels, checked in Python.

Each function has the name of one OCL constraint of Part I and checks the same condition. They are
written in Python because the BESSER OCL evaluator (bocl 1.0.4) cannot evaluate most of our
constraints: it fails with Python syntax errors on `implies`, `oclIsTypeOf` and `forAll`, and it
resolves `isUnique(id)` to Python's built-in `id`.

T1 runs `check_problem_model` on its input (precondition) and `check_solution_model` on its output
(postcondition). Each check returns a list of violations; an empty list means the invariant holds.
"""

import metamodels as mm
from metamodels import attr, linked, objects_of


def _one(obj, end):
    found = linked(obj, end)
    return found[0] if found else None


# ---------------------------------------------------------------- Problem DSL (19 invariants)

def HasFeatures(m):
    return [f"{fm.name_}: no features" for fm in objects_of(m, mm.FeatureModel) if not linked(fm, "features")]


def HasRoot(m):
    return [f"{fm.name_}: no root" for fm in objects_of(m, mm.FeatureModel) if not linked(fm, "root")]


def RootBelongsToModel(m):
    return [f"{fm.name_}: root {r.name_} not in features" for fm in objects_of(m, mm.FeatureModel)
            for r in linked(fm, "root") if r not in linked(fm, "features")]


def RootHasNoParent(m):
    return [f"root {r.name_} has a parent" for fm in objects_of(m, mm.FeatureModel)
            for r in linked(fm, "root") if linked(r, "parent")]


def UniqueFeatureIds(m):
    out = []
    for fm in objects_of(m, mm.FeatureModel):
        ids = [attr(f, "id") for f in linked(fm, "features")]
        out += [f"{fm.name_}: id {i!r} used twice" for i in sorted(set(ids)) if ids.count(i) > 1]
    return out


def OnlyRootHasNoParent(m):
    return [f"{f.name_}: no parent but not the root" for f in objects_of(m, mm.Feature)
            if not linked(f, "parent") and _one(_one(f, "featuremodel"), "root") is not f]


def ParentInSameModel(m):
    return [f"{f.name_}: parent in another model" for f in objects_of(m, mm.Feature)
            for p in linked(f, "parent") if _one(p, "featuremodel") is not _one(f, "featuremodel")]


def XorAtLeastTwo(m):
    return [f"{g.name_}: Xor with fewer than 2 members" for g in objects_of(m, mm.Xor) if len(linked(g, "members")) < 2]


def OrAtLeastOne(m):
    return [f"{g.name_}: Or without members" for g in objects_of(m, mm.Or) if len(linked(g, "members")) < 1]


def MembersAreChildren(m):
    return [f"{g.name_}: member {x.name_} is not a child of the group's parent"
            for g in objects_of(m, mm.Or) + objects_of(m, mm.Xor)
            for x in linked(g, "members") if linked(x, "parent") != linked(g, "parent")]


def Differentfeatures(m):
    return [f"{c.name_}: source = target" for c in _constraints(m) if linked(c, "source") == linked(c, "target")]


def SameModel(m):
    return [f"{c.name_}: source or target in another model" for c in _constraints(m)
            for x in linked(c, "source") + linked(c, "target")
            if _one(x, "featuremodel") is not _one(c, "featuremodel")]


def OneChoicePerFeature(m):
    out = []
    for r in objects_of(m, mm.SelectionRequest):
        feats = [_one(ch, "feature") for ch in linked(r, "choices")]
        out += [f"{r.name_}: two choices for {f.name_}" for f in set(feats) if feats.count(f) > 1]
    return out


def FeatureInRequestModel(m):
    return [f"{ch.name_}: feature of another model" for ch in objects_of(m, mm.FeatureChoice)
            if _one(_one(ch, "feature"), "featuremodel") is not _one(_one(ch, "selectionrequest"), "featuremodel")]


def RootNotMandatory(m):
    return [f"root {r.name_} is mandatory" for fm in objects_of(m, mm.FeatureModel)
            for r in linked(fm, "root") if attr(r, "isMandatory")]


def IdNotEmpty(m):
    return [f"{f.name_}: empty id" for f in objects_of(m, mm.Feature) if not attr(f, "id")]


def GroupMembersNotMandatory(m):
    return [f"{g.name_}: member {x.name_} is mandatory" for g in objects_of(m, mm.Or) + objects_of(m, mm.Xor)
            for x in linked(g, "members") if attr(x, "isMandatory")]


def NoCycles(m):
    out = []
    for f in objects_of(m, mm.Feature):
        seen, p = set(), _one(f, "parent")
        while p is not None and p not in seen:
            if p is f:
                out.append(f"{f.name_}: cycle in the hierarchy")
                break
            seen.add(p)
            p = _one(p, "parent")
    return out


def UniqueMembers(m):
    out = []
    for g in objects_of(m, mm.Or) + objects_of(m, mm.Xor):
        ids = [attr(x, "id") for x in linked(g, "members")]
        out += [f"{g.name_}: member id {i!r} twice" for i in set(ids) if ids.count(i) > 1]
    return out


def _constraints(m):
    return objects_of(m, mm.RequiresConstraint) + objects_of(m, mm.ExcludesConstraint)


PROBLEM_CHECKS = [HasFeatures, HasRoot, RootBelongsToModel, RootHasNoParent, UniqueFeatureIds, OnlyRootHasNoParent,
                  ParentInSameModel, XorAtLeastTwo, OrAtLeastOne, MembersAreChildren, Differentfeatures, SameModel,
                  OneChoicePerFeature, FeatureInRequestModel, RootNotMandatory, IdNotEmpty,
                  GroupMembersNotMandatory, NoCycles, UniqueMembers]


# ---------------------------------------------------------------- Solution DSL (17 invariants)

def _formulas(m):
    return objects_of(m, mm.CnfFormula)


def HasVariables(m):
    return [f"{c.name_}: no variables" for c in _formulas(m) if not linked(c, "variables")]


def HasSolverConfig(m):
    return [f"{c.name_}: no SolverConfig" for c in _formulas(m) if not linked(c, "solverconfig")]


def UniqueVariableNames(m):
    out = []
    for c in _formulas(m):
        names = [attr(v, "name") for v in linked(c, "variables")]
        out += [f"{c.name_}: variable name {n!r} twice" for n in set(names) if names.count(n) > 1]
    return out


def UniqueVariableIndexes(m):
    out = []
    for c in _formulas(m):
        idx = [attr(v, "index") for v in linked(c, "variables")]
        out += [f"{c.name_}: index {i} twice" for i in set(idx) if idx.count(i) > 1]
    return out


def UniqueClauseIds(m):
    out = []
    for c in _formulas(m):
        ids = [attr(cl, "id") for cl in linked(c, "clauses")]
        out += [f"{c.name_}: clause id {i!r} twice" for i in set(ids) if ids.count(i) > 1]
    return out


def NameNotEmpty(m):
    return [f"{v.name_}: empty name" for v in objects_of(m, mm.Variable) if not attr(v, "name")]


def NonNegativeIndex(m):
    return [f"{v.name_}: negative index" for v in objects_of(m, mm.Variable) if attr(v, "index") < 0]


def AtLeastOneLiteral(m):
    return [f"{cl.name_}: no literals" for cl in objects_of(m, mm.Clause) if not linked(cl, "literals")]


def IdNotEmpty_Clause(m):
    return [f"{cl.name_}: empty id" for cl in objects_of(m, mm.Clause) if not attr(cl, "id")]


IdNotEmpty_Clause.ocl_name = "IdNotEmpty"  # same name as the Feature invariant, other context (Clause)


def UniqueVariablePerClause(m):
    out = []
    for cl in objects_of(m, mm.Clause):
        targets = [_one(l, "target") for l in linked(cl, "literals")]
        out += [f"{cl.name_}: variable {t.name_} twice" for t in set(targets) if targets.count(t) > 1]
    return out


def LiteralsBelongToFromulaVariables(m):
    return [f"{cl.name_}: literal on a variable of another formula" for cl in objects_of(m, mm.Clause)
            for l in linked(cl, "literals") if _one(l, "target") not in linked(_one(cl, "cnfformula"), "variables")]


def PositiveExecutionParams(m):
    return [f"{s.name_}: rounds and shots must be > 0" for s in objects_of(m, mm.SolverConfig)
            if not (attr(s, "rounds") > 0 and attr(s, "shots") > 0)]


def NonNegativeKnownSolutions(m):
    return [f"{s.name_}: negative knownSolutions" for s in objects_of(m, mm.SolverConfig) if attr(s, "knownSolutions") < 0]


def HasClauses(m):
    return [f"{c.name_}: no clauses" for c in _formulas(m) if not linked(c, "clauses")]


def ContigousIndexes(m):
    return [f"{c.name_}: index {attr(v, 'index')} >= number of variables" for c in _formulas(m)
            for v in linked(c, "variables") if attr(v, "index") >= len(linked(c, "variables"))]


def KnownSolutionsBounded(m):
    return [f"{c.name_}: knownSolutions > 2^n" for c in _formulas(m) for s in linked(c, "solverconfig")
            if attr(s, "knownSolutions") > 2 ** len(linked(c, "variables"))]


def QubitLimit(m):
    return [f"{c.name_}: {len(linked(c, 'variables'))} variables > 12" for c in _formulas(m)
            if len(linked(c, "variables")) > 12]


SOLUTION_CHECKS = [HasVariables, HasSolverConfig, UniqueVariableNames, UniqueVariableIndexes, UniqueClauseIds,
                   NameNotEmpty, NonNegativeIndex, AtLeastOneLiteral, IdNotEmpty_Clause, UniqueVariablePerClause,
                   LiteralsBelongToFromulaVariables, PositiveExecutionParams, NonNegativeKnownSolutions, HasClauses,
                   ContigousIndexes, KnownSolutionsBounded, QubitLimit]


def ocl_name(check):
    return getattr(check, "ocl_name", check.__name__)


def _run(model, checks):
    return {ocl_name(c): v for c in checks if (v := c(model))}


def check_problem_model(model):
    """Violated Problem DSL invariants of `model`, as {constraint name: [violations]}."""
    return _run(model, PROBLEM_CHECKS)


def check_solution_model(model):
    """Violated Solution DSL invariants of `model`, as {constraint name: [violations]}."""
    return _run(model, SOLUTION_CHECKS)
