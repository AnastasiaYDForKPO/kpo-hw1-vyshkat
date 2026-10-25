from .assets import Asset, require_energy
from vyshkat.domain.interfaces import EnergyConsumer

class Item(Asset):
    pass

class Helmet(Item):
    KIND = "Шлем"

# пс вещь, которая потребляет заряд
class _PoweredItem(Item, EnergyConsumer):
        def __init__(self, name, daily_energy_kwh):
            Item.__init__(self, name)
            self._daily_energy_kwh = require_energy(daily_energy_kwh)
        @property
        def daily_energy_kwh(self):
            return self._daily_energy_kwh

class DockStation(_PoweredItem):
    KIND = "Док-станция"

class ChargingCabinet(_PoweredItem):
    KIND = "Зарядный шкаф"