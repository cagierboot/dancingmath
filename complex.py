from manim import *

class Create3DCube(ThreeDScene):
    def construct(self):
        # Create a square
        square = Square(color=WHITE)

        # Create a cube with no fill
        cube = Cube(fill_opacity=0)

        # Set the stroke color and width to highlight the edges if needed
        cube.set_stroke(color=WHITE, width=2)

        # Add the square
        self.play(Create(square))  # Changed from ShowCreation to Create

        # Wait for a moment
        self.wait(1)

        # Transform the square into a cube
        self.play(ReplacementTransform(square, cube))

        # Set the initial camera orientation to isometric view
        self.set_camera_orientation(phi=PI / 4, theta=PI / 4)

        # Start the camera rotation
        self.begin_ambient_camera_rotation(rate=0.2)

        # Show the cube for 5 seconds
        self.wait(5)

        # Stop the camera rotation
        self.stop_ambient_camera_rotation()
