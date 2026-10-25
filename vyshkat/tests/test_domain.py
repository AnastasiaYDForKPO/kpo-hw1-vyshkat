import unittest

from vyshkat.domain import (
    BeginnerRated,
    Bicycle,
    ChargingCabinet,
    DockStation,
    ElectricBicycle,
    EnergyConsumer,
    Helmet,
    Inventoriable,
    Scooter,
)


class RolesTest(unittest.TestCase):
    """Объекты реализуют только свои роли (ISP)."""

    def test_electric_vehicles_consume_energy_and_have_simplicity(self):
        for vehicle in (Scooter("S", 7, 90, 0.4), ElectricBicycle("E", 5, 90, 0.7)):
            self.assertIsInstance(vehicle, EnergyConsumer)
            self.assertIsInstance(vehicle, BeginnerRated)
            self.assertIsInstance(vehicle, Inventoriable)

    def test_bicycle_does_not_consume_energy(self):
        bike = Bicycle("B", 9, 90)
        self.assertNotIsInstance(bike, EnergyConsumer)
        self.assertIsInstance(bike, BeginnerRated)

    def test_items_are_inventoriable_but_not_rated_for_beginners(self):
        for item in (Helmet("H"), DockStation("D", 4.0), ChargingCabinet("C", 7.5)):
            self.assertIsInstance(item, Inventoriable)
            self.assertNotIsInstance(item, BeginnerRated)

    def test_helmet_does_not_consume_energy(self):
        self.assertNotIsInstance(Helmet("H"), EnergyConsumer)


class ValidationTest(unittest.TestCase):
    def test_simplicity_bounds(self):
        Bicycle("min", 1, 90)
        Bicycle("max", 10, 90)
        for bad in (0, 11):
            with self.assertRaises(ValueError):
                Bicycle("bad", bad, 90)

    def test_condition_bounds(self):
        for bad in (-1, 101):
            with self.assertRaises(ValueError):
                Bicycle("bad", 5, bad)

    def test_energy_must_be_positive(self):
        with self.assertRaises(ValueError):
            Scooter("S", 7, 90, 0)
        with self.assertRaises(ValueError):
            DockStation("D", -1)

    def test_name_must_not_be_blank(self):
        with self.assertRaises(ValueError):
            Helmet("   ")

    def test_name_is_trimmed(self):
        self.assertEqual(Helmet("  Шлем  ").name, "Шлем")


class InventoryNumberTest(unittest.TestCase):
    def test_new_asset_has_no_number(self):
        self.assertIsNone(Helmet("H").inventory_number)

    def test_number_can_be_assigned_only_once(self):
        helmet = Helmet("H")
        helmet.assign_inventory_number("VK-0001")
        self.assertEqual(helmet.inventory_number, "VK-0001")
        with self.assertRaises(ValueError):
            helmet.assign_inventory_number("VK-0002")

    def test_str_contains_kind_and_name(self):
        self.assertEqual(str(Scooter("G30", 7, 90, 0.4)), "Электросамокат <G30>")


if __name__ == "__main__":
    unittest.main()
