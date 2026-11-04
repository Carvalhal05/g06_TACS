"""Tests for T1, the classical baseline and the validation.

    python -m unittest test_part2 -v      (from the Part2 folder)
"""

import random
import unittest
from itertools import product

import metamodels as mm
from metamodels import attr, objects_of
import baseline
import checks
import instances
import t1_problem_to_cnf as t1
import validation
from run_t1 import OUT, load_solution_model, signature

# n, m, M and rounds of each instance, as listed in Part1/Instances.md (I5: rounds 1, see grover_rounds)
EXPECTED = {"I1": (4, 8, 1, 3), "I2": (7, 15, 1, 8), "I3": (11, 20, 8, 12), "I4": (11, 23, 1, 35),
            "I5": (11, 20, 0, 1)}

INSTANCES = instances.all_instances()


def clause_set(model):
    names, clauses = baseline.read_cnf(model)
    return {frozenset((names[i], neg) for i, neg in lits) for _, lits in clauses}


def qiskit_key(bits):
    """Qiskit bitstring for an assignment (qubit 0 is the rightmost character)."""
    return "".join("1" if b else "0" for b in reversed(bits))


class TestOclChecks(unittest.TestCase):
    def test_every_ocl_constraint_has_a_check(self):
        for dm, cs in ((mm.problem_dsl, checks.PROBLEM_CHECKS), (mm.solution_dsl, checks.SOLUTION_CHECKS)):
            self.assertEqual(sorted(c.name for c in dm.constraints), sorted(map(checks.ocl_name, cs)))

    def test_part1_models_satisfy_the_invariants(self):
        self.assertEqual(checks.check_problem_model(mm.example_problem_model), {})
        self.assertEqual(checks.check_solution_model(mm.example_solution_model), {})

    def test_a_broken_model_is_rejected(self):
        spec = {**instances.MINIWATCH, "features": {**instances.MINIWATCH["features"],
                                                     "analog": ("Analog", "display", True)}}
        broken = instances.build_problem_model(spec)
        self.assertIn("GroupMembersNotMandatory", checks.check_problem_model(broken))
        with self.assertRaises(t1.T1Error):
            t1.transform(broken)


class TestT1(unittest.TestCase):
    def test_reproduces_the_hand_built_example(self):
        out, _ = t1.transform(mm.example_problem_model)
        self.assertEqual(clause_set(out), clause_set(mm.example_solution_model))
        (cfg,) = objects_of(out, mm.SolverConfig)
        (ref,) = objects_of(mm.example_solution_model, mm.SolverConfig)
        for a in ("knownSolutions", "rounds", "shots"):
            self.assertEqual(attr(cfg, a), attr(ref, a), a)

    def test_instance_sizes_match_instances_md(self):
        for inst, (_d, problem, request) in INSTANCES.items():
            out, _ = t1.transform(problem, request_name=request)
            names, clauses = baseline.read_cnf(out)
            (cfg,) = objects_of(out, mm.SolverConfig)
            got = (len(names), len(clauses), attr(cfg, "knownSolutions"), attr(cfg, "rounds"))
            self.assertEqual(got, EXPECTED[inst], inst)

    def test_output_satisfies_solution_dsl_invariants(self):
        for inst, (_d, problem, request) in INSTANCES.items():
            out, _ = t1.transform(problem, request_name=request)
            self.assertEqual(checks.check_solution_model(out), {}, inst)

    def test_every_clause_is_traced_to_a_rule_and_a_reference(self):
        for inst, (_d, problem, request) in INSTANCES.items():
            out, trace = t1.transform(problem, request_name=request)
            self.assertEqual(len(trace), len(baseline.read_cnf(out)[1]), inst)
            self.assertTrue(all(t["rule"] and t["ref"] for t in trace), inst)

    def test_shots_come_from_the_parameter(self):
        out, _ = t1.transform(mm.example_problem_model, shots=4000)
        (cfg,) = objects_of(out, mm.SolverConfig)
        self.assertEqual(attr(cfg, "shots"), 4000)

    def test_helper_built_i3_equals_the_part1_model(self):
        rebuilt = instances.build_problem_model(instances.SMARTWATCH, ("onlyGPS", ["gps"], ["heartrate"]))
        a, _ = t1.transform(rebuilt)
        b, _ = t1.transform(mm.example_problem_model)
        self.assertEqual(signature(a), signature(b))

    def test_generated_files_are_up_to_date(self):
        for inst, (_d, problem, request) in INSTANCES.items():
            out, _ = t1.transform(problem, request_name=request)
            (path,) = OUT.glob(f"{inst}_*.py")
            self.assertEqual(signature(load_solution_model(path)), signature(out), path.name)


class TestBaseline(unittest.TestCase):
    def test_cnf_agrees_with_feature_model_semantics(self):
        cases = [(p, r) for _d, p, r in INSTANCES.values()]
        cases += [(instances.build_problem_model(s), None)
                  for s in (instances.MINIWATCH, instances.SMARTWATCH_7, instances.SMARTWATCH)]
        for problem, request in cases:
            out, _ = t1.transform(problem, request_name=request)
            self.assertEqual(baseline.cnf_solutions(out), baseline.feature_model_configurations(problem, request))

    def test_counts_without_request(self):
        # Example.md: 33 configurations without the request; Instances.md: MiniWatch has 2.
        for spec, n in ((instances.SMARTWATCH, 33), (instances.MINIWATCH, 2)):
            out, _ = t1.transform(instances.build_problem_model(spec))
            self.assertEqual(len(baseline.cnf_solutions(out)), n)

    def test_grover_parameters(self):
        self.assertEqual(baseline.grover_rounds(11, 8), 12)
        self.assertEqual(baseline.grover_rounds(11, 1), 35)
        self.assertEqual(baseline.grover_rounds(11, 0), 1)
        self.assertEqual(baseline.success_probability(11, 0, 1), 0.0)
        self.assertGreater(baseline.success_probability(4, 1, 3), 0.96)


class TestValidation(unittest.TestCase):
    """The counts here are sampled from the ideal Grover distribution, not from a quantum run."""

    def ideal_counts(self, solution, shots, seed=7):
        names, clauses = baseline.read_cnf(solution)
        (cfg,) = objects_of(solution, mm.SolverConfig)
        n, m, k = len(names), attr(cfg, "knownSolutions"), attr(cfg, "rounds")
        p = baseline.success_probability(n, m, k)
        keys, weights = [], []
        for bits in product((False, True), repeat=n):
            ok = baseline.satisfies(bits, clauses)
            keys.append(qiskit_key(bits))
            weights.append(p / m if ok else (1 - p) / (2 ** n - m))
        counts = {}
        for key in random.Random(seed).choices(keys, weights, k=shots):
            counts[key] = counts.get(key, 0) + 1
        return counts

    def test_decode_uses_qiskit_bit_order(self):
        out, _ = t1.transform(INSTANCES["I1"][1], request_name="digitalOnly")
        names, _ = baseline.read_cnf(out)        # watch 0, display 1, analog 2, digital 3
        self.assertEqual(validation.decode("1011", names), {"watch", "display", "digital"})

    def test_ideal_run_matches_the_baseline(self):
        for inst in ("I1", "I3", "I4"):
            _d, problem, request = INSTANCES[inst]
            out, _ = t1.transform(problem, request_name=request)
            r = validation.validate(out, self.ideal_counts(out, 1024), problem)
            self.assertTrue(r["allFoundAreBaselineSolutions"], inst)
            self.assertAlmostEqual(r["measuredSuccess"], r["theoreticalSuccess"], delta=0.03, msg=inst)
            self.assertTrue(r["mostFrequent"][3], inst)

    def test_no_solution_instance(self):
        _d, problem, request = INSTANCES["I5"]
        out, _ = t1.transform(problem, request_name=request)
        r = validation.validate(out, self.ideal_counts(out, 1024), problem)
        self.assertEqual((r["validShots"], r["foundSolutions"], r["theoreticalSuccess"]), (0, 0, 0.0))
        self.assertIn("not valid", validation.report("I5", r))


if __name__ == "__main__":
    unittest.main()
