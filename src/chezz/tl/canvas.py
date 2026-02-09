from chezz import gr
from chezz.geo import V2
import turtle


class Canvas(gr.Canvas):
    def __init__(self, ttl: turtle.Turtle) -> None:
        super().__init__()
        self.pen: turtle.Turtle = ttl

    def draw_line(self, a: V2, b: V2, width: float):
        self.pen.goto(a.into_tuple())
        self.pen.pensize(int(width))
        self.pen.pendown()
        self.pen.goto(b.into_tuple())
        self.pen.penup()
