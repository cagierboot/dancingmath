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

        # Create a white rectangle to cover the entire scene
        background_rect = Rectangle(height=config.frame_height, width=config.frame_width, fill_color=WHITE, fill_opacity=0)
        self.add(background_rect)

        # All available shape factories
        shape_factories = [
            lambda: Cube(fill_opacity=0).set_stroke(color=WHITE, width=2),
            lambda: Circle(color=WHITE),
            lambda: Sphere(fill_opacity=0).set_stroke(color=WHITE, width=2),
            lambda: Line(start=[-1, 0, 0], end=[1, 0, 0], color=WHITE),
            lambda: Triangle(color=WHITE),
            lambda: Square(color=WHITE),
            lambda: Polygon(*regular_polygon_points(6, radius=1), color=WHITE),  # Hexagon
            lambda: Ellipse(width=2, height=1, color=WHITE),
            lambda: Prism(dimensions=[2, 2, 2], fill_opacity=0).set_stroke(color=WHITE, width=2)
        ]

        # Force the first 4 shapes and then begin the random generations
        elapsed_time = 0
        shape = None

        for i in range(total_beats):
            if i < 4:
                next_shape = shape_factories[i]()
            else:
                random.shuffle(shape_factories[4:])
                next_shape_index = i % len(shape_factories[4:]) + 4
                next_shape = shape_factories[next_shape_index]()

            # Scaling the shape according to the loudness
            scaling_factor = 0.5 + loudness[i] * 3
            next_shape.scale(scaling_factor)

            if shape is not None:
                shape.clear_updaters()

            if shape:
                self.play(
                    ReplacementTransform(shape, next_shape),
                    run_time=beat_times[i] - elapsed_time if i != 0 else 0.1
                )
                
                self.play(background_rect.animate.set_opacity(1), run_time=0.1)
                self.play(background_rect.animate.set_opacity(0), run_time=0.1)
            else:
                self.play(FadeIn(next_shape), run_time=beat_times[i] - elapsed_time if i != 0 else 0.1)
            
            next_shape.add_updater(lambda m, dt: m.rotate(0.05, axis=UP))
            shape = next_shape
            elapsed_time = beat_times[i] if i != 0 else 0.1

scene = CreateShapesToBeat()
scene.render()
