from typing import List
from manim import *
from math import factorial

def sin_taylor(n: int, x: float) -> float:
    assert n > 0
    
    result = 0
    for i in range(n):
        result += ((-1) ** i) * (x ** (2*i+1)) / factorial(2*i+1)
        
    return result

def sin_taylor_tex(n: int, cap_at: int) -> List[str]:
    assert n > 0

    result = ['x']

    for i in range(1, n):
        result.append('-' if i % 2 == 1 else '+')

        if i == cap_at:
            result.append('...')
            return result

        exponent = 2 * i + 1
        result.append(f'\\frac{{x^{{{exponent}}}}}{{{exponent}!}}')

    return result

class SinTaylorScene(Scene):

    def switch_taylor(self, n = 1, wait = 0.5):
        taylor_graph = self.axes.get_graph(lambda x: sin_taylor(n, x), color=YELLOW)
        taylor_label = MathTex(*sin_taylor_tex(n, 5)).set_color(YELLOW)
        taylor_label.to_corner(UP+LEFT)

        a1 = Transform(self.taylor_graph, taylor_graph)
        a2 = FadeOut(self.taylor_label)
        a3 = FadeIn(taylor_label)

        self.play(AnimationGroup(a1, a2, a3))
        self.wait(wait)

        self.remove(self.taylor_graph, self.taylor_label)

        self.taylor_graph = taylor_graph
        self.taylor_label = taylor_label


    def construct(self):
        self.axes = Axes(
            x_range=[-20, 20, 1],
            y_range=[-4.0, 4.0, 1],
            x_length=30,
            y_length=12,
            axis_config={"color": GREEN},
            x_axis_config={
                "numbers_to_include": np.arange(-10, 10.01, 2),
                "numbers_with_elongated_ticks": np.arange(-10, 10.01, 2),
            },
            tips=False,
        )
        axes_labels = self.axes.get_axis_labels()
        sin_graph = self.axes.get_graph(lambda x: np.sin(x), color=BLUE)
        sin_label = self.axes.get_graph_label(
            sin_graph, "\\sin(x)", x_val=-7.5, direction=DOWN
        )
        
        self.taylor_graph = self.axes.get_graph(lambda x: sin_taylor(1, x), color=YELLOW)
        self.taylor_label = MathTex(*sin_taylor_tex(1, 5)).set_color(YELLOW)
        self.taylor_label.to_corner(UP + LEFT)
        self.taylor_label.shift(DOWN * 0.52)

        self.add(self.axes, sin_graph, axes_labels, sin_label)
        self.wait(3.0)
        self.play(FadeIn(self.taylor_graph, self.taylor_label))
        self.wait(2.5)

        self.switch_taylor(2, wait=2.5)
        self.switch_taylor(3, wait=2.5)

        for i in range(4, 7):
            self.switch_taylor(i, wait=1.0)

        for i in range(7, 12):
            self.switch_taylor(i, wait=0.5)



