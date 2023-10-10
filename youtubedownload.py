from pytube import YouTube

url = 'https://youtu.be/6Hj5tucYv1Q?si=MRrv36FHz8EdTimz'
yt = YouTube(url)
ys = yt.streams.filter(only_audio=True).first()

# Download the audio file
download_path = ys.download()
print(f"Audio downloaded to {download_path}")
