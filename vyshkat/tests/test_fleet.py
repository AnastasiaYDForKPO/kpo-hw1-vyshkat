import unittest

from vyshkat.domain import Bicycle, DockStation, Helmet, Scooter
from vyshkat.services import Fleet, ServiceCenter, TechnicalInspection

from vyshkat.tests.fakes import StubInspection, container_with
# тесты парка, три шшага (подготовка действие и проверка)
# подмена техосмотра через di-кнтейнер

class FleetAdmissionWithStubInspectionTest(unittest.TestCase):
    # парк спрашивает заглушку
    def test_container_injects_the_stub_into_fleet(self):
        stub = StubInspection(accepted=True) # заглушка всех принимать
        fleet = container_with(inspection=stub).resolve(Fleet) # парк с этой заглушкой
        bike = Bicycle("B", 9, 10) # состояние 10% настоящий центр бы кикнул

        result = fleet.admit_vehicle(bike)

        self.assertEqual(stub.inspected, [bike]) # велосипед приносили именно загулшке
        self.assertTrue(result.accepted) # и раз он сказал да => принят

    # принятая машина получает номер и попадает в парк
    def test_accepted_vehicle_is_added_and_gets_inventory_number(self):
        fleet = container_with(inspection=StubInspection(accepted=True)).resolve(Fleet)
        scooter = Scooter("S", 7, 90, 0.4)

        result = fleet.admit_vehicle(scooter)

        self.assertEqual(result.inventory_number, "VK-0001")
        self.assertEqual(scooter.inventory_number, "VK-0001")
        self.assertIn(scooter, fleet.vehicles)

    # отклоенная машина не попадает в парк и не получает номер
    def test_rejected_vehicle_is_not_added_and_gets_no_number(self):
        stub = StubInspection(accepted=False, reason="тормоза не работают")
        fleet = container_with(inspection=stub).resolve(Fleet)
        scooter = Scooter("S", 10, 100, 0.3)

        result = fleet.admit_vehicle(scooter)

        self.assertFalse(result.accepted)
        self.assertEqual(result.reason, "тормоза не работают")
        self.assertIsNone(result.inventory_number)
        self.assertIsNone(scooter.inventory_number)
        self.assertEqual(fleet.vehicles, ())

    # не тратит номер
    def test_rejection_does_not_consume_inventory_number(self):
        stub = StubInspection(accepted=False)
        container = container_with(inspection=stub)
        fleet = container.resolve(Fleet)
        fleet.admit_vehicle(Bicycle("rejected", 5, 90))

        number = fleet.register_item(Helmet("H"))

        self.assertEqual(number, "VK-0001")

    # одну машину нельзя поставить дважды
    def test_same_vehicle_cannot_be_admitted_twice(self):
        stub = StubInspection(accepted=True)
        fleet = container_with(inspection=stub).resolve(Fleet)
        bike = Bicycle("B", 9, 90)
        fleet.admit_vehicle(bike)

        with self.assertRaises(ValueError):
            fleet.admit_vehicle(bike)
        self.assertEqual(len(stub.inspected), 1)

    # без подмены контейнер дает настоящий сервисцентр и он реально отклоняет износ
    def test_default_container_uses_real_service_center(self):
        container = container_with()
        self.assertIsInstance(container.resolve(TechnicalInspection), ServiceCenter)
        result = container.resolve(Fleet).admit_vehicle(Bicycle("worn", 9, 10))
        self.assertFalse(result.accepted)

# тесты про вещи
class FleetItemsTest(unittest.TestCase):

    def setUp(self):
        self.stub = StubInspection(accepted=True)
        self.fleet = container_with(inspection=self.stub).resolve(Fleet)

    # вещи ставятся без техосмотра
    def test_items_are_registered_without_inspection(self):
        self.fleet.register_item(DockStation("D", 4.0))
        self.assertEqual(self.stub.inspected, [])
        self.assertEqual(len(self.fleet.items), 1)

    # нумерация общая
    def test_numbers_are_shared_between_vehicles_and_items(self):
        self.fleet.admit_vehicle(Bicycle("B", 9, 90))
        helmet_number = self.fleet.register_item(Helmet("H"))
        self.assertEqual(helmet_number, "VK-0002")
        self.assertEqual(len(self.fleet.assets), 2)

    # вещь дважды не поставить
    def test_same_item_cannot_be_registered_twice(self):
        helmet = Helmet("H")
        self.fleet.register_item(helmet)
        with self.assertRaises(ValueError):
            self.fleet.register_item(helmet)

    # наружу парк отдает кортежи
    def test_exposed_collections_are_read_only(self):
        self.assertIsInstance(self.fleet.vehicles, tuple)
        self.assertIsInstance(self.fleet.items, tuple)

# позволяет запустить файл напрямую
if __name__ == "__main__":
    unittest.main()