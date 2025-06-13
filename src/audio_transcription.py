import whisper
import yt_dlp
import os


def download_audio_from_youtube(url, output_dir="data/audio", filename="audio"):
    
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)  # No extension here
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return output_path + ".mp3"  # Return full path including extension



youtube_url= "https://www.youtube.com/watch?v=IWwI-coTp44&ab_channel=Psych2Go"
audio_path = download_audio_from_youtube(youtube_url)  # download the audio file
print(f"Audio downloaded to: {audio_path}")