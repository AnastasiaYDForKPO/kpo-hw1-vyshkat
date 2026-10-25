from vyshkat.catalog import AssetKind, ItemCatalog, VehicleCatalog
from vyshkat.console import ConsoleApp, ConsoleIO, StdConsoleIO
from vyshkat.di import Container
from .domain import Bicycle, ChargingCabinet, DockStation, ElectricBicycle, Helmet, Scooter
from .services import (
    BeginnerPolicy,
    Fleet,
    FleetReports,
    InventoryNumberGenerator,
    ServiceCenter,
    SimplicityThresholdPolicy,
    TechnicalInspection,
)
# это сборка
# техосмотр это ServiceCenter с порогом 70%, ввод это терминал и тд и тп



# новый вид транспорта = класс в vehicles.py + строка тут
# AssetKind(код, название в меню, расход, рецепт)
def _vehicle_kinds():
    return [
        AssetKind("scooter", "Электросамокат", True,
                  lambda f: Scooter(f.name, f.simplicity, f.condition, f.daily_energy_kwh)),
        AssetKind("bike", "Велосипед", False,
                  lambda f: Bicycle(f.name, f.simplicity, f.condition)),
        AssetKind("ebike", "Электровелосипед", True,
                  lambda f: ElectricBicycle(f.name, f.simplicity, f.condition, f.daily_energy_kwh)),
    ]

# карточки видов вещей
def _item_kinds():
    return [
        AssetKind("helmet", "Шлем", False, lambda f: Helmet(f.name)),
        AssetKind("dock", "Док-станция", True, lambda f: DockStation(f.name, f.daily_energy_kwh)),
        AssetKind("cabinet", "Зарядный шкаф", True, lambda f: ChargingCabinet(f.name, f.daily_energy_kwh)),
    ]


# register_singleton (что как) - сделать один раз и отдавать его же
# register_transient(что как) - делать новый при каждой просьбе
def build_container():
    c = Container()
    c.register_singleton(TechnicalInspection, lambda _: ServiceCenter(min_condition=70, max_daily_energy_kwh=1.5)) # техосмотр
    c.register_singleton(InventoryNumberGenerator, lambda _: InventoryNumberGenerator(prefix="VK")) # номера
    c.register_singleton(BeginnerPolicy, lambda _: SimplicityThresholdPolicy(min_simplicity=6)) # простота от 6
    c.register_singleton(Fleet, lambda c: Fleet(c.resolve(TechnicalInspection), c.resolve(InventoryNumberGenerator))) # парк берет у контейнера техосмотр + рулон (пс один на все приложение)
    c.register_singleton(FleetReports, lambda c: FleetReports(c.resolve(Fleet), c.resolve(BeginnerPolicy))) # отчеты
    c.register_singleton(VehicleCatalog, lambda _: VehicleCatalog(_vehicle_kinds())) # каталоги видов для меню
    c.register_singleton(ItemCatalog, lambda _: ItemCatalog(_item_kinds()))
    c.register_singleton(ConsoleIO, lambda _: StdConsoleIO()) # терминал
    c.register_transient( # консоль(собирается из 5 помощников)
        ConsoleApp,
        lambda c: ConsoleApp(
            c.resolve(Fleet),
            c.resolve(FleetReports),
            c.resolve(VehicleCatalog),
            c.resolve(ItemCatalog),
            c.resolve(ConsoleIO),
        ),
    )
    return c