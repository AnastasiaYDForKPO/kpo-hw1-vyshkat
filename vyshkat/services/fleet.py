# он делает несколько вещей: принять/не принять, причина(техосмотр), выданный номер
class AdmissionResult:
    def __init__(self, accepted, reason, inventory_number=None):
        self.accepted = accepted
        self.reason = reason
        self.inventory_number = inventory_number

class Fleet:
    def __init__(self, inspection, numbers):
        self._inspection = inspection
        self._numbers = numbers
        self._vehicles = []
        self._items = []
    def admit_vehicle(self, vehicles):
        self._ensure_not_registered(vehicles)
        # отправляем на тех осмотр и получаем справку
        verdict = self._inspection.inspect(vehicles)
        # если отказ сразу кик
        if verdict.accepted == False:
            return AdmissionResult(False, verdict.reason)
        # если все супер, то даем номер и кладем в список транспорта
        number = self._put_on_balance(vehicles)
        self._vehicles.append(vehicles)
        return AdmissionResult(True, verdict.reason, number)

    # вещам не нужен техосмотр, поэтому возвращет просто номер
    def register_item(self, item):
        self._ensure_not_registered(item)
        number = self._put_on_balance(item)
        self._items.append(item)
        return number

  # отдаем кортеж копию, потому что инае кто-то может протащить самкокат без техосмотра
    @property
    def vehicles(self):
        return tuple(self._vehicles)

    @property
    def items(self):
        return tuple(self._items)

    @property
    def assets(self):
        return tuple(self._vehicles + self._items)

    # взять следующий номер из рулона и наклеить на объект
    def _put_on_balance(self, asset):
        number = self._numbers.next_number()
        asset.assign_inventory_number(number)
        return number
    # если у объекта есть номер, то повторно мы его не можем наклеить, тк он уже на балансе
    def _ensure_not_registered(self, asset):
        if asset.inventory_number is not None:
            raise ValueError(str(asset) + " уже на балансе под номером " + asset.inventory_number)
