import yt_dlp
import os
import json
import cv2

def ensure_directory_exists(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")

def download_video_from_youtube(url, output_dir="data/video", filename="video"):
    ensure_directory_exists(output_dir)  # Ensure the output directory exists
    output_path = os.path.join(output_dir, filename)  # No extension here
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'quiet': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return output_path + ".mp4"  # Return full path including extension


def transcribe_video(video_path, segments):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        exit()

    output_dir = "data/frames"
    ensure_directory_exists(output_dir)  # Ensure the output directory exists
    

    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second of the video

    for i, segment in enumerate(segments):
        frame_number = int(segment['start']) * fps

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Could not read frame at {segment['start']} seconds.")
            continue

        frame_filename = os.path.join(output_dir, f"frame_{i:04d}.jpg")
        cv2.imwrite(frame_filename, frame)  # Save the frame as an image

    cap.release()
    print(f"frames synched to transcript segments, and saved in '{output_dir}'.")
    return

if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=wgbV6DLVezo&ab_channel=TED-Ed"
    video_path = download_video_from_youtube(youtube_url)  # download the video file
    print(f"Video downloaded to: {video_path}")  # print the path of the downloaded video file

    with open("data/transcripts/transcripts.json", 'r') as f:
        transcript = json.load(f)
    
    transcribe_video(video_path, transcript['segments'])  # transcribe the video file
    # print