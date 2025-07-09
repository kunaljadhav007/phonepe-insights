import base64
import streamlit as st
from utils import *
from PIL import Image
from io import BytesIO
from fpdf import FPDF
from utils import generate_gemini_insight as generate_insight_summary


# --- Page Setup ---
st.set_page_config(page_title="📱 PhonePe Pulse Dashboard", layout="wide")

# --- Branding / Logo ---
logo = Image.open("dashboard/assets/phonepe_logo.jpg")
st.image(logo, width=150)
st.title("📱 PhonePe Pulse Dashboard")
st.markdown("Track, Explore, and Visualize Digital Payment Trends in India")

# --- Sidebar Navigation ---
st.sidebar.title("🧭 Navigation")
selected_tab = st.sidebar.radio("Go to Section", ["🗺️ Overall Geo", "📍 District View", "📆 Year & Month Trends", "🤖 AI Insights"])

# --- Tab 1: Overall Geo ---
if selected_tab == "🗺️ Overall Geo":
    st.subheader("🗺️ Geo-level Overview of Transactions and Users")

    col1, col2 = st.columns(2)
    with col1:
        year = st.selectbox("📅 Select Year", get_years(), index=len(get_years()) - 1, key="map_year")
    with col2:
        quarter = st.selectbox("📆 Select Quarter", [1, 2, 3, 4], index=3, key="map_quarter")

    st.plotly_chart(plot_geo_transaction(year, quarter), use_container_width=True)
    st.divider()

    st.markdown("### 📊 Total Transactions and Registered Users by State")
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(plot_total_transaction_by_state(), use_container_width=True)
    with col4:
        st.plotly_chart(plot_total_users_by_state(), use_container_width=True)

# --- Tab 2: District-wise ---
elif selected_tab == "📍 District View":
    st.subheader("📍 State-wise District Insights")

    state = st.selectbox("🏙️ Select State", get_states(), key="district_state")

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(plot_district_transactions(state), use_container_width=True)
    with col2:
        st.plotly_chart(plot_district_users(state), use_container_width=True)

# --- Tab 3: Quarterly Trends ---
elif selected_tab == "📆 Year & Month Trends":
    st.subheader("📆 Quarterly Trends and Insights")

    col1, col2 = st.columns(2)
    with col1:
        state = st.selectbox("🏙️ Select State", get_states(), key="q_state")
    with col2:
        year = st.selectbox("📅 Select Year", get_years(), key="q_year")

    st.markdown("#### 📈 Quarterly Breakdown")
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(plot_quarterly_transactions(state, year), use_container_width=True)
    with col4:
        st.plotly_chart(plot_quarterly_app_opens(state, year), use_container_width=True)

    st.divider()
    st.markdown("#### 🔍 Transaction Type Insights")
    st.plotly_chart(get_transaction_insights(state, year), use_container_width=True)

# --- Tab 4: AI Insights using Gemini ---

elif selected_tab == "🤖 AI Insights":
    st.subheader("🧠 AI-Powered Insight Summary")

    col1, col2, col3 = st.columns(3)
    with col1:
        state = st.selectbox("🏙️ Select State", get_states(), key="ai_state")
    with col2:
        year = st.selectbox("📅 Select Year", get_years(), key="ai_year")
    with col3:
        quarter = st.selectbox("📆 Select Quarter", [1, 2, 3, 4], key="ai_quarter")

    if st.button("🔍 Generate AI Insight"):
        with st.spinner("Generating insight from Gemini..."):
            insight = generate_insight_summary(state, year, quarter)

        st.markdown("### 📄 Summary Report")
        st.success(insight)

        # 📄 PDF Generation with Unicode (Emoji) Support
        class PDF(FPDF):
            def header(self):
                self.set_font("DejaVu", '', 14)
                self.cell(0, 10, "📊 PhonePe AI Insight Report", ln=True, align="C")
                self.ln(10)

            def footer(self):
                self.set_y(-15)
                self.set_font("DejaVu", '', 8)
                self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

        # Create PDF
        pdf = PDF()
        
        # Add DejaVu Unicode Font
        font_path = os.path.join("dashboard", "assets", "dejavu-fonts-ttf-2.37", "ttf", "DejaVuSans.ttf")
        pdf.add_font("DejaVu", "", font_path, uni=True)  # Must come BEFORE pdf.add_page()
        pdf.set_font("DejaVu", "", 12)

        pdf.add_page()
        pdf.multi_cell(0, 10, f"📊 PhonePe AI Insight Report\n\nState: {state}\nYear: {year}\nQuarter: Q{quarter}\n\n{insight}")

        # Save to file
        pdf_path = f"insight_{state}_{year}_Q{quarter}.pdf"
        pdf.output(pdf_path)

        # Show download button
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="⬇️ Download PDF Report",
                data=f,
                file_name=pdf_path,
                mime="application/pdf"
            )

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 PhonePe Pulse Dashboard | Made by Kunal Jadhav ❤️", unsafe_allow_html=True)

