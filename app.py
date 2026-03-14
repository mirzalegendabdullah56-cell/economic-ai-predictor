import streamlit as st
import joblib

# Page Configuration
st.set_page_config(page_title="Economic AI Predictor", page_icon="📈", layout="centered")

# Custom CSS for styling
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
        font-weight: bold;
        border: none;
    }
    .stButton>button:hover {
        background-color: #ff2b2b;
        border: none;
    }
    .prediction-card {
        padding: 20px;
        border-radius: 15px;
        background-color: #1e2130;
        border-left: 5px solid #ff4b4b;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# Load Models
try:
    model = joblib.load("economic-ai-predictor.pkl")
    vectorizer = joblib.load("tfidf_vectorizer.pkl")
except:
    st.error("Model files not found. Please check filenames on GitHub!")

# Header Section
st.title("📈 Economic AI Predictor")
st.markdown("---")
st.write("Enter a global news headline below to analyze economic sentiment and stability.")

# Input Area
user_input = st.text_input("Enter economic news headline:", placeholder="e.g. Stock markets reach all-time high...")

if st.button("Analyze Economic Impact"):
    if user_input:
        # Prediction Logic
        input_vector = vectorizer.transform([user_input])
        prediction = model.predict(input_vector)[0]
        
        # UI logic for Sentiment and Stability
        # Note: Assuming your model returns 'Unstable'/'Stable' or similar categories
        is_stable = "Stable" in str(prediction)
        
        st.markdown("### Analysis Result")
        
        # Creating Columns for metrics
        col1, col2 = st.columns(2)
        
        with col1:
            sentiment_label = "Negative" if not is_stable else "Positive"
            st.metric(label="Market Sentiment", value=sentiment_label, delta="- Risk" if not is_stable else "+ Growth")
            
        with col2:
            stability_label = "Unstable" if not is_stable else "Stable"
            st.metric(label="Economic Stability", value=stability_label)

        # Colorful Alert Boxes
        if not is_stable:
            st.error(f"⚠️ **Warning:** The system predicts market volatility and **{stability_label}** conditions.")
        else:
            st.success(f"✅ **Positive Outlook:** The system predicts **{stability_label}** economic conditions.")
            
    else:
        st.warning("Please enter some text first!")

# Footer
st.markdown("---")
st.caption("Powered by Machine Learning | The Cinema Freak Production")
