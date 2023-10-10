from manim import *
import numpy as np

class VectorFieldScene(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=60 * DEGREES, theta=45 * DEGREES)
        
        # Create a vector field
        vector_field = self.get_vector_field()
        self.add(vector_field)

        self.wait(5)
    
    def get_vector_field(self):
        # Define vector field function
        def vector_field_func(point):
            x, y, z = point
            return np.array([y, -x, z])  # Example function; modify as needed

        # Generate vectors for the field
        vectors = VGroup()
        for x in np.arange(-2, 2.1, 0.5):
            for y in np.arange(-2, 2.1, 0.5):
                for z in np.arange(-2, 2.1, 0.5):
                    point = np.array([x, y, z])
                    vector = vector_field_func(point)
                    vectors.add(Arrow(point, point + vector * 0.3, buff=0, color=YELLOW))

        return vectors

