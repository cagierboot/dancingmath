from manim import *

class ShapeTransformation(Scene):
    def construct(self):
        # Add a grid
        grid = NumberPlane()
        self.add(grid)
odascnkvncasinj
        # Create a line
        line = Line(start=[-1, 0, 0], end=[1, 0, 0])

        # Create a square
        square = Square()

        # Create a circle
        circle = Circle()

        # Create a triangle
        triangle = Triangle()

        # Add corresponding equations for each shape
        line_equation = MathTex("y = ax + b")
        square_equation = MathTex("x^2 + y^2 = a^2")
        circle_equation = MathTex("x^2 + y^2 = r^2")
        triangle_equation = MathTex("a + b + c = 180^\circ")

        # Display the line and its equation
        self.play(Create(line), Write(line_equation))
        self.wait(0.5)

        # Transform the line into a square and update the equation
        self.play(Transform(line, square), Transform(line_equation, square_equation), run_time=1)
        self.wait(0.5)

        # Transform the square into a circle and update the equation
        self.play(Transform(line, circle), Transform(line_equation, circle_equation), run_time=1)
        self.wait(0.5)

        # Transform the circle into a triangle and update the equation
        self.play(Transform(line, triangle), Transform(line_equation, triangle_equation), run_time=1)
        self.wait(0.5)

        # Clear the screen
        self.play(FadeOut(line), FadeOut(line_equation))

        