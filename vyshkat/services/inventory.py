# в общем, это те самые индвидуальные номера
# пс его используем вообще для всех вещей, транспортов
class InventoryNumberGenerator:
    def __init__(self, prefix="VK", start=1):
        self._prefix = prefix
        self._next = start
    def next_number(self):
        digits = str(self._next).zfill(4)
        number = self._prefix + "-" + digits
        self._next += 1
        return number