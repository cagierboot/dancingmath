import librosa
import numpy as np
import random
from manim import *

# Function to generate the vertices of a pentagon
def pentagon_points(radius=1):
    return [
        np.array([np.cos(np.pi / 2.5 * i) * radius, np.sin(np.pi / 2.5 * i) * radius, 0])
        for i in range(5)
    ]

# Load the song and get the beat timings
y, sr = librosa.load("expanse.mp3")
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

        # All available shape factories
        shape_factories = [
            lambda: Line(start=[-1, 0, 0], end=[1, 0, 0], color=WHITE),
            lambda: Triangle(color=WHITE),
            lambda: Polygon(*pentagon_points(radius=1), color=WHITE),
            lambda: Circle(color=WHITE),
            lambda: Square(color=WHITE),
            lambda: Cube(fill_opacity=0).set_stroke(color=WHITE, width=2),
            lambda: Sphere(fill_opacity=0).set_stroke(color=WHITE, width=2),
            lambda: Cone(fill_opacity=0).set_stroke(color=WHITE, width=2).scale(np.array([1, 3, 1])),
            lambda: Prism(dimensions=[2, 2, 2], fill_opacity=0).set_stroke(color=WHITE, width=2)
        ]
        
        random.shuffle(shape_factories)

        elapsed_time = 0
        shape = shape_factories[0]()

        for i in range(total_beats):
            duration = beat_times[i] - elapsed_time if i != 0 else 0.1
            next_shape_index = i % len(shape_factories)
            next_shape = shape_factories[next_shape_index]()

            scaling_factor = 0.5 + loudness[i] * 3
            next_shape.scale(scaling_factor)

            self.play(
                ReplacementTransform(shape, next_shape),
                run_time=duration
            )

            next_shape.add_updater(lambda m, dt: m.rotate(0.05, axis=UP))
            shape = next_shape
            elapsed_time += duration
            
        shape.clear_updaters()

scene = CreateShapesToBeat()
scene.render()
