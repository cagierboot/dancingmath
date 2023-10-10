from manim import *


class CreateGraph(ThreeDScene):
    def construct(self):
        # Create a Line
        line = Line(start=LEFT, end=RIGHT)
        self.play(Create(line))
        self.wait(1)

        # Turn the Line into a Square
        square = Square()
        self.play(Transform(line, square))
        self.wait(1)

        # Turn the Square into a 3D square (Cube) with see-through faces
        cube = Cube(fill_opacity=0)
        self.play(Transform(square, cube))

        # Create white edges for the cube
        edges = [
            Line(start=cube.get_corner(start), end=cube.get_corner(end), color=WHITE)
            for start, end in [
                (DLF, DLF + RIGHT), (DLF + RIGHT, DLF + RIGHT + UP), 
                (DLF + RIGHT + UP, DLF + UP), (DLF + UP, DLF),
                (DLF, DLF + OUT), (DLF + RIGHT, DLF + RIGHT + OUT), 
                (DLF + RIGHT + UP, DLF + RIGHT + UP + OUT), 
                (DLF + UP, DLF + UP + OUT),
                (DLF + OUT, DLF + OUT + RIGHT), (DLF + OUT + RIGHT, DLF + OUT + RIGHT + UP), 
                (DLF + OUT + RIGHT + UP, DLF + OUT + UP), (DLF + OUT + UP, DLF + OUT)
            ]
        ]

        self.play(*[Create(edge) for edge in edges])
        self.wait(1)

        # Slowly move Camera to show 3D structure of the cube isometrically
        self.move_camera(phi=45*DEGREES, theta=45*DEGREES, run_time=3)
        self.wait(2)
