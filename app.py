import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import json
import re

st.set_page_config(
    page_title="Eco-Insight AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Space+Grotesk:wght@300;400;500;600&display=swap');

    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }
    .stApp { background-color: #0a0e1a; color: #e2e8f0; }
    .main .block-container { padding: 2rem 3rem 4rem 3rem; max-width: 1300px; }

    .eco-header {
        text-align: center; padding: 3rem 0 2.5rem 0;
        border-bottom: 1px solid #1e2d4a; margin-bottom: 2.5rem;
    }
    .eco-header .badge {
        display: inline-block; font-family: 'IBM Plex Mono', monospace;
        font-size: 11px; letter-spacing: 3px; color: #38bdf8;
        background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.2);
        padding: 5px 16px; border-radius: 2px; margin-bottom: 1.2rem; text-transform: uppercase;
    }
    .eco-header h1 { font-size: 2.8rem; font-weight: 600; color: #f1f5f9; letter-spacing: -1px; margin: 0 0 0.5rem 0; }
    .eco-header h1 span { color: #38bdf8; }
    .eco-header p { font-size: 15px; color: #64748b; margin: 0; font-weight: 300; }

    .stat-strip {
        display: flex; gap: 1px; background: #1e2d4a;
        border: 1px solid #1e2d4a; border-radius: 8px; overflow: hidden; margin-bottom: 2rem;
    }
    .stat-item { flex: 1; background: #0d1526; padding: 1.1rem 1.5rem; text-align: center; }
    .stat-item .val { font-family: 'IBM Plex Mono', monospace; font-size: 1.4rem; font-weight: 500; color: #38bdf8; }
    .stat-item .lbl { font-size: 11px; color: #475569; letter-spacing: 1px; text-transform: uppercase; margin-top: 3px; }

    .input-panel { background: #0d1526; border: 1px solid #1e2d4a; border-radius: 10px; padding: 1.8rem 2rem; margin-bottom: 1.5rem; }
    .input-panel .panel-label { font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 2px; color: #475569; text-transform: uppercase; margin-bottom: 0.8rem; }

    .stTextArea textarea {
        background: #060c18 !important; border: 1px solid #1e2d4a !important;
        border-radius: 8px !important; color: #cbd5e1 !important;
        font-family: 'Space Grotesk', sans-serif !important; font-size: 14px !important;
        line-height: 1.7 !important; padding: 14px 16px !important; resize: vertical !important;
    }
    .stTextArea textarea:focus { border-color: #38bdf8 !important; box-shadow: 0 0 0 3px rgba(56,189,248,0.08) !important; }
    .stTextArea textarea::placeholder { color: #334155 !important; }
    .stTextArea label { display: none !important; }

    .stTextInput input {
        background: #060c18 !important; border: 1px solid #1e2d4a !important;
        border-radius: 8px !important; color: #cbd5e1 !important;
        font-family: 'IBM Plex Mono', monospace !important; font-size: 13px !important;
        padding: 10px 14px !important;
    }
    .stTextInput input:focus { border-color: #38bdf8 !important; }
    .stTextInput label { font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; letter-spacing: 2px; color: #475569 !important; text-transform: uppercase; }

    .stButton > button {
        width: 100%; background: #38bdf8 !important; color: #060c18 !important;
        border: none !important; border-radius: 8px !important; padding: 0.85rem 2rem !important;
        font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important;
        font-size: 15px !important; letter-spacing: 0.3px !important;
    }
    .stButton > button:hover { background: #7dd3fc !important; transform: translateY(-1px); }

    .result-card { background: #0d1526; border: 1px solid #1e2d4a; border-radius: 10px; padding: 1.6rem 1.8rem; margin-bottom: 1rem; height: 100%; }
    .result-card.stable  { border-left: 3px solid #22c55e; }
    .result-card.unstable { border-left: 3px solid #ef4444; }
    .result-card.moderate { border-left: 3px solid #f59e0b; }

    .verdict-stable { display: inline-flex; align-items: center; gap: 8px; background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.25); color: #22c55e; font-family: 'IBM Plex Mono', monospace; font-size: 13px; font-weight: 500; padding: 8px 18px; border-radius: 6px; margin-bottom: 1.2rem; }
    .verdict-unstable { display: inline-flex; align-items: center; gap: 8px; background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.25); color: #ef4444; font-family: 'IBM Plex Mono', monospace; font-size: 13px; font-weight: 500; padding: 8px 18px; border-radius: 6px; margin-bottom: 1.2rem; }
    .verdict-moderate { display: inline-flex; align-items: center; gap: 8px; background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.25); color: #f59e0b; font-family: 'IBM Plex Mono', monospace; font-size: 13px; font-weight: 500; padding: 8px 18px; border-radius: 6px; margin-bottom: 1.2rem; }

    .reason-box { background: #060c18; border: 1px solid #1e2d4a; border-radius: 8px; padding: 1rem 1.2rem; font-size: 14px; color: #94a3b8; line-height: 1.75; margin-bottom: 1.2rem; }
    .reason-box strong { color: #cbd5e1; }

    .keyword-chip { display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: 11px; padding: 3px 10px; border-radius: 4px; margin: 3px 3px 0 0; }
    .chip-stable   { background: rgba(34,197,94,0.1);  color: #22c55e;  border: 1px solid rgba(34,197,94,0.2); }
    .chip-unstable { background: rgba(239,68,68,0.1);  color: #ef4444;  border: 1px solid rgba(239,68,68,0.2); }
    .chip-neutral  { background: rgba(245,158,11,0.1); color: #f59e0b;  border: 1px solid rgba(245,158,11,0.2); }

    .section-title { font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 2px; color: #475569; text-transform: uppercase; margin-bottom: 0.8rem; }

    .outlook-box { background: #060c18; border: 1px solid #1e2d4a; border-radius: 8px; padding: 1rem 1.2rem; font-size: 14px; color: #94a3b8; line-height: 1.75; margin-top: 1rem; }
    .outlook-box .icon { font-size: 18px; margin-right: 6px; }
    .outlook-box strong { color: #cbd5e1; }

    .divider { border: none; border-top: 1px solid #1e2d4a; margin: 2rem 0; }
    .api-info { background: rgba(56,189,248,0.05); border: 1px solid rgba(56,189,248,0.15); border-radius: 8px; padding: 0.8rem 1.2rem; font-size: 12px; color: #475569; font-family: 'IBM Plex Mono', monospace; margin-bottom: 1rem; }

    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Claude API call ──────────────────────────────────────────
def analyze_with_claude(text: str, api_key: str) -> dict:
    """
    Calls Claude claude-sonnet-4-20250514 with a structured prompt.
    Returns a dict with keys: verdict, confidence, reason, keywords_pos, keywords_neg, outlook, risk_score
    """
    system_prompt = """You are a world-class macroeconomic analyst with expertise in global financial markets, sovereign debt, currency dynamics, inflation, and geopolitical risk.

Your task: analyze the economic statement provided and classify it as STABLE, UNSTABLE, or MODERATE_RISK.

DEFINITIONS:
- STABLE: Economy shows growth, low inflation, fiscal discipline, employment gains, strong exports, currency stability, investor confidence, credit rating upgrades.
- UNSTABLE: Economy shows recession, hyperinflation, currency collapse, debt default, banking crisis, capital flight, political turmoil affecting economy, sanctions, war impact, IMF bailout distress.
- MODERATE_RISK: Mixed signals, some positive + some negative indicators, uncertainty but not crisis.

CRITICAL RULES:
1. Read the ACTUAL CONTENT of the statement — do not default to STABLE.
2. Words like "crisis", "crash", "collapse", "hyperinflation", "default", "war", "sanctions", "recession", "debt crisis" ALWAYS indicate UNSTABLE.
3. Be a strict analyst, not an optimist. If there are clear risk signals, classify accordingly.
4. Confidence should reflect how clearly the statement signals the verdict.

Respond ONLY with a valid JSON object, no markdown, no explanation outside JSON:
{
  "verdict": "STABLE" | "UNSTABLE" | "MODERATE_RISK",
  "confidence": <integer 60-99>,
  "risk_score": <integer 0-100, where 0=perfectly stable, 100=complete collapse>,
  "reason": "<2-3 sentences explaining WHY based on specific terms in the input>",
  "keywords_positive": ["<word1>", "<word2>"],
  "keywords_negative": ["<word1>", "<word2>"],
  "outlook_6m": "<one sentence forecast for next 6 months>",
  "gdp_trend": [<6 floats, monthly GDP growth % forecast>],
  "inflation_trend": [<6 floats, monthly inflation % forecast>]
}"""

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1000,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": f"Analyze this economic statement:\n\n{text}"}
        ]
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }

    resp = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    raw = resp.json()["content"][0]["text"].strip()

    # Strip markdown fences if present
    raw = re.sub(r"```json|```", "", raw).strip()
    return json.loads(raw)


# ── Header ──────────────────────────────────────────────────
st.markdown("""
<div class="eco-header">
    <div class="badge">Claude AI · Semantic NLP · Economic Intelligence</div>
    <h1>Eco-Insight <span>AI</span></h1>
    <p>Global Economic Analyzer & Forecaster — powered by Claude claude-sonnet-4-20250514 LLM</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stat-strip">
    <div class="stat-item"><div class="val">190+</div><div class="lbl">Countries</div></div>
    <div class="stat-item"><div class="val">Claude</div><div class="lbl">AI Engine</div></div>
    <div class="stat-item"><div class="val">3-Class</div><div class="lbl">Classification</div></div>
    <div class="stat-item"><div class="val">Real-time</div><div class="lbl">Inference</div></div>
</div>
""", unsafe_allow_html=True)

# ── API Key input ────────────────────────────────────────────
st.markdown('<div class="input-panel"><div class="panel-label">Anthropic API Key</div>', unsafe_allow_html=True)
api_key = st.text_input(
    label="API KEY",
    type="password",
    placeholder="sk-ant-api03-..."
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="api-info">🔒 Key is never stored. Get yours at console.anthropic.com — free tier available.</div>', unsafe_allow_html=True)

# ── Text input ───────────────────────────────────────────────
st.markdown('<div class="input-panel"><div class="panel-label">Economic Statement Input</div>', unsafe_allow_html=True)
user_input = st.text_area(
    label="input",
    placeholder="e.g. Pakistan is facing a severe debt crisis with inflation at 38%, currency collapse and IMF bailout talks failing...",
    height=140
)
st.markdown('</div>', unsafe_allow_html=True)

run = st.button("🔍 Generate Detailed Analysis")


# ── Analysis ─────────────────────────────────────────────────
if run:
    if not api_key.strip():
        st.error("Please enter your Anthropic API key above.")
        st.stop()
    if not user_input.strip():
        st.warning("Please enter an economic statement.")
        st.stop()

    with st.spinner("Analyzing with Claude AI..."):
        try:
            result = analyze_with_claude(user_input.strip(), api_key.strip())
        except requests.exceptions.HTTPError as e:
            st.error(f"API Error: {e.response.status_code} — {e.response.text[:300]}")
            st.stop()
        except json.JSONDecodeError as e:
            st.error(f"Failed to parse Claude response as JSON: {e}")
            st.stop()
        except Exception as e:
            st.error(f"Unexpected error: {e}")
            st.stop()

    verdict     = result.get("verdict", "MODERATE_RISK")
    confidence  = result.get("confidence", 70)
    risk_score  = result.get("risk_score", 50)
    reason      = result.get("reason", "")
    kw_pos      = result.get("keywords_positive", [])
    kw_neg      = result.get("keywords_negative", [])
    outlook     = result.get("outlook_6m", "")
    gdp_trend   = result.get("gdp_trend",   [1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
    inf_trend   = result.get("inflation_trend", [4.0, 3.8, 3.6, 3.4, 3.2, 3.0])

    # Determine colors / classes
    if verdict == "STABLE":
        card_cls     = "stable"
        verdict_html = '<div class="verdict-stable">● STABLE — ECONOMY</div>'
        line_color_g = '#22c55e'
        line_color_i = '#38bdf8'
        outlook_icon = "💡"
        gauge_color  = '#22c55e'
    elif verdict == "UNSTABLE":
        card_cls     = "unstable"
        verdict_html = '<div class="verdict-unstable">⚠ UNSTABLE — HIGH RISK</div>'
        line_color_g = '#ef4444'
        line_color_i = '#f97316'
        outlook_icon = "🚨"
        gauge_color  = '#ef4444'
    else:
        card_cls     = "moderate"
        verdict_html = '<div class="verdict-moderate">◈ MODERATE RISK</div>'
        line_color_g = '#f59e0b'
        line_color_i = '#fb923c'
        outlook_icon = "⚡"
        gauge_color  = '#f59e0b'

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    col1, col2 = st.columns([1.15, 1], gap="large")

    # ── Left col ─────────────────────────────────────────────
    with col1:
        st.markdown('<div class="section-title">Prediction Reasoning</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="result-card {card_cls}">', unsafe_allow_html=True)
        st.markdown(verdict_html, unsafe_allow_html=True)
        st.markdown(f'<div class="reason-box"><strong>Why?</strong> {reason}</div>', unsafe_allow_html=True)

        chips = ""
        for w in kw_pos[:5]:
            chips += f'<span class="keyword-chip chip-stable">{w}</span>'
        for w in kw_neg[:5]:
            chips += f'<span class="keyword-chip chip-unstable">{w}</span>'
        if chips:
            st.markdown(f'<div style="margin-bottom:0.5rem"><div class="section-title" style="margin-bottom:6px">Detected Keywords</div>{chips}</div>', unsafe_allow_html=True)

        # Risk score bar
        st.markdown(f'<div class="section-title" style="margin-top:1rem">Risk Score: {risk_score}/100</div>', unsafe_allow_html=True)
        risk_color = '#22c55e' if risk_score < 35 else ('#f59e0b' if risk_score < 65 else '#ef4444')
        st.markdown(f"""
        <div style="background:#060c18;border-radius:6px;height:10px;overflow:hidden;margin-bottom:1rem;">
            <div style="width:{risk_score}%;height:100%;background:{risk_color};border-radius:6px;transition:width 1s;"></div>
        </div>""", unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Confidence bar chart
        st.markdown('<div class="section-title" style="margin-top:1.4rem">Model Confidence</div>', unsafe_allow_html=True)
        remaining = 100 - confidence
        if verdict == "STABLE":
            conf_labels = ['Stable', 'Unstable']
            conf_vals   = [confidence, remaining]
            conf_colors = {'Stable': '#22c55e', 'Unstable': '#ef4444'}
        elif verdict == "UNSTABLE":
            conf_labels = ['Unstable', 'Stable']
            conf_vals   = [confidence, remaining]
            conf_colors = {'Unstable': '#ef4444', 'Stable': '#22c55e'}
        else:
            conf_labels = ['Moderate', 'Stable']
            conf_vals   = [confidence, remaining]
            conf_colors = {'Moderate': '#f59e0b', 'Stable': '#22c55e'}

        prob_df = pd.DataFrame({'Status': conf_labels, 'Confidence (%)': conf_vals})
        fig = px.bar(
            prob_df, x='Status', y='Confidence (%)',
            color='Status', color_discrete_map=conf_colors,
            text='Confidence (%)'
        )
        fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside', marker_line_width=0, width=0.45)
        fig.update_layout(
            paper_bgcolor='#0d1526', plot_bgcolor='#060c18',
            font_color='#94a3b8', font_family='Space Grotesk',
            showlegend=False, margin=dict(t=20, b=10, l=10, r=10), height=260,
            xaxis=dict(showgrid=False, tickfont=dict(size=13, color='#cbd5e1')),
            yaxis=dict(showgrid=True, gridcolor='#1e2d4a', range=[0, 115],
                       ticksuffix='%', tickfont=dict(size=11, color='#475569'))
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Right col ────────────────────────────────────────────
    with col2:
        st.markdown('<div class="section-title">6-Month Economic Forecast</div>', unsafe_allow_html=True)
        st.markdown('<div class="result-card">', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="outlook-box">
            <span class="icon">{outlook_icon}</span>
            <strong>Outlook:</strong> {outlook}
        </div>""", unsafe_allow_html=True)

        month_labels = ['M+1', 'M+2', 'M+3', 'M+4', 'M+5', 'M+6']
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(
            x=month_labels, y=gdp_trend,
            mode='lines+markers', name='GDP Growth (%)',
            line=dict(color=line_color_g, width=2.5),
            marker=dict(size=6, color=line_color_g),
        ))
        fig2.add_trace(go.Scatter(
            x=month_labels, y=inf_trend,
            mode='lines+markers', name='Inflation (%)',
            line=dict(color=line_color_i, width=2.5, dash='dot'),
            marker=dict(size=6, color=line_color_i),
        ))
        fig2.update_layout(
            paper_bgcolor='#0d1526', plot_bgcolor='#060c18',
            font_color='#94a3b8', font_family='Space Grotesk',
            legend=dict(orientation='h', y=1.12, x=0, font=dict(size=11, color='#94a3b8'), bgcolor='rgba(0,0,0,0)'),
            margin=dict(t=30, b=10, l=10, r=10), height=240,
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color='#475569')),
            yaxis=dict(showgrid=True, gridcolor='#1e2d4a', ticksuffix='%', tickfont=dict(size=11, color='#475569'))
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Gauge
        st.markdown('<div class="section-title" style="margin-top:0.5rem">Confidence Gauge</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=confidence,
            number={'suffix': '%', 'font': {'size': 28, 'color': '#f1f5f9', 'family': 'IBM Plex Mono'}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#1e2d4a', 'tickfont': {'color': '#475569', 'size': 10}},
                'bar': {'color': gauge_color, 'thickness': 0.22},
                'bgcolor': '#060c18', 'borderwidth': 0,
                'steps': [
                    {'range': [0, 50],  'color': '#0d1526'},
                    {'range': [50, 75], 'color': '#111827'},
                    {'range': [75, 100],'color': '#0d1526'},
                ],
                'threshold': {'line': {'color': gauge_color, 'width': 2}, 'thickness': 0.8, 'value': confidence}
            }
        ))
        fig3.update_layout(
            paper_bgcolor='#0d1526', font_color='#94a3b8',
            margin=dict(t=10, b=0, l=20, r=20), height=180,
        )
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; margin-top:4rem; padding-top:1.5rem;
            border-top:1px solid #1e2d4a;
            font-family:'IBM Plex Mono',monospace; font-size:11px;
            color:#334155; letter-spacing:1px;">
    ECO-INSIGHT AI &nbsp;·&nbsp; POWERED BY CLAUDE claude-sonnet-4-20250514 &nbsp;·&nbsp; SEMANTIC ECONOMIC CLASSIFIER
</div>
""", unsafe_allow_html=True)
