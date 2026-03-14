import streamlit as st
import pickle
import pandas as pd
import plotly.express as px # Charts ke liye

# 1. Load Models
try:
    model = pickle.load(open('economic-ai-predictor.pkl', 'rb'))
    vectorizer = pickle.load(open('tfidf_vectorizer.pkl', 'rb'))
except Exception as e:
    st.error(f"Error loading models: {e}")

st.set_page_config(page_title="Economic Predictor", layout="wide")

st.title("📊 Global Economic Stability Analyzer")
st.markdown("Enter economic news or indicators to analyze market sentiment and stability.")

# Sidebar for extra info
st.sidebar.header("About Model")
st.sidebar.write("This model uses NLP and Machine Learning to predict economic shifts.")

user_input = st.text_area("Input Text (News/Reports):", placeholder="e.g., Inflation rates are rising and stock market is volatile...")

if st.button("Analyze & Predict"):
    if user_input:
        # Transform & Predict
        data = vectorizer.transform([user_input])
        prediction = model.predict(data)[0]
        
        # Confidence Score (Probability)
        try:
            probs = model.predict_proba(data)[0]
        except:
            probs = [0.5, 0.5] # Fallback agar model proba support na kare

        # UI Layout with Columns
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Final Prediction")
            if prediction == 0: # Check your label mapping (0 or 1)
                st.success("### STATUS: STABLE ✅")
                st.write("The model detects positive economic indicators.")
            else:
                st.error("### STATUS: UNSTABLE ⚠️")
                st.write("Alert: Signs of volatility or risk detected.")

        with col2:
            st.subheader("Confidence Analysis")
            # Creating a Pie Chart for Probability
            prob_df = pd.DataFrame({
                'Status': ['Stable', 'Unstable'],
                'Confidence': [probs[0], probs[1]]
            })
            fig = px.pie(prob_df, values='Confidence', names='Status', 
                         color='Status', color_discrete_map={'Stable':'green', 'Unstable':'red'})
            st.plotly_chart(fig, use_container_width=True)

        # Bar Chart for better visualization
        st.subheader("Statistical Probability")
        st.bar_chart(prob_df.set_index('Status'))

    else:
        st.warning("Please enter some text for analysis.")
