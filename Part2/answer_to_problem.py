"""Mapping the answer of a run back to the Problem DSL.

A configuration found by the Grover run (a set of feature ids) is written as a Problem DSL model:
the same feature model as the input, with one new SelectionRequest that fixes every feature,
REQUIRED if it is in the configuration and EXCLUDED if it is not. No new concept is needed in the
metamodel: a complete selection request denotes exactly one product.

The model is a new object model, rebuilt from the input with `instances.build_problem_model`, so the
input model is not changed. It is checked in two ways:
  - it satisfies the Problem DSL invariants (`checks.check_problem_model`);
  - T1 applied to it gives a CNF whose only solution is the configuration (round trip).
"""

import metamodels as mm
from metamodels import attr, linked, objects_of
import baseline
import checks
import instances
import t1_problem_to_cnf as t1


class AnswerError(Exception):
    """The configuration cannot be written as a valid answer of the problem."""


def spec_of(problem_model):
    """The feature model of `problem_model` as a spec for `instances.build_problem_model`."""
    (fm,) = objects_of(problem_model, mm.FeatureModel)
    fid = lambda f: attr(f, "id")
    features = {}
    for f in linked(fm, "features"):
        parent = linked(f, "parent")
        features[fid(f)] = (attr(f, "name"), fid(parent[0]) if parent else None, attr(f, "isMandatory"))
    groups = [(g.classifier.name, g.name_, fid(linked(g, "parent")[0]), sorted(fid(x) for x in linked(g, "members")))
              for g in sorted(objects_of(problem_model, mm.Or) + objects_of(problem_model, mm.Xor),
                              key=lambda g: g.name_)]
    constraints = sorted(linked(fm, "constraints"), key=lambda c: c.name_)
    pairs = lambda cls: [(c.name_, fid(linked(c, "source")[0]), fid(linked(c, "target")[0]))
                         for c in constraints if mm.is_a(c, cls)]
    return {"name": attr(fm, "name"), "features": features, "groups": groups,
            "requires": pairs(mm.RequiresConstraint), "excludes": pairs(mm.ExcludesConstraint)}


def answer_model(problem_model, configuration, request_name="answer"):
    """Problem DSL model whose SelectionRequest `request_name` selects exactly `configuration`.

    configuration: iterable of feature ids (the true variables of a measured bitstring).
    """
    spec = spec_of(problem_model)
    chosen = set(configuration)
    unknown = chosen - set(spec["features"])
    if unknown:
        raise AnswerError(f"unknown feature ids {sorted(unknown)}")
    required = sorted(chosen)
    excluded = sorted(set(spec["features"]) - chosen)
    model = instances.build_problem_model(spec, (request_name, required, excluded))

    violations = checks.check_problem_model(model)
    if violations:
        raise AnswerError(f"answer model violates Problem DSL invariants: {violations}")
    solution, _trace = t1.transform(model, request_name=request_name)
    if baseline.cnf_solutions(solution) != {frozenset(chosen)}:
        raise AnswerError("the configuration is not a valid product of the feature model")
    return model
