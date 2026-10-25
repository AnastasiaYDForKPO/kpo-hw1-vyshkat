from __future__ import annotations

from .assets import Asset, require_condition, require_energy, require_simplicity
from vyshkat.domain.interfaces import BeginnerRated, EnergyConsumer

# наш любой транспорт состоит в принципе из всего имущества и из оценки (прописывалось в интерфейсе)
class Vehicle(Asset, BeginnerRated):
    def __init__(self, name: str, simplicity: int, condition: int):
        Asset.__init__(self, name)
        self._simplicity = require_simplicity(simplicity)
        self._condition = require_condition(condition)

    # отдаем сложность от 1 до 10
    @property
    def simplicity(self):
        return self._simplicity

    # отдаем тех состояние от 0 до 100
    @property
    def condition(self):
        return self._condition

class ElectricVehicle(Vehicle, EnergyConsumer):
    def __init__(self, name, simplicity, condition, daily_energy_kwh):
        Vehicle.__init__(self, name, simplicity, condition)
        self._daily_energy_kwh = require_energy(daily_energy_kwh)
    @property
    def daily_energy_kwh(self):
        return self._daily_energy_kwh

class Scooter(ElectricVehicle):
    KIND = "Электросамокат"

class ElectricBicycle(ElectricVehicle):
    KIND = "Электровелосипед"

class Bicycle(Vehicle):
    KIND = "Велосипед"
