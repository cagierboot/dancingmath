import librosa
from manim import *
import numpy as np

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

class Create3DCubeWithoutEquations(ThreeDScene):
    def construct(self):
        total_beats = len(beat_times)
        if total_beats == 0:
            raise Exception("No beats found in the audio file.")

        # Initial shape factories before the beat drops
        initial_shape_factories = [
            lambda: Line(start=[-1,0,0], end=[1,0,0], color=WHITE),
            lambda: Circle(color=WHITE),
            lambda: Square(color=WHITE)
        ]

        # All shape factories including the cube after the beat drops
        all_shape_factories = initial_shape_factories + [lambda: Cube(fill_opacity=0).set_stroke(color=WHITE, width=2)]

        # Use the initial shapes before the beat drops
        shape_factories = initial_shape_factories
        elapsed_time = 0
        shape = shape_factories[0]()

        beat_dropped = False

        for i in range(total_beats):
            duration = beat_times[i] - elapsed_time if i != 0 else 0.1

            if not beat_dropped and loudness[i] > 0.8:  # Adjust the threshold as needed to detect the beat drop
                beat_dropped = True
                # Switch to including the cube in the shape cycle after the beat drops
                shape_factories = all_shape_factories

            next_shape_index = i % len(shape_factories)
            next_shape = shape_factories[next_shape_index]()
            scaling_factor = 0.5 + loudness[i] * 3
            next_shape.scale(scaling_factor)

            self.play(
                ReplacementTransform(shape, next_shape),
                run_time=duration
            )

            shape = next_shape
            elapsed_time += duration

scene = Create3DCubeWithoutEquations()
scene.render()
