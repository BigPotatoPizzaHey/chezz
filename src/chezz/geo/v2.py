from __future__ import annotations

from dataclasses import dataclass
import typing_extensions as t

import math


@dataclass
class V2:
    x: float
    y: float

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __eq__(self, other: object, /) -> bool:
        if isinstance(other, V2):
            return self.x == other.x and self.y == other.y
        raise NotImplementedError(f"Bad type {type(other)=}")

    def __add__(self, other: V2, /) -> V2:
        return V2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: V2, /) -> V2:
        return V2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: float, /) -> V2:
        return V2(self.x * other, self.y * other)

    @t.overload
    def __truediv__(self, other: float, /) -> V2: ...
    @t.overload
    def __truediv__(
        self, other: V2, /
    ) -> (
        float
    ): ...  # only works if self is a multiple of other, i.e. it's determinant with other == 0
    def __truediv__(self, other: float | V2, /) -> V2 | float:
        if isinstance(other, float):
            return V2(self.x / other, self.y / other)
        elif isinstance(other, V2):
            if (
                abs(self.x * other.y - self.y * other.x) > 0.001
            ):  # NOTE: Leniency because of floating-point error
                raise ValueError(f"{self} is not divisible by {other}")
            return self.x / other.x
        raise NotImplementedError(f"Bad type {type(other)=}")

    def __rmul__(self, other: float) -> V2:
        return self * other

    def __neg__(self) -> V2:
        return V2(-self.x, -self.y)

    def __abs__(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __iter__(self) -> t.Generator[float]:
        yield self.x
        yield self.y

    def __matmul__(self, other: V2) -> float:
        """
        Dot product. Overrides `self @ other`
        """
        return self.x * other.x + self.y * other.y

    def into_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def into_idx(self) -> int:
        return int(self.y * 8 + self.x)

    @classmethod
    def from_idx(cls, idx: int) -> t.Self:
        return cls(idx % 8, idx // 8)

    @classmethod
    def from_notation(cls, notation: str) -> t.Self:
        assert len(notation) == 2
        return cls(float("abcdefgh".index(notation[0])), 8 - float(notation[1]))

    def is_black(self):
        return bool((self.x + self.y) % 2)

    def is_valid(self):
        return 0 <= self.x < 8 and 0 <= self.y < 8
