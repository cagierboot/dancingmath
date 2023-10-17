import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

# Load the audio file
file_path = 'interstellar.mp3'
y, sr = librosa.load(file_path)

# Analyze the tempo
onset_env = librosa.onset.onset_strength(y=y, sr=sr)
tempo, _ = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
print(f"Estimated Tempo: {tempo} beats per minute")

# Analyze the Melody
chromagram = librosa.feature.chroma_cqt(y=y, sr=sr)
plt.figure(figsize=(10, 4))
librosa.display.specshow(chromagram, x_axis='time', y_axis='chroma', cmap='coolwarm')
plt.title('Chromagram')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()
print("Above is the Chromagram which displays the energy content of each pitch class over time.")

# Analyze the Harmonic content
harmonic, percussive = librosa.effects.hpss(y)
plt.figure(figsize=(10, 4))
librosa.display.waveshow(harmonic, sr=sr, alpha=0.25)
plt.title('Harmonic content')
plt.colorbar(format='%+2.0f dB')
plt.tight_layout()
plt.show()
print("Above is the Harmonic content of the audio.")

# Analyze the Beat
plt.figure()
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
librosa.display.waveshow(y, sr=sr, alpha=0.4)
plt.vlines(librosa.frames_to_time(beat_frames), -1, 1, color='r', alpha=0.9, label='Beats')
plt.legend()
plt.title('Beat content')
plt.show()
print("Above is the Beat content of the audio.")

# If you want to extract more information like MFCCs, Spectral Contrast, etc., you can easily do so with librosa's comprehensive feature extraction functions.
