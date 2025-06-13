# 🎬 ClipGist: Multimodal YouTube Summarizer

**ClipGist** is an advanced Python-based tool that generates **smart, multimodal summaries of YouTube videos** by combining insights from both **audio (speech)** and **visual content (keyframes)**.

Unlike basic transcript summarizers, ClipGist leverages **OpenAI Whisper** for transcription, **OpenAI CLIP** for vision-language alignment, and an encoder-decoder **LLM** to produce rich summaries that reflect both **what is said** and **what is shown**.

---

## 🚀 Features

- 🔊 **Audio Transcription**: Uses OpenAI Whisper to transcribe spoken content into timestamped text.
- 🖼️ **Keyframe Extraction**: Extracts key video frames at intervals or via scene changes.
- 🤝 **Multimodal Fusion**: Combines encoded transcript and visuals into a joint representation.
- ✨ **LLM-Based Summary Generation**: Uses an encoder-decoder language model to create a coherent, concise summary of the video.
- 🎯 *(Planned)*: Interactive Q&A and timeline navigation based on multimodal understanding.

---

## 🧠 How It Works

### 1. Transcribe Audio
- Download audio using `yt-dlp`
- Transcribe using OpenAI Whisper (local model)

### 2. Extract Visual Content
- Extract keyframes using OpenCV or FFmpeg
- Encode keyframes using OpenAI CLIP (image encoder)

### 3. Encode Text
- Segment transcript and encode each chunk using CLIP (text encoder)

### 4. Combine Modalities
- Align each text segment with the nearest keyframe (based on timestamp)
- Concatenate embeddings to form a multimodal feature vector

### 5. Summarize
- Feed multimodal vectors into a vision-language LLM (e.g., MiniGPT-4, LLaVA)
- Generate a natural language summary

---

## 📦 Tech Stack

| Component       | Tool / Library              |
|----------------|-----------------------------|
| Audio Download | `yt-dlp`                    |
| Transcription  | `openai-whisper`            |
| Frame Extraction | `opencv-python` / `ffmpeg` |
| Image Encoding | `openai-clip`               |
| Text Encoding  | `openai-clip` / `SentenceTransformers` |
| Summarization  | `MiniGPT-4`, `LLaVA`, or other encoder-decoder LLMs |
| Language       | Python 3.8+                  |

---

## 📁 Project Structure (WIP)

