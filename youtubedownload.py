from pytube import YouTube
from http.client import IncompleteRead

max_retries = 5  # Adjust the number of retries as needed
url = 'https://youtu.be/vvsF2nF3rTo?si=LC31cKwQ3KhCmpXZ'

for i in range(max_retries):
    try:
        yt = YouTube(url)
        ys = yt.streams.filter(only_audio=True).first()
        download_path = ys.download()
        print(f"Audio downloaded to {download_path}")
        break  # Break the loop if download is successful
    except IncompleteRead as e:
        print(f"Attempt {i+1} failed with IncompleteRead error, retrying...")
