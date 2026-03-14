import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Economic Predictor", layout="wide")
st.title("📊 Global Economic Stability Analyzer")

# --- Load Assets Safely ---
def load_model_assets():
    try:
        # Hum dono options try karenge: joblib aur pickle
        m = joblib.load('economic-ai-predictor.pkl')
        v = joblib.load('tfidf_vectorizer.pkl')
        return m, v
    except:
        import pickle
        with open('economic-ai-predictor.pkl', 'rb') as f:
            m = pickle.load(f)
        with open('tfidf_vectorizer.pkl', 'rb') as f:
            v = pickle.load(f)
        return m, v

try:
    model, vectorizer = load_model_assets()
except Exception as e:
    st.error("⚠️ Model Loading Failed!")
    st.warning("Version mismatch detected. Please re-save your model using 'joblib' on your local PC and upload again.")
    st.stop()

# --- Prediction UI ---
user_input = st.text_area("Input Text (News/Reports):", placeholder="Type here...")

if st.button("Analyze & Predict"):
    if user_input:
        data = vectorizer.transform([user_input])
        prediction = model.predict(data)[0]
        
        try:
            probs = model.predict_proba(data)[0]
        except:
            probs = [0.5, 0.5]

        col1, col2 = st.columns(2)
        with col1:
            if prediction == 0:
                st.success("### STATUS: STABLE ✅")
            else:
                st.error("### STATUS: UNSTABLE ⚠️")
        
        with col2:
            prob_df = pd.DataFrame({'Status': ['Stable', 'Unstable'], 'Score': [probs[0], probs[1]]})
            fig = px.pie(prob_df, values='Score', names='Status', color_discrete_sequence=['#2ecc71', '#e74c3c'])
            st.plotly_chart(fig)
