from manim import *
import random

class ShapeTransformation(Scene):
    def construct(self):
      
        # Create a line
        line = Line(start=[-1, 0, 0], end=[1, 0, 0])

        # Create a square
        square = Square()

        # Create a circle
        circle = Circle()

        # Create a triangle
        triangle = Triangle()

        # Display the line
        self.play(Create(line))
        self.wait(0.5)

        # Create a list of shapes
        shapes = [square, circle, triangle]

        # Shuffle the order of shapes randomly
        random.shuffle(shapes)

        # Transform the line into each shape in the randomly determined order
        for shape in shapes:
            self.play(Transform(line, shape), run_time=1)
            self.wait(0.5)

        # Clear the screen
        self.play(FadeOut(line))
