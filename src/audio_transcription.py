import whisper
import yt_dlp
import os
import json

def ensure_directory_exists(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")


def download_audio_from_youtube(url, output_dir="data/audio", filename="audio"):
    
    ensure_directory_exists(output_dir)  # Ensure the output directory exists
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

    transcript_path = "data/transcripts"
    ensure_directory_exists(transcript_path)  # Ensure the transcript directory exists

    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    filename = os.path.join(transcript_path , "transcripts.json")
    with open(filename, 'w') as f:
        json.dump(result, f, indent=4)  # Save the transcription result to a JSON file
    return result['text']# Return the transcribed text


if __name__ == "__main__":

    youtube_url = "https://www.youtube.com/watch?v=wgbV6DLVezo&ab_channel=TED-Ed"
    audio_path = download_audio_from_youtube(youtube_url)  # download the audio file
    print(f"Audio downloaded to: {audio_path}") # print the path of the downloaded audio file
    transcript = transcribe_audio(audio_path) # transcribe the audio file
    print(f"Transcription: {transcript}") # print the transcription