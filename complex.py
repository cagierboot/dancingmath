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

        # Turn the Square into a 3D square (Cube)
        cube = Cube()
        self.play(Transform(square, cube))
        self.wait(1)

        # Move Camera to show 3D structure of the cube
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        self.wait(2)
