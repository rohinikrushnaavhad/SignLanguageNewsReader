import string

SIGN_MAPPING = {
    "india": "India.mp4",
    "indian": "India.mp4",
    "government": "Government.mp4",
    "education": "Education.mp4",
    "technology": "Technology.mp4",
    "health": "Health.mp4",
    "know": "I_Know.mp4",
    "understand": "I_Understand.mp4"
}


def convert_to_signs(text):
    words = [
        word.strip(string.punctuation)
        for word in text.lower().split()
    ]

    sign_sequence = []

    for word in words:
        if word in SIGN_MAPPING:
            sign_sequence.append(SIGN_MAPPING[word])
        else:
            sign_sequence.append("fingerspell_" + word)

    return sign_sequence