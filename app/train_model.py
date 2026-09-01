import os
import re

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split

# ==========================================
# Load Original Dataset
# ==========================================

data = pd.read_csv("data/tickets.csv")


# ==========================================
# Additional Training Examples
# ==========================================

additional_data = [
    # -----------------------------
    # Account
    # -----------------------------
    {
        "description": "I cannot login to my university account",
        "category": "Account",
    },
    {
        "description": "My university account is locked",
        "category": "Account",
    },
    {
        "description": "I forgot my university password",
        "category": "Account",
    },
    {
        "description": "I need to reset my account password",
        "category": "Account",
    },
    {
        "description": "My student account login is not working",
        "category": "Account",
    },
    {
        "description": "I cannot access my university account",
        "category": "Account",
    },
    {
        "description": "My password is not accepted",
        "category": "Account",
    },
    {
        "description": "The account login keeps failing",
        "category": "Account",
    },
    {
        "description": "I am unable to sign into my account",
        "category": "Account",
    },
    {
        "description": "Please help me unlock my university account",
        "category": "Account",
    },
    # -----------------------------
    # Network
    # -----------------------------
    {
        "description": "The university WiFi is not connecting",
        "category": "Network",
    },
    {
        "description": "My laptop cannot connect to campus WiFi",
        "category": "Network",
    },
    {
        "description": "The internet connection keeps dropping",
        "category": "Network",
    },
    {
        "description": "I cannot connect to the university network",
        "category": "Network",
    },
    {
        "description": "Campus internet is not working",
        "category": "Network",
    },
    {
        "description": "The WiFi connection keeps failing",
        "category": "Network",
    },
    {
        "description": "My computer has no internet connection",
        "category": "Network",
    },
    {
        "description": "The university network is unavailable",
        "category": "Network",
    },
    {
        "description": "I cannot access the internet on campus",
        "category": "Network",
    },
    {
        "description": "WiFi disconnects every few minutes",
        "category": "Network",
    },
    # -----------------------------
    # Software
    # -----------------------------
    {
        "description": "The university application keeps crashing",
        "category": "Software",
    },
    {
        "description": "The application crashes when I open it",
        "category": "Software",
    },
    {
        "description": "The software is not starting",
        "category": "Software",
    },
    {
        "description": "The application freezes when I use it",
        "category": "Software",
    },
    {
        "description": "The program stopped responding",
        "category": "Software",
    },
    {
        "description": "I cannot open the university application",
        "category": "Software",
    },
    {
        "description": "The software keeps showing an error",
        "category": "Software",
    },
    {
        "description": "The application is not working correctly",
        "category": "Software",
    },
    {
        "description": "The program closes unexpectedly",
        "category": "Software",
    },
    {
        "description": "The university software crashes frequently",
        "category": "Software",
    },
    # -----------------------------
    # Hardware
    # -----------------------------
    {
        "description": "My laptop keyboard is not working",
        "category": "Hardware",
    },
    {
        "description": "The printer is not working",
        "category": "Hardware",
    },
    {
        "description": "The printer in the lab is not responding",
        "category": "Hardware",
    },
    {
        "description": "My laptop battery is not charging",
        "category": "Hardware",
    },
    {
        "description": "My computer mouse is not working",
        "category": "Hardware",
    },
    {
        "description": "The laptop screen is broken",
        "category": "Hardware",
    },
    {
        "description": "My keyboard stopped responding",
        "category": "Hardware",
    },
    {
        "description": "The computer will not turn on",
        "category": "Hardware",
    },
    {
        "description": "The monitor is not displaying anything",
        "category": "Hardware",
    },
    {
        "description": "The university printer cannot print documents",
        "category": "Hardware",
    },
    # -----------------------------
    # Academic System
    # -----------------------------
    {
        "description": "I cannot access the student portal",
        "category": "Academic System",
    },
    {
        "description": "The academic portal is not working",
        "category": "Academic System",
    },
    {
        "description": "I cannot register for my courses",
        "category": "Academic System",
    },
    {
        "description": "My course registration is not working",
        "category": "Academic System",
    },
    {
        "description": "I cannot see my university grades",
        "category": "Academic System",
    },
    {
        "description": "The student portal keeps showing an error",
        "category": "Academic System",
    },
    {
        "description": "I cannot access my academic schedule",
        "category": "Academic System",
    },
    {
        "description": "The university registration system is unavailable",
        "category": "Academic System",
    },
    {
        "description": "My courses are not appearing in the student portal",
        "category": "Academic System",
    },
    {
        "description": "I cannot submit my course registration",
        "category": "Academic System",
    },
]


# ==========================================
# Add Examples to Dataset
# ==========================================

additional_df = pd.DataFrame(additional_data)

data = pd.concat(
    [
        data,
        additional_df,
    ],
    ignore_index=True,
)


# ==========================================
# Text Preprocessing
# ==========================================


def clean_text(text):

    text = str(text).lower()

    text = re.sub(r"[^a-z\s]", "", text)

    text = re.sub(r"\s+", " ", text).strip()

    return text


data["clean_description"] = data["description"].apply(clean_text)


# ==========================================
# Features and Labels
# ==========================================

X = data["clean_description"]

y = data["category"]


# ==========================================
# Dataset Information
# ==========================================

print("Total dataset samples:", len(data))

print("\nSamples per category")
print("--------------------")

print(data["category"].value_counts())


# ==========================================
# Train / Test Split
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)


print("\nTraining samples:", len(X_train))

print("Testing samples:", len(X_test))


# ==========================================
# TF-IDF
# ==========================================

vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    min_df=1,
)


X_train_tfidf = vectorizer.fit_transform(X_train)


X_test_tfidf = vectorizer.transform(X_test)


# ==========================================
# Logistic Regression
# ==========================================

model = LogisticRegression(
    max_iter=2000,
    random_state=42,
)


model.fit(X_train_tfidf, y_train)


# ==========================================
# Predictions
# ==========================================

y_pred = model.predict(X_test_tfidf)


# ==========================================
# Evaluation
# ==========================================

accuracy = accuracy_score(y_test, y_pred)


precision = precision_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0,
)


recall = recall_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0,
)


f1 = f1_score(
    y_test,
    y_pred,
    average="weighted",
    zero_division=0,
)


print("\nModel Evaluation")
print("----------------")

print(f"Accuracy:  {accuracy:.2f}")

print(f"Precision: {precision:.2f}")

print(f"Recall:    {recall:.2f}")

print(f"F1-score:  {f1:.2f}")


# ==========================================
# Confusion Matrix
# ==========================================

print("\nConfusion Matrix")
print("----------------")

print(confusion_matrix(y_test, y_pred))


# ==========================================
# Classification Report
# ==========================================

print("\nClassification Report")
print("---------------------")

print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0,
    )
)


# ==========================================
# Save Model
# ==========================================

os.makedirs("saved_model", exist_ok=True)


joblib.dump(
    {
        "model": model,
        "vectorizer": vectorizer,
    },
    "saved_model/ticket_classifier.joblib",
)


print("\nModel saved successfully.")

print("Saved to: saved_model/ticket_classifier.joblib")
