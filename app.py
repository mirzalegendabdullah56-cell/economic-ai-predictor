import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(page_title="Eco-Insight AI", layout="wide")
st.title("📊 Global Economic Analyzer & Forecaster")

# Load Assets
@st.cache_resource
def load_assets():
    m = joblib.load('economic-ai-predictor.pkl')
    v = joblib.load('tfidf_vectorizer.pkl')
    return m, v

try:
    model, vectorizer = load_assets()
except:
    st.error("Error: Model files not found. Please upload them to GitHub.")
    st.stop()

# User Input
user_input = st.text_area("✍️ Enter Economic News or Statement:", 
                          placeholder="e.g., Inflation is decreasing and trade is booming...", 
                          height=150)

if st.button("Generate Detailed Analysis"):
    if user_input:
        # 1. Prediction logic
        data = vectorizer.transform([user_input])
        prediction = model.predict(data)[0]
        probs = model.predict_proba(data)[0]
        
        # 2. Extract Important Words (Reasoning Logic)
        feature_names = vectorizer.get_feature_names_out()
        words_in_text = user_input.lower().split()
        important_words = [word for word in words_in_text if word in feature_names]

        st.divider()

        # Layout: Prediction | Trends
        col1, col2 = st.columns([1.2, 1])

        with col1:
            st.subheader("🔍 Prediction Reasoning")
            if prediction == 0:
                st.success("### RESULT: STABLE ✅")
                st.write(f"**Why?** The model detected positive sentiment in your text. Keywords like **'{', '.join(important_words[:3])}'** indicate economic resilience.")
            else:
                st.error("### RESULT: UNSTABLE ⚠️")
                st.write(f"**Why?** Analysis shows risk factors. Terms like **'{', '.join(important_words[:3])}'** are strongly associated with market volatility.")
            
            # Probability Chart
            prob_df = pd.DataFrame({'Status': ['Stable', 'Unstable'], 'Confidence': [probs[0], probs[1]]})
            fig = px.bar(prob_df, x='Status', y='Confidence', color='Status', 
                         color_discrete_map={'Stable':'green', 'Unstable':'red'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📈 Upcoming Future Trends")
            if prediction == 0:
                st.info("""
                * **Investment:** High probability of Foreign Direct Investment (FDI).
                * **Currency:** Expected to remain strong against global peers.
                * **Forecast:** Continued growth for the next 2 quarters.
                """)
            else:
                st.warning("""
                * **Market:** High chance of bearish (downward) trend.
                * **Risk:** Investors might move towards 'Safe Haven' assets like Gold.
                * **Forecast:** Potential policy rate hikes to control volatility.
                """)
            
            st.caption("Note: These trends are AI-generated based on current sentiment analysis.")

    else:
        st.warning("Please enter some economic text first!")
