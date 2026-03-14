import streamlit as st
import pickle
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Economic Predictor", layout="wide")

# --- 1. Load Models Safely ---
# Ensure these filenames match EXACTLY with your GitHub files
MODEL_PATH = 'economic-ai-predictor.pkl'
VECTORIZER_PATH = 'tfidf_vectorizer.pkl'

@st.cache_resource
def load_assets():
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    with open(VECTORIZER_PATH, 'rb') as f:
        vectorizer = pickle.load(f)
    return model, vectorizer

# Load them once
model, vectorizer = load_assets()

# --- 2. UI Setup ---
st.title("📊 Global Economic Stability Analyzer")
st.write("Analyze market sentiment and predict stability using AI.")

user_input = st.text_area("Input Text (News/Reports):", 
                          placeholder="Enter economic news here...",
                          height=150)

if st.button("Analyze & Predict"):
    if user_input:
        # Step 1: Transform
        data = vectorizer.transform([user_input])
        
        # Step 2: Predict
        prediction = model.predict(data)[0]
        
        # Step 3: Get Probabilities for the Graph
        try:
            probs = model.predict_proba(data)[0]
        except:
            # Fallback agar model probability support nahi karta
            probs = [0.5, 0.5] if prediction == 1 else [0.5, 0.5]

        # --- 3. Display Results ---
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Final Prediction")
            # Yahan check karein: 0 Stable hai ya 1? 
            # Agar output ulta aye to 0 aur 1 ko swap kar dein niche
            if prediction == 0: 
                st.success("### STATUS: STABLE ✅")
                st.write("Model interpretation: The economy shows signs of resilience.")
            else:
                st.error("### STATUS: UNSTABLE ⚠️")
                st.write("Model interpretation: High risk or volatility detected.")

        with col2:
            st.subheader("Confidence Score")
            prob_df = pd.DataFrame({
                'Status': ['Stable', 'Unstable'],
                'Score': [probs[0], probs[1]]
            })
            fig = px.pie(prob_df, values='Score', names='Status', 
                         color='Status', 
                         color_discrete_map={'Stable':'#2ecc71', 'Unstable':'#e74c3c'})
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Please enter some text to analyze.")
