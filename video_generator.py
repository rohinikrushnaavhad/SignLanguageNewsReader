
import os
import subprocess
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from gtts import gTTS


def generate_news_video(news_text):

    project_path = "/content/SignLanguageNewsReader"
    video_folder = os.path.join(project_path, "sign_videos")

    audio_path = os.path.join(
        project_path, "news", "generated_audio.mp3"
    )

    video_temp = os.path.join(
        project_path, "news", "combined_signs.mp4"
    )

    final_output = os.path.join(
        project_path, "news", "final_news.mp4"
    )

    # -----------------------------
    # 1. Generate audio
    # -----------------------------
    tts = gTTS(news_text, lang="en")
    tts.save(audio_path)

    # -----------------------------
    # 2. Sign video mapping
    # -----------------------------
    mapping = {
        "india": "India.mp4",
        "government": "Government.mp4",
        "education": "Education.mp4",
        "technology": "Technology.mp4",
        "health": "Health.mp4",
        "know": "I_Know.mp4",
        "understand": "I_Understand.mp4"
    }

    words = news_text.lower().split()

    clips = []

    for word in words:

        if word in mapping:

            video_path = os.path.join(
                video_folder,
                mapping[word]
            )

            if os.path.exists(video_path):
                clips.append(VideoFileClip(video_path))

    if not clips:
        print("No matching ISL videos found.")
        return None

    # -----------------------------
    # 3. Combine all sign videos
    # -----------------------------
    combined = concatenate_videoclips(
        clips,
        method="compose"
    )

    combined.write_videofile(
        video_temp,
        codec="libx264",
        audio=False
    )

    video_duration = combined.duration

    combined.close()

    for clip in clips:
        clip.close()

    print("Combined video duration:", video_duration)

    # -----------------------------
    # 4. Add audio without cutting video
    # -----------------------------
    command = [
        "ffmpeg",
        "-y",
        "-i", video_temp,
        "-i", audio_path,

        "-filter_complex",
        "[1:a]apad[a]",

        "-map", "0:v:0",
        "-map", "[a]",

        "-c:v", "libx264",
        "-c:a", "aac",

        "-t", str(video_duration),

        final_output
    ]

    subprocess.run(command, check=True)

    print("\nFinal video created:")
    print(final_output)

    return final_output
