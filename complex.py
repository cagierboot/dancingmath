from manim import *

class Create3DCube(ThreeDScene):
    def construct(self):
        # Create a line
        line = Line(start=[-1,0,0], end=[1,0,0], color=WHITE)

        # Create a square
        square = Square(color=WHITE)

        # Create a cube with no fill
        cube = Cube(fill_opacity=0)

        # Set the stroke color and width to highlight the edges if needed
        cube.set_stroke(color=WHITE, width=2)

        # Set the initial camera orientation to straight forward view
        self.set_camera_orientation(phi=0, theta=0)  # Adjust these angles as needed

        # Add the line
        self.play(Create(line))

        # Wait for a moment
        self.wait(1)

        # Transform the line into a square with increased run_time
        self.play(ReplacementTransform(line, square), run_time=2)  # Increased run_time to 2 seconds

        # Wait for another moment
        self.wait(1)

        # Transform the square into a cube with increased run_time
        self.play(ReplacementTransform(square, cube), run_time=3)  # Increased run_time to 3 seconds

        # Move the camera to the isometric view
        self.move_camera(phi=PI/4, theta=PI/4, run_time=2)  # Adjusting the run_time as needed

        # Start the camera rotation
        self.begin_ambient_camera_rotation(rate=0.2)

        # Show the cube for 5 seconds
        self.wait(5)

        # Stop the camera rotation
        self.stop_ambient_camera_rotation()