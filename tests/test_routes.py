import copy, unittest
from geospatial_route_planner.core import route, validate


class RouteTests(unittest.TestCase):
    def setUp(self):
        self.spec = {
            "nodes": ["a", "b", "c", "d"],
            "edges": [
                {"from": "a", "to": "b", "cost": 2},
                {"from": "b", "to": "d", "cost": 2},
                {"from": "a", "to": "c", "cost": 3},
                {"from": "c", "to": "d", "cost": 2},
            ],
        }

    def test_shortest_path(self):
        self.assertEqual(route(self.spec, "a", "d")["path"], ["a", "b", "d"])
        self.assertEqual(route(self.spec, "a", "d")["cost"], 4)

    def test_blocked_edge(self):
        self.assertEqual(route(self.spec, "a", "d", ["a:b"])["path"], ["a", "c", "d"])

    def test_direction_and_unreachable(self):
        self.assertFalse(route(self.spec, "d", "a")["reachable"])

    def test_identity(self):
        self.assertEqual(route(self.spec, "a", "a")["cost"], 0)

    def test_negative_and_nan_costs(self):
        for cost in [-1, float("nan")]:
            self.spec["edges"][0]["cost"] = cost
            with self.assertRaises(ValueError):
                validate(self.spec)

    def test_zero_cost_cycle(self):
        self.spec["edges"] += [{"from": "b", "to": "a", "cost": 0}]
        self.assertTrue(route(self.spec, "a", "d")["reachable"])

    def test_tie_determinism(self):
        self.spec["edges"][2]["cost"] = 2
        self.assertEqual(route(self.spec, "a", "d")["path"], ["a", "b", "d"])

    def test_unknown_node_and_duplicate_edge(self):
        with self.assertRaises(ValueError):
            route(self.spec, "missing", "a")
        self.spec["edges"].append(copy.deepcopy(self.spec["edges"][0]))
        with self.assertRaises(ValueError):
            validate(self.spec)
