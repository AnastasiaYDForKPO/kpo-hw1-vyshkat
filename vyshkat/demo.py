from .domain import Bicycle, ChargingCabinet, DockStation, ElectricBicycle, Helmet, Scooter


def run_demo(app, io):
    io.write("=== ВышКат: демонстрация сценариев ===")

    io.write("")
    io.write("--- 1. Приём техники: техосмотр пройден ---")
    city_scooter = Scooter("Ninebot Max G30", 7, 95, 0.45)
    app.admit(city_scooter)
    app.admit(Bicycle("Stels Navigator 300", 9, 88))
    app.admit(ElectricBicycle("Eltreco XT 850", 4, 90, 0.8))
    app.admit(Scooter("Kugoo Kirin M4", 6, 70, 0.5))

    io.write("")
    io.write("--- 2. Приём техники: техосмотр НЕ пройден ---")
    app.admit(Scooter("Xiaomi Pro 2 (б/у)", 8, 45, 0.4))
    app.admit(ElectricBicycle("Eltreco «с перегревом»", 5, 92, 3.2))

    io.write("")
    io.write("--- 3. Повторная постановка на баланс — защита от дублей ---")
    app.admit(city_scooter)

    io.write("")
    io.write("--- 4. Некорректные данные отсекаются моделью ---")
    try:
        Bicycle("Велосипед-фантазия", 12, 100)
    except ValueError as error:
        io.write("  ✗ Ошибка: " + str(error))

    io.write("")
    io.write("--- 5. Вещи на балансе (без техосмотра) ---")
    app.register(Helmet("Шлем городской M"))
    app.register(Helmet("Шлем городской L"))
    app.register(DockStation("Док-станция у корпуса на Покровке", 4.0))
    app.register(ChargingCabinet("Зарядный шкаф на 12 АКБ", 7.5))

    io.write("")
    io.write("--- 6. Отчёт: количество единиц ---")
    app.show_summary()

    io.write("")
    io.write("--- 7. Отчёт: суммарное суточное энергопотребление ---")
    app.show_energy()

    io.write("")
    io.write("--- 8. Транспорт для новичков (простота ≥ 6) ---")
    app.show_beginners()

    io.write("")
    io.write("--- 9. Инвентарная ведомость ---")
    app.show_inventory()