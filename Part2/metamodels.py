"""Problem DSL and Solution DSL metamodels, loaded from the Part I B-UML file.

The metamodels are defined once, in Part1/tacs262_assignment_project-4.py (exported from BESSER).
Part II imports them from there so that every model built or read here conforms to exactly the
metamodels handed in for Part I.
"""

import runpy
from pathlib import Path

from besser.BUML.metamodel.structural import EnumerationLiteral

PART1_FILE = Path(__file__).resolve().parent.parent / "Part1" / "tacs262_assignment_project-4.py"

_part1 = runpy.run_path(str(PART1_FILE))

# Problem DSL (domain_model_1, "Problem_DSL")
problem_dsl = _part1["domain_model_1"]
FeatureModel = _part1["FeatureModel"]
Feature = _part1["Feature"]
Or = _part1["Or"]
Xor = _part1["Xor"]
RequiresConstraint = _part1["RequiresConstraint"]
ExcludesConstraint = _part1["ExcludesConstraint"]
SelectionRequest = _part1["SelectionRequest"]
FeatureChoice = _part1["FeatureChoice"]
SelectionType = _part1["SelectionType"]

# Solution DSL (domain_model_2, "Solution_DSL")
solution_dsl = _part1["domain_model_2"]
CnfFormula = _part1["CnfFormula"]
Variable = _part1["Variable"]
Clause = _part1["Clause"]
Literal = _part1["Literal"]
SolverConfig = _part1["SolverConfig"]

# Hand-built example of Part I (instance I3)
example_problem_model = _part1["object_model_1"]
example_solution_model = _part1["object_model_2"]


def attr(obj, name):
    """Value of attribute `name` of a B-UML object.

    Read from the object's slots: `obj.id` cannot be used, because BESSER objects have an internal
    `id` property that hides an attribute with the same name.
    """
    for slot in obj.slots:
        if slot.attribute.name == name:
            value = slot.value.value
            # enumeration literals (SelectionType) are returned by name, e.g. "REQUIRED"
            return value.name if isinstance(value, EnumerationLiteral) else value
    raise AttributeError(f"{obj.name_} has no attribute {name!r}")


def linked(obj, end):
    """Objects linked to `obj` through the association end named `end`, always as a list."""
    return [le.object for le in obj.link_ends() if le.name == end]


def objects_of(model, cls):
    """Objects of `model` whose class is `cls` or a subclass of it.

    Classes are compared by name, so that models loaded from a generated B-UML file (which defines
    its own copy of the metamodel classes) can be read with the same functions.
    """
    return [o for o in model.objects
            if o.classifier.name == cls.name or cls.name in {p.name for p in o.classifier.all_parents()}]


def is_a(obj, cls):
    """True if the class of `obj` is `cls` (compared by name, see `objects_of`)."""
    return obj.classifier.name == cls.name