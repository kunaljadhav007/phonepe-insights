# 📱 PhonePe Pulse Dashboard

An interactive data visualization dashboard built using **Streamlit**, **Plotly**, and **Gemini AI API** to analyze digital payment trends in India using **PhonePe Pulse data**.

---

## 🔍 Project Overview

The PhonePe Pulse Dashboard is a data analytics tool that visualizes transaction trends and user behavior across Indian states and districts. It uses official PhonePe data to provide real-time insights and integrates **Google Gemini AI** for automated insight generation.

---

## 🚀 Features

✅ Interactive Geo-level maps with transaction heatmaps  
✅ State-wise and district-wise bar charts for transaction amounts and user counts  
✅ Yearly and quarterly breakdowns for transactions and app opens  
✅ AI-generated insights with Gemini 2.0 Flash API  
✅ Downloadable PDF summary reports with key findings  
✅ Clean UI with light/dark theme compatibility

---

## 🧠 AI-Powered Insights

Using the **Gemini 2.0 Flash API**, users can:
- Generate short summaries of transaction behavior
- Get growth patterns and trends
- Download PDF reports automatically

---

## 📂 Folder Structure

```
phonepe-insights/
├── dashboard/
│   ├── app.py                # Main Streamlit app
│   ├── utils.py              # All utility and plotting functions
│   ├── db_config.py          # DB connection logic
│   ├── assets/               # Static assets (logos, fonts)
│   └── states_india.geojson  # GeoJSON for choropleth map
├── .env                      # Gemini API key (excluded in .gitignore)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
```

---

## 🧪 Tech Stack

| Tech           | Description                         |
|----------------|-------------------------------------|
| **Streamlit**  | Fast and interactive Python UI      |
| **Plotly**     | For dynamic charts and maps         |
| **MySQL**      | Backend database for transactions   |
| **Gemini API** | AI-powered insights via Google AI   |
| **FPDF**       | Generate PDF reports of insights    |

---

## 📊 Data Source

Data is sourced from the official [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse), structured and stored in a local MySQL database.

---

## 🛠️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/phonepe-pulse-dashboard.git
cd phonepe-pulse-dashboard
```

### 2. Create Virtual Environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Set Up `.env`

Create a `.env` file in the root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Run the App

```bash
cd dashboard
streamlit run app.py
```

---

## 📸 Screenshots

| Dashboard Page         | AI Insights Report           |
|------------------------|------------------------------|
| ![Dashboard](assets/screenshot_dashboard.png) | ![AI Report](assets/screenshot_ai.png) |

---

## 📜 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙋‍♂️ Author

**Kunal Jadhav**  
Connect on [LinkedIn](https://www.linkedin.com/in/kunal-jadhav/) | GitHub: [@kunaljv](https://github.com/kunaljv)

---

## 💡 Feedback & Contributions

Feel free to fork this repo, raise issues, or suggest features via pull requests.

---
