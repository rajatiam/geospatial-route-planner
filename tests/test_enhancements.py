import unittest, json, csv, io
from tests import test_routes as fixtures
from geospatial_route_planner.core import route_via


class FeatureTests(unittest.TestCase):
    setUp = fixtures.RouteTests.setUp

    def test_required_waypoint_changes_path(self):
        result = route_via(self.spec, "a", "d", ["c"])
        self.assertEqual(result["path"], ["a", "c", "d"])
        self.assertEqual(result["cost"], 5)

    def test_unreachable_waypoint_reports_segment(self):
        result = route_via(self.spec, "a", "d", ["c"], ["a:c"])
        self.assertFalse(result["reachable"])
        self.assertEqual(result["failed_segment"], ["a", "c"])

    def test_unknown_waypoint_rejected(self):
        with self.assertRaises(ValueError):
            route_via(self.spec, "a", "d", ["unknown"])
