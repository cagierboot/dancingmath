from manim import *
import random

class ExtendedShapeTransformationWithEquations(Scene):
    def construct(self):

        # Create a line
        line = Line(start=[-1, 0, 0], end=[1, 0, 0])

        # Create various shapes and their associated equations
        shapes_and_equations = [
            (Square(), Tex("$A = s^2$").scale(0.5)),
            (Circle(), Tex("$A = \\pi r^2$").scale(0.5)),
            (Triangle(), Tex("$A = \\frac{1}{2}bh$").scale(0.5)),
            (Ellipse(width=2, height=1), Tex("$A = \\pi ab$").scale(0.5)),
            (Rectangle(width=2, height=1), Tex("$A = lw$").scale(0.5)),
            (RegularPolygon(n=5), Tex("$A = \\frac{1}{4}\\sqrt{5(5+2\\sqrt{5})}a^2$").scale(0.5)),
            (RegularPolygon(n=6), Tex("$A = \\frac{3\\sqrt{3}}{2}a^2$").scale(0.5)),
            (RegularPolygon(n=7), Tex("$A \\approx 3.63a^2$").scale(0.5)), # Approximate formula for heptagon area
            (RegularPolygon(n=8), Tex("$A = 2a^2(1+\\sqrt{2})$").scale(0.5))
        ]

        # Shuffle the shapes and equations randomly
        random.shuffle(shapes_and_equations)

        # Display the initial line
        self.play(Create(line))
        self.wait(0.5)

        # Transform the line into each shape in the randomly determined order and display equation
        for shape, equation in shapes_and_equations:
            self.play(Transform(line, shape), run_time=1)
            equation.next_to(line, DOWN)
            self.play(Write(equation))
            self.wait(0.5)
            self.play(FadeOut(equation))

        # Clear the screen
        self.play(FadeOut(line))
