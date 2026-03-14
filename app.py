import streamlit as st
import joblib

# Load model and vectorizer
model = joblib.load("economic-ai-predictor.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

st.title("Economic AI Predictor")

headline = st.text_input("Enter economic news headline:")

if st.button("Predict Sentiment and Stability"):
    vec = vectorizer.transform([headline])
    sentiment = model.predict(vec)[0]
    stability = "Stable" if sentiment in ["Positive", "Neutral"] else "Unstable"
    
    st.write(f"Sentiment: {sentiment}")
    st.write(f"Predicted Economic Stability: {stability}")
