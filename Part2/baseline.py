"""Classical baseline: exhaustive (brute-force) search over all 2^n assignments.

Two independent computations of the valid configurations of an instance:

- `cnf_solutions` evaluates the CNF formula (Solution DSL model produced by T1);
- `feature_model_configurations` reads the feature model (Problem DSL model) and applies the
  semantics of each construct directly, without any CNF.

If T1 is correct, both give the same set of configurations. The number of solutions M is what
fixes the number of Grover rounds (SolverConfig.rounds).

With at most 12 variables (OCL rule QubitLimit) there are at most 4096 assignments, so brute
force is exact and fast; no SAT solver is needed.
"""

import math
from itertools import product

import metamodels as mm
from metamodels import attr, linked, objects_of


# ---------------------------------------------------------------- reading a CNF model

def read_cnf(solution_model):
    """(variables, clauses) of the single CnfFormula of `solution_model`.

    variables: list of variable names, position i = Variable with index i (= qubit i).
    clauses:   list of (clause id, [(variable index, isNegated), ...]).
    """
    (cnf,) = objects_of(solution_model, mm.CnfFormula)
    variables = sorted(linked(cnf, "variables"), key=lambda v: attr(v, "index"))
    names = [attr(v, "name") for v in variables]
    clauses = []
    for cl in sorted(linked(cnf, "clauses"), key=lambda c: int(attr(c, "id")[1:])):
        lits = [(attr(linked(l, "target")[0], "index"), attr(l, "isNegated")) for l in linked(cl, "literals")]
        clauses.append((attr(cl, "id"), sorted(lits)))
    return names, clauses


def satisfies(bits, clauses):
    """True if the assignment `bits` (bits[i] = value of variable i) satisfies every clause."""
    return all(any(bits[i] != neg for i, neg in lits) for _, lits in clauses)


def cnf_solutions(solution_model):
    """All satisfying assignments of the CNF, each as the frozenset of names of the true variables."""
    names, clauses = read_cnf(solution_model)
    return {frozenset(n for n, b in zip(names, bits) if b)
            for bits in product((False, True), repeat=len(names)) if satisfies(bits, clauses)}


# ---------------------------------------------------------------- feature model semantics (no CNF)

def feature_model_configurations(problem_model, request_name=None):
    """All valid configurations of the feature model, as frozensets of feature ids.

    A set S of features is a valid configuration when (Batory 2005, sec. 2-3):
      - the root is in S;
      - every feature in S other than the root has its parent in S;
      - every mandatory child of a feature in S is in S;
      - for every group whose parent is in S, at least one member is in S (Or),
        or exactly one member is in S (Xor);
      - for every "A requires B": A in S implies B in S; for every "A excludes B": not both in S;
      - and, if a selection request is given, its REQUIRED features are in S and its EXCLUDED
        features are not.
    """
    (fm,) = objects_of(problem_model, mm.FeatureModel)
    features = linked(fm, "features")
    fid = {f: attr(f, "id") for f in features}
    root = fid[linked(fm, "root")[0]]
    parent = {fid[f]: fid[p[0]] for f in features if (p := linked(f, "parent"))}
    mandatory = {fid[f] for f in features if attr(f, "isMandatory")}
    groups = [(g.classifier.name, fid[linked(g, "parent")[0]], [fid[x] for x in linked(g, "members")])
              for g in objects_of(problem_model, mm.Or) + objects_of(problem_model, mm.Xor)]
    pairs = [(c.classifier.name, fid[linked(c, "source")[0]], fid[linked(c, "target")[0]])
             for c in linked(fm, "constraints")]
    required, excluded = set(), set()
    if request_name is not None:
        (req,) = [r for r in linked(fm, "requests") if attr(r, "name") == request_name]
        for ch in linked(req, "choices"):
            (required if attr(ch, "type") == "REQUIRED" else excluded).add(fid[linked(ch, "feature")[0]])

    def valid(s):
        if root not in s or not required <= s or excluded & s:
            return False
        if any(f != root and parent[f] not in s for f in s):
            return False
        if any(f in mandatory and parent[f] in s and f not in s for f in parent):
            return False
        for kind, p, members in groups:
            if p in s:
                k = sum(x in s for x in members)
                if k < 1 or (kind == "Xor" and k > 1):
                    return False
        for kind, a, b in pairs:
            if kind == "RequiresConstraint" and a in s and b not in s:
                return False
            if kind == "ExcludesConstraint" and a in s and b in s:
                return False
        return True

    ids = sorted(fid.values())
    return {s for bits in product((False, True), repeat=len(ids))
            if valid(s := frozenset(i for i, b in zip(ids, bits) if b))}


# ---------------------------------------------------------------- Grover parameters

def grover_rounds(n, m):
    """Number of Grover rounds for N = 2^n states and M solutions: floor(pi/4 * sqrt(N/M)).

    Boyer, Brassard, Hoyer, Tapp (1998), "Tight bounds on quantum searching".
    When M = 0 the oracle marks nothing, so every round leaves the uniform superposition unchanged
    and the number of rounds does not change the measured distribution; we then use 1, the smallest
    value allowed by the OCL rule PositiveExecutionParams (rounds > 0). For the same reason the
    result is never below 1.
    """
    if m == 0:
        return 1
    return max(1, math.floor(math.pi / 4 * math.sqrt(2 ** n / m)))


def success_probability(n, m, rounds):
    """Probability that one measurement after `rounds` Grover rounds gives a solution.

    sin^2((2k+1) theta) with sin^2(theta) = M/N (Boyer et al. 1998).
    """
    if m == 0:
        return 0.0
    theta = math.asin(math.sqrt(m / 2 ** n))
    return math.sin((2 * rounds + 1) * theta) ** 2
