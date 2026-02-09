import abc

from src.chezz.geo.v2 import V2


class Canvas(abc.ABC):
    @abc.abstractmethod
    def draw_line(self, a: V2, b: V2, width: float): ...
