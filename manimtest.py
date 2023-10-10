from manim import *
import random
import numpy as np

class ExtendedShapeTransformationWithEquations(Scene):
    def construct(self):
        # Binary trigger array where 1 means transition and 0 means wait
        binary_trigger_array = [0, 1, 0, 0, 0, 0, 0, 0, 0, 1,1,1,1,0,1]  # Example array

        # Create a white grid
        grid = NumberPlane(axis_config={"color": WHITE})
        self.add(grid)  
         

        # Create various shapes and their associated equations
        shapes_and_equations = [
            (Square(), Tex("$A = s^2$").scale(0.5)),
            (Circle(), Tex("$A = \\pi r^2$").scale(0.5)),
            (Triangle(), Tex("$A = \\frac{1}{2}bh$").scale(0.5)),
            (Ellipse(width=2, height=1), Tex("$A = \\pi ab$").scale(0.5)),
            (Rectangle(width=2, height=1), Tex("$A = lw$").scale(0.5)),
            (RegularPolygon(n=5), Tex("$A = \\frac{1}{4}\\sqrt{5(5+2\\sqrt{5})}a^2$").scale(0.5)),
            (RegularPolygon(n=6), Tex("$A = \\frac{3\\sqrt{3}}{2}a^2$").scale(0.5)),
            (RegularPolygon(n=7), Tex("$A \\approx 3.63a^2$").scale(0.5)), 
            (RegularPolygon(n=8), Tex("$A = 2a^2(1+\\sqrt{2})$").scale(0.5)),

            # Cardioid
            (ParametricFunction(
                lambda t: np.array([
                    0.5 * (2 * np.cos(t) - np.cos(2*t)),
                    0.5 * (2 * np.sin(t) - np.sin(2*t)),
                    0]),
                t_range=[0, 2*PI],
                color=BLUE), Tex("Cardioid").scale(0.5)),
            # Spiral
            (ParametricFunction(
                lambda t: np.array([
                    t * np.cos(t),
                    t * np.sin(t),
                    0]),
                t_range=[0, 4*PI],
                color=PURPLE), Tex("Spiral").scale(0.5)),
            # Lissajous Curve
            (ParametricFunction(
                lambda t: np.array([
                    np.sin(3*t),
                    np.sin(2*t),
                    0]),
                t_range=[0, 2*PI],
                color=RED), Tex("Lissajous").scale(0.5)),
        ]

        # Shuffle the shapes and equations randomly
        random.shuffle(shapes_and_equations)

        # Create an initial shape and equation
        shape, equation = shapes_and_equations.pop(0)
        self.play(Create(shape))
        equation.next_to(shape, direction=DOWN, buff=0.5)
        self.play(Write(equation))
        self.wait(0.5)

        # Iterate through the binary trigger array
        for trigger in binary_trigger_array:
            if trigger == 1 and shapes_and_equations:  # If trigger is 1 and there are still shapes left
                next_shape, next_equation = shapes_and_equations.pop(0)
                next_equation.next_to(shape, direction=DOWN, buff=0.5)
                self.play(Transform(shape, next_shape), Transform(equation, next_equation), run_time=1)
                self.wait(0.5)
            else:  # If trigger is 0 or no shapes left
                self.wait(1)  # Wait for 1 second

        # Clear the screen
        self.play(FadeOut(shape), FadeOut(equation))