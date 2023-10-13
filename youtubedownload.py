from pytube import YouTube

url = 'https://youtu.be/1Dzh0XkuNPg?si=ZKWTl-9Ef1ARO4ew'
yt = YouTube(url)
ys = yt.streams.filter(only_audio=True).first()

# Download the audio file
download_path = ys.download()
print(f"Audio downloaded to {download_path}")
