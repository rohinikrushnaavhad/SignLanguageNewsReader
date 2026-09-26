
import os
from news.news_processor import clean_news
from isl.sign_mapping import convert_to_signs
from news.audio import create_audio

# Get news
news = input("Enter news: ")

# Clean news
cleaned_news = clean_news(news)

print("\nCleaned News:")
print(cleaned_news)

# Convert news to ISL sign sequence
sign_sequence = convert_to_signs(cleaned_news)

print("\nISL Sign Sequence:")
print(sign_sequence)

# Create audio
audio_path = "/content/SignLanguageNewsReader/news/main_news_audio.mp3"

create_audio(cleaned_news, audio_path)

print("\nAudio created:")
print(audio_path)

# Display ISL videos
from IPython.display import Video, Audio, display

video_folder = "/content/SignLanguageNewsReader/sign_videos"

print("\nISL Videos + Audio:")

display(Audio(audio_path, autoplay=True))

for sign_video in sign_sequence:
    if sign_video.endswith(".mp4"):
        video_path = os.path.join(video_folder, sign_video)

        if os.path.exists(video_path):
            print("Playing:", sign_video)
            display(Video(video_path, embed=True))
        else:
            print("Video not found:", sign_video)
