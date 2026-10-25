from vyshkat.bootstrap import build_container
from vyshkat.console import ConsoleIO
from vyshkat.services import InspectionResult, TechnicalInspection
# двойники для тестов
# тк в тесах не нужен настоящий сервис центр и клавиатура, мы вместо них подсовываем подделку



# заглушка техосмотра
class StubInspection(TechnicalInspection):

    def __init__(self, accepted, reason="решение заглушки"):
        self._result = InspectionResult(accepted, reason) # заранее готовая справка
        self.inspected = [] # список машин, которые проверяли

    def inspect(self, vehicle):
        self.inspected.append(vehicle) # запомнили что эту машину приносили
        return self._result # всегда одна и та же справка


# поддельная клава и экран
class ScriptedIO(ConsoleIO):

    def __init__(self, inputs=None):
        if inputs is None:
            inputs = []
        self._inputs = list(inputs) # что вводить
        self.lines = [] # все что приложение напечатало
        self.prompts = [] # все вопросы которые приложение задало

    def read(self, prompt):
        self.prompts.append(prompt)
        if len(self._inputs) == 0:
            raise EOFError
        return self._inputs.pop(0)

    def write(self, text=""):
        self.lines.append(text)

    # все напечатанное одним текстом
    @property
    def output(self):
        return "\n".join(self.lines)

# настоящая сборка но с подменой
# берем билд_контейнер() как в настоящей проге и перерегистрируем техосмотр
def container_with(inspection=None, io=None):
    container = build_container()
    if inspection is not None:
        container.register_instance(TechnicalInspection, inspection) # подменили техосмотр
    if io is not None:
        container.register_instance(ConsoleIO, io) # подменили ввод вывод
    return container