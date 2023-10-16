import librosa
import numpy as np
import random
from manim import *

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_height = 8.0
config.frame_width = config.frame_height * config.pixel_width / config.pixel_height

def pentagon_points(radius=1):
    return [
        np.array([np.cos(np.pi / 2.5 * i) * radius, np.sin(np.pi / 2.5 * i) * radius, 0])
        for i in range(5)
    ]

y, sr = librosa.load("expanse.mp3")
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

S = np.abs(librosa.stft(y))
loudness = librosa.amplitude_to_db(S, ref=np.max)

time_index = (beat_times * sr / 512).astype(int)
loudness_beat = loudness[:, time_index].mean(axis=0)

loudness = (loudness_beat - np.min(loudness_beat)) / (np.max(loudness_beat) - np.min(loudness_beat))

class CreateCubeAtBeatDrop(ThreeDScene):
    def construct(self):
        total_beats = len(beat_times)
        if total_beats == 0:
            raise Exception("No beats found in the audio file.")

        shape_factories = [
            lambda: Line(start=[-1, 0, 0], end=[1, 0, 0], color=WHITE),
            lambda: Triangle(color=WHITE),
            lambda: Polygon(*pentagon_points(radius=1), color=WHITE),
            lambda: Circle(color=WHITE),
            lambda: Square(color=WHITE),
            lambda: Cube(fill_opacity=0).set_stroke(color=WHITE, width=2),
            lambda: Sphere(fill_opacity=0).set_stroke(color=WHITE, width=2),
            lambda: Cone(fill_opacity=0).set_stroke(color=WHITE, width=2).scale(np.array([1, 3.5, 1])),
        ]

        random.shuffle(shape_factories)

        elapsed_time = 0
        shape = shape_factories[0]()

        equation = self.get_equation_for_shape(shape).scale(0.5).next_to(shape, DOWN)
        self.add(equation)

        for i in range(total_beats):
            duration = beat_times[i] - elapsed_time if i != 0 else 0.1

            next_shape_index = i % len(shape_factories)
            next_shape = shape_factories[next_shape_index]()

            scaling_factor = 0.5 + loudness[i] * 2
            scaling_factor = min(scaling_factor, 1.5)
            next_shape.scale(scaling_factor)

            new_equation = self.get_equation_for_shape(next_shape)
            new_equation.scale(0.5).next_to(next_shape, DOWN)

            self.play(
                ReplacementTransform(shape, next_shape),
                ReplacementTransform(equation, new_equation),
                run_time=duration
            )

            equation = new_equation
            shape = next_shape
            elapsed_time += duration
            
            shape.add_updater(lambda m, dt: m.rotate(0.05, axis=UP))

        shape.clear_updaters()

    def get_equation_for_shape(self, shape):
        if isinstance(shape, Line):
            return MathTex("y = mx + c")
        elif isinstance(shape, Triangle):
            return MathTex("Ax + By + Cz + D = 0")
        elif isinstance(shape, Polygon):  # Assuming polygon is a pentagon here
            return MathTex("Ax_1 + By_1 + Cz_1 + D = 0, \\ldots")
        elif isinstance(shape, Circle):
            return MathTex("x^2 + y^2 = r^2")
        elif isinstance(shape, Square):
            return MathTex("4\\text{ sides}, 90^\\circ \\text{ angles}")
        elif isinstance(shape, Cube):
            return MathTex("l = w = h")
        elif isinstance(shape, Sphere):
            return MathTex("x^2 + y^2 + z^2 = r^2")
        elif isinstance(shape, Cone):
            return MathTex("x^2 + y^2 - z^2 = 0")


scene = CreateCubeAtBeatDrop()
scene.render()
