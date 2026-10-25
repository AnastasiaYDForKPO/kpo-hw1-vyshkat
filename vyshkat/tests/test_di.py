import unittest

from vyshkat.bootstrap import build_container
from vyshkat.catalog import AssetForm, AssetKind, Catalog, ItemCatalog, VehicleCatalog
from vyshkat.console import ConsoleApp
from vyshkat.di import Container, DependencyError
from vyshkat.domain import Helmet
from vyshkat.services import Fleet, FleetReports


class ContainerTest(unittest.TestCase):
    def test_singleton_returns_same_instance(self):
        c = Container()
        c.register_singleton(list, lambda _: [])
        self.assertIs(c.resolve(list), c.resolve(list))

    def test_transient_returns_new_instance(self):
        c = Container()
        c.register_transient(list, lambda _: [])
        self.assertIsNot(c.resolve(list), c.resolve(list))

    def test_re_registration_replaces_cached_singleton(self):
        c = Container()
        c.register_singleton(str, lambda _: "old")
        self.assertEqual(c.resolve(str), "old")
        c.register_instance(str, "new")
        self.assertEqual(c.resolve(str), "new")

    def test_unknown_dependency(self):
        with self.assertRaises(DependencyError):
            Container().resolve(int)

    def test_cycle_detection(self):
        c = Container()
        c.register_singleton(int, lambda c: c.resolve(str))
        c.register_singleton(str, lambda c: c.resolve(int))
        with self.assertRaisesRegex(DependencyError, "Циклическая"):
            c.resolve(int)

    def test_failed_factory_does_not_leave_container_broken(self):
        c = Container()
        c.register_singleton(int, lambda _: 1 / 0)
        with self.assertRaises(ZeroDivisionError):
            c.resolve(int)
        c.register_instance(int, 42)
        self.assertEqual(c.resolve(int), 42)


class CompositionRootTest(unittest.TestCase):
    def test_whole_graph_resolves(self):
        container = build_container()
        app = container.resolve(ConsoleApp)
        self.assertIsInstance(app, ConsoleApp)

    def test_reports_and_fleet_share_one_fleet(self):
        container = build_container()
        fleet = container.resolve(Fleet)
        fleet.register_item(Helmet("H"))
        self.assertEqual(container.resolve(FleetReports).summary().items, 1)

    def test_catalogs_are_populated(self):
        container = build_container()
        self.assertEqual([k.key for k in container.resolve(VehicleCatalog).kinds()], ["scooter", "bike", "ebike"])
        self.assertEqual(len(container.resolve(ItemCatalog).kinds()), 3)


class CatalogTest(unittest.TestCase):
    def test_duplicate_keys_rejected(self):
        kind = AssetKind("h", "Шлем", False, lambda f: Helmet(f.name))
        with self.assertRaises(ValueError):
            Catalog([kind, kind])

    def test_unknown_key(self):
        with self.assertRaises(ValueError):
            Catalog([]).get("nope")

    def test_kind_creates_asset_from_form(self):
        kind = build_container().resolve(VehicleCatalog).get("ebike")
        ebike = kind.create(AssetForm("E", simplicity=5, condition=90, daily_energy_kwh=0.7))
        self.assertEqual(ebike.daily_energy_kwh, 0.7)


if __name__ == "__main__":
    unittest.main()
