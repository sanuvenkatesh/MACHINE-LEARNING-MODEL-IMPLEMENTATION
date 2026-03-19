"""
-----------------------------------------------
Name            : Sahana V
College         : [Seshadripuram College]
Internship Domain : Python Internship


Description:

This project is developed as part of my internship task.
It demonstrates the implementation of Python-based
solutions using libraries such as scikit-learn, NLTK,
and spaCy for building intelligent applications.

Technologies Used:
- Python
- Machine Learning
- Natural Language Processing
- VS Code
-----------------------------------------------
"""

# Hybrid Spam Email Detection System (ML + Rule Based) with GUI

import pandas as pd
from tkinter import *
from tkinter import messagebox

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB



# Loading of Dataset

url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"

data = pd.read_csv(url, sep='\t', header=None, names=['label','message'])

# Convert labels

data['label'] = data['label'].map({'ham':0, 'spam':1})

X = data['message']
y = data['label']


# Train Machine Learning Model

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

vectorizer = TfidfVectorizer(stop_words='english')

X_train_vec = vectorizer.fit_transform(X_train)

model = MultinomialNB()
model.fit(X_train_vec, y_train)

print("Machine Learning model trained successfully!")



# Rule Based Spam Detection

def rule_based_spam_check(message):

    spam_score = 0
    msg = message.lower()

    spam_keywords = [
        "win", "winner", "prize", "lottery", "free",
        "cash", "bonus", "urgent", "claim", "reward"
    ]

    generic_greetings = [
        "dear customer",
        "dear user",
        "dear winner"
    ]

    # Keyword check
    for word in spam_keywords:
        if word in msg:
            spam_score += 1

    # Greeting check
    for greeting in generic_greetings:
        if greeting in msg:
            spam_score += 1

    # Suspicious link
    if "http" in msg:
        spam_score += 1

    # Too many exclamation marks
    if message.count("!") > 3:
        spam_score += 1

    if spam_score >= 2:
        return "Spam"
    else:
        return "Not Spam"



# Prediction Function

def check_spam():

    msg = text_input.get("1.0", END).strip()

    if msg == "":
        messagebox.showwarning("Warning", "Please enter a message")
        return

    # ML Prediction
    msg_vec = vectorizer.transform([msg])
    ml_prediction = model.predict(msg_vec)

    if ml_prediction[0] == 1:
        ml_result = "Spam"
    else:
        ml_result = "Not Spam"

    # Rule-based Prediction
    rule_result = rule_based_spam_check(msg)

    # Final Decision
    if ml_result == "Spam" or rule_result == "Spam":
        result_label.config(text="Spam Message ❌", fg="red")
    else:
        result_label.config(text="Not Spam Message ✅", fg="green")



# GUI Design

root = Tk()

root.title("Hybrid Spam Detector")
root.geometry("500x420")
root.config(bg="lightblue")


title = Label(
    root,
    text="Hybrid Spam Detection System",
    font=("Arial", 18, "bold"),
    bg="lightblue"
)
title.pack(pady=10)


instruction = Label(
    root,
    text="Enter your message:",
    font=("Arial", 12),
    bg="lightblue"
)
instruction.pack()


text_input = Text(root, height=8, width=50)
text_input.pack(pady=10)


check_button = Button(
    root,
    text="Check Message",
    font=("Arial", 12),
    command=check_spam
)
check_button.pack(pady=5)


result_label = Label(
    root,
    text="",
    font=("Arial", 14, "bold"),
    bg="lightblue"
)
result_label.pack(pady=20)


root.mainloop()