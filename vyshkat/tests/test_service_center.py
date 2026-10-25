import unittest

from vyshkat.domain import Bicycle, ElectricBicycle, Scooter
from vyshkat.services import ServiceCenter


class ServiceCenterTest(unittest.TestCase):
    """Правила реального техосмотра."""

    def setUp(self):
        self.center = ServiceCenter(min_condition=70, max_daily_energy_kwh=1.5)

    def test_accepts_vehicle_in_good_condition(self):
        result = self.center.inspect(Scooter("S", 7, 95, 0.45))
        self.assertTrue(result.accepted)

    def test_accepts_condition_exactly_on_threshold(self):
        self.assertTrue(self.center.inspect(Bicycle("B", 9, 70)).accepted)

    def test_rejects_worn_vehicle(self):
        result = self.center.inspect(Bicycle("B", 9, 69))
        self.assertFalse(result.accepted)
        self.assertIn("Изношен", result.reason)

    def test_rejects_abnormal_energy_consumption(self):
        result = self.center.inspect(ElectricBicycle("E", 5, 95, 3.2))
        self.assertFalse(result.accepted)
        self.assertIn("расход", result.reason)

    def test_energy_rule_does_not_apply_to_non_electric(self):
        self.assertTrue(self.center.inspect(Bicycle("B", 9, 100)).accepted)

    def test_thresholds_are_configurable(self):
        strict = ServiceCenter(min_condition=99)
        self.assertFalse(strict.inspect(Bicycle("B", 9, 95)).accepted)


if __name__ == "__main__":
    unittest.main()
