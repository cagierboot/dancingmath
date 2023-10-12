import librosa
from manim import *
import numpy as np

# Load the song and get the beat timings
y, sr = librosa.load("4D.mp3")
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

# Compute the loudness in dB at each beat
loudness = librosa.amplitude_to_db(y[beat_frames], ref=np.max)

# Normalize the loudness values to a scale from 0 to 1 for resizing the shapes
loudness = (loudness - np.min(loudness)) / (np.max(loudness) - np.min(loudness))

class Create3DCubeWithoutEquations(ThreeDScene):
    def construct(self):
        # Getting the total number of beats
        total_beats = len(beat_times)
        if total_beats == 0:
            raise Exception("No beats found in the audio file.")

        # Create a list of shape factories to create new objects each time
        shape_factories = [
            lambda: Line(start=[-1,0,0], end=[1,0,0], color=WHITE),
            lambda: Square(color=WHITE),
            lambda: Cube(fill_opacity=0).set_stroke(color=WHITE, width=2)
        ]

        # Initialize the scene with the first shape
        shape = shape_factories[0]()
        self.play(Create(shape))  # Removed the initial wait time

        elapsed_time = 0  # Set the initial elapsed time to 0

        # Loop through the remaining beats to animate the transformations
        for i in range(total_beats):
            # Calculate the time duration until the next beat
            duration = beat_times[i] - elapsed_time if i != 0 else beat_times[0]

            # Create new shapes for each transformation
            next_shape = shape_factories[i % len(shape_factories)]()

            # Resize the shape based on the loudness
            next_shape.scale(1 + loudness[i])

            # Animate the transformation
            self.play(
                ReplacementTransform(shape, next_shape),
                run_time=duration  # Sync with the beat
            )

            # Set the current shape to the new ones for the next loop iteration
            shape = next_shape
            elapsed_time += duration  # Update the elapsed time

        # Add rotation to make the animation more dynamic
        self.begin_ambient_camera_rotation(rate=0.2)
        self.play(
            Animation(shape),  # Keep the last shape on screen while rotating the camera
            run_time=beat_times[-1] - elapsed_time  # Adjust the time to match the audio length
        )
        self.stop_ambient_camera_rotation()
