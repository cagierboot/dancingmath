import librosa
import datetime
import numpy as np

# Load the audio file
audio_file = '4th Dimension.mp4'
y, sr = librosa.load(audio_file, sr=None)

# Detect beat
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)

# Calculate the total length of the audio in seconds
total_length_seconds = len(y) / sr

# Calculate the total number of .25 second chunks in the audio
total_chunks = int(total_length_seconds / 0.25)

# Initialize an array to hold the beat data
beat_array = np.zeros(total_chunks, dtype=int)

# Convert beat frames to the time
beat_times = librosa.frames_to_time(beats, sr=sr)

# Convert beat times to .25 second chunks
beat_chunks = (beat_times / 0.25).astype(int)

# Set the value of the chunks containing beats to 1
beat_array[beat_chunks] = 1

# Get the current timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Open a text file in write mode with the timestamp in the filename
filename = f'beats_{timestamp}.txt'
with open(filename, 'w') as f:
    beat_str = ''.join(map(str, beat_array.tolist()))  # Convert array to string
    f.write(beat_str)  # Write string to file

print(f"Data written to {filename}")
