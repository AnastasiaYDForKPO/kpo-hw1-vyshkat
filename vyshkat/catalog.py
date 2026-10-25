class AssetForm:

    def __init__(self, name, simplicity=None, condition=None, daily_energy_kwh=None):
        self.name = name
        self.simplicity = simplicity
        self.condition = condition
        self.daily_energy_kwh = daily_energy_kwh


class AssetKind:

    def __init__(self, key, title, needs_energy, create):
        self.key = key
        self.title = title # как показать в меню
        self.needs_energy = needs_energy # спрашивать ли у пользователя расход
        self.create = create # функция, которая из анкеты делает объект


class Catalog: # список карточек AssetKind, которые кладём в каталог
# собственно перебираем карточки, если код есть в каталоге, то кладет карточку под ее кодом
    def __init__(self, kinds):
        self._kinds = {}
        for kind in kinds:
            if kind.key in self._kinds:
                raise ValueError("Вид «" + kind.key + "» зарегистрирован дважды")
            self._kinds[kind.key] = kind

    def kinds(self):
        return list(self._kinds.values())
# ищем карточку по коду
    def get(self, key):
        if key not in self._kinds:
            raise ValueError("Неизвестный вид: " + key)
        return self._kinds[key]

# два каталога пс транспорт и вещи (внутри они одианаковые)
class VehicleCatalog(Catalog):
    pass


class ItemCatalog(Catalog):
    pass