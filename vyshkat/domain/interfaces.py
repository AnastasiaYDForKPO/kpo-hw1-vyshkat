from abc import ABC, abstractmethod
# здесь я делаю значки, которые будут показывать, что тот кто носит, тот точно что-то имеет
# значки ваще ничего не делают сами по себе, просто разделение
# стоим на балансе
class Inventoriable(ABC): # есть навазние и инвентарный номер
    @property
    @abstractmethod
    def name(self):
        pass # реализация в ассэте

    @property
    @abstractmethod
    def inventory_number(self):
        pass

class EnergyConsumer(ABC): # есть суточный расход
    # потребители энергии те самокаты всякие, зарядные шкафы
    @property
    @abstractmethod
    def daily_energy_kwh(self):
        pass # сколько энергии тратит за сутки

class BeginnerRated(ABC): # есть простота от 1 до 10
    # оценен для новичков
    # носит весь транспорт (вещи нет)
    @property
    @abstractmethod
    def simplicity(self):
        pass