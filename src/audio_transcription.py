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

def transcribe_audio(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result['text']# Return the transcribed text



if __name__ == "__main__":

    youtube_url = "https://www.youtube.com/watch?v=wgbV6DLVezo&ab_channel=TED-Ed"
    audio_path = download_audio_from_youtube(youtube_url)  # download the audio file
    print(f"Audio downloaded to: {audio_path}") # print the path of the downloaded audio file
    transcript = transcribe_audio(audio_path) # transcribe the audio file
    print(f"Transcription: {transcript}") # print the transcription