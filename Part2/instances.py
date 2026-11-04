"""Problem DSL object models of the test instances of Part1/Instances.md (all SmartWatch family).

I3 is the hand-built object model of Part I (Part1/tacs262_assignment_project-4.py). The others are
built here with `build_problem_model`, which creates the same kind of B-UML objects and links as the
Part I model. I4 and I5 use the I3 feature model with a different selection request.
"""

from besser.BUML.metamodel.object import ObjectModel

import metamodels as mm

# id: (name, parent id, isMandatory)
MINIWATCH = {
    "name": "MiniWatch",
    "features": {
        "watch": ("Watch", None, False),
        "display": ("Display", "watch", True),
        "analog": ("Analog", "display", False),
        "digital": ("Digital", "display", False),
    },
    "groups": [("Xor", "xor_1", "display", ["analog", "digital"])],
    "requires": [],
    "excludes": [],
}

SMARTWATCH_7 = {
    "name": "SmartWatch7",
    "features": {
        **MINIWATCH["features"],
        "sensors": ("Sensors", "watch", False),
        "gps": ("GPS", "sensors", False),
        "heartrate": ("Heartrate", "sensors", False),
    },
    "groups": MINIWATCH["groups"] + [("Or", "or_1", "sensors", ["gps", "heartrate"])],
    "requires": [("requiresConstraint_1", "gps", "digital")],
    "excludes": [("excludesConstraint_1", "analog", "heartrate")],
}

SMARTWATCH = {
    **SMARTWATCH_7,
    "name": "SmartWatch",
    "features": {
        **SMARTWATCH_7["features"],
        "battery": ("Battery", "digital", True),
        "temperature": ("Temperature", "digital", False),
        "steps": ("StepsDistance", "digital", False),
        "weather": ("Weather", "digital", False),
    },
}


def build_problem_model(spec, request=None):
    """B-UML object model (Problem_DSL) for a feature model spec and an optional request.

    request: (name, [REQUIRED feature ids], [EXCLUDED feature ids]) or None.
    """
    fm = mm.FeatureModel(spec["name"]).attributes(name=spec["name"]).build()
    feats = {}
    for fid, (name, _parent, mandatory) in spec["features"].items():
        feats[fid] = mm.Feature(fid).attributes(id=fid, name=name, isMandatory=mandatory).build()
        feats[fid].featuremodel = fm
    root = [fid for fid, (_n, parent, _m) in spec["features"].items() if parent is None][0]
    feats[root].rootOf = fm
    for fid, (_n, parent, _m) in spec["features"].items():
        if parent is not None:
            feats[fid].parent = feats[parent]
    objects = [fm, *feats.values()]

    for kind, gname, parent, members in spec["groups"]:
        g = (mm.Xor if kind == "Xor" else mm.Or)(gname).build()
        g.parent = feats[parent]
        g.members = {feats[x] for x in members}
        objects.append(g)
    for cls, key in ((mm.RequiresConstraint, "requires"), (mm.ExcludesConstraint, "excludes")):
        for cname, src, tgt in spec[key]:
            c = cls(cname).build()
            c.source = feats[src]
            c.target = feats[tgt]
            c.featuremodel = fm
            objects.append(c)

    if request is not None:
        rname, required, excluded = request
        req = mm.SelectionRequest(f"selectionRequest_{rname}").attributes(name=rname).build()
        req.featuremodel = fm
        objects.append(req)
        choices = [(x, mm.SelectionType.REQUIRED) for x in required]
        choices += [(x, mm.SelectionType.EXCLUDED) for x in excluded]
        for k, (x, literal) in enumerate(choices, start=1):
            ch = mm.FeatureChoice(f"featureChoice_{rname}_{k}").attributes(type=literal).build()
            ch.selectionrequest = req
            ch.feature = feats[x]
            objects.append(ch)

    return ObjectModel(name=f"{spec['name']}_problem", objects=set(objects))


# instance id: (description, problem model, request name)
def all_instances():
    return {
        "I1": ("MiniWatch, digitalOnly (tiny, checkable by hand)",
               build_problem_model(MINIWATCH, ("digitalOnly", ["digital"], [])), "digitalOnly"),
        "I2": ("SmartWatch Part I version (7 features), onlyGPS (unique solution)",
               build_problem_model(SMARTWATCH_7, ("onlyGPS", ["gps"], ["heartrate"])), "onlyGPS"),
        "I3": ("SmartWatch (11 features), onlyGPS (main example, several solutions)",
               mm.example_problem_model, "onlyGPS"),
        "I4": ("SmartWatch (11 features), fullDigital (largest, unique solution)",
               build_problem_model(SMARTWATCH, ("fullDigital", ["gps", "temperature", "steps", "weather"],
                                                ["heartrate"])), "fullDigital"),
        "I5": ("SmartWatch (11 features), analogWithGPS (no solution)",
               build_problem_model(SMARTWATCH, ("analogWithGPS", ["analog", "gps"], [])), "analogWithGPS"),
    }
