from manim import *
import numpy as np

class GravityField(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)

        # Create a vector field with all vectors pointing downwards initially
        vector_field = self.get_vector_field(DOWN * 2)
        self.add(vector_field)

        # Create a sphere that will move to simulate a planet
        sphere = Sphere(radius=0.2, color=RED)
        sphere.shift(DOWN * 2)
        self.add(sphere)

        # Animate the sphere moving upward while updating the vector field
        for _ in range(40):
            sphere.shift(UP * 0.1)
            new_field = self.get_vector_field(sphere.get_center())
            self.play(
                Transform(vector_field, new_field),
                sphere.animate.shift(UP * 0.1),
                run_time=0.1
            )
        
        self.wait(1)

    def get_vector_field(self, sphere_center):
        # Generate vectors that point towards the sphere
        vectors = VGroup()
        for x in np.arange(-2, 2.1, 0.5):
            for y in np.arange(-2, 2.1, 0.5):
                for z in np.arange(-2, 2.1, 0.5):
                    point = np.array([x, y, z])
                    direction = normalize(sphere_center - point) * 0.3
                    vectors.add(Arrow(point, point + direction, buff=0, color=YELLOW))

        return vectors
