import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import qrcode

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="AgriSense Morocco",
    page_icon="🌱",
    layout="wide"
)

# =====================================================
# GLOBAL STYLE (Apple-like, Jury-friendly)
# =====================================================
st.markdown("""
<style>
* {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                 Roboto, Helvetica, Arial, sans-serif !important;
}
.stButton>button {
    border-radius: 14px;
    background-color:#D97706;
    color:white;
    height:48px;
    font-size:17px;
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
    <p style='text-align:center; font-size:15px;'>
    Built for Morocco • Climate-Aware • AI-Powered
    </p>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("### 🚜 Project Concept")
        st.write("""
        **AgriSense Morocco** is an AI-based agricultural decision-support system
        designed to help farmers, cooperatives, and policymakers make
        **data-driven and climate-aware decisions**.

        The platform analyzes **regional climate conditions and vegetation
        behavior**, then uses **machine-learning models** to recommend
        suitable crops and irrigation strategies.
        """)

        st.markdown("### 🎯 Objectives")
        st.markdown("""
        - Improve agricultural planning under climate uncertainty  
        - Reduce water waste and inefficient irrigation  
        - Support sustainable farming practices  
        - Make AI accessible to Moroccan agriculture  
        """)

    with col2:
        st.markdown("### 🇲🇦 Why Morocco?")
        st.write("""
        Morocco faces water scarcity, strong climate variability,
        and diverse agricultural zones.

        AgriSense adapts decisions to **local regional realities**,
        not one-size-fits-all farming.
        """)

    st.markdown("---")

    if st.button("🚀 Launch Interactive Dashboard"):
        st.session_state.page = "dashboard"
        st.rerun()

# =====================================================
# DASHBOARD PAGE
# =====================================================
def dashboard_page():

    st.sidebar.title("📍 Select Region")

    region = st.sidebar.selectbox(
        "Moroccan Region",
        ["Souss-Massa", "Gharb", "Saïss", "Haouz", "Oriental", "Drâa-Tafilalet"]
    )

    if st.sidebar.button("⬅ Back to Introduction"):
        st.session_state.page = "intro"
        st.rerun()

    # ---------------- SIMULATED DATA (Demo-Safe) ----------------
    np.random.seed(len(region))
    temperature = np.random.uniform(12, 38)
    rainfall = np.random.uniform(0, 40)
    ndvi = np.clip(np.random.normal(0.55, 0.1), 0.25, 0.85)

    # ---------------- METRICS ----------------
    c1, c2, c3 = st.columns(3)
    c1.metric("🌡 Temperature", f"{temperature:.1f} °C")
    c2.metric("🌧 Rainfall", f"{rainfall:.1f} mm")
    c3.metric("🌿 NDVI", f"{ndvi:.2f}")

    st.markdown("---")

    # ---------------- MAP ----------------
    region_coords = {
        "Souss-Massa": (30.4, -9.6),
        "Gharb": (34.2, -6.3),
        "Saïss": (33.9, -5.5),
        "Haouz": (31.6, -7.9),
        "Oriental": (34.8, -2.4),
        "Drâa-Tafilalet": (31.9, -4.4)
    }

    lat, lon = region_coords[region]

    fig_map = go.Figure(go.Scattermapbox(
        lat=[lat],
        lon=[lon],
        mode="markers",
        marker=dict(size=14, color="#D97706"),
        text=[region]
    ))

    fig_map.update_layout(
        mapbox=dict(style="open-street-map", zoom=5, center=dict(lat=lat, lon=lon)),
        margin=dict(l=0, r=0, t=0, b=0),
        height=380
    )

    st.plotly_chart(fig_map, use_container_width=True)

    # ---------------- AI MODELS ----------------
    data = pd.DataFrame({
        "temp": np.linspace(temperature-4, temperature+4, 6),
        "rain": np.linspace(max(rainfall-15,0), rainfall+15, 6),
        "ndvi": np.linspace(ndvi-0.1, ndvi+0.1, 6),
        "crop": ["Wheat", "Olives", "Tomatoes", "Citrus", "Dates", "Wheat"],
        "irrigation": ["High", "Low", "High", "Medium", "Low", "High"]
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

    # ---------------- RESULTS ----------------
    st.success(f"🌾 Recommended Crop: **{crop_pred}**")
    st.info(f"💧 Irrigation Strategy: **{irr_pred}**")

    # ---------------- PDF REPORT ----------------
    def generate_pdf():
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer)
        styles = getSampleStyleSheet()
        content = [
            Paragraph("<b>AgriSense Morocco – AI Report</b>", styles["Title"]),
            Paragraph(f"Region: {region}", styles["Normal"]),
            Paragraph(f"Temperature: {temperature:.1f} °C", styles["Normal"]),
            Paragraph(f"Rainfall: {rainfall:.1f} mm", styles["Normal"]),
            Paragraph(f"NDVI: {ndvi:.2f}", styles["Normal"]),
            Paragraph(f"Recommended Crop: {crop_pred}", styles["Normal"]),
            Paragraph(f"Irrigation Strategy: {irr_pred}", styles["Normal"]),
        ]
        doc.build(content)
        buffer.seek(0)
        return buffer

    st.markdown("---")
    st.download_button(
        "📄 Download AI Report (PDF)",
        generate_pdf(),
        file_name="AgriSense_Report.pdf",
        mime="application/pdf"
    )

    # ---------------- QR CODE ----------------
    APP_URL = "https://agrisense-moroccomaj-nngj5uc898kzkk7ae4j9go.streamlit.app/"
    qr = qrcode.make(APP_URL)
    buf = BytesIO()
    qr.save(buf)
    buf.seek(0)

    st.markdown("### 📱 Scan to access AgriSense Morocco")
    st.image(buf, width=150)

# =====================================================
# ROUTER
# =====================================================
if st.session_state.page == "intro":
    intro_page()
else:
    dashboard_page()
