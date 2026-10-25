from abc import ABC, abstractmethod

from vyshkat.catalog import AssetForm
from .domain import EnergyConsumer, Vehicle
# консоль точка спрашивает и печатает => передает данные и показывает ответ


# прилоежение пользуется только этим значком, а не input/print напрямую
# в тестах вместо клавы подсовываем объект, который вводит заранее заготовленные строки
class ConsoleIO(ABC):

    @abstractmethod
    def read(self, prompt): # показывает вопрос + вернуть что ввел человек
        pass

    @abstractmethod
    def write(self, text=""): # напечатать строку
        pass


class StdConsoleIO(ConsoleIO):

    def read(self, prompt): # input
        return input(prompt)

    def write(self, text=""): # print
        print(text)


class ConsoleApp:
    # пункты меню
    MENU = [
        ("1", "Принять транспорт (через техосмотр)"),
        ("2", "Поставить вещь на баланс"),
        ("3", "Отчёт: количество единиц"),
        ("4", "Отчёт: суммарное суточное энергопотребление"),
        ("5", "Транспорт для новичков"),
        ("6", "Инвентарная ведомость (вся техника и вещи)"),
        ("0", "Выход"),
    ]
    # нужны 5 помощников (парк/отчеты/каталог вида транспорта/каталог видов вещей/через что читать и писать)
    def __init__(self, fleet, reports, vehicle_catalog, item_catalog, io):
        self._fleet = fleet
        self._reports = reports
        self._vehicle_catalog = vehicle_catalog
        self._item_catalog = item_catalog
        self._io = io
        self._actions = {
            "1": self._admit_vehicle_dialog,
            "2": self._register_item_dialog,
            "3": self.show_summary,
            "4": self.show_energy,
            "5": self.show_beginners,
            "6": self.show_inventory,
        }

    def run(self):
        self._io.write("=== ВышКат — учёт парка. «Доедем до дедлайна» ===")
        try:
            while True:
                self._io.write()
                for key, title in self.MENU: # печатает меню
                    self._io.write("  " + key + ". " + title)

                choice = self._io.read("Выберите пункт: ").strip()

                if choice == "0":
                    break

                if choice not in self._actions:
                    self._io.write("Нет такого пункта меню.")
                    continue

                action = self._actions[choice] # достали нужный метод и вызываем его
                action()
        except (EOFError, KeyboardInterrupt):
            self._io.write()
        self._io.write("До свидания!")

    # отдать транспорт парку и напечатать результат
    def admit(self, vehicle):
        try:
            result = self._fleet.admit_vehicle(vehicle)
        except ValueError as error:
            self._io.write("  ✗ Ошибка: " + str(error))
            return None
        if result.accepted:
            self._io.write("  ✓ " + str(vehicle) + " принят. Инвентарный № " + result.inventory_number)
        else:
            self._io.write("  ✗ " + str(vehicle) + " отклонён техосмотром: " + result.reason)
        return result

    # отдать вещь парку и напечатать номер
    def register(self, item):
        try:
            number = self._fleet.register_item(item)
        except ValueError as error:
            self._io.write("  ✗ Ошибка: " + str(error))
            return None
        self._io.write("  ✓ " + str(item) + " — на балансе. Инвентарный № " + number)
        return number

    def show_summary(self):
        summary = self._reports.summary()
        self._io.write("На балансе: " + str(summary.total) + " ед. (транспорт: "
                       + str(summary.vehicles) + ", вещи: " + str(summary.items) + ")")
        for kind, count in sorted(summary.by_kind.items()):
            self._io.write("  - " + kind + ": " + str(count))

    def show_energy(self):
        total = self._reports.total_daily_energy_kwh()
        self._io.write("Суммарное суточное энергопотребление парка: " + "%.2f" % total + " кВт·ч")

    def show_beginners(self):
        vehicles = self._reports.beginner_friendly_vehicles()
        if len(vehicles) == 0:
            self._io.write("Транспорта для новичков нет.")
            return
        self._io.write("Можно выдавать новичкам:")
        for v in vehicles:
            self._io.write("  " + v.inventory_number + "  " + str(v)
                           + "  (простота " + str(v.simplicity) + "/10)")

    def show_inventory(self):
        assets = self._reports.inventory()
        if len(assets) == 0:
            self._io.write("На балансе пока ничего нет.")
            return
        self._io.write("Инвентарная ведомость:")
        for asset in assets:
            self._io.write("  " + asset.inventory_number + "  " + self._describe(asset))

    def _describe(self, asset):
        text = str(asset)
        if isinstance(asset, EnergyConsumer):
            text = text + ", " + "%g" % asset.daily_energy_kwh + " кВт·ч/сут"
        if isinstance(asset, Vehicle):
            text = text + ", простота " + str(asset.simplicity) + "/10"
        return text

    # спросить вид и данные/собрать анкету/создать объект/отдать парку
    def _admit_vehicle_dialog(self):
        kind = self._choose_kind("Вид транспорта", self._vehicle_catalog.kinds())
        name = self._ask_text("Наименование (модель): ")
        simplicity = self._ask_int("Простота для новичка (1–10): ", 1, 10)
        condition = self._ask_int("Техническое состояние, % (0–100): ", 0, 100)
        energy = None
        if kind.needs_energy:
            energy = self._ask_positive_float("Суточный расход, кВт·ч: ")
        form = AssetForm(name, simplicity, condition, energy)
        self.admit(kind.create(form))

    # то же для вещи (имя + если нужно расход)
    def _register_item_dialog(self):
        kind = self._choose_kind("Вид вещи", self._item_catalog.kinds())
        name = self._ask_text("Наименование: ")
        energy = None
        if kind.needs_energy:
            energy = self._ask_positive_float("Суточный расход, кВт·ч: ")
        form = AssetForm(name, daily_energy_kwh=energy)
        self.register(kind.create(form))

    # напечатать виды из каталога с номерами и спросить номер
    def _choose_kind(self, title, kinds):
        self._io.write(title + ":")
        number = 1
        for kind in kinds:
            self._io.write("  " + str(number) + ". " + kind.title)
            number = number + 1
        chosen = self._ask_int("Номер: ", 1, len(kinds))
        return kinds[chosen - 1]

    def _ask_text(self, prompt):
        while True:
            value = self._io.read(prompt).strip()
            if value != "":
                return value
            self._io.write("Значение не может быть пустым.")

    def _ask_int(self, prompt, low, high):
        while True:
            raw = self._io.read(prompt).strip()
            try:
                value = int(raw)
            except ValueError:
                self._io.write("Введите целое число.")
                continue
            if value < low or value > high:
                self._io.write("Число должно быть от " + str(low) + " до " + str(high) + ".")
                continue
            return value

    def _ask_positive_float(self, prompt):
        while True:
            raw = self._io.read(prompt).strip().replace(",", ".")
            try:
                value = float(raw)
            except ValueError:
                self._io.write("Введите число, например 0.4")
                continue
            if value <= 0:
                self._io.write("Значение должно быть больше нуля.")
                continue
            return value