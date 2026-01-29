
```markdown
# 🌱 AgriSense Morocco
### AI-Powered Smart Agriculture Platform 🇲🇦

AgriSense Morocco is an **intelligent decision-support platform for agriculture**, designed to help farmers, students, and researchers choose the **right crop** and **optimal irrigation strategy** based on **geolocation, real-time weather, and AI predictions**.

This project focuses on **Morocco’s climate and agricultural context**, combining **machine learning**, **geospatial data**, and **interactive analytics** into a modern web application.

---

## 🌍 Why AgriSense?

Agriculture in Morocco faces:
- Climate variability 🌡️  
- Water scarcity 💧  
- Crop selection uncertainty 🌾  

AgriSense transforms **raw environmental data** into **clear, actionable insights** using artificial intelligence.

---

## ✨ Key Features

### 📍 Location Intelligence
- Interactive map or GPS coordinates
- Works across all Moroccan regions
- Reverse geocoding for city detection

### ☁️ Real-Time Weather Analysis
- Live temperature, rainfall, and humidity
- OpenWeather API integration
- Automatic fallback to demo data

### 🤖 AI Decision Engine
- Machine Learning using **Random Forest**
- Crop suitability prediction
- Irrigation level optimization

### 📊 Visual Analytics
- Crop probability bar charts
- Intuitive dashboard metrics
- NDVI-based vegetation insight (simulated)

### 🔄 What-If Simulation
- Analyze impact of rainfall variation
- Compare AI recommendations dynamically

### 📄 Smart Reporting
- One-click **PDF export**
- Location-specific agronomic summary
- Shareable for academic or professional use

### 📱 QR-Code Friendly
- Web-based
- Accessible from any device
- Ideal for demos & presentations

---

## 🧠 AI & Data Pipeline

**Inputs**
- Latitude / Longitude
- Temperature
- Rainfall
- Humidity
- NDVI (simulated)

**Models**
- RandomForestClassifier (Scikit-Learn)

**Outputs**
- 🌾 Recommended Crop
- 💧 Irrigation Level (Low / Medium / High)
- 📊 Probability Distribution

> This project prioritizes explainability and educational value over black-box predictions.

---

## 🛠️ Tech Stack

| Layer | Technology |
|------|-----------|
| Frontend | Streamlit |
| Backend | Python 3.11 |
| ML | Scikit-learn |
| Data | Pandas, NumPy |
| Visualization | Plotly |
| Weather API | OpenWeather |
| Reports | ReportLab (PDF) |
| Deployment | Streamlit Cloud |

---

## 📁 Project Structure

```

AgriSense-Morocco/
│
├── app.py               # Streamlit main app
├── requirements.txt     # Dependencies
└── README.md            # Documentation

````

---

## ⚙️ Local Installation

```bash
git clone https://github.com/MAmine-A99/AgriSense-Morocco.git
cd AgriSense-Morocco
pip install -r requirements.txt
streamlit run app.py
````

---

## ☁️ Deployment

* Deployed using **Streamlit Cloud**
* No server configuration required
* Continuous deployment from GitHub

---

## 🎓 Target Use Cases

* AI & Data Science portfolios
* Engineering school applications
* Agricultural innovation projects
* Smart farming prototypes
* Hackathons & research demos

---

## 🔮 Future Enhancements

* 🛰️ Real satellite NDVI (Sentinel-2)
* 🌱 Soil type & fertility integration
* 📡 IoT sensor support
* 🌍 Climate-change scenario modeling
* 🇲🇦 Arabic / French multilingual UI
* 📲 SMS & WhatsApp farmer alerts

---

## 👤 Author

**Mohamed Amine Jaghouti**
AI & Digital Engineering Student
Morocco 🇲🇦

> Passionate about AI, sustainability, and real-world impact.

---

## 📜 License

This project is open for **educational and research purposes**.
For commercial use, please contact the author.

---

🌱 *AgriSense Morocco — Turning Data into Smarter Farming Decisions.*

```

---

If you want, next I can:
- 🔥 Add **badges** (Python, Streamlit, AI, Morocco)
- 🌐 Write a **startup-style pitch**
- 📈 Prepare this for **Polytech / IDIA / alternance dossiers**
- 🎥 Create a **demo video script**

Just tell me what’s next 😎
::contentReference[oaicite:0]{index=0}
```
