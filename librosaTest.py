import librosa
import numpy as np
import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import AudioFileClip

# Load the audio file
audio_file = 'Can You Hear The Music.mp4'
y, sr = librosa.load(audio_file, sr=None)

# Compute the onset envelope for beats
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)

# Compute Chroma feature for harmony
chroma = librosa.feature.chroma_stft(y=y, sr=sr)

# Compute MFCCs for melody
mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=5)

# Create a video file with music-responsive visual effects
height, width = 720, 1280  # Set the width and height of the video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('music_visualization_noaudio.mp4', fourcc, 30.0, (width, height))

total_frames = int(y.shape[0] / sr * 30)  # Total frames for 30 fps video
beat_frames = (librosa.frames_to_time(beats, sr=sr) * 30).astype(int)  # Beat times in terms of video frames

for i in range(total_frames):
    img = np.zeros((height, width, 3), dtype=np.uint8)  # Create a black image

    # Create color effects based on Chroma and MFCCs
    chroma_color = (chroma[:, i % chroma.shape[1]] * 255).astype(np.uint8)
    melody_color = np.mean(mfccs[:, i % mfccs.shape[1]])  # Averaging the MFCCs for simplicity

    # Convert chroma_color to a color that can be used for the entire image
    chroma_color_avg = np.mean(chroma_color)  # Averaging chroma values
    img[:] = [chroma_color_avg, chroma_color_avg, chroma_color_avg]  # Set the image color based on averaged chroma
    
    # If needed, you can apply additional color mappings or visual effects here

    # Flash effect on beats
    if i in beat_frames:
        img = cv2.addWeighted(img, 0.7, np.ones((height, width, 3), dtype=np.uint8) * 255, 0.3, 0)

    video.write(img)


video.release()
cv2.destroyAllWindows()

# Load the no-audio video
video_noaudio = VideoFileClip('music_visualization_noaudio.mp4')

# Load the audio file
audio = AudioFileClip(audio_file)

# Set the audio of the video clip
videoclip = video_noaudio.set_audio(audio)

# Write the result to a new file
videoclip.write_videofile('music_visualization.mp4', codec='libx264')
