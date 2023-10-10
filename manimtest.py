from manim import *
import random

class ExtendedShapeTransformation(Scene):
    def construct(self):

        # Create a line
        line = Line(start=[-1, 0, 0], end=[1, 0, 0])

        # Create various shapes
        square = Square()
        circle = Circle()
        triangle = Triangle()
        ellipse = Ellipse(width=2, height=1)
        rectangle = Rectangle(width=2, height=1)
        pentagon = RegularPolygon(n=5)
        hexagon = RegularPolygon(n=6)
        heptagon = RegularPolygon(n=7)
        octagon = RegularPolygon(n=8)

        # List of all shapes
        shapes = [
            square, circle, triangle, ellipse,
            rectangle, pentagon, hexagon, heptagon, octagon
        ]

        # Shuffle the shapes randomly
        random.shuffle(shapes)

        # Display the initial line
        self.play(Create(line))
        self.wait(0.5)

        # Transform the line into each shape in the randomly determined order
        for shape in shapes:
            self.play(Transform(line, shape), run_time=1)
            self.wait(0.5)

        # Clear the screen
        self.play(FadeOut(line))
