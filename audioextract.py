import librosa
import numpy as np
import datetime

# Load the audio file
audio_file = 'Idylls of Pegasus - Richard Meyer (ThatCelloGuy).mp4'
y, sr = librosa.load(audio_file, sr=None)

# Detect onsets
onsets = librosa.onset.onset_detect(y=y, sr=sr)
onset_frames = librosa.onset.onset_detect(y=y, sr=sr, units='frames')

# Collect 1 for onsets and 0 for non-onsets by checking the presence of each frame in the onsets array
onset_values = [1 if frame in onset_frames else 0 for frame in range(len(y)//512)]

# Get the current timestamp
timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

# Open a text file in write mode with the timestamp in the filename
filename = f'onsets_{timestamp}.txt'
with open(filename, 'w') as f:
    f.write(str(onset_values))  # Write array to file

print(f"Data written to {filename}")
