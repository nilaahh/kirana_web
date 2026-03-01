import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("chatbot_data.csv")

data.dropna(inplace=True)

# Optional: remove completely blank strings
data = data[data["text"].str.strip() != ""]
data = data[data["intent"].str.strip() != ""]

# Extract features and labels
X = data["text"]
y = data["intent"]

# Convert text to vectors
vectorizer = TfidfVectorizer()
X_vectorized = vectorizer.fit_transform(X)

# Train classifier
model = LogisticRegression()
model.fit(X_vectorized, y)

# Save model + vectorizer
pickle.dump(model, open("intent_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Model trained and saved successfully.")
