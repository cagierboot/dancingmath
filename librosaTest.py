import librosa
import numpy as np
import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import AudioFileClip

# Load the audio file
audio_file = '4th Dimension.mp4'
y, sr = librosa.load(audio_file, sr=None)

# Compute the onset envelope
onset_env = librosa.onset.onset_strength(y=y, sr=sr)

# Detect the beat frames and convert to frame indices
tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
beat_times = librosa.frames_to_time(beats, sr=sr)

# Create a video file with beat flashes
height, width = 720, 1280  # Set the width and height of the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('beat_flash_video_noaudio.mp4', fourcc, 30.0, (width, height))

# Fill video with flashes on beats
total_frames = int(y.shape[0] / sr * 30)  # Total frames for 30 fps video
beat_frames = (beat_times * 30).astype(int)  # Beat times in terms of video frames

for i in range(total_frames):
    img = np.zeros((height, width, 3), dtype=np.uint8)  # Create a black image

    if i in beat_frames:
        img[:] = [0, 255, 0]  # Change the color to green for a flash effect

    video.write(img)

video.release()
cv2.destroyAllWindows()

# Load the no-audio video
video_noaudio = VideoFileClip('beat_flash_video_noaudio.mp4')

# Load the audio file
audio = AudioFileClip(audio_file)

# Set the audio of the video clip
videoclip = video_noaudio.set_audio(audio)

# Write the result to a new file
videoclip.write_videofile('beat_flash_video.mp4', codec='libx264')
