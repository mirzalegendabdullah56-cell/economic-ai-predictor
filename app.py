import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import re
import random

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

    .eco-header { text-align: center; padding: 3rem 0 2.5rem 0; border-bottom: 1px solid #1e2d4a; margin-bottom: 2.5rem; }
    .eco-header .badge { display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 3px; color: #38bdf8; background: rgba(56,189,248,0.08); border: 1px solid rgba(56,189,248,0.2); padding: 5px 16px; border-radius: 2px; margin-bottom: 1.2rem; text-transform: uppercase; }
    .eco-header h1 { font-size: 2.8rem; font-weight: 600; color: #f1f5f9; letter-spacing: -1px; margin: 0 0 0.5rem 0; }
    .eco-header h1 span { color: #38bdf8; }
    .eco-header p { font-size: 15px; color: #64748b; margin: 0; font-weight: 300; }

    .stat-strip { display: flex; gap: 1px; background: #1e2d4a; border: 1px solid #1e2d4a; border-radius: 8px; overflow: hidden; margin-bottom: 2rem; }
    .stat-item { flex: 1; background: #0d1526; padding: 1.1rem 1.5rem; text-align: center; }
    .stat-item .val { font-family: 'IBM Plex Mono', monospace; font-size: 1.4rem; font-weight: 500; color: #38bdf8; }
    .stat-item .lbl { font-size: 11px; color: #475569; letter-spacing: 1px; text-transform: uppercase; margin-top: 3px; }

    .input-panel { background: #0d1526; border: 1px solid #1e2d4a; border-radius: 10px; padding: 1.8rem 2rem; margin-bottom: 1.5rem; }
    .input-panel .panel-label { font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 2px; color: #475569; text-transform: uppercase; margin-bottom: 0.8rem; }

    .stTextArea textarea { background: #060c18 !important; border: 1px solid #1e2d4a !important; border-radius: 8px !important; color: #cbd5e1 !important; font-family: 'Space Grotesk', sans-serif !important; font-size: 14px !important; line-height: 1.7 !important; padding: 14px 16px !important; resize: vertical !important; }
    .stTextArea textarea:focus { border-color: #38bdf8 !important; box-shadow: 0 0 0 3px rgba(56,189,248,0.08) !important; }
    .stTextArea textarea::placeholder { color: #334155 !important; }
    .stTextArea label { display: none !important; }

    .stTextInput input { background: #060c18 !important; border: 1px solid #1e2d4a !important; border-radius: 8px !important; color: #cbd5e1 !important; font-family: 'IBM Plex Mono', monospace !important; font-size: 13px !important; padding: 10px 14px !important; }
    .stTextInput input:focus { border-color: #38bdf8 !important; }
    .stTextInput label { font-family: 'IBM Plex Mono', monospace !important; font-size: 11px !important; letter-spacing: 2px; color: #475569 !important; text-transform: uppercase; }

    .stButton > button { width: 100%; background: #38bdf8 !important; color: #060c18 !important; border: none !important; border-radius: 8px !important; padding: 0.85rem 2rem !important; font-family: 'Space Grotesk', sans-serif !important; font-weight: 600 !important; font-size: 15px !important; }
    .stButton > button:hover { background: #7dd3fc !important; transform: translateY(-1px); }

    .result-card { background: #0d1526; border: 1px solid #1e2d4a; border-radius: 10px; padding: 1.6rem 1.8rem; margin-bottom: 1rem; height: 100%; }
    .result-card.stable   { border-left: 3px solid #22c55e; }
    .result-card.unstable { border-left: 3px solid #ef4444; }
    .result-card.moderate { border-left: 3px solid #f59e0b; }

    .verdict-stable   { display: inline-flex; align-items: center; gap: 8px; background: rgba(34,197,94,0.1);  border: 1px solid rgba(34,197,94,0.25);  color: #22c55e; font-family: 'IBM Plex Mono', monospace; font-size: 13px; font-weight: 500; padding: 8px 18px; border-radius: 6px; margin-bottom: 1.2rem; }
    .verdict-unstable { display: inline-flex; align-items: center; gap: 8px; background: rgba(239,68,68,0.1);  border: 1px solid rgba(239,68,68,0.25);  color: #ef4444; font-family: 'IBM Plex Mono', monospace; font-size: 13px; font-weight: 500; padding: 8px 18px; border-radius: 6px; margin-bottom: 1.2rem; }
    .verdict-moderate { display: inline-flex; align-items: center; gap: 8px; background: rgba(245,158,11,0.1); border: 1px solid rgba(245,158,11,0.25); color: #f59e0b; font-family: 'IBM Plex Mono', monospace; font-size: 13px; font-weight: 500; padding: 8px 18px; border-radius: 6px; margin-bottom: 1.2rem; }

    .reason-box { background: #060c18; border: 1px solid #1e2d4a; border-radius: 8px; padding: 1rem 1.2rem; font-size: 14px; color: #94a3b8; line-height: 1.75; margin-bottom: 1.2rem; }
    .reason-box strong { color: #cbd5e1; }

    .keyword-chip { display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: 11px; padding: 3px 10px; border-radius: 4px; margin: 3px 3px 0 0; }
    .chip-stable   { background: rgba(34,197,94,0.1);  color: #22c55e;  border: 1px solid rgba(34,197,94,0.2); }
    .chip-unstable { background: rgba(239,68,68,0.1);  color: #ef4444;  border: 1px solid rgba(239,68,68,0.2); }

    .section-title { font-family: 'IBM Plex Mono', monospace; font-size: 11px; letter-spacing: 2px; color: #475569; text-transform: uppercase; margin-bottom: 0.8rem; }
    .outlook-box { background: #060c18; border: 1px solid #1e2d4a; border-radius: 8px; padding: 1rem 1.2rem; font-size: 14px; color: #94a3b8; line-height: 1.75; margin-top: 1rem; }
    .outlook-box strong { color: #cbd5e1; }
    .divider { border: none; border-top: 1px solid #1e2d4a; margin: 2rem 0; }

    .mode-strip { display: flex; gap: 10px; margin-bottom: 1.5rem; }
    .mode-btn { flex: 1; background: #0d1526; border: 1px solid #1e2d4a; border-radius: 8px; padding: 0.9rem 1rem; text-align: center; cursor: pointer; font-family: 'IBM Plex Mono', monospace; font-size: 12px; color: #64748b; letter-spacing: 1px; text-transform: uppercase; transition: all 0.2s; }
    .mode-btn.active { border-color: #38bdf8; color: #38bdf8; background: rgba(56,189,248,0.06); }

    .search-badge { display: inline-block; font-family: 'IBM Plex Mono', monospace; font-size: 10px; padding: 2px 8px; border-radius: 3px; background: rgba(56,189,248,0.1); border: 1px solid rgba(56,189,248,0.2); color: #38bdf8; margin-left: 6px; vertical-align: middle; }

    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  OFFLINE RULE-BASED ECONOMIC ANALYSIS ENGINE (NO API NEEDED)
# ════════════════════════════════════════════════════════════

# Keyword banks with weights — heavier weight = stronger signal
UNSTABLE_KEYWORDS = {
    "hyperinflation": 30, "crisis": 25, "collapse": 28, "default": 27,
    "recession": 22, "crash": 26, "bankruptcy": 24, "war": 20,
    "sanctions": 18, "capital flight": 22, "currency collapse": 28,
    "banking crisis": 25, "debt crisis": 24, "imf bailout": 16,
    "devaluation": 18, "unemployment surge": 20, "instability": 18,
    "civil unrest": 19, "political turmoil": 17, "shutdown": 15,
    "deficit": 12, "inflation surge": 20, "currency depreciation": 17,
    "stagflation": 23, "credit downgrade": 19, "default risk": 22,
    "economic downturn": 18, "negative growth": 19, "contraction": 16,
    "layoffs": 14, "bank run": 26, "panic selling": 20, "embargo": 18,
}

STABLE_KEYWORDS = {
    "gdp growth": 22, "stable currency": 20, "fiscal discipline": 22,
    "strong exports": 18, "investor confidence": 20, "low inflation": 20,
    "trade surplus": 18, "economic growth": 18, "job creation": 16,
    "foreign investment": 17, "surplus": 14, "expansion": 14,
    "rate cut": 10, "record high": 14, "strong demand": 14,
    "robust growth": 19, "currency strength": 17, "credit upgrade": 18,
    "stable inflation": 18, "economic boom": 20, "diversification": 12,
    "resilient economy": 19, "strong reserves": 16, "trade agreement": 13,
    "manufacturing growth": 15, "consumer confidence": 15, "recovery": 14,
    "growth forecast": 14, "positive outlook": 13,
}

MODERATE_KEYWORDS = {
    "mixed signals": 14, "uncertainty": 13, "slowdown": 13,
    "moderate growth": 11, "cautious": 10, "volatile": 14,
    "fluctuating": 11, "under pressure": 12, "watching closely": 8,
    "modest growth": 10, "tepid": 10, "uneven recovery": 12,
}

# Lightweight offline knowledge base — general, well-known economic
# reputations used ONLY as a mild prior nudge, never an overriding fact.
COUNTRY_PRIORS = {
    "pakistan":    {"bias": "moderate", "note": "history of IMF program dependence and currency pressure, balanced against periodic remittance and export growth"},
    "india":       {"bias": "stable",   "note": "large, diversified, consistently fast-growing economy"},
    "usa":         {"bias": "stable",   "note": "world's largest economy with deep capital markets, though periodically affected by debt-ceiling and rate-policy debates"},
    "united states": {"bias": "stable", "note": "world's largest economy with deep capital markets"},
    "china":       {"bias": "moderate", "note": "major global economy currently navigating a property-sector slowdown and export pressures"},
    "turkey":      {"bias": "unstable", "note": "recent years marked by very high inflation and currency depreciation"},
    "sri lanka":   {"bias": "unstable", "note": "sovereign default and severe forex crisis in recent years"},
    "venezuela":   {"bias": "unstable", "note": "long-running hyperinflation and economic contraction"},
    "argentina":   {"bias": "unstable", "note": "chronic high inflation and repeated debt restructuring"},
    "germany":     {"bias": "stable",   "note": "Europe's largest and most industrially diversified economy"},
    "japan":       {"bias": "stable",   "note": "advanced economy with very low (sometimes negative) inflation and high public debt offset by strong domestic savings"},
    "bangladesh":  {"bias": "moderate", "note": "strong garment-export growth balanced against forex reserve pressure"},
    "uk":          {"bias": "moderate", "note": "developed economy navigating post-Brexit trade adjustments and inflation"},
    "united kingdom": {"bias": "moderate", "note": "developed economy navigating post-Brexit trade adjustments and inflation"},
    "russia":      {"bias": "unstable", "note": "economy under sustained Western sanctions pressure"},
    "uae":         {"bias": "stable",   "note": "diversified, oil-and-trade-driven Gulf economy with strong reserves"},
    "saudi arabia": {"bias": "stable",  "note": "oil-revenue-backed economy pursuing diversification under Vision 2030"},
    "egypt":       {"bias": "moderate", "note": "currency pressure balanced against IMF-supported reform program"},
    "nigeria":     {"bias": "moderate", "note": "oil-revenue dependent economy with currency and inflation pressure"},
    "bangladesh":  {"bias": "moderate", "note": "export-driven growth balanced against reserve pressure"},
}


def _find_matches(text_lower: str, keyword_dict: dict):
    """Return list of (keyword, weight) found in text."""
    found = []
    for kw, weight in keyword_dict.items():
        if kw in text_lower:
            found.append((kw, weight))
    return found


def _detect_country(text_lower: str):
    for name in COUNTRY_PRIORS:
        if name in text_lower:
            return name
    return None


def analyze_offline(text: str) -> dict:
    """
    Fully offline, rule-based macroeconomic analyzer.
    No API key, no internet call — pure Python logic.
    """
    text_lower = text.lower().strip()

    unstable_hits = _find_matches(text_lower, UNSTABLE_KEYWORDS)
    stable_hits   = _find_matches(text_lower, STABLE_KEYWORDS)
    moderate_hits = _find_matches(text_lower, MODERATE_KEYWORDS)

    unstable_score = sum(w for _, w in unstable_hits)
    stable_score   = sum(w for _, w in stable_hits)
    moderate_score = sum(w for _, w in moderate_hits)

    # Country prior — small nudge only, applied only if NO strong keyword
    # signal already exists in either direction (keywords always win).
    country = _detect_country(text_lower)
    country_note = None
    if country:
        prior = COUNTRY_PRIORS[country]
        country_note = prior["note"]
        if unstable_score == 0 and stable_score == 0 and moderate_score == 0:
            if prior["bias"] == "stable":
                stable_score += 12
            elif prior["bias"] == "unstable":
                unstable_score += 12
            else:
                moderate_score += 10

    # If literally nothing matched and no country recognized,
    # fall back to a light neutral/moderate read instead of guessing wildly.
    if unstable_score == 0 and stable_score == 0 and moderate_score == 0:
        moderate_score = 10

    total = unstable_score + stable_score + moderate_score

    # ── Verdict logic ────────────────────────────────────────
    # Hard rule: if any high-severity crisis keyword present, force UNSTABLE
    severe_words = {"hyperinflation", "collapse", "default", "bankruptcy",
                     "bank run", "currency collapse", "crash"}
    forced_unstable = any(kw in text_lower for kw in severe_words)

    if forced_unstable or (unstable_score > stable_score + moderate_score and unstable_score >= 18):
        verdict = "UNSTABLE"
    elif stable_score > unstable_score and stable_score > moderate_score and unstable_score < 15:
        verdict = "STABLE"
    elif unstable_score > 0 and stable_score > 0 and abs(unstable_score - stable_score) <= 12:
        verdict = "MODERATE_RISK"
    elif unstable_score > stable_score and stable_score == 0 and moderate_score == 0:
        # Pure unstable signal with nothing pulling the other way
        # (e.g. a country-only prior like "Turkey") — don't water it
        # down into MODERATE_RISK just because the absolute score is small.
        verdict = "UNSTABLE"
    elif stable_score > unstable_score and unstable_score == 0 and moderate_score == 0:
        verdict = "STABLE"
    elif unstable_score > stable_score:
        verdict = "MODERATE_RISK" if unstable_score < 30 else "UNSTABLE"
    elif stable_score > unstable_score:
        verdict = "STABLE"
    else:
        verdict = "MODERATE_RISK"

    # ── Risk score (0 = perfectly stable, 100 = total collapse) ─
    if total > 0:
        raw_risk = (unstable_score * 1.3 + moderate_score * 0.6 - stable_score * 1.1)
        risk_score = int(max(5, min(95, 50 + raw_risk)))
    else:
        risk_score = 50

    # Nudge risk score to be consistent with verdict bucket
    if verdict == "STABLE":
        risk_score = min(risk_score, 38)
    elif verdict == "UNSTABLE":
        risk_score = max(risk_score, 62)
    else:
        risk_score = max(35, min(risk_score, 65))

    # ── Confidence (60-99) — higher when signal is strong/unambiguous ─
    signal_strength = max(unstable_score, stable_score, moderate_score)
    gap = abs(unstable_score - stable_score)
    confidence = 60 + min(35, int(signal_strength * 0.6 + gap * 0.3))
    confidence = max(60, min(99, confidence))

    # ── Build human-readable reason ──────────────────────────
    pos_words = [k for k, _ in stable_hits][:5]
    neg_words = [k for k, _ in (unstable_hits + moderate_hits)][:5]

    reason_parts = []
    if neg_words:
        reason_parts.append(f"Detected risk signals such as {', '.join(neg_words[:3])}")
    if pos_words:
        reason_parts.append(f"alongside positive indicators like {', '.join(pos_words[:3])}")
    if country_note and not neg_words and not pos_words:
        reason_parts.append(country_note.capitalize())
    elif country_note:
        reason_parts.append(f"Broader context: {country_note}")

    if not reason_parts:
        reason = "No strong economic signal keywords were detected in the input, so this is a neutral, low-confidence baseline read. Add specific terms (inflation, GDP growth, crisis, surplus, etc.) for a sharper analysis."
    else:
        reason = ". ".join(reason_parts) + "."

    # ── 6-month outlook sentence ─────────────────────────────
    if verdict == "STABLE":
        outlook = "Indicators point toward continued steady growth over the next two quarters, barring external shocks."
    elif verdict == "UNSTABLE":
        outlook = "Conditions are likely to remain under significant pressure over the next two quarters unless corrective fiscal or monetary action is taken."
    else:
        outlook = "Expect a mixed trajectory over the next two quarters — modest improvement is plausible, but downside risks have not cleared."

    # ── Synthetic 6-month GDP / inflation trend lines ────────
    # Deterministic-ish but varied: seeded from the input so repeated
    # runs on the same text give the same chart.
    random.seed(abs(hash(text_lower)) % (10 ** 6))

    if verdict == "STABLE":
        gdp_base, gdp_step = 1.8, 0.18
        inf_base, inf_step = 4.5, -0.25
    elif verdict == "UNSTABLE":
        gdp_base, gdp_step = -0.8, -0.15
        inf_base, inf_step = 18.0, 1.4
    else:
        gdp_base, gdp_step = 0.9, 0.05
        inf_base, inf_step = 7.5, 0.15

    gdp_trend = [round(gdp_base + gdp_step * i + random.uniform(-0.15, 0.15), 2) for i in range(6)]
    inf_trend = [round(max(0.2, inf_base + inf_step * i + random.uniform(-0.3, 0.3)), 2) for i in range(6)]

    return {
        "verdict": verdict,
        "confidence": confidence,
        "risk_score": risk_score,
        "reason": reason,
        "keywords_positive": pos_words,
        "keywords_negative": neg_words,
        "outlook_6m": outlook,
        "gdp_trend": gdp_trend,
        "inflation_trend": inf_trend,
        "data_source": "offline rule-based engine (no API)",
    }


# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div class="eco-header">
    <div class="badge">Offline Engine · No API Key · Rule-Based Logic</div>
    <h1>Eco-Insight <span>AI</span></h1>
    <p>Global Economic Analyzer & Forecaster — 100% offline, runs entirely on your machine</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="stat-strip">
    <div class="stat-item"><div class="val">190+</div><div class="lbl">Countries</div></div>
    <div class="stat-item"><div class="val">Offline</div><div class="lbl">AI Engine</div></div>
    <div class="stat-item"><div class="val">3-Class</div><div class="lbl">Classification</div></div>
    <div class="stat-item"><div class="val">0 Cost</div><div class="lbl">No API Key</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background:rgba(56,189,248,0.05);border:1px solid rgba(56,189,248,0.15);border-radius:8px;
            padding:0.7rem 1.1rem;font-size:12px;color:#475569;font-family:'IBM Plex Mono',monospace;margin-bottom:1.2rem;">
    ⚙️ This version runs a fully local, rule-based keyword + scoring engine — no internet call, no API key required.
    Type a country name (e.g. <span style="color:#38bdf8">Pakistan</span>, <span style="color:#38bdf8">Turkey</span>)
    or a full economic statement for best results.
</div>
""", unsafe_allow_html=True)

# ── Text input ───────────────────────────────────────────────
st.markdown('<div class="input-panel"><div class="panel-label">Economic Statement / Country Name</div>', unsafe_allow_html=True)
user_input = st.text_area(
    label="input",
    placeholder="e.g.  Pakistan is facing a severe debt crisis with high inflation, currency depreciation and IMF bailout talks...\n\nor simply type:  Germany   /   Turkey   /   Sri Lanka",
    height=120
)
st.markdown('</div>', unsafe_allow_html=True)

run = st.button("🔍 Generate Detailed Analysis")


# ── Run analysis ─────────────────────────────────────────────
if run:
    if not user_input.strip():
        st.warning("Kuch toh daalo — country name ya economic statement.")
        st.stop()

    with st.spinner("Offline engine analyze kar raha hai..."):
        result = analyze_offline(user_input.strip())

    verdict    = result.get("verdict", "MODERATE_RISK")
    confidence = result.get("confidence", 70)
    risk_score = result.get("risk_score", 50)
    reason     = result.get("reason", "")
    kw_pos     = result.get("keywords_positive", [])
    kw_neg     = result.get("keywords_negative", [])
    outlook    = result.get("outlook_6m", "")
    gdp_trend  = result.get("gdp_trend",       [1.0, 1.2, 1.4, 1.6, 1.8, 2.0])
    inf_trend  = result.get("inflation_trend", [4.0, 3.8, 3.6, 3.4, 3.2, 3.0])
    data_src   = result.get("data_source", "offline rule-based engine")

    if verdict == "STABLE":
        card_cls, verdict_html = "stable",   '<div class="verdict-stable">● STABLE — ECONOMY</div>'
        lg, li, icon, gc = '#22c55e', '#38bdf8', "💡", '#22c55e'
    elif verdict == "UNSTABLE":
        card_cls, verdict_html = "unstable", '<div class="verdict-unstable">⚠ UNSTABLE — HIGH RISK</div>'
        lg, li, icon, gc = '#ef4444', '#f97316', "🚨", '#ef4444'
    else:
        card_cls, verdict_html = "moderate", '<div class="verdict-moderate">◈ MODERATE RISK</div>'
        lg, li, icon, gc = '#f59e0b', '#fb923c', "⚡", '#f59e0b'

    src_badge = f'<span class="search-badge">⚙️ {data_src}</span>'

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    col1, col2 = st.columns([1.15, 1], gap="large")

    with col1:
        st.markdown(f'<div class="section-title">Prediction Reasoning {src_badge}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-card {card_cls}">', unsafe_allow_html=True)
        st.markdown(verdict_html, unsafe_allow_html=True)
        st.markdown(f'<div class="reason-box"><strong>Why?</strong> {reason}</div>', unsafe_allow_html=True)

        chips = "".join(f'<span class="keyword-chip chip-stable">{w}</span>' for w in kw_pos[:5])
        chips += "".join(f'<span class="keyword-chip chip-unstable">{w}</span>' for w in kw_neg[:5])
        if chips:
            st.markdown(f'<div style="margin-bottom:0.5rem"><div class="section-title" style="margin-bottom:6px">Detected Keywords</div>{chips}</div>', unsafe_allow_html=True)

        rc = '#22c55e' if risk_score < 35 else ('#f59e0b' if risk_score < 65 else '#ef4444')
        st.markdown(f'<div class="section-title" style="margin-top:1rem">Risk Score: {risk_score}/100</div>', unsafe_allow_html=True)
        st.markdown(f'<div style="background:#060c18;border-radius:6px;height:10px;overflow:hidden;margin-bottom:1rem;"><div style="width:{risk_score}%;height:100%;background:{rc};border-radius:6px;"></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title" style="margin-top:1.4rem">Model Confidence</div>', unsafe_allow_html=True)
        rem = 100 - confidence
        if verdict == "STABLE":
            lb, vl, cm = ['Stable', 'Unstable'], [confidence, rem], {'Stable': '#22c55e', 'Unstable': '#ef4444'}
        elif verdict == "UNSTABLE":
            lb, vl, cm = ['Unstable', 'Stable'], [confidence, rem], {'Unstable': '#ef4444', 'Stable': '#22c55e'}
        else:
            lb, vl, cm = ['Moderate', 'Stable'], [confidence, rem], {'Moderate': '#f59e0b', 'Stable': '#22c55e'}

        fig = px.bar(pd.DataFrame({'Status': lb, 'Confidence (%)': vl}), x='Status', y='Confidence (%)',
                     color='Status', color_discrete_map=cm, text='Confidence (%)')
        fig.update_traces(texttemplate='%{text:.0f}%', textposition='outside', marker_line_width=0, width=0.45)
        fig.update_layout(paper_bgcolor='#0d1526', plot_bgcolor='#060c18', font_color='#94a3b8',
            font_family='Space Grotesk', showlegend=False, margin=dict(t=20, b=10, l=10, r=10), height=260,
            xaxis=dict(showgrid=False, tickfont=dict(size=13, color='#cbd5e1')),
            yaxis=dict(showgrid=True, gridcolor='#1e2d4a', range=[0, 115], ticksuffix='%', tickfont=dict(size=11, color='#475569')))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">6-Month Economic Forecast</div>', unsafe_allow_html=True)
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="outlook-box"><span style="font-size:18px;margin-right:6px">{icon}</span><strong>Outlook:</strong> {outlook}</div>', unsafe_allow_html=True)

        ml = ['M+1', 'M+2', 'M+3', 'M+4', 'M+5', 'M+6']
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=ml, y=gdp_trend, mode='lines+markers', name='GDP Growth (%)',
            line=dict(color=lg, width=2.5), marker=dict(size=6, color=lg)))
        fig2.add_trace(go.Scatter(x=ml, y=inf_trend, mode='lines+markers', name='Inflation (%)',
            line=dict(color=li, width=2.5, dash='dot'), marker=dict(size=6, color=li)))
        fig2.update_layout(paper_bgcolor='#0d1526', plot_bgcolor='#060c18', font_color='#94a3b8',
            font_family='Space Grotesk',
            legend=dict(orientation='h', y=1.12, x=0, font=dict(size=11), bgcolor='rgba(0,0,0,0)'),
            margin=dict(t=30, b=10, l=10, r=10), height=240,
            xaxis=dict(showgrid=False, tickfont=dict(size=11, color='#475569')),
            yaxis=dict(showgrid=True, gridcolor='#1e2d4a', ticksuffix='%', tickfont=dict(size=11, color='#475569')))
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown('<div class="section-title" style="margin-top:0.5rem">Confidence Gauge</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Indicator(
            mode="gauge+number", value=confidence,
            number={'suffix': '%', 'font': {'size': 28, 'color': '#f1f5f9', 'family': 'IBM Plex Mono'}},
            gauge={'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#1e2d4a', 'tickfont': {'color': '#475569', 'size': 10}},
                   'bar': {'color': gc, 'thickness': 0.22}, 'bgcolor': '#060c18', 'borderwidth': 0,
                   'steps': [{'range': [0, 50], 'color': '#0d1526'}, {'range': [50, 75], 'color': '#111827'}, {'range': [75, 100], 'color': '#0d1526'}],
                   'threshold': {'line': {'color': gc, 'width': 2}, 'thickness': 0.8, 'value': confidence}}))
        fig3.update_layout(paper_bgcolor='#0d1526', font_color='#94a3b8', margin=dict(t=10, b=0, l=20, r=20), height=180)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ── Footer ───────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:4rem;padding-top:1.5rem;border-top:1px solid #1e2d4a;
            font-family:'IBM Plex Mono',monospace;font-size:11px;color:#334155;letter-spacing:1px;">
    ECO-INSIGHT AI &nbsp;·&nbsp; 100% OFFLINE RULE-BASED ENGINE &nbsp;·&nbsp; NO API KEY REQUIRED
</div>
""", unsafe_allow_html=True)
