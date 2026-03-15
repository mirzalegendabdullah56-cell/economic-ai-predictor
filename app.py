import streamlit as st
import joblib
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Eco-Insight AI", layout="wide")
st.title("📊 Global Economic Analyzer & Forecaster")

@st.cache_resource
def load_assets():
    m = joblib.load('economic-ai-predictor.pkl')
    v = joblib.load('tfidf_vectorizer.pkl')
    return m, v

try:
    model, vectorizer = load_assets()
except:
    st.error("Error: Model files not found.")
    st.stop()

user_input = st.text_area("✍️ Enter Economic News:", height=150)

if st.button("Generate Detailed Analysis"):
    if user_input:
        data = vectorizer.transform([user_input])
        prediction = model.predict(data)[0]
        probs = model.predict_proba(data)[0]
        
        # --- Advanced Reasoning Logic ---
        stable_words = ['growth', 'steady', 'increase', 'confidence', 'low', 'rising', 'positive', 'resilient', 'strong', 'stable']
        unstable_words = ['crisis', 'crash', 'inflation', 'risk', 'volatility', 'war', 'tensions', 'drop', 'unstable', 'panic']
        
        found_words = [w for w in user_input.lower().split() if w in stable_words + unstable_words]
        
        st.divider()
        col1, col2 = st.columns([1.2, 1])

        with col1:
            st.subheader("🔍 Prediction Reasoning")
            if prediction == 0:
                st.success("### RESULT: STABLE ✅")
                reason = "The model detected a pattern of economic resilience. "
                if found_words:
                    reason += f"Key terms like **'{', '.join(found_words[:3])}'** suggest a balanced and growing market environment."
                else:
                    reason += "The overall structure of the statement reflects positive market sentiment."
                st.write(f"**Why?** {reason}")
            else:
                st.error("### RESULT: UNSTABLE ⚠️")
                reason = "The model identified indicators of market risk. "
                if found_words:
                    reason += f"Keywords such as **'{', '.join(found_words[:3])}'** are statistically linked to economic volatility."
                else:
                    reason += "The input suggests a lack of stability in the current economic parameters."
                st.write(f"**Why?** {reason}")
            
            # Confidence Chart
            prob_df = pd.DataFrame({'Status': ['Stable', 'Unstable'], 'Confidence (%)': [probs[0]*100, probs[1]*100]})
            fig = px.bar(prob_df, x='Status', y='Confidence (%)', color='Status', 
                         color_discrete_map={'Stable':'#2ecc71', 'Unstable':'#e74c3c'})
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("📈 Upcoming Future Trends")
            if prediction == 0:
                st.info("💡 **Outlook:** High probability of Foreign Direct Investment (FDI) and currency strength.")
            else:
                st.warning("🚨 **Outlook:** Investors may shift to Gold. Potential for interest rate hikes.")

    else:
        st.warning("Kuch text enter karein!")
