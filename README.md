# 🌱 AgriSense Morocco

AgriSense Morocco is an **AI-powered agriculture decision support system** designed to help farmers, students, and researchers make smarter agricultural decisions based on **weather data, location, and AI predictions**.

The platform uses **machine learning**, **real-time weather APIs**, and **interactive maps** to recommend:
- 🌾 The most suitable crop
- 💧 The optimal irrigation level

Built with **Streamlit** and deployed on **Streamlit Cloud**.

---

## 🚀 Features

- 📍 **Interactive map** to select any region in Morocco  
- ☁️ **Real-time weather data** (OpenWeather API)
- 🤖 **AI crop recommendation** using Random Forest
- 💧 **Smart irrigation level prediction**
- 📊 **Probability visualization** for crop suitability
- 🔄 **What-if analysis** (e.g., increased rainfall)
- 📄 **Exportable PDF report**
- 📱 **QR-code friendly web access**

---

## 🧠 Technologies Used

- **Python 3.11**
- **Streamlit**
- **Scikit-learn**
- **Pandas & NumPy**
- **Plotly**
- **OpenWeather API**
- **ReportLab (PDF export)**

---

## ⚙️ Installation (Local)

```bash
git clone https://github.com/MAmine-A99/AgriSense-Morocco.git
cd AgriSense-Morocco
pip install -r requirements.txt
streamlit run app.py

