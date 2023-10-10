from manim import *

class Create3DCube(ThreeDScene):
    def construct(self):
        # Create a cube
        cube = Cube()

        # Set the initial camera orientation to isometric view
        self.set_camera_orientation(phi=PI / 4, theta=PI / 4)

        # Add the cube
        self.add(cube)

        # Start the camera rotation
        self.begin_ambient_camera_rotation(rate=0.2)

        # Show the cube for 5 seconds
        self.wait(5)

        # Stop the camera rotation
        self.stop_ambient_camera_rotation()
