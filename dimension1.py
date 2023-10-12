import librosa
from manim import *

# Load the song and get the beat timings
y, sr = librosa.load("4th Dimension.mp4")
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
beat_times = librosa.frames_to_time(beat_frames, sr=sr)

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
        self.play(Create(shape))
        self.wait(beat_times[0])  # Wait for the first beat

        elapsed_time = beat_times[0]  # Keep track of the elapsed time

        # Loop through the remaining beats to animate the transformations
        for i in range(1, total_beats):
            # Calculate the time duration until the next beat
            duration = beat_times[i] - elapsed_time

            # Create new shapes for each transformation
            next_shape = shape_factories[i % len(shape_factories)]()

            # Animate the transformation
            self.play(
                ReplacementTransform(shape, next_shape),
                run_time=duration  # Sync with the beat
            )
            self.wait(duration)  # Wait for the next beat

            # Set the current shape to the new ones for the next loop iteration
            shape = next_shape
            elapsed_time += duration  # Update the elapsed time

        # Add rotation to make the animation more dynamic
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(beat_times[-1] - elapsed_time)  # Wait until the end of the song
        self.stop_ambient_camera_rotation()
