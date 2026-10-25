from abc import ABC, abstractmethod
DEFAULT_MIN_SIMPLICITY = 6
# значок для новчиков типо он может подходиьт true, а может не подходить false
class BeginnerPolicy(ABC):
    @abstractmethod
    def is_suitable(self, device):
        pass

# конструктор запоминает порог
class SimplicityThresholdPolicy(BeginnerPolicy):
    def __init__(self, min_simplicity=DEFAULT_MIN_SIMPLICITY):
        self._min_simplicity = min_simplicity
# подходит ли это устройство новичку
# типо условно device.simplicity это простота устройства
# _min_simplicity- это наш порог
    def is_suitable(self, device):
        return device.simplicity >= self._min_simplicity