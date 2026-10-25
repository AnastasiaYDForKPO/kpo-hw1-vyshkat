from .interfaces import Inventoriable
MIN_SIMPLICITY = 1
MAX_SIMPLICITY = 10
# чекап
def require_name(name):
    name = name.strip()
    if name == "":
        raise ValueError("Номер не может быть пустым")
    return name

def require_simplicity(value):
    if value < MIN_SIMPLICITY or value > MAX_SIMPLICITY:
        raise ValueError("Для новичка легкость от 1 до 10")
    return value

def require_condition(value):
    if value < 0 or value > 100:
        raise ValueError("Тех состояние должно быть от 0 до 100 процентов")
    return value

def require_energy(value):
    if value <= 0:
        raise ValueError("Расход энергии должен быть больше нуля")
    return float(value)

# родитель для всех вещей (пс от самокатов до шлемов)
class Asset(Inventoriable):
    KIND = "Единица" # каждый наследник ставит свою
    # условно у нас шлем это будет "Шлем" ну и остальное так же
    def __init__(self, name):
        self._name = require_name(name)
        self._inventory_number = None # номера пока нет

    @property
    # пишу для себя тк в первый раз делаю проект на питоне
    # поменять снаружи нельзя
    def name(self):
        return self._name

    @property
    def kind(self):
        return self.KIND # отдаем табличку с видом

    @property
    def inventory_number(self):
        return self._inventory_number # просматриваем номер или ноне

    # клеим номер
    def assign_inventory_number(self, number):
        if self._inventory_number is not None:
            raise ValueError("у объекта есть свой личный номер")
        self._inventory_number = number

    # печатаем тип какой-то и название
    def __str__(self):
        return self.KIND + " <" + self.name + ">"