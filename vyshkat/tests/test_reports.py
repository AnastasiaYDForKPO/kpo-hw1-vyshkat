import unittest

from vyshkat.di import Container
from vyshkat.domain import BeginnerRated, Bicycle, ChargingCabinet, DockStation, ElectricBicycle, Helmet, Scooter
from vyshkat.services import BeginnerPolicy, Fleet, FleetReports, SimplicityThresholdPolicy

from vyshkat.tests.fakes import StubInspection, container_with


class BeginnerPolicyTest(unittest.TestCase):
    """Правило «для новичков»: простота ≥ 6."""

    def setUp(self):
        self.policy = SimplicityThresholdPolicy()

    def test_threshold_boundary(self):
        self.assertFalse(self.policy.is_suitable(Bicycle("5", 5, 90)))
        self.assertTrue(self.policy.is_suitable(Bicycle("6", 6, 90)))
        self.assertTrue(self.policy.is_suitable(Bicycle("10", 10, 90)))

    def test_custom_threshold(self):
        self.assertFalse(SimplicityThresholdPolicy(min_simplicity=8).is_suitable(Bicycle("7", 7, 90)))


class _ReportsTestCase(unittest.TestCase):
    def build(self, container: Container | None = None) -> tuple[Fleet, FleetReports]:
        container = container or container_with(inspection=StubInspection(accepted=True))
        return container.resolve(Fleet), container.resolve(FleetReports)


class FleetReportsTest(_ReportsTestCase):
    def setUp(self):
        self.fleet, self.reports = self.build()
        self.easy_scooter = Scooter("easy", 7, 90, 0.5)
        self.hard_ebike = ElectricBicycle("hard", 4, 90, 0.8)
        self.edge_bike = Bicycle("edge", 6, 90)
        for vehicle in (self.easy_scooter, self.hard_ebike, self.edge_bike):
            self.fleet.admit_vehicle(vehicle)
        self.fleet.register_item(Helmet("H"))
        self.fleet.register_item(DockStation("D", 4.0))
        self.fleet.register_item(ChargingCabinet("C", 7.5))

    def test_summary_counts(self):
        summary = self.reports.summary()
        self.assertEqual((summary.vehicles, summary.items, summary.total), (3, 3, 6))
        self.assertEqual(summary.by_kind["Электросамокат"], 1)
        self.assertEqual(summary.by_kind["Шлем"], 1)

    def test_total_energy_includes_vehicles_and_items_but_skips_non_consumers(self):
        # 0.5 + 0.8 + 4.0 + 7.5; велосипед и шлем не учитываются
        self.assertAlmostEqual(self.reports.total_daily_energy_kwh(), 12.8)

    def test_beginner_list_uses_threshold_six(self):
        self.assertEqual(self.reports.beginner_friendly_vehicles(), [self.easy_scooter, self.edge_bike])

    def test_inventory_lists_vehicles_and_items_by_number(self):
        numbers = [asset.inventory_number for asset in self.reports.inventory()]
        self.assertEqual(numbers, ["VK-0001", "VK-0002", "VK-0003", "VK-0004", "VK-0005", "VK-0006"])

    def test_rejected_vehicle_is_absent_from_reports(self):
        container = container_with(inspection=StubInspection(accepted=False))
        fleet, reports = self.build(container)
        fleet.admit_vehicle(Scooter("rejected", 9, 90, 0.4))
        self.assertEqual(reports.summary().total, 0)
        self.assertEqual(reports.total_daily_energy_kwh(), 0)
        self.assertEqual(reports.beginner_friendly_vehicles(), [])


class ReplaceBeginnerPolicyTest(_ReportsTestCase):
    """Правило «для новичков» подменяется через DI — отчёты не меняются (OCP)."""

    class NoElectricForBeginners(BeginnerPolicy):
        def is_suitable(self, device: BeginnerRated) -> bool:
            return device.simplicity >= 6 and not isinstance(device, (Scooter, ElectricBicycle))

    def test_reports_use_injected_policy(self):
        container = container_with(inspection=StubInspection(accepted=True))
        container.register_instance(BeginnerPolicy, self.NoElectricForBeginners())
        fleet, reports = self.build(container)
        bike = Bicycle("bike", 9, 90)
        fleet.admit_vehicle(Scooter("scooter", 9, 90, 0.4))
        fleet.admit_vehicle(bike)

        self.assertEqual(reports.beginner_friendly_vehicles(), [bike])


if __name__ == "__main__":
    unittest.main()
