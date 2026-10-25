from abc import ABC, abstractmethod
from ..domain import EnergyConsumer

class InspectionResult:
    def __init__(self, accepted, reason):
        self.accepted = accepted
        self.reason = reason

    @staticmethod
    def accept(reason="Техосмотр пройден"):
        return InspectionResult(True, reason)

    @staticmethod
    def reject(reason):
        return InspectionResult(False, reason)

class TechnicalInspection(ABC):

    @abstractmethod
    def inspect(self, vehicle):
        pass

class ServiceCenter(TechnicalInspection): # сервисный центр
    def __init__(self, min_condition=70, max_daily_energy_kwh=1.5):
        self._min_condition = min_condition
        self._max_daily_energy_kwh = max_daily_energy_kwh
    # чек один транспорт и выдаем справку
    def inspect(self, vehicle):
        if vehicle.condition < self._min_condition:
            return InspectionResult.reject(
                "Изношено: сотояние " + str(vehicle.condition) + " % <" + str(self._min_condition) + " %"
            )

        if isinstance(vehicle, EnergyConsumer):
            if vehicle.daily_energy_kwh > self._max_daily_energy_kwh:
                return InspectionResult.reject(
                    "Аномальный расход энергии: " + str(vehicle.daily_energy_kwh) + " кВтч/сут > " + str(self._max_daily_energy_kwh) + " кВтч/сут"
                )
        # если ничего не сработает, то все супер
        return InspectionResult.accept()