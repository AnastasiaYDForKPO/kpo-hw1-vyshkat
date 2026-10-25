import unittest

from vyshkat.console import ConsoleApp, ConsoleIO
from vyshkat.demo import run_demo
from vyshkat.services import Fleet

from vyshkat.tests.fakes import StubInspection, ScriptedIO, container_with


def run_app(inputs: list[str], inspection=None) -> tuple[ScriptedIO, Fleet]:
    io = ScriptedIO(inputs)
    container = container_with(inspection=inspection, io=io)
    container.resolve(ConsoleApp).run()
    return io, container.resolve(Fleet)


class ConsoleScenariosTest(unittest.TestCase):
    def test_admit_scooter_through_menu(self):
        io, fleet = run_app(["1", "1", "Ninebot", "7", "95", "0,45", "0"])
        self.assertEqual(len(fleet.vehicles), 1)
        self.assertEqual(fleet.vehicles[0].daily_energy_kwh, 0.45)  # запятая допустима
        self.assertIn("принят. Инвентарный № VK-0001", io.output)

    def test_bicycle_dialog_does_not_ask_for_energy(self):
        io, fleet = run_app(["1", "2", "Stels", "9", "90", "0"])
        self.assertEqual(len(fleet.vehicles), 1)
        self.assertFalse(any("расход" in prompt for prompt in io.prompts))

    def test_rejection_is_shown(self):
        io, fleet = run_app(["1", "2", "Stels", "9", "90", "0"], inspection=StubInspection(False, "проверка"))
        self.assertIn("отклонён техосмотром: проверка", io.output)
        self.assertEqual(fleet.vehicles, ())

    def test_invalid_input_is_asked_again(self):
        inputs = ["7", "1", "x", "9", "2", "", "Stels", "11", "6", "-5", "90", "0"]
        io, fleet = run_app(inputs)
        self.assertIn("Нет такого пункта меню.", io.output)
        self.assertIn("Введите целое число.", io.output)
        self.assertIn("Число должно быть от 1 до", io.output)
        self.assertIn("Значение не может быть пустым.", io.output)
        self.assertEqual(fleet.vehicles[0].simplicity, 6)

    def test_invalid_energy_is_asked_again(self):
        io, fleet = run_app(["2", "2", "Dock", "abc", "0", "4", "0"])
        self.assertIn("Введите число", io.output)
        self.assertIn("больше нуля", io.output)
        self.assertEqual(fleet.items[0].daily_energy_kwh, 4.0)

    def test_register_item_and_all_reports(self):
        io, _ = run_app([
            "2", "1", "Шлем M",
            "1", "1", "Ninebot", "7", "95", "0.5",
            "3", "4", "5", "6", "0",
        ])
        out = io.output
        self.assertIn("На балансе: 2 ед. (транспорт: 1, вещи: 1)", out)
        self.assertIn("0.50 кВт·ч", out)
        self.assertIn("Можно выдавать новичкам:", out)
        self.assertIn("VK-0001  Шлем <Шлем M>", out)
        self.assertIn("VK-0002  Электросамокат <Ninebot>, 0.5 кВт·ч/сут, простота 7/10", out)

    def test_empty_reports(self):
        io, _ = run_app(["5", "6", "0"])
        self.assertIn("Транспорта для новичков нет.", io.output)
        self.assertIn("На балансе пока ничего нет.", io.output)

    def test_end_of_input_exits_gracefully(self):
        io, _ = run_app(["1"])
        self.assertEqual(io.lines[-1], "До свидания!")


class DemoTest(unittest.TestCase):
    def test_demo_covers_all_scenarios(self):
        io = ScriptedIO()
        container = container_with(io=io)
        run_demo(container.resolve(ConsoleApp), io)
        out = io.output
        self.assertEqual(out.count("принят."), 4)
        self.assertEqual(out.count("отклонён техосмотром"), 2)
        self.assertIn("уже на балансе", out)
        self.assertIn("от 1 до 10", out)
        self.assertIn("На балансе: 8 ед.", out)
        self.assertIn("13.25 кВт·ч", out)
        self.assertIn("VK-0008", out)


if __name__ == "__main__":
    unittest.main()
