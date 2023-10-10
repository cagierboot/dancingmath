from pytube import YouTube

url = 'https://youtu.be/S66IfQky21I?si=5y0WfPkyAD5jUGOo'
yt = YouTube(url)
ys = yt.streams.filter(only_audio=True).first()

# Download the audio file
download_path = ys.download()
print(f"Audio downloaded to {download_path}")
