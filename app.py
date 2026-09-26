import streamlit as st
import os
import joblib
import numpy as np

from news.news_processor import clean_news
from news.news_api import get_latest_news
from isl.sign_mapping import convert_to_signs
from gtts import gTTS
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.feature import hog


# -------------------------------------------------
# PAGE SETTINGS
# -------------------------------------------------

st.set_page_config(
    page_title="AI-Based Sign Language News Reader",
    page_icon="🤟"
)

st.title("🤟 AI-Based Sign Language News Reader")

st.write(
    "Convert news into audio and Indian Sign Language videos."
)


# -------------------------------------------------
# PROJECT PATHS
# -------------------------------------------------

project_folder = os.path.dirname(
    os.path.abspath(__file__)
)

video_folder = os.path.join(
    project_folder,
    "sign_videos"
)

alphabet_folder = project_folder

model_path = os.path.join(
    project_folder,
    "model",
    "svm_model.pkl"
)


# -------------------------------------------------
# NEWS INPUT
# -------------------------------------------------

if "news_input" not in st.session_state:
    st.session_state.news_input = ""

if "news_articles" not in st.session_state:
    st.session_state.news_articles = []


# -------------------------------------------------
# GET LATEST NEWS
# -------------------------------------------------

if st.button("📰 Get Latest News"):

    articles = get_latest_news()

    if articles:

        st.session_state.news_articles = articles

        st.success(
            "Latest news loaded successfully!"
        )

    else:

        st.warning(
            "No news found."
        )


# -------------------------------------------------
# SELECT NEWS
# -------------------------------------------------

if st.session_state.news_articles:

    news_options = []

    for article in st.session_state.news_articles:

        title = article.get(
            "title",
            "No title"
        )

        news_options.append(title)

    selected_news = st.selectbox(
        "📰 Select News",
        news_options
    )

    st.session_state.news_input = selected_news


# -------------------------------------------------
# MANUAL NEWS INPUT
# -------------------------------------------------

news = st.text_area(
    "📰 Enter News",
    value=st.session_state.news_input,
    placeholder="Example: India government education technology"
)


# -------------------------------------------------
# READ NEWS
# -------------------------------------------------

if st.button("🔊 Read News"):
    st.write("Read News button clicked")

    if not news.strip():

        st.warning(
            "Please enter some news."
        )

    else:

        # -----------------------------------------
        # CLEAN NEWS
        # -----------------------------------------

        cleaned_news = clean_news(news)

        st.subheader("📰 News")
        st.write(cleaned_news)


        # -----------------------------------------
        # AUDIO
        # -----------------------------------------

        audio_path = os.path.join(
            project_folder,
            "news",
            "streamlit_audio.mp3"
        )

        tts = gTTS(
            text=cleaned_news,
            lang="en"
        )

        tts.save(audio_path)

        st.subheader("🔊 Audio")
        st.audio(audio_path)


        # -----------------------------------------
        # ISL SIGN MAPPING
        # -----------------------------------------

        sign_sequence = convert_to_signs(
            cleaned_news
        )

        st.subheader(
            "🤟 Indian Sign Language"
        )

        words = cleaned_news.lower().split()

        for word, sign in zip(
            words,
            sign_sequence
        ):

            # Remove punctuation
            clean_word = word.strip(
                ".,!?;:\"'()[]{}"
            )


            # -------------------------------------
            # KNOWN SIGN VIDEO
            # -------------------------------------

            if sign.endswith(".mp4"):

                video_path = os.path.join(
                    video_folder,
                    sign
                )

                if os.path.exists(video_path):

                    st.write(
                        "🤟 Sign:",
                        sign.replace(
                            ".mp4",
                            ""
                        )
                    )

                    st.video(
                        video_path
                    )

                else:

                    st.warning(
                        "Video not found: "
                        + sign
                    )


            # -------------------------------------
            # UNKNOWN WORD
            # -------------------------------------

            else:

                st.write(
                    "🔤 Fingerspelling:",
                    clean_word
                )

                for letter in clean_word.upper():

                    if letter.isalpha():

                        image_path = os.path.join(
                            alphabet_folder,
                            letter + ".jpg"
                        )

                        if os.path.exists(
                            image_path
                        ):

                            st.image(
                                image_path,
                                caption=letter,
                                width=120
                            )

                        else:

                            st.warning(
                                "A-Z sign not found: "
                                + letter
                            )


# =================================================
# SVM SIGN RECOGNITION
# =================================================

st.divider()

st.header(
    "🤖 Sign Language Alphabet Recognition"
)

st.write(
    "Upload an ISL alphabet hand-sign image "
    "to predict its letter using the trained SVM model."
)


uploaded_image = st.file_uploader(
    "Upload Sign Image",
    type=[
        "jpg",
        "jpeg",
        "png"
    ]
)


if uploaded_image is not None:

    # ---------------------------------------------
    # DISPLAY IMAGE
    # ---------------------------------------------

    st.image(
        uploaded_image,
        caption="Uploaded Sign Image",
        width=300
    )


    if st.button("🔍 Predict Sign"):

        try:

            # -------------------------------------
            # LOAD SVM MODEL
            # -------------------------------------

            model_data = joblib.load(
                model_path
            )

            svm_model = model_data["model"]

            classes = model_data["classes"]


            # -------------------------------------
            # READ IMAGE
            # -------------------------------------

            image = imread(
                uploaded_image
            )


            # -------------------------------------
            # CONVERT TO GRAYSCALE
            # -------------------------------------

            if image.ndim == 3:

                image = rgb2gray(
                    image
                )

            else:

                image = image.astype(
                    np.float32
                )

                if image.max() > 1:

                    image = image / 255.0


            # -------------------------------------
            # RESIZE
            # -------------------------------------

            image = resize(
                image,
                (128, 128),
                anti_aliasing=True
            )


            # -------------------------------------
            # HOG FEATURES
            # -------------------------------------

            features = hog(
                image,
                orientations=9,
                pixels_per_cell=(8, 8),
                cells_per_block=(2, 2),
                block_norm="L2-Hys"
            )


            # -------------------------------------
            # PREDICTION
            # -------------------------------------

            features = features.reshape(
                1,
                -1
            )

            prediction = svm_model.predict(
                features
            )[0]


            # -------------------------------------
            # RESULT
            # -------------------------------------

            predicted_letter = str(
                prediction
            ).upper()

            st.success(
                "Predicted Sign: "
                + predicted_letter
            )


        except Exception as e:

            st.error(
                "Prediction error: "
                + str(e)
            )