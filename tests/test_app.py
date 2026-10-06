import unittest

from app import generate_recommendations, load_activity_catalog


class TestOutdoorPlanner(unittest.TestCase):
    def test_catalog_loads_activity_data(self):
        activities = load_activity_catalog()
        self.assertGreater(len(activities), 5)
        self.assertIn("name", activities[0])

    def test_recommendations_return_results(self):
        results = generate_recommendations(
            "I want a calm walk with birds and fall colors",
            "Sunny",
            "Morning",
            2,
            "Relax",
        )
        self.assertGreater(len(results), 0)
        self.assertIn("name", results[0][0])


if __name__ == "__main__":
    unittest.main()
