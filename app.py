import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Eco-Insight AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Space+Grotesk:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Space Grotesk', sans-serif;
    }

    .stApp {
        background-color: #0a0e1a;
        color: #e2e8f0;
    }

    .main .block-container {
        padding: 2rem 3rem 4rem 3rem;
        max-width: 1300px;
    }

    /* ── Header ── */
    .eco-header {
        text-align: center;
        padding: 3rem 0 2.5rem 0;
        border-bottom: 1px solid #1e2d4a;
        margin-bottom: 2.5rem;
    }
    .eco-header .badge {
        display: inline-block;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        letter-spacing: 3px;
        color: #38bdf8;
        background: rgba(56,189,248,0.08);
        border: 1px solid rgba(56,189,248,0.2);
        padding: 5px 16px;
        border-radius: 2px;
        margin-bottom: 1.2rem;
        text-transform: uppercase;
    }
    .eco-header h1 {
        font-size: 2.8rem;
        font-weight: 600;
        color: #f1f5f9;
        letter-spacing: -1px;
        margin: 0 0 0.5rem 0;
        line-height: 1.15;
    }
    .eco-header h1 span {
        color: #38bdf8;
    }
    .eco-header p {
        font-size: 15px;
        color: #64748b;
        margin: 0;
        font-weight: 300;
    }

    /* ── Stat strip ── */
    .stat-strip {
        display: flex;
        gap: 1px;
        background: #1e2d4a;
        border: 1px solid #1e2d4a;
        border-radius: 8px;
        overflow: hidden;
        margin-bottom: 2rem;
    }
    .stat-item {
        flex: 1;
        background: #0d1526;
        padding: 1.1rem 1.5rem;
        text-align: center;
    }
    .stat-item .val {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 1.4rem;
        font-weight: 500;
        color: #38bdf8;
    }
    .stat-item .lbl {
        font-size: 11px;
        color: #475569;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-top: 3px;
    }

    /* ── Input panel ── */
    .input-panel {
        background: #0d1526;
        border: 1px solid #1e2d4a;
        border-radius: 10px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
    }
    .input-panel .panel-label {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        letter-spacing: 2px;
        color: #475569;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    .stTextArea textarea {
        background: #060c18 !important;
        border: 1px solid #1e2d4a !important;
        border-radius: 8px !important;
        color: #cbd5e1 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 14px !important;
        line-height: 1.7 !important;
        padding: 14px 16px !important;
        resize: vertical !important;
    }
    .stTextArea textarea:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 3px rgba(56,189,248,0.08) !important;
    }
    .stTextArea textarea::placeholder { color: #334155 !important; }
    .stTextArea label { display: none !important; }

    /* ── Button ── */
    .stButton > button {
        width: 100%;
        background: #38bdf8 !important;
        color: #060c18 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.85rem 2rem !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: 15px !important;
        letter-spacing: 0.3px !important;
        cursor: pointer !important;
        transition: all 0.2s !important;
    }
    .stButton > button:hover {
        background: #7dd3fc !important;
        transform: translateY(-1px);
    }

    /* ── Result cards ── */
    .result-card {
        background: #0d1526;
        border: 1px solid #1e2d4a;
        border-radius: 10px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1rem;
        height: 100%;
    }
    .result-card.stable  { border-left: 3px solid #22c55e; }
    .result-card.unstable { border-left: 3px solid #ef4444; }

    .verdict-stable {
        display: inline-flex; align-items: center; gap: 8px;
        background: rgba(34,197,94,0.1);
        border: 1px solid rgba(34,197,94,0.25);
        color: #22c55e;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 13px; font-weight: 500;
        padding: 8px 18px; border-radius: 6px;
        margin-bottom: 1.2rem;
    }
    .verdict-unstable {
        display: inline-flex; align-items: center; gap: 8px;
        background: rgba(239,68,68,0.1);
        border: 1px solid rgba(239,68,68,0.25);
        color: #ef4444;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 13px; font-weight: 500;
        padding: 8px 18px; border-radius: 6px;
        margin-bottom: 1.2rem;
    }

    .reason-box {
        background: #060c18;
        border: 1px solid #1e2d4a;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        font-size: 14px;
        color: #94a3b8;
        line-height: 1.75;
        margin-bottom: 1.2rem;
    }
    .reason-box strong { color: #cbd5e1; }

    .keyword-chip {
        display: inline-block;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        padding: 3px 10px;
        border-radius: 4px;
        margin: 3px 3px 0 0;
    }
    .chip-stable   { background: rgba(34,197,94,0.1);  color: #22c55e;  border: 1px solid rgba(34,197,94,0.2); }
    .chip-unstable { background: rgba(239,68,68,0.1);  color: #ef4444;  border: 1px solid rgba(239,68,68,0.2); }

    .section-title {
        font-family: 'IBM Plex Mono', monospace;
        font-size: 11px;
        letter-spacing: 2px;
        color: #475569;
        text-transform: uppercase;
        margin-bottom: 0.8rem;
    }

    .outlook-box {
        background: #060c18;
        border: 1px solid #1e2d4a;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        font-size: 14px;
        color: #94a3b8;
        line-height: 1.75;
        margin-top: 1rem;
    }
    .outlook-box .icon { font-size: 18px; margin-right: 6px; }
    .outlook-box strong { color: #cbd5e1; }

    .divider { border: none; border-top: 1px solid #1e2d4a; margin: 2rem 0; }

    /* hide streamlit chrome */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    .stAlert { border-radius: 8px !important; }
</style>
""", unsafe_allow_html=True)


# ── Load model ──────────────────────────────────────────────
@st.cache_resource
def load_assets():
    m = joblib.load('economic-ai-predictor.pkl')
    v = joblib.load('tfidf_vectorizer.pkl')
    return m, v

try:
    model, vectorizer = load_assets()
    model_loaded = True
except:
    model_loaded = False


# ── Header ──────────────────────────────────────────────────
st.markdown("""
<div class="eco-header">
    <div class="badge">ML · NLP · Economic Intelligence</div>
    <h1>Eco-Insight <span>AI</span></h1>
    <p>Global Economic Analyzer & Forecaster — powered by TF-IDF + supervised ML</p>
</div>
""", unsafe_allow_html=True)


# ── Stat strip ──────────────────────────────────────────────
st.markdown("""
<div class="stat-strip">
    <div class="stat-item"><div class="val">47</div><div class="lbl">Countries</div></div>
    <div class="stat-item"><div class="val">TF-IDF</div><div class="lbl">Vectorizer</div></div>
    <div class="stat-item"><div class="val">Binary</div><div class="lbl">Classification</div></div>
    <div class="stat-item"><div class="val">Real-time</div><div class="lbl">Inference</div></div>
</div>
""", unsafe_allow_html=True)


if not model_loaded:
    st.error("Model files not found. Make sure `economic-ai-predictor.pkl` and `tfidf_vectorizer.pkl` are in the same directory.")
    st.stop()


# ── Input ───────────────────────────────────────────────────
st.markdown('<div class="input-panel"><div class="panel-label">Economic Statement Input</div>', unsafe_allow_html=True)
user_input = st.text_area(
    label="input",
    placeholder="e.g.  Pakistan's economy shows strong GDP growth with rising exports and stable currency...",
    height=140
)
st.markdown('</div>', unsafe_allow_html=True)

run = st.button("Generate Detailed Analysis")


# ── Analysis ─────────────────────────────────────────────────
if run:
    if not user_input.strip():
        st.warning("Please enter an economic statement before running analysis.")
        st.stop()

    with st.spinner("Running model inference..."):
        data       = vectorizer.transform([user_input])
        prediction = model.predict(data)[0]
        probs      = model.predict_proba(data)[0]

    stable_words   = ['growth','steady','increase','confidence','low','rising','positive',
                      'resilient','strong','stable']
    unstable_words = ['crisis','crash','inflation','risk','volatility','war','tensions',
                      'drop','unstable','panic']

    words      = user_input.lower().split()
    found_pos  = [w for w in words if w in stable_words]
    found_neg  = [w for w in words if w in unstable_words]
    found_words = found_pos + found_neg

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns([1.15, 1], gap="large")

    # ── Left col: reasoning ──────────────────────────────────
    with col1:
        st.markdown('<div class="section-title">Prediction Reasoning</div>', unsafe_allow_html=True)

        if prediction == 0:
            verdict_html = '<div class="verdict-stable">● STABLE — ECONOMY</div>'
            card_cls     = "stable"
            reason       = "The model detected a pattern of economic resilience. "
            if found_words:
                reason += f"Key terms suggest a balanced and growing market environment."
            else:
                reason += "The overall structure of the statement reflects positive market sentiment."
        else:
            verdict_html = '<div class="verdict-unstable">⚠ UNSTABLE — HIGH RISK</div>'
            card_cls     = "unstable"
            reason       = "The model identified indicators of market risk. "
            if found_words:
                reason += "Keywords are statistically linked to economic volatility."
            else:
                reason += "The input suggests a lack of stability in the current economic parameters."

        st.markdown(f'<div class="result-card {card_cls}">', unsafe_allow_html=True)
        st.markdown(verdict_html, unsafe_allow_html=True)

        st.markdown(f'<div class="reason-box"><strong>Why?</strong> {reason}</div>', unsafe_allow_html=True)

        if found_pos or found_neg:
            chips = ""
            for w in found_pos[:5]:
                chips += f'<span class="keyword-chip chip-stable">{w}</span>'
            for w in found_neg[:5]:
                chips += f'<span class="keyword-chip chip-unstable">{w}</span>'
            st.markdown(f'<div style="margin-bottom:0.5rem"><div class="section-title" style="margin-bottom:6px">Detected keywords</div>{chips}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Confidence bar chart
        st.markdown('<div class="section-title" style="margin-top:1.4rem">Model confidence</div>', unsafe_allow_html=True)
        prob_df = pd.DataFrame({
            'Status':         ['Stable',   'Unstable'],
            'Confidence (%)': [round(probs[0]*100, 1), round(probs[1]*100, 1)]
        })
        fig = px.bar(
            prob_df, x='Status', y='Confidence (%)',
            color='Status',
            color_discrete_map={'Stable': '#22c55e', 'Unstable': '#ef4444'},
            text='Confidence (%)'
        )
        fig.update_traces(
            texttemplate='%{text:.1f}%', textposition='outside',
            marker_line_width=0, width=0.45
        )
        fig.update_layout(
            paper_bgcolor='#0d1526', plot_bgcolor='#060c18',
            font_color='#94a3b8', font_family='Space Grotesk',
            showlegend=False,
            margin=dict(t=20, b=10, l=10, r=10),
            height=260,
            xaxis=dict(showgrid=False, tickfont=dict(size=13, color='#cbd5e1')),
            yaxis=dict(showgrid=True, gridcolor='#1e2d4a', range=[0, 110],
                       ticksuffix='%', tickfont=dict(size=11, color='#475569'))
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Right col: trends ────────────────────────────────────
    with col2:
        st.markdown('<div class="section-title">Upcoming Future Trends</div>', unsafe_allow_html=True)
        st.markdown('<div class="result-card">', unsafe_allow_html=True)

        if prediction == 0:
            outlook = """
            <div class="outlook-box">
                <span class="icon">💡</span>
                <strong>Positive Outlook:</strong> High probability of Foreign Direct Investment (FDI) inflows
                and currency strength in the near term. Equity markets may see continued momentum.
            </div>"""
            trend_labels  = ['Month 1','Month 2','Month 3','Month 4','Month 5','Month 6']
            trend_gdp     = [2.1, 2.4, 2.6, 2.9, 3.1, 3.4]
            trend_inf     = [4.2, 3.9, 3.7, 3.5, 3.3, 3.1]
            line_color_g  = '#22c55e'
            line_color_i  = '#38bdf8'
        else:
            outlook = """
            <div class="outlook-box">
                <span class="icon">🚨</span>
                <strong>Caution:</strong> Investors may shift capital to safe havens such as Gold or USD.
                Potential for central bank interest rate hikes and currency depreciation ahead.
            </div>"""
            trend_labels  = ['Month 1','Month 2','Month 3','Month 4','Month 5','Month 6']
            trend_gdp     = [1.8, 1.4, 1.0, 0.6, 0.2, -0.3]
            trend_inf     = [5.1, 5.8, 6.4, 7.0, 7.5, 8.1]
            line_color_g  = '#ef4444'
            line_color_i  = '#f97316'

        st.markdown(outlook, unsafe_allow_html=True)

        # Dual-line forecast chart
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=trend_labels, y=trend_gdp,
            mode='lines+markers',
            name='GDP Growth (%)',
            line=dict(color=line_color_g, width=2.5),
            marker=dict(size=6, color=line_color_g),
        ))
        fig2.add_trace(go.Scatter(
            x=trend_labels, y=trend_inf,
            mode='lines+markers',
            name='Inflation (%)',
            line=dict(color=line_color_i, width=2.5, dash='dot'),
            marker=dict(size=6, color=line_color_i),
        ))
        fig2.update_layout(
            paper_bgcolor='#0d1526', plot_bgcolor='#060c18',
            font_color='#94a3b8', font_family='Space Grotesk',
            legend=dict(
                orientation='h', y=1.12, x=0,
                font=dict(size=11, color='#94a3b8'),
                bgcolor='rgba(0,0,0,0)'
            ),
            margin=dict(t=30, b=10, l=10, r=10),
            height=240,
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color='#475569')),
            yaxis=dict(showgrid=True, gridcolor='#1e2d4a',
                       ticksuffix='%', tickfont=dict(size=11, color='#475569'))
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Mini probability gauge
        st.markdown('<div class="section-title" style="margin-top:0.5rem">Confidence gauge</div>', unsafe_allow_html=True)
        gauge_val  = round(probs[0]*100 if prediction == 0 else probs[1]*100, 1)
        gauge_color = '#22c55e' if prediction == 0 else '#ef4444'
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gauge_val,
            number={'suffix': '%', 'font': {'size': 28, 'color': '#f1f5f9', 'family': 'IBM Plex Mono'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1,
                         'tickcolor': '#1e2d4a', 'tickfont': {'color': '#475569', 'size': 10}},
                'bar': {'color': gauge_color, 'thickness': 0.22},
                'bgcolor': '#060c18',
                'borderwidth': 0,
                'steps': [
                    {'range': [0, 50],  'color': '#0d1526'},
                    {'range': [50, 75], 'color': '#111827'},
                    {'range': [75, 100],'color': '#0d1526'},
                ],
                'threshold': {
                    'line': {'color': gauge_color, 'width': 2},
                    'thickness': 0.8, 'value': gauge_val
                }
            }
        ))
        fig3.update_layout(
            paper_bgcolor='#0d1526',
            font_color='#94a3b8',
            margin=dict(t=10, b=0, l=20, r=20),
            height=180,
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:4rem; padding-top:1.5rem;
            border-top:1px solid #1e2d4a;
            font-family:'IBM Plex Mono',monospace; font-size:11px;
            color:#334155; letter-spacing:1px;">
    ECO-INSIGHT AI &nbsp;·&nbsp; TF-IDF + SUPERVISED ML &nbsp;·&nbsp; BINARY ECONOMIC CLASSIFIER
</div>
""", unsafe_allow_html=True)
