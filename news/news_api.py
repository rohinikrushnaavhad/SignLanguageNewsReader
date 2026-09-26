
import requests
import streamlit as st

API_KEY = st.secrets["NEWS_API_KEY"]


def get_latest_news():
    url = "https://newsapi.org/v2/everything"

    params = {
        "q": "India",
        "language": "en",
        "pageSize": 5,
        "sortBy": "publishedAt",
        "apiKey": API_KEY
    }

    response = requests.get(url, params=params)

    data = response.json()

    if data.get("status") == "ok":
        return data.get("articles", [])

    return []