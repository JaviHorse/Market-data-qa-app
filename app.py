import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import altair as alt
from io import BytesIO
from google import genai


# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="AI-Assisted Market Data QA",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------
# Custom CSS
# -----------------------------
st.markdown(
    """
    <style>
    /* Import clean corporate-style typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Main app background */
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(37, 99, 235, 0.10), transparent 30%),
            linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
    }

    /* Hide default Streamlit clutter */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Page spacing */
    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #111827 55%, #1e293b 100%);
        border-right: 1px solid rgba(148, 163, 184, 0.18);
    }

    section[data-testid="stSidebar"] * {
        color: #e5e7eb !important;
    }

    section[data-testid="stSidebar"] input,
    section[data-testid="stSidebar"] textarea,
    section[data-testid="stSidebar"] select {
        background-color: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(203, 213, 225, 0.24) !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }

    section[data-testid="stSidebar"] .stSlider {
        padding-top: 0.35rem;
        padding-bottom: 0.35rem;
    }

    /* Corporate hero */
    .hero-card {
        position: relative;
        overflow: hidden;
        border-radius: 28px;
        padding: 34px 38px;
        margin-bottom: 28px;
        background:
            linear-gradient(135deg, rgba(15, 23, 42, 0.98) 0%, rgba(30, 64, 175, 0.92) 58%, rgba(14, 165, 233, 0.82) 100%);
        box-shadow: 0 24px 70px rgba(15, 23, 42, 0.24);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    .hero-card:before {
        content: "";
        position: absolute;
        top: -90px;
        right: -90px;
        width: 280px;
        height: 280px;
        background: rgba(255, 255, 255, 0.12);
        border-radius: 999px;
    }

    .hero-card:after {
        content: "";
        position: absolute;
        bottom: -110px;
        left: 50%;
        width: 360px;
        height: 360px;
        background: rgba(59, 130, 246, 0.18);
        border-radius: 999px;
    }

    .hero-content {
        position: relative;
        z-index: 1;
        max-width: 980px;
    }

    .eyebrow {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.18);
        color: #dbeafe;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 18px;
    }

    .hero-title {
        color: #ffffff;
        font-size: 42px;
        line-height: 1.05;
        font-weight: 800;
        letter-spacing: -0.04em;
        margin-bottom: 14px;
    }

    .hero-subtitle {
        color: #dbeafe;
        font-size: 17px;
        line-height: 1.65;
        max-width: 900px;
        margin-bottom: 22px;
    }

    .hero-badges {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
    }

    .hero-badge {
        padding: 9px 12px;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.11);
        border: 1px solid rgba(255, 255, 255, 0.16);
        color: #eff6ff;
        font-size: 13px;
        font-weight: 600;
    }

    /* Section headers */
    .section-heading {
        margin-top: 10px;
        margin-bottom: 16px;
    }

    .section-kicker {
        color: #2563eb;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .section-title {
        color: #0f172a;
        font-size: 25px;
        line-height: 1.2;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 4px;
    }

    .section-caption {
        color: #64748b;
        font-size: 14px;
        line-height: 1.55;
    }

    /* Professional cards */
    .soft-card {
        background: rgba(255, 255, 255, 0.88);
        border: 1px solid rgba(203, 213, 225, 0.78);
        border-radius: 22px;
        padding: 22px;
        box-shadow: 0 12px 34px rgba(15, 23, 42, 0.07);
        margin-bottom: 18px;
    }

    .upload-help-box {
        border: 1px solid rgba(37, 99, 235, 0.18);
        background:
            linear-gradient(135deg, rgba(239, 246, 255, 0.96), rgba(255, 255, 255, 0.96));
        padding: 20px 22px;
        border-radius: 22px;
        margin-bottom: 16px;
        box-shadow: 0 10px 26px rgba(37, 99, 235, 0.06);
        color: #1e293b;
        line-height: 1.65;
    }

    .format-pill {
        display: inline-block;
        margin-top: 10px;
        padding: 8px 12px;
        background: #0f172a;
        color: #f8fafc;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.02em;
    }

    /* Streamlit widgets */
    div[data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.88);
        border: 1px dashed rgba(37, 99, 235, 0.35);
        border-radius: 22px;
        padding: 16px;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.06);
    }

    div[data-testid="stFileUploader"] section {
        border: none !important;
        background: transparent !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 16px !important;
        border: 0 !important;
        padding: 0.78rem 1.1rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.01em !important;
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 45%, #0284c7 100%) !important;
        color: white !important;
        box-shadow: 0 14px 28px rgba(37, 99, 235, 0.22) !important;
        transition: all 0.18s ease-in-out !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 18px 34px rgba(37, 99, 235, 0.30) !important;
    }

    .stButton > button:disabled {
        background: #cbd5e1 !important;
        color: #64748b !important;
        box-shadow: none !important;
        transform: none !important;
    }

    /* Metric cards */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid rgba(203, 213, 225, 0.7);
        border-radius: 20px;
        padding: 18px 18px 16px 18px;
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.07);
    }

    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-weight: 700 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-weight: 800 !important;
        letter-spacing: -0.04em;
    }

    /* Dataframes and charts */
    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;
        border: 1px solid rgba(203, 213, 225, 0.70);
        box-shadow: 0 12px 30px rgba(15, 23, 42, 0.06);
    }

    div[data-testid="stExpander"] {
        border-radius: 18px !important;
        border: 1px solid rgba(203, 213, 225, 0.75) !important;
        background: rgba(255, 255, 255, 0.85) !important;
        box-shadow: 0 10px 24px rgba(15, 23, 42, 0.04);
    }

    /* Loading overlay */
    .ai-loading-overlay {
        position: fixed;
        z-index: 9999;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background:
            radial-gradient(circle at top, rgba(59, 130, 246, 0.30), transparent 30%),
            rgba(15, 23, 42, 0.72);
        backdrop-filter: blur(8px);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .ai-loading-card {
        background: rgba(255, 255, 255, 0.96);
        padding: 34px;
        border-radius: 26px;
        width: 440px;
        box-shadow: 0 28px 80px rgba(0, 0, 0, 0.35);
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.80);
    }

    .ai-spinner {
        margin: 0 auto 20px auto;
        width: 58px;
        height: 58px;
        border: 6px solid #e2e8f0;
        border-top: 6px solid #2563eb;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .ai-loading-title {
        font-size: 22px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
        letter-spacing: -0.03em;
    }

    .ai-loading-text {
        font-size: 15px;
        color: #475569;
        line-height: 1.6;
    }

    /* Make warnings/info feel less default */
    div[data-testid="stAlert"] {
        border-radius: 18px;
        border: 1px solid rgba(203, 213, 225, 0.75);
    }

    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .hero-card {
            padding: 26px 24px;
            border-radius: 22px;
        }

        .hero-title {
            font-size: 32px;
        }

        .hero-subtitle {
            font-size: 15px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)


def section_header(kicker, title, caption=""):
    st.markdown(
        f"""
        <div class="section-heading">
            <div class="section-kicker">{kicker}</div>
            <div class="section-title">{title}</div>
            <div class="section-caption">{caption}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def count_bar_chart(series, category_name, value_name="Records"):
    chart_df = (
        series
        .value_counts()
        .rename_axis(category_name)
        .reset_index(name=value_name)
    )

    chart = (
        alt.Chart(chart_df)
        .mark_bar(cornerRadiusTopRight=8, cornerRadiusBottomRight=8)
        .encode(
            x=alt.X(f"{value_name}:Q", title=value_name, axis=alt.Axis(grid=False)),
            y=alt.Y(f"{category_name}:N", title=None, sort="-x"),
            tooltip=[
                alt.Tooltip(f"{category_name}:N", title=category_name),
                alt.Tooltip(f"{value_name}:Q", title=value_name)
            ]
        )
        .properties(height=285)
        .configure_view(strokeWidth=0)
        .configure_axis(labelColor="#475569", titleColor="#64748b", labelFontSize=12, titleFontSize=12)
    )

    st.altair_chart(chart, use_container_width=True)


def risk_line_chart(df):
    chart_df = df.copy()
    chart_df["Date"] = pd.to_datetime(chart_df["Date"], errors="coerce")

    chart = (
        alt.Chart(chart_df)
        .mark_line(point=True, strokeWidth=2.5)
        .encode(
            x=alt.X("Date:T", title="Date"),
            y=alt.Y("ML_Risk_Probability_%:Q", title="ML Risk Probability (%)"),
            tooltip=[
                alt.Tooltip("Date:T", title="Date"),
                alt.Tooltip("ML_Risk_Probability_%:Q", title="ML Risk Probability", format=".2f")
            ]
        )
        .properties(height=320)
        .configure_view(strokeWidth=0)
        .configure_axis(labelColor="#475569", titleColor="#64748b", labelFontSize=12, titleFontSize=12)
    )

    st.altair_chart(chart, use_container_width=True)


st.markdown(
    """
    <div class="hero-card">
        <div class="hero-content">
            <div class="eyebrow">Market Data Quality Assurance</div>
            <div class="hero-title">AI-Assisted Equity Market Data QA System</div>
            <div class="hero-subtitle">
                A corporate-grade review workflow for historical equity data: automated cleaning,
                vendor variance simulation, abnormal movement checks, ML-based review prioritization,
                and AI-generated analyst investigation notes.
            </div>
            <div class="hero-badges">
                <span class="hero-badge">Vendor Variance Analysis</span>
                <span class="hero-badge">ML Review Classifier</span>
                <span class="hero-badge">Volume Spike Detection</span>
                <span class="hero-badge">AI Analyst Notes</span>
                <span class="hero-badge">Excel Export</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# -----------------------------
# How-To Pop-Up
# -----------------------------
def show_how_to_content():
    st.markdown(
        """
        ### How to use this app

        **Step 1: Upload a historical equity market data CSV file**  
        Upload a 1-year historical stock data file. The preferred format is similar to historical data exported from **Investing.com**.

        **Recommended CSV columns:**
        ```text
        Date, Price, Open, High, Low, Vol., Change %
        ```

        **Step 2: Enter the ticker and company name**  
        Use the sidebar to specify the uploaded stock’s ticker and company name.

        **Step 3: Review the automatic QA results**  
        The app will clean the file, simulate a second vendor source, calculate vendor variance, detect abnormal returns, identify volume spikes, and run the ML review classifier.

        **Step 4: Click “Generate AI Analyst Notes”**  
        This generates AI-written investigation notes for the top highest-risk records only. The notes will appear in the `Analyst_Review_Note` column.

        **Step 5: Check the `Note_Source` column**  
        This tells you whether each note came from:
        - `Rule-Based`
        - `Gemini Generated`
        - `Gemini Failed - Rule-Based Fallback`

        **Step 6: Download the scored output**  
        Export the QA-scored Excel file with all flags, ML scores, risk bands, and analyst notes.
        """
    )


if "show_intro_modal" not in st.session_state:
    st.session_state.show_intro_modal = True

if "generate_ai_notes" not in st.session_state:
    st.session_state.generate_ai_notes = False

if hasattr(st, "dialog"):
    @st.dialog("Welcome: How to Use the Market Data QA App")
    def intro_dialog():
        show_how_to_content()
        if st.button("Got it — start using the app", type="primary"):
            st.session_state.show_intro_modal = False
            st.rerun()

    if st.session_state.show_intro_modal:
        intro_dialog()
else:
    with st.expander("How to use this app", expanded=True):
        show_how_to_content()


# -----------------------------
# Load Model
# -----------------------------
@st.cache_resource
def load_model_and_features():
    model = joblib.load("market_data_qa_model.pkl")

    with open("model_features.json", "r") as f:
        model_features = json.load(f)

    return model, model_features


try:
    model, model_features = load_model_and_features()
except Exception:
    st.error(
        "Model files could not be loaded. Make sure market_data_qa_model.pkl and model_features.json are in the same folder as app.py."
    )
    st.stop()


# -----------------------------
# Helper Functions
# -----------------------------
def clean_numeric(value):
    if pd.isna(value):
        return np.nan

    value = str(value).strip()
    value = value.replace(",", "")
    value = value.replace("%", "")
    value = value.replace("$", "")

    if value in ["", "-", "nan", "NaN", "None"]:
        return np.nan

    return pd.to_numeric(value, errors="coerce")


def clean_volume(value):
    if pd.isna(value):
        return np.nan

    value = str(value).strip().upper()
    value = value.replace(",", "")

    if value in ["", "-", "NAN", "NONE"]:
        return np.nan

    if value.endswith("M"):
        return pd.to_numeric(value.replace("M", ""), errors="coerce") * 1_000_000

    if value.endswith("B"):
        return pd.to_numeric(value.replace("B", ""), errors="coerce") * 1_000_000_000

    if value.endswith("K"):
        return pd.to_numeric(value.replace("K", ""), errors="coerce") * 1_000

    return pd.to_numeric(value, errors="coerce")


def assign_issue_type(row):
    issues = []

    if row["Vendor Mismatch Flag"] == "Vendor Mismatch":
        issues.append("Vendor Mismatch")

    if row["Abnormal Return Flag"] == "Abnormal Return":
        issues.append("Abnormal Return")

    if row["Volume Spike Flag"] == "Volume Spike":
        issues.append("Volume Spike")

    if len(issues) == 0:
        return "Clean"

    return ", ".join(issues)


def calculate_quality_score(row):
    score = 100

    if row["Vendor Mismatch Flag"] == "Vendor Mismatch":
        score -= 15

    if row["Abnormal Return Flag"] == "Abnormal Return":
        score -= 10

    if row["Volume Spike Flag"] == "Volume Spike":
        score -= 5

    return score


def assign_risk_level(score):
    if score < 80:
        return "High Risk"
    elif score < 95:
        return "Medium Risk"
    else:
        return "Low Risk"


def assign_ml_risk_band(prob):
    if prob >= 0.75:
        return "High ML Risk"
    elif prob >= 0.40:
        return "Medium ML Risk"
    else:
        return "Low ML Risk"


def generate_basic_analyst_note(row):
    reasons = []

    if row["Vendor Mismatch Flag"] == "Vendor Mismatch":
        reasons.append("vendor price variance exceeded the tolerance threshold")

    if row["Abnormal Return Flag"] == "Abnormal Return":
        reasons.append("daily return exceeded the abnormal movement threshold")

    if row["Volume Spike Flag"] == "Volume Spike":
        reasons.append("trading volume was more than 2x the recent 30-day average")

    if row["ML_Risk_Probability"] >= 0.75:
        model_text = "The model assigned a high review probability"
    elif row["ML_Risk_Probability"] >= 0.40:
        model_text = "The model assigned a medium review probability"
    else:
        model_text = "The model assigned a low review probability"

    if len(reasons) == 0:
        return f"{model_text}. No major rule-based issue was detected."

    return (
        f"{model_text} because "
        + ", ".join(reasons)
        + ". Recommended action: verify the price, volume, and relevant market event context."
    )


def generate_gemini_analyst_note(row):
    try:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

        prompt = f"""
You are assisting a market data quality analyst.

Generate a concise analyst investigation note for this equity market data record.

Context:
This system is for market data quality assurance, not investment recommendation.
The goal is to help analysts validate suspicious equity market data records before they are used in analytics or reporting.

Record:
Company: {row['Company']}
Ticker: {row['Ticker']}
Date: {row['Date']}
Close Price Vendor A: {row['Vendor_A_Close']}
Close Price Vendor B: {row['Vendor_B_Close']}
Vendor Variance %: {row['Vendor Variance %']:.4%}
Daily Change %: {row['Change %']:.4%}
Volume Numeric: {row['Volume Numeric']}
Issue Type: {row['Issue Type']}
Rule-Based Risk Level: {row['Risk Level']}
ML Risk Probability: {row['ML_Risk_Probability_%']:.2f}%
ML Risk Band: {row['ML_Risk_Band']}

Write one short paragraph under 80 words.

Explain:
1. Why this record may need review
2. What the analyst should validate next

Rules:
- Do not give investment advice.
- Do not say buy, sell, hold, bullish, or bearish.
- Focus only on data quality, vendor variance, abnormal return behavior, volume behavior, and validation steps.
"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        note = response.text.strip()

        if not note:
            return row["Analyst_Review_Note"], "Gemini Failed - Empty Response"

        return note, "Gemini Generated"

    except Exception as e:
        fallback_note = row["Analyst_Review_Note"]
        return fallback_note, f"Gemini Failed: {str(e)[:100]}"


def convert_df_to_excel(df):
    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="QA Scored Output")

    return output.getvalue()


# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.markdown("## Configuration Panel")
st.sidebar.caption("Set the market-data parameters before running the QA workflow.")
st.sidebar.markdown("---")
st.sidebar.markdown("### Security & Instrument")
ticker_input = st.sidebar.text_input("Ticker", value="AXP")
company_input = st.sidebar.text_input("Company Name", value="American Express")

st.sidebar.markdown("---")
st.sidebar.markdown("### QA Thresholds")
vendor_mismatch_threshold = st.sidebar.slider(
    "Vendor Mismatch Threshold",
    min_value=0.005,
    max_value=0.05,
    value=0.01,
    step=0.005,
    format="%.3f"
)

abnormal_return_threshold = st.sidebar.slider(
    "Abnormal Return Threshold",
    min_value=0.02,
    max_value=0.15,
    value=0.05,
    step=0.01,
    format="%.2f"
)

volume_spike_multiplier = st.sidebar.slider(
    "Volume Spike Multiplier",
    min_value=1.5,
    max_value=5.0,
    value=2.0,
    step=0.5
)

st.sidebar.markdown("---")
st.sidebar.markdown("### AI Note Generation")

max_ai_note_rows = st.sidebar.slider(
    "Max rows for AI Analyst Notes",
    min_value=3,
    max_value=20,
    value=5,
    step=1
)


# -----------------------------
# File Upload
# -----------------------------
section_header("Input", "Upload Historical Equity Market Data", "Use an Investing.com-style CSV export or any file with the required historical price columns.")

st.markdown(
    """
    <div class="upload-help-box">
        <b>Recommended source:</b> Investing.com historical data export or any CSV following the same structure.<br>
        <b>Preferred columns:</b> Date, Price, Open, High, Low, Vol., Change %
        <br>
        <span class="format-pill">Required schema: Date · Price · Open · High · Low · Vol. · Change %</span>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload historical stock data CSV",
    type=["csv"]
)

generate_ai_notes_clicked = st.button(
    "✨ Generate AI Analyst Notes",
    type="primary",
    use_container_width=True,
    disabled=uploaded_file is None
)

if generate_ai_notes_clicked:
    st.session_state.generate_ai_notes = True

if uploaded_file is None:
    st.warning("Upload a CSV file to begin.")
    st.stop()


# -----------------------------
# Load Uploaded Data
# -----------------------------
try:
    raw_df = pd.read_csv(uploaded_file)
    raw_df.columns = raw_df.columns.str.strip()
except Exception:
    st.error("Could not read the uploaded CSV file.")
    st.stop()


required_cols = ["Date", "Price", "Open", "High", "Low", "Vol.", "Change %"]

missing_cols = [col for col in required_cols if col not in raw_df.columns]

if missing_cols:
    st.error(f"Missing required columns: {missing_cols}")
    st.stop()


section_header("Preview", "Uploaded Data Preview", "First 10 rows from the uploaded file before QA processing.")
st.dataframe(raw_df.head(10), use_container_width=True)


# -----------------------------
# Data Cleaning and Standardization
# -----------------------------
stock_df = raw_df.copy()

stock_df["Date"] = pd.to_datetime(stock_df["Date"], errors="coerce")

stock_df["Close Price"] = stock_df["Price"].apply(clean_numeric)

for col in ["Open", "High", "Low"]:
    stock_df[col] = stock_df[col].apply(clean_numeric)

stock_df["Volume Numeric"] = stock_df["Vol."].apply(clean_volume)

stock_df["Change %"] = stock_df["Change %"].apply(clean_numeric) / 100

stock_df["Ticker"] = ticker_input
stock_df["Company"] = company_input

stock_df = stock_df.dropna(subset=["Date", "Close Price"])

if stock_df.empty:
    st.error("No valid rows remain after cleaning. Please check your file format.")
    st.stop()


# -----------------------------
# Simulate Vendor B
# -----------------------------
np.random.seed(42)

stock_df["Vendor_A_Close"] = stock_df["Close Price"]

normal_noise = np.random.normal(
    loc=0,
    scale=0.0015,
    size=len(stock_df)
)

stock_df["Vendor_B_Close"] = stock_df["Vendor_A_Close"] * (1 + normal_noise)

mismatch_rate = 0.05
num_mismatches = max(1, int(len(stock_df) * mismatch_rate))

mismatch_indices = np.random.choice(
    stock_df.index,
    size=num_mismatches,
    replace=False
)

stock_df.loc[mismatch_indices, "Vendor_B_Close"] = (
    stock_df.loc[mismatch_indices, "Vendor_A_Close"]
    * (
        1
        + np.random.choice([-1, 1], size=num_mismatches)
        * np.random.uniform(0.012, 0.025, size=num_mismatches)
    )
)

stock_df["Vendor Variance %"] = (
    abs(stock_df["Vendor_A_Close"] - stock_df["Vendor_B_Close"])
    / stock_df["Vendor_A_Close"]
)


# -----------------------------
# Rule-Based QA Checks
# -----------------------------
stock_df = stock_df.sort_values("Date")

stock_df["Rolling_30D_Avg_Volume_For_Rules"] = (
    stock_df["Volume Numeric"]
    .rolling(window=30, min_periods=1)
    .mean()
)

stock_df["Vendor Mismatch Flag"] = np.where(
    stock_df["Vendor Variance %"] > vendor_mismatch_threshold,
    "Vendor Mismatch",
    "OK"
)

stock_df["Abnormal Return Flag"] = np.where(
    stock_df["Change %"].abs() > abnormal_return_threshold,
    "Abnormal Return",
    "Normal"
)

stock_df["Volume Spike Flag"] = np.where(
    stock_df["Volume Numeric"] > stock_df["Rolling_30D_Avg_Volume_For_Rules"] * volume_spike_multiplier,
    "Volume Spike",
    "Normal"
)

stock_df["Issue Type"] = stock_df.apply(assign_issue_type, axis=1)
stock_df["Quality Score"] = stock_df.apply(calculate_quality_score, axis=1)
stock_df["Risk Level"] = stock_df["Quality Score"].apply(assign_risk_level)


# -----------------------------
# ML Feature Engineering
# -----------------------------
stock_df["Rolling_7D_Avg_Volume"] = (
    stock_df["Volume Numeric"]
    .rolling(window=7, min_periods=1)
    .mean()
)

stock_df["Rolling_30D_Avg_Volume"] = (
    stock_df["Volume Numeric"]
    .rolling(window=30, min_periods=1)
    .mean()
)

stock_df["Rolling_7D_Return_Volatility"] = (
    stock_df["Change %"]
    .rolling(window=7, min_periods=2)
    .std()
)

stock_df["Rolling_30D_Return_Volatility"] = (
    stock_df["Change %"]
    .rolling(window=30, min_periods=2)
    .std()
)

stock_df["Previous_Day_Change"] = stock_df["Change %"].shift(1)

stock_df["Volume_vs_30D_Avg"] = (
    stock_df["Volume Numeric"] / stock_df["Rolling_30D_Avg_Volume"]
)

rolling_cols = [
    "Rolling_7D_Avg_Volume",
    "Rolling_30D_Avg_Volume",
    "Rolling_7D_Return_Volatility",
    "Rolling_30D_Return_Volatility",
    "Previous_Day_Change",
    "Volume_vs_30D_Avg"
]

stock_df[rolling_cols] = stock_df[rolling_cols].fillna(0)


# -----------------------------
# ML Prediction
# -----------------------------
try:
    X_new = stock_df[model_features].copy()
except KeyError as e:
    st.error(f"The uploaded file could not produce all model features: {e}")
    st.stop()

stock_df["ML_Review_Prediction"] = model.predict(X_new)
stock_df["ML_Risk_Probability"] = model.predict_proba(X_new)[:, 1]

stock_df["ML_Review_Label"] = stock_df["ML_Review_Prediction"].map({
    0: "Clean / Low Priority",
    1: "Needs Analyst Review"
})

stock_df["ML_Risk_Probability_%"] = stock_df["ML_Risk_Probability"] * 100
stock_df["ML_Risk_Band"] = stock_df["ML_Risk_Probability"].apply(assign_ml_risk_band)

# First generate rule-based notes for all records
stock_df["Analyst_Review_Note"] = stock_df.apply(generate_basic_analyst_note, axis=1)
stock_df["Note_Source"] = "Rule-Based"


# -----------------------------
# Optional AI Analyst Notes
# -----------------------------
if st.session_state.generate_ai_notes:
    if "GEMINI_API_KEY" not in st.secrets:
        st.warning("No Gemini API key found. Add GEMINI_API_KEY to .streamlit/secrets.toml.")
    else:
        overlay = show_loading_overlay(max_ai_note_rows)

        top_ai_indices = (
            stock_df.sort_values("ML_Risk_Probability", ascending=False)
            .head(max_ai_note_rows)
            .index
        )

        for idx in top_ai_indices:
            ai_note, note_source = generate_gemini_analyst_note(stock_df.loc[idx])
            stock_df.loc[idx, "Analyst_Review_Note"] = ai_note
            stock_df.loc[idx, "Note_Source"] = note_source

        overlay.empty()

        generated_count = int((stock_df["Note_Source"] == "Gemini Generated").sum())

        if generated_count > 0:
            st.success(
                f"AI analyst notes generated for {generated_count} record(s). Check the Note_Source column."
            )
        else:
            st.warning(
                "Gemini did not generate any notes. Check the Note_Source column for the error message."
            )

        st.session_state.generate_ai_notes = False


# -----------------------------
# Dashboard Summary
# -----------------------------
section_header("Executive Summary", "Market Data QA Summary", "High-level QA counts, model risk, and AI note coverage.")

total_records = len(stock_df)
rule_flagged_records = int((stock_df["Issue Type"] != "Clean").sum())
ml_review_records = int((stock_df["ML_Review_Label"] == "Needs Analyst Review").sum())
avg_quality_score = stock_df["Quality Score"].mean()
avg_ml_risk = stock_df["ML_Risk_Probability_%"].mean()
vendor_mismatch_count = int((stock_df["Vendor Mismatch Flag"] == "Vendor Mismatch").sum())
abnormal_return_count = int((stock_df["Abnormal Return Flag"] == "Abnormal Return").sum())
volume_spike_count = int((stock_df["Volume Spike Flag"] == "Volume Spike").sum())
ai_notes_count = int((stock_df["Note_Source"] == "Gemini Generated").sum())

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Records Checked", f"{total_records:,}")
col2.metric("Rule-Based Flagged Records", f"{rule_flagged_records:,}")
col3.metric("ML Review Records", f"{ml_review_records:,}")
col4.metric("AI Notes Generated", f"{ai_notes_count:,}")

col5, col6, col7, col8 = st.columns(4)

col5.metric("Average ML Risk", f"{avg_ml_risk:.2f}%")
col6.metric("Vendor Mismatches", f"{vendor_mismatch_count:,}")
col7.metric("Abnormal Returns", f"{abnormal_return_count:,}")
col8.metric("Volume Spikes", f"{volume_spike_count:,}")


# -----------------------------
# Charts
# -----------------------------
section_header("Diagnostics", "QA Breakdown", "Breakdown of rule-based flags, ML risk bands, note sources, and risk levels.")

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("#### Issue Type Breakdown")
    count_bar_chart(stock_df["Issue Type"], "Issue Type")

with chart_col2:
    st.markdown("#### ML Risk Band Distribution")
    count_bar_chart(stock_df["ML_Risk_Band"], "ML Risk Band")


chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.markdown("#### Note Source Breakdown")
    count_bar_chart(stock_df["Note_Source"], "Note Source")

with chart_col4:
    st.markdown("#### Risk Level Distribution")
    count_bar_chart(stock_df["Risk Level"], "Risk Level")


st.markdown("#### ML Risk Probability Over Time")

risk_time_df = stock_df[["Date", "ML_Risk_Probability_%"]].copy()
risk_line_chart(risk_time_df)


# -----------------------------
# Review Queue
# -----------------------------
section_header("Review Queue", "AI-Assisted Analyst Review Queue", "Records are sorted by ML risk probability so analysts can prioritize the highest-risk rows first.")

review_queue = stock_df[
    [
        "Date",
        "Ticker",
        "Company",
        "Close Price",
        "Vendor_B_Close",
        "Vendor Variance %",
        "Change %",
        "Volume Numeric",
        "Issue Type",
        "Risk Level",
        "ML_Review_Label",
        "ML_Risk_Probability_%",
        "ML_Risk_Band",
        "Note_Source",
        "Analyst_Review_Note"
    ]
].copy()

review_queue = review_queue.sort_values(
    by="ML_Risk_Probability_%",
    ascending=False
)

st.dataframe(review_queue, use_container_width=True)


# -----------------------------
# Download Output
# -----------------------------
section_header("Export", "Download Scored Output", "Download the complete QA-scored dataset with all flags, model scores, risk bands, and analyst notes.")

excel_data = convert_df_to_excel(stock_df)

st.download_button(
    label="Download QA-Scored Excel File",
    data=excel_data,
    file_name=f"{ticker_input}_Market_Data_QA_Scored_Output.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


# -----------------------------
# Methodology Note
# -----------------------------
with st.expander("Methodology Note"):
    st.markdown(
        """
        This system is designed for market data quality assurance, not investment recommendation.

        The app performs:
        - Market data cleaning and standardization
        - Simulated vendor-source comparison
        - Vendor variance detection
        - Abnormal return detection
        - Volume spike detection
        - ML-based analyst review classification
        - Optional AI-generated analyst investigation notes using Gemini
        - Review queue generation

        Since public historical stock files usually contain only one price source, Vendor B is simulated for portfolio demonstration purposes.
        The purpose is to demonstrate the workflow of vendor variance analysis and market data QA.

        Recommended input format:
        ```text
        Date, Price, Open, High, Low, Vol., Change %
        ```

        This format is similar to many historical stock data exports, including Investing.com-style historical data files.
        """
    )