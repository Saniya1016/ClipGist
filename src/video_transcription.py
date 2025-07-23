import yt_dlp
import os
import json
import cv2
from utils.helpers import ensure_directory_exists

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


def draw_text_on_frame(frame, text, font_scale=0.6, font_thickness=1):
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)       # White text
    bg_color = (0, 0, 0)          # Black background
    margin = 10

    # Wrap text manually (since OpenCV doesn't do it natively)
    max_width = frame.shape[1] - 2 * margin
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        text_size = cv2.getTextSize(test_line, font, font_scale, font_thickness)[0]
        if text_size[0] <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)

    y = margin
    for line in lines:
        text_size = cv2.getTextSize(line, font, font_scale, font_thickness)[0]
        x = margin
        # Background rectangle
        cv2.rectangle(frame, (x - 5, y - 15), (x + text_size[0] + 5, y + 5), bg_color, -1)
        # Text
        cv2.putText(frame, line, (x, y), font, font_scale, color, font_thickness, cv2.LINE_AA)
        y += int(text_size[1] * 1.5)
    
    return frame


def transcribe_video(video_path, segments, draw_text = False):

    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Could not open video file.")
        exit()

    output_dir = "data/frames"
    ensure_directory_exists(output_dir)  # Ensure the output directory exists
    

    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second of the video

    data = []

    for i, segment in enumerate(segments):
        frame_number = int(segment['start']) * fps

        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if not ret:
            print(f"Error: Could not read frame at {segment['start']} seconds.")
            continue

        # Draw the text on the frame
        if draw_text:
            text = segment["text"]
            frame = draw_text_on_frame(frame, text)

        frame_filename = os.path.join(output_dir, f"frame_{i:04d}.jpg")
        cv2.imwrite(frame_filename, frame)  # Save the frame as an image

        data.append({
            "start": segment['start'],
            "end": segment['end'],
            "text": segment['text'],
            "frame_path": frame_filename
        })

    # Save the data to a JSON file
    with open("data/frame_segment_pairs.json", "w") as f:
        json.dump(data, f, indent=2)

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