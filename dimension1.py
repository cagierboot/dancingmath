import librosa
import numpy as np
import random
from manim import *

# Function to generate the vertices of a pentagon
def pentagon_points(radius=1):
    """Return the vertices of a regular pentagon with the given radius."""
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

# Get the loudness at each beat by converting beat times to indices on the time axis
time_index = (beat_times * sr / 512).astype(int)
loudness_beat = loudness[:, time_index].mean(axis=0)

# Normalize the loudness values to a scale from 0 to 1 for scaling shapes
loudness = (loudness_beat - np.min(loudness_beat)) / (np.max(loudness_beat) - np.min(loudness_beat))

class CreateCubeAtBeatDrop(ThreeDScene):
    def construct(self):
        total_beats = len(beat_times)
        if total_beats == 0:
            raise Exception("No beats found in the audio file.")

        # Initial shape factories before the beat drops
        initial_shape_factories = [
            lambda: Line(start=[-1, 0, 0], end=[1, 0, 0], color=WHITE),
            lambda: Triangle(color=WHITE),
            lambda: Polygon(*pentagon_points(radius=1), color=WHITE),
            lambda: Circle(color=WHITE),
            lambda: Square(color=WHITE),
        ]

        # Use the initial shapes before the beat drops
        shape_factories = initial_shape_factories.copy()

        elapsed_time = 0
        shape = shape_factories[0]()

        beat_dropped = False

        for i in range(total_beats):
            duration = beat_times[i] - elapsed_time if i != 0 else 0.1

            if not beat_dropped and loudness[i] > 0.8:
                beat_dropped = True
                next_shape = Cube(fill_opacity=0).set_stroke(color=WHITE, width=2)
                shape_factories.append(lambda: Cube(fill_opacity=0).set_stroke(color=WHITE, width=2))

                shape_factories.append(lambda: Sphere(fill_opacity=0).set_stroke(color=WHITE, width=2))

                shape_factories.append(
                    lambda: Cone(fill_opacity=0).set_stroke(color=WHITE, width=2).scale(np.array([1, 3, 1]))

                )
                shape_factories.append(lambda: Prism(dimensions=[2, 2, 2], fill_opacity=0).set_stroke(color=WHITE, width=2))

                # Shuffle the shapes after the beat drops
                random.shuffle(shape_factories)

            else:
                next_shape_index = i % len(shape_factories)
                next_shape = shape_factories[next_shape_index]()

            scaling_factor = 0.5 + loudness[i] * 3
            next_shape.scale(scaling_factor)

            self.play(
                ReplacementTransform(shape, next_shape),
                run_time=duration
            )

            # Adding rotation with add_updater
            next_shape.add_updater(lambda m, dt: m.rotate(0.05, axis=UP))



            shape = next_shape
            elapsed_time += duration
            
        # To remove updater when animation is done to prevent continuation of rotation after scene end
        shape.clear_updaters()

scene = CreateCubeAtBeatDrop()
scene.render()
