import os
from pathlib import Path
import librosa
import numpy as np
from manim import *
import librosa.display


class ComplexBeatVisual(Scene):
    def construct(self):
        audio_file = "4th Dimension.mp4"

        # Load the audio file, extract beats and other features
        y, sr = librosa.load(audio_file)
        S = np.abs(librosa.stft(y))
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)
        beat_intervals = np.diff(np.concatenate(([0], beat_times)))

        chroma = librosa.feature.chroma_stft(S=S, sr=sr)
        mean_chroma = np.mean(chroma, axis=1)

        # Function to map pitch to color
        def pitch_to_color(pitch):
            colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]
            index = int(pitch * (len(colors) - 1))
            return colors[index]

        # Create a circle and set its initial radius
        circle = Circle(radius=0.5, color=pitch_to_color(np.mean(mean_chroma)))
        self.add(circle)

        # Animate the circle with beat, volume, and pitch
        for i, interval in enumerate(beat_intervals):
            volume = np.mean(S[:, beat_frames[i]:beat_frames[i] + int(sr * interval)]) * 10
            color = pitch_to_color(np.mean(mean_chroma))
            self.play(
                circle.animate.scale(volume).set_color(color).rotate(PI/2),
                run_time=interval
            )


if __name__ == "__main__":
    script_name = f"{Path(__file__).resolve()}"
    os.system(f"manim -pql {script_name} ComplexBeatVisual")
