
import re

def clean_news(text):
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text

def get_news():
    text = input("Enter news: ")
    return clean_news(text)

if __name__ == "__main__":
    news = get_news()
    print("\nCleaned News:")
    print(news)
