import streamlit as st
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import plotly.graph_objects as go
from io import BytesIO
from reportlab.pdfgen import canvas
import qrcode

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(page_title="AgriSense Morocco", layout="wide", page_icon="🌱")

# ==========================
# GLOBAL STYLE
# ==========================
st.markdown("""
<style>
.stButton>button {
    border-radius: 20px;
    background-color:#D97706;
    color:white;
    height:55px;
    font-size:18px;
    font-weight:bold;
    width:80%;
}
.intro-text {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color:#1C1C1C;
}
h1,h2,h3 {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color:#1C1C1C;
}
</style>
""", unsafe_allow_html=True)

# ==========================
# SESSION STATE – PAGE ROUTER
# ==========================
if "page" not in st.session_state:
    st.session_state.page = "intro"

if "marker" not in st.session_state:
    st.session_state.marker = {"lat": 31.6295, "lon": -7.9811}

if "weather" not in st.session_state:
    st.session_state.weather = {"temp": 25, "humidity": 50, "rain": 2}

# ==========================
# INTRO PAGE
# ==========================
def intro_page():

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- IMAGES AT THE TOP ---
    st.image([
        "/mnt/data/aa0717d6-9be8-4217-b16e-bf754e5e8b97.png",
        "/mnt/data/80f59ee9-b845-48ea-947d-43468a39050f.png",
        "/mnt/data/a64658b5-e730-46f1-bf79-91045d073cf1.png"
    ], width=900, caption=["Smart AI in the field", "Dashboard preview", "Mobile interface"])

    st.markdown("<br>", unsafe_allow_html=True)

    # --- TITLE & SUBTITLE ---
    st.markdown("<h1 style='text-align:center;'>🌱 AgriSense Morocco</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h3 style='text-align:center;color:#555555;'>AI-powered Sustainable Agriculture Decision Support</h3>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- DESCRIPTION ---
    st.markdown("""
    <div class='intro-text' style='text-align:center; max-width:900px; margin:auto; font-size:18px;'>
    AgriSense Morocco combines <b>climate intelligence, geospatial analytics, NDVI vegetation indices,</b> 
    and <b>machine learning models</b> to support farmers, cooperatives, and institutions in Morocco.
    It helps choose optimal crops, irrigation strategies, and sustainable practices for a productive and resilient agriculture.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # --- CTA BUTTON ---
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🚀 LET’S EXPLORE AGRISENSE"):
            st.session_state.page = "dashboard"
            st.rerun()

    st.markdown("<br><br><br>", unsafe_allow_html=True)

    # --- FOOTER ---
    st.markdown(
        "<p style='text-align:center;color:#888888;'>Powered by Mohamed Amine Jaghouti • AI for Sustainable Agriculture</p>",
        unsafe_allow_html=True
    )


# ==========================
# DASHBOARD PAGE (UNCHANGED)
# ==========================
def dashboard_page():

    st.sidebar.title("📍 Select Region (Morocco)")

    lat = st.sidebar.number_input("Latitude", 21.0, 36.0, st.session_state.marker["lat"])
    lon = st.sidebar.number_input("Longitude", -17.0, -1.0, st.session_state.marker["lon"])

    if st.sidebar.button("Set Region"):
        st.session_state.marker = {"lat": lat, "lon": lon}
        st.session_state.weather = {"temp": 25, "humidity": 50, "rain": 2}

    if st.sidebar.button("⬅ Back to Presentation"):
        st.session_state.page = "intro"
        st.rerun()

    lat, lon = st.session_state.marker["lat"], st.session_state.marker["lon"]

    # ---------------- MAP ----------------
    map_df = pd.DataFrame([{"lat": lat, "lon": lon}])
    fig_map = go.Figure(go.Scattermapbox(
        lat=map_df["lat"], lon=map_df["lon"],
        mode="markers",
        marker=go.scattermapbox.Marker(size=14, color="#D97706"),
        text=["Selected Region"]
    ))
    fig_map.update_layout(
        mapbox=dict(style="open-street-map", zoom=5, center=dict(lat=lat, lon=lon)),
        margin=dict(l=0, r=0, t=0, b=0),
        height=420
    )
    st.plotly_chart(fig_map, use_container_width=True)

    # ---------------- LOCATION ----------------
    API_KEY = "be87b67bc35d53a2b6db5abe4f569460"
    city_name = "Unknown"

    try:
        geo = requests.get(
            f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={API_KEY}",
            timeout=5
        ).json()
        if geo:
            city_name = geo[0]["name"]
    except:
        pass

    st.markdown(f"### 📌 Selected Area: **{city_name}**")

    # ---------------- WEATHER ----------------
    if st.sidebar.button("🔄 Refresh Weather"):
        try:
            weather = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={API_KEY}",
                timeout=5
            ).json()
            st.session_state.weather = {
                "temp": weather["main"]["temp"],
                "humidity": weather["main"]["humidity"],
                "rain": weather.get("rain", {}).get("1h", np.random.uniform(0, 6))
            }
        except:
            st.warning("Using demo weather data")

    temp = st.session_state.weather["temp"]
    humidity = st.session_state.weather["humidity"]
    rain = st.session_state.weather["rain"]

    ndvi = float(np.clip(np.random.normal(0.55, 0.1), 0.2, 0.85))

    # ---------------- AI ----------------
    crops = ["wheat", "olives", "tomatoes", "citrus", "grapes", "almonds", "vegetables"]
    irrigation = ["low", "low", "high", "medium", "medium", "low", "high"]

    df = pd.DataFrame({
        "temperature": np.linspace(temp-3, temp+3, len(crops)),
        "rainfall": np.linspace(max(rain-10, 0), rain+10, len(crops)),
        "ndvi": np.linspace(ndvi-0.05, ndvi+0.05, len(crops)),
        "crop": crops,
        "irrigation": irrigation
    })

    X = df[["temperature", "rainfall", "ndvi"]]
    crop_enc = LabelEncoder()
    irr_enc = LabelEncoder()

    y_crop = crop_enc.fit_transform(df["crop"])
    y_irr = irr_enc.fit_transform(df["irrigation"])

    crop_model = RandomForestClassifier(200, random_state=42)
    irr_model = RandomForestClassifier(200, random_state=42)
    crop_model.fit(X, y_crop)
    irr_model.fit(X, y_irr)

    X_input = pd.DataFrame([[temp, rain, ndvi]], columns=X.columns)
    crop_pred = crop_enc.inverse_transform(crop_model.predict(X_input))[0]
    irr_pred = irr_enc.inverse_transform(irr_model.predict(X_input))[0]
    probs = crop_model.predict_proba(X_input)[0]

    # ---------------- METRICS ----------------
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🌡 Temperature", f"{temp:.1f} °C")
    c2.metric("🌧 Rainfall", f"{rain:.1f} mm")
    c3.metric("💧 Humidity", f"{humidity}%")
    c4.metric("🌿 NDVI", f"{ndvi:.2f}")

    st.success(f"🌾 Recommended Crop: **{crop_pred.capitalize()}**")
    st.info(f"💦 Irrigation Level: **{irr_pred.capitalize()}**")

    # ---------------- CHART ----------------
    fig = go.Figure(go.Bar(x=crop_enc.classes_, y=probs, marker_color="#6B8E23"))
    fig.update_layout(title="Crop Suitability Probabilities")
    st.plotly_chart(fig, use_container_width=True)

    # ---------------- PDF ----------------
    def generate_pdf():
        buffer = BytesIO()
        c = canvas.Canvas(buffer)
        c.drawString(50, 800, "AgriSense Morocco Report")
        y = 760
        for line in [
            f"Region: {city_name}",
            f"Temperature: {temp:.1f} °C",
            f"Rainfall: {rain:.1f} mm",
            f"NDVI: {ndvi:.2f}",
            f"Crop: {crop_pred}"
        ]:
            c.drawString(50, y, line)
            y -= 20
        c.save()
        buffer.seek(0)
        return buffer

    if st.button("📄 Export PDF Report"):
        st.download_button("Download PDF", generate_pdf(),
                           file_name=f"AgriSense_{city_name}.pdf",
                           mime="application/pdf")

    # ---------------- QR ----------------
    APP_URL = "https://agrisense-moroccomaj-nngj5uc898kzkk7ae4j9go.streamlit.app/"
    qr = qrcode.make(APP_URL)
    buf = BytesIO()
    qr.save(buf)
    buf.seek(0)

    st.markdown("### 📱 Scan to open AgriSense Morocco")
    st.image(buf, width=160)


# ==========================
# ROUTER
# ==========================
if st.session_state.page == "intro":
    intro_page()
else:
    dashboard_page()
