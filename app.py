import streamlit as st
import pickle
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Economic Predictor", layout="wide")

st.title("📊 Global Economic Stability Analyzer")

# --- Load Models ---
try:
    with open('economic-ai-predictor.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)
except Exception as e:
    st.error("⚠️ Model Loading Error!")
    st.info("Aapka model file version match nahi kar raha. Try deleting the model from GitHub and re-uploading it.")
    st.stop() # App ko yahan rok do agar model load na ho

# --- UI Setup ---
user_input = st.text_area("Input Text (News/Reports):", placeholder="Enter economic news here...")

if st.button("Analyze & Predict"):
    if user_input:
        data = vectorizer.transform([user_input])
        prediction = model.predict(data)[0]
        
        try:
            probs = model.predict_proba(data)[0]
        except:
            probs = [0.5, 0.5]

        col1, col2 = st.columns([1, 1])
        with col1:
            st.subheader("Final Prediction")
            if prediction == 0: 
                st.success("### STATUS: STABLE ✅")
            else:
                st.error("### STATUS: UNSTABLE ⚠️")

        with col2:
            st.subheader("Confidence Score")
            prob_df = pd.DataFrame({'Status': ['Stable', 'Unstable'], 'Score': [probs[0], probs[1]]})
            fig = px.pie(prob_df, values='Score', names='Status', color='Status', 
                         color_discrete_map={'Stable':'#2ecc71', 'Unstable':'#e74c3c'})
            st.plotly_chart(fig, use_container_width=True)
