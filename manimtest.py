from manim import *
import random
import numpy as np

class ExtendedShapeTransformationWithEquations(Scene):
    def construct(self):
        # Create a white grid with thinner lines
        grid = NumberPlane(
            axis_config={"color": WHITE, "stroke_width": 2},
            background_line_style={"stroke_width": 1}
        )
        self.add(grid)

        # Create various shapes and their associated equations
        shapes_and_equations = [
            (Square(), Tex("$A = s^2$").scale(0.5)),
            (Circle(), Tex("$A = \\pi r^2$").scale(0.5)),
            (Triangle(), Tex("$A = \\frac{1}{2}bh$").scale(0.5)),
            (Ellipse(width=2, height=1), Tex("$A = \\pi ab$").scale(0.5)),
            (Rectangle(width=2, height=1), Tex("$A = lw$").scale(0.5)),
            (RegularPolygon(n=5), Tex("$A = \\frac{1}{4}\\sqrt{5(5+2\\sqrt{5})}a^2$").scale(0.5)),
            # Add more shapes here if you need
        ]

        # Shuffle the shapes and equations randomly
        random.shuffle(shapes_and_equations)

        # Create an initial shape and equation
        shape, equation = shapes_and_equations.pop(0)
        self.play(Create(shape))
        equation.next_to(shape, direction=DOWN, buff=0.5)
        self.play(Write(equation))
        self.wait(0.5)

        # Transform the shape into each shape in the randomly determined order and transform the equation
        for next_shape, next_equation in shapes_and_equations:
            next_equation.next_to(shape, direction=DOWN, buff=0.5)
            self.play(Transform(shape, next_shape), Transform(equation, next_equation), run_time=1)
            
            # Evolve shapes
            if isinstance(next_shape, Square):
                self.evolve_square(next_shape)
            elif isinstance(next_shape, Circle):
                self.evolve_circle(next_shape)
            elif isinstance(next_shape, Ellipse):
                self.evolve_ellipse(next_shape)
            elif isinstance(next_shape, Rectangle):
                self.evolve_rectangle(next_shape)

            self.wait(0.5)

        # Clear the screen
        self.play(FadeOut(shape), FadeOut(equation))

    def evolve_square(self, square):
        for _ in range(5):
            side_length = random.uniform(0.5, 3)
            new_square = Square(side_length=side_length)
            self.play(Transform(square, new_square), run_time=0.5)

    def evolve_circle(self, circle):
        for _ in range(5):
            radius = random.uniform(0.5, 3)
            new_circle = Circle(radius=radius)
            self.play(Transform(circle, new_circle), run_time=0.5)

    def evolve_ellipse(self, ellipse):
        for _ in range(5):
            width = random.uniform(0.5, 3)
            height = random.uniform(0.5, 3)
            new_ellipse = Ellipse(width=width, height=height)
            self.play(Transform(ellipse, new_ellipse), run_time=0.5)

    def evolve_rectangle(self, rectangle):
        for _ in range(5):
            width = random.uniform(0.5, 3)
            height = random.uniform(0.5, 3)
            new_rectangle = Rectangle(width=width, height=height)
            self.play(Transform(rectangle, new_rectangle), run_time=0.5)
