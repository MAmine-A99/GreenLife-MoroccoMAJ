import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AgriSense Morocco",
    page_icon="🌱",
    layout="wide"
)

# =====================================================
# GLOBAL STYLE (Apple-like)
# =====================================================
st.markdown("""
<style>
* {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                 Roboto, Helvetica, Arial, sans-serif !important;
}
.stButton>button {
    border-radius: 16px;
    height: 52px;
    font-size: 18px;
    background-color: #D97706;
    color: white;
}
.metric {
    text-align:center;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================
if "page" not in st.session_state:
    st.session_state.page = "intro"

# =====================================================
# INTRO PAGE
# =====================================================
def intro_page():
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
    <h1 style='text-align:center; color:#D97706;'>🌱 AgriSense Morocco</h1>
    <h3 style='text-align:center; color:#6B8E23;'>
    AI-Driven Decision Support for Sustainable Agriculture
    </h3>
    <p style='text-align:center; font-size:16px;'>
    Designed for Morocco • Climate-Aware • Data-Driven
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("### 🚜 Project Idea")
        st.write("""
        AgriSense Morocco is a smart agriculture decision-support platform
        designed to help farmers and stakeholders make **informed,
        sustainable decisions**.

        The system uses AI to analyze agro-environmental indicators
        such as climate conditions and vegetation behavior,
        transforming them into **clear recommendations** for crop selection,
        irrigation strategy, and risk management.
        """)

        st.markdown("### 🎯 Objectives")
        st.markdown("""
        - Support sustainable farming under climate stress  
        - Reduce water and resource waste  
        - Enable data-driven agricultural planning  
        - Make AI accessible to farmers and cooperatives  
        """)

    with col2:
        st.markdown("### 🇲🇦 Why Morocco?")
        st.write("""
        Morocco faces:
        - Water scarcity  
        - Climate variability  
        - Regional agricultural diversity  

        AgriSense Morocco is designed to **adapt decisions to regional realities**.
        """)

    st.markdown("---")

    if st.button("🚀 Launch Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

# =====================================================
# DASHBOARD PAGE
# =====================================================
def dashboard_page():

    st.sidebar.title("🌍 Select Region")
    region = st.sidebar.selectbox(
        "Moroccan Region",
        ["Souss-Massa", "Gharb", "Saïss", "Haouz", "Oriental", "Draa-Tafilalet"]
    )

    crop = st.sidebar.selectbox(
        "Crop of Interest",
        ["Wheat", "Olives", "Tomatoes", "Citrus", "Dates"]
    )

    if st.sidebar.button("⬅ Back"):
        st.session_state.page = "intro"
        st.rerun()

    # ---------------- Simulated Indicators ----------------
    np.random.seed(len(region))
    temperature = np.random.uniform(10, 35)
    rainfall = np.random.uniform(0, 50)
    ndvi = np.clip(np.random.normal(0.55, 0.1), 0.25, 0.85)

    # ---------------- Metrics ----------------
    m1, m2, m3 = st.columns(3)
    m1.metric("🌡 Temperature", f"{temperature:.1f} °C")
    m2.metric("🌧 Rainfall", f"{rainfall:.1f} mm")
    m3.metric("🌿 Vegetation Index", f"{ndvi:.2f}")

    st.markdown("---")

    # ---------------- AI Model (Demo Logic) ----------------
    data = pd.DataFrame({
        "temp": np.linspace(temperature-5, temperature+5, 6),
        "rain": np.linspace(max(rainfall-20,0), rainfall+20, 6),
        "ndvi": np.linspace(ndvi-0.1, ndvi+0.1, 6),
        "crop": ["Wheat","Olives","Tomatoes","Citrus","Dates","Wheat"],
        "irrigation": ["High","Low","High","Medium","Low","High"]
    })

    X = data[["temp","rain","ndvi"]]
    le_crop = LabelEncoder()
    le_irr = LabelEncoder()

    y_crop = le_crop.fit_transform(data["crop"])
    y_irr = le_irr.fit_transform(data["irrigation"])

    crop_model = RandomForestClassifier(n_estimators=150, random_state=42)
    irr_model = RandomForestClassifier(n_estimators=150, random_state=42)

    crop_model.fit(X, y_crop)
    irr_model.fit(X, y_irr)

    X_input = pd.DataFrame([[temperature, rainfall, ndvi]], columns=X.columns)
    crop_pred = le_crop.inverse_transform(crop_model.predict(X_input))[0]
    irr_pred = le_irr.inverse_transform(irr_model.predict(X_input))[0]

    # ---------------- Results ----------------
    st.success(f"🌾 Recommended Crop: **{crop_pred}**")
    st.info(f"💧 Suggested Irrigation Level: **{irr_pred}**")

    # ---------------- Risk Alerts ----------------
    risks = []
    if rainfall < 10:
        risks.append("Drought risk")
    if temperature > 32:
        risks.append("Heat stress risk")
    if ndvi < 0.35:
        risks.append("Low vegetation health")

    if risks:
        st.warning("⚠️ Risks detected: " + ", ".join(risks))
    else:
        st.success("✅ No major agricultural risks detected")

    # ---------------- Suitability Chart ----------------
    probs = crop_model.predict_proba(X_input)[0]

    fig = go.Figure(
        go.Bar(
            x=le_crop.classes_,
            y=probs,
            marker_color="#6B8E23"
        )
    )
    fig.update_layout(
        title="Crop Suitability (AI-Estimated)",
        yaxis_title="Probability"
    )

    st.plotly_chart(fig, use_container_width=True)

    # ---------------- AI Insight ----------------
    st.markdown("### 🤖 AI Insight")
    st.write(f"""
    For **{region}**, the current agro-environmental conditions indicate that
    **{crop_pred}** is the most suitable option under existing climate pressure.
    The system recommends **{irr_pred.lower()} irrigation**
    to balance productivity and sustainability.
    """)

# =====================================================
# ROUTER
# =====================================================
if st.session_state.page == "intro":
    intro_page()
else:
    dashboard_page()
