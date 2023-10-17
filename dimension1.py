import librosa
import numpy as np
import random
from manim import *

# Function to generate the vertices of a regular polygon
def regular_polygon_points(sides, radius=1):
    return [
        np.array([np.cos(2 * np.pi / sides * i) * radius, np.sin(2 * np.pi / sides * i) * radius, 0])
        for i in range(sides)
    ]

# Load the song and get the beat timings
y, sr = librosa.load("interstellar.mp3")
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# Compute the loudness in dB
S = np.abs(librosa.stft(y))
loudness = librosa.amplitude_to_db(S, ref=np.max)

# Get the loudness at each beat
time_index = (beat_times * sr / 512).astype(int)
loudness_beat = loudness[:, time_index].mean(axis=0)

# Normalize the loudness values
loudness = (loudness_beat - np.min(loudness_beat)) / (np.max(loudness_beat) - np.min(loudness_beat))

class CreateShapesToBeat(ThreeDScene):
    def construct(self):
        total_beats = len(beat_times)
        if total_beats == 0:
            raise Exception("No beats found in the audio file.")


class CreateShapesToBeat(ThreeDScene):
    def construct(self):
        total_beats = len(beat_times)
        if total_beats == 0:
            raise Exception("No beats found in the audio file.")

        # All available shape factories with their respective equations
        shape_factories = [
    (lambda: Cube(fill_opacity=0).set_stroke(color=WHITE, width=2), 
r"$-\frac{s}{2} \leq x \leq \frac{s}{2}$, $-\frac{s}{2} \leq y \leq \frac{s}{2}$, $-\frac{s}{2} \leq z \leq \frac{s}{2}$"),
    (lambda: Circle(color=WHITE), r"$x^2+y^2=r^2$"),
    (lambda: Sphere(fill_opacity=0).set_stroke(color=WHITE, width=2), r"$x^2+y^2+z^2=r^2$"),
    (lambda: Line(start=[-1, 0, 0], end=[1, 0, 0], color=WHITE), r"$y=mx+c$"),
    (lambda: Triangle(color=WHITE), r"$A=\frac{1}{2}bh$"),
    (lambda: Square(color=WHITE), r"$A=s^2$"),
    (lambda: Polygon(*regular_polygon_points(6, radius=1), color=WHITE), r"$A=\frac{3\sqrt{3}}{2}s^2$"),
    (lambda: Ellipse(width=2, height=1, color=WHITE), r"$\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$"),
    (lambda: Prism(dimensions=[2, 2, 2], fill_opacity=0).set_stroke(color=WHITE, width=2), r"$V=Bh$")
]

        # Force the first 4 shapes and then begin the random generations
        elapsed_time = 0
        shape = None
        equation = None

        for i in range(total_beats):
            if i < len(shape_factories):
                next_shape, eq_text = shape_factories[i]
                next_shape = next_shape()
            else:
                random.shuffle(shape_factories)  # Randomize the order of shapes on each iteration
                next_shape, eq_text = random.choice(shape_factories)
                next_shape = next_shape()

            # Create equation text
            next_equation = Tex(eq_text, color=WHITE).scale(0.5)
            next_equation.next_to(next_shape, DOWN)

            # Scaling the shape according to the loudness
            scaling_factor = 0.5 + loudness[i] * 2.5  # You can adjust the base size and multiplier as needed
            next_shape.scale(scaling_factor)
            next_equation.scale(scaling_factor)

            # Update the position of the equation based on the boundaries of the shape
            shape_bottom = next_shape.get_critical_point(DOWN)[1]
            equation_top = next_equation.get_critical_point(UP)[1]
            next_equation.next_to(next_shape, DOWN, buff=(equation_top - shape_bottom) * .4)
            
            # Calculate the combined bounding box of the shape and equation
            combined = VGroup(next_shape, next_equation)
            combined_width = combined.get_width()
            combined_height = combined.get_height()
            
            scale_factor = min(config.frame_width / combined_width, config.frame_height / combined_height * .7)

            
            # If the bounding box is larger than the viewport, scale down both the shape and equation
            if scale_factor < 1:
                next_shape.scale(scale_factor)
                next_equation.scale(scale_factor)
            
            if shape and equation:
                self.play(
                    ReplacementTransform(shape, next_shape),
                    ReplacementTransform(equation, next_equation),
                    run_time=beat_times[i] - elapsed_time if i != 0 else 0.1
                )
            else:
               self.play(Create(VGroup(next_shape, next_equation)),
                          run_time=beat_times[i] - elapsed_time if i != 0 else 0.1)

            next_shape.add_updater(lambda m, dt: m.rotate(0.15, axis=UP))
            shape = next_shape
            equation = next_equation
            elapsed_time = beat_times[i] if i != 0 else 0.1

        shape.clear_updaters()

class PortraitConfig:
    def __init__(self):
        config.pixel_height = 2000
        config.pixel_width = 2000
        config.frame_height = 8.0
        config.frame_width = config.frame_height * (config.pixel_width / config.pixel_height)

# Create an instance of the configuration class
PortraitConfig()

# Create an instance of the scene class with the custom configuration
scene = CreateShapesToBeat()

# Render the scene
scene.render()
