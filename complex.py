from manim import *

class Create3DCubeWithEquations(ThreeDScene):
    def construct(self):
        # Equations
        line_eqn = MathTex("y = mx + c", color=WHITE).scale(0.7)
        square_eqn = MathTex("x^2 + y^2 = r^2", color=WHITE).scale(0.7)
        cube_eqn = MathTex("x^2 + y^2 + z^2 = r^2", color=WHITE).scale(0.7)

        # Create a line
        line = Line(start=[-1,0,0], end=[1,0,0], color=WHITE)

        # Create a square
        square = Square(color=WHITE)

        # Create a cube with no fill
        cube = Cube(fill_opacity=0)
        cube.set_stroke(color=WHITE, width=2)

        # Position the equations
        line_eqn.next_to(line, DOWN, buff=0.5)
        square_eqn.next_to(square, DOWN, buff=0.5)
        cube_eqn.next_to(cube, DOWN, buff=0.5)

        # Set the initial camera orientation
        self.set_camera_orientation(phi=0, theta=0)

        # Add the line and its equation
        self.play(
            Create(line),
            Write(line_eqn)
        )
        self.wait(1)

        # Transform the line into a square and the equation
        self.play(
            ReplacementTransform(line, square),
            ReplacementTransform(line_eqn, square_eqn),
            run_time=2
        )
        self.wait(1)

        # Transform the square into a cube and the equation
        self.play(
            ReplacementTransform(square, cube),
            ReplacementTransform(square_eqn, cube_eqn),
            run_time=3
        )

        # Adjust the position of the cube equation after cube is rendered
        cube_eqn.next_to(cube, DOWN, buff=0.5)

        # Move the camera to the isometric view
        self.move_camera(phi=PI/4, theta=PI/4, run_time=2)
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()
