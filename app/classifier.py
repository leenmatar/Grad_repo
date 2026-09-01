import re

import joblib

saved_data = joblib.load("saved_model/ticket_classifier.joblib")

model = saved_data["model"]
vectorizer = saved_data["vectorizer"]


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


def predict_category(description):
    cleaned_text = clean_text(description)

    text_tfidf = vectorizer.transform([cleaned_text])

    predicted_category = model.predict(text_tfidf)[0]

    probabilities = model.predict_proba(text_tfidf)[0]

    confidence = max(probabilities)

    return (
        predicted_category,
        round(float(confidence) * 100, 2),
    )
