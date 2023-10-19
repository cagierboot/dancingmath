from flask import Flask, send_file, jsonify
from flask_cors import CORS
import librosa
import numpy as np
import random
from manim import *

app = Flask(__name__)
CORS(app)  # This allows CORS for all routes

def pentagon_points(radius=1):
    return [
        np.array([np.cos(np.pi / 2.5 * i) * radius, np.sin(np.pi / 2.5 * i) * radius, 0])
        for i in range(5)
    ]

class CreateCubeAtBeatDrop(ThreeDScene):
    def construct(self):
        y, sr = librosa.load("expanse.mp3")
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        S = np.abs(librosa.stft(y))
        loudness = librosa.amplitude_to_db(S, ref=np.max)
        time_index = (beat_times * sr / 512).astype(int)
        loudness_beat = loudness[:, time_index].mean(axis=0)
        loudness = (loudness_beat - np.min(loudness_beat)) / (np.max(loudness_beat) - np.min(loudness_beat))

        total_beats = len(beat_times)
        if total_beats == 0:
            raise Exception("No beats found in the audio file.")

        initial_shape_factories = [
            lambda: Line(start=[-1, 0, 0], end=[1, 0, 0], color=WHITE),
            lambda: Triangle(color=WHITE),
            lambda: Polygon(*pentagon_points(radius=1), color=WHITE),
            lambda: Circle(color=WHITE),
            lambda: Square(color=WHITE),
        ]

        shape_factories = initial_shape_factories.copy()

        elapsed_time = 0
        shape = shape_factories[0]()

        beat_dropped = False

        for i in range(total_beats):
            duration = beat_times[i] - elapsed_time if i != 0 else 0.1

            if not beat_dropped and loudness[i] > 0.8:
                beat_dropped = True
                shape_factories.extend([
                    lambda: Cube(fill_opacity=0).set_stroke(color=WHITE, width=2),
                    lambda: Sphere(fill_opacity=0).set_stroke(color=WHITE, width=2),
                    lambda: Cone(fill_opacity=0).set_stroke(color=WHITE, width=2).scale(np.array([1, 3, 1])),
                    lambda: Prism(dimensions=[2, 2, 2], fill_opacity=0).set_stroke(color=WHITE, width=2)
                ])

                random.shuffle(shape_factories)

            next_shape = shape_factories[i % len(shape_factories)]()
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

@app.route('/')
def hello_world():
    return "Hello, Mark"

@app.route('/render_video', methods=['POST'])
def render_video():
    try:
        audio_file = request.files['audio']
        audio_filepath = "/tmp/" + audio_file.filename  # Adjust the path as needed
        audio_file.save(audio_filepath)
        
        scene = CreateCubeAtBeatDrop(audio_filepath=audio_filepath)
        video_path = "/tmp/video.mp4"  # Adjust the path as needed
        scene.render(file_path=video_path, save_last_frame=True)

        os.remove(audio_filepath)  # Optional: remove the saved audio file after processing

        return send_file(video_path, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
