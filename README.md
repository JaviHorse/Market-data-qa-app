# AI-Assisted Market Data Quality & Vendor Variance Monitor

An AI-assisted market data quality assurance system designed to simulate how equity market data teams validate, monitor, and prioritize financial data records before they are used in analytics, reporting, or client-facing investment tools.

This project was built to demonstrate workflows similar to those used in **Instrument Data Management**, including equity market data QA, vendor-source comparison, data discrepancy detection, abnormal market behavior flagging, analyst review prioritization, and AI-assisted operational automation.

---

## Project Overview

This project has two main components:

1. **Market Data Quality Dashboard**

   * Monitors equity market data quality across historical stock records.
   * Flags vendor price mismatches, abnormal returns, volume spikes, and high-risk records.
   * Provides dashboard pages for overall data health, vendor consistency analysis, company-level investigation, and analyst review queues.

2. **Python/Streamlit ML Review App**

   * Lets users upload historical equity CSV files.
   * Cleans and standardizes the uploaded data.
   * Simulates a second vendor price source for vendor variance analysis.
   * Flags suspicious market data records using rule-based QA checks.
   * Uses a trained scikit-learn classifier to assign ML risk probabilities.
   * Generates analyst review queues with issue types, quality scores, risk bands, and review priorities.
   * Uses Gemini API to generate AI-assisted analyst investigation notes for high-risk records.
   * Allows users to download the final QA-scored output as an Excel file.

---

## Why This Project Exists

Financial market data is not automatically trustworthy. Before data is used in index products, investment analytics, reporting systems, or client-facing tools, it needs to be validated.

This project answers the question:

> Can this equity market data be trusted before it is used for investment analytics or financial database workflows?

Instead of building a generic stock prediction project, this project focuses on the operational side of financial data:

* Is the price data consistent across vendor sources?
* Are there abnormal daily returns that may need investigation?
* Are there unusual volume spikes?
* Which records should analysts review first?
* Can AI help summarize why a record was flagged?

---

## Key Features

### Market Data Upload

Users can upload a historical equity CSV file following this preferred format:

```text
Date, Price, Open, High, Low, Vol., Change %
```

The format is compatible with common historical stock data exports, such as Investing.com-style CSV files.

---

### Data Cleaning and Standardization

The app automatically:

* Converts price fields into numeric values.
* Converts volume values such as `2.41M`, `890K`, or `1.2B` into numeric volume.
* Converts percentage fields into decimal format.
* Standardizes the uploaded file into the same structure used by the ML model.
* Removes invalid rows where core fields such as date or close price cannot be read.

---

### Vendor-Source Simulation

Public historical stock files usually contain only one price source. To simulate a real market data QA workflow, the app creates a second vendor source:

* `Vendor_A_Close` = original close price from the uploaded file
* `Vendor_B_Close` = simulated second vendor price source

Most simulated vendor prices remain close to Vendor A, while a small percentage intentionally contains larger differences to demonstrate vendor variance detection.

This is used to simulate workflows such as:

* Vendor price comparison
* Source-to-source variance analysis
* Data discrepancy detection
* Analyst investigation prioritization

---

### Rule-Based QA Checks

The system applies market data quality rules to identify suspicious records.

It checks for:

#### Vendor Price Mismatch

Flags records where the difference between Vendor A and Vendor B exceeds the selected threshold.

```text
Vendor Variance % = ABS(Vendor_A_Close - Vendor_B_Close) / Vendor_A_Close
```

#### Abnormal Return

Flags records where the absolute daily return exceeds the selected threshold.

#### Volume Spike

Flags records where trading volume is significantly higher than the recent rolling average.

#### Issue Type

Each row receives an issue classification such as:

* Clean
* Vendor Mismatch
* Abnormal Return
* Volume Spike
* Multiple issue combinations

#### Quality Score

Each record receives a quality score based on detected issues.

Example logic:

```text
Start at 100
Vendor mismatch: -15
Abnormal return: -10
Volume spike: -5
```

#### Risk Level

Quality scores are translated into:

* Low Risk
* Medium Risk
* High Risk

---

## Machine Learning Layer

The project includes a trained scikit-learn model that predicts whether a market data record should be prioritized for analyst review.

### Model Type

The app uses a trained **Random Forest Classifier**.

### Model Objective

The model predicts:

```text
Clean / Low Priority
Needs Analyst Review
```

### Model Inputs

The model uses engineered market data features such as:

* Open
* High
* Low
* Close Price
* Vendor A close
* Vendor B close
* Volume Numeric
* Change %
* Vendor Variance %
* Rolling 7-day average volume
* Rolling 30-day average volume
* Rolling 7-day return volatility
* Rolling 30-day return volatility
* Previous day change
* Volume vs 30-day average

### Model Outputs

The app produces:

* ML review prediction
* ML risk probability
* ML risk band
* Analyst review queue

The model is not used to predict stock prices. Its purpose is to support market data quality review and prioritize suspicious records for analyst investigation.

---

## AI Analyst Notes

The app integrates the **Gemini API** to generate analyst-style investigation notes for high-risk records.

The generated notes summarize:

* Why the record may need review
* Which data quality issue was detected
* What the analyst should validate next

The AI notes focus only on market data quality and validation. They do not provide investment advice.

Each row includes a `Note_Source` field so users can see whether the note came from:

* Rule-Based
* Gemini Generated
* Gemini Failed - Rule-Based Fallback

---

## Dashboard and App Outputs

The Streamlit app displays:

### Summary KPI Cards

* Total Records Checked
* Rule-Based Flagged Records
* ML Review Records
* AI Notes Generated
* Average ML Risk
* Vendor Mismatches
* Abnormal Returns
* Volume Spikes

### Visual Breakdowns

* Issue Type Breakdown
* ML Risk Band Distribution
* Note Source Breakdown
* Risk Level Distribution
* ML Risk Probability Over Time

### Analyst Review Queue

The review queue includes:

* Date
* Ticker
* Company
* Close Price
* Vendor B Close
* Vendor Variance %
* Change %
* Volume Numeric
* Issue Type
* Risk Level
* ML Review Label
* ML Risk Probability %
* ML Risk Band
* Note Source
* Analyst Review Note

### Downloadable Output

Users can download the QA-scored dataset as an Excel file.

---

## Tech Stack

### Dashboard

* Google Sheets
* Looker Studio

### Machine Learning and App

* Python
* pandas
* NumPy
* scikit-learn
* joblib
* Streamlit
* openpyxl

### AI Layer

* Gemini API
* Google Gen AI SDK

---

## Project Structure

```text
market-data-qa-app/
│
├── app.py
├── requirements.txt
├── market_data_qa_model.pkl
├── model_features.json
├── sample_data/
│   └── AXP Historical Data.csv
└── README.md
```

---

## How to Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/your-username/market-data-qa-app.git
cd market-data-qa-app
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\Activate.ps1
```

Mac/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Gemini API key

Create a folder named `.streamlit`, then create a file inside it named `secrets.toml`.

```text
.streamlit/secrets.toml
```

Add:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## Deployment Notes

When deploying to Streamlit Community Cloud:

1. Push the project to GitHub.
2. Deploy the app using `app.py` as the main file.
3. Add the Gemini API key in Streamlit Cloud Secrets:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

4. Make sure the repository includes:

   * `app.py`
   * `requirements.txt`
   * `market_data_qa_model.pkl`
   * `model_features.json`

Do not push your local `.streamlit/secrets.toml` file to GitHub.

---

## Important Disclaimer

This project is for market data quality assurance and portfolio demonstration purposes only.

It does not provide investment advice, trading recommendations, or stock price predictions.

The simulated Vendor B price source is used to demonstrate vendor variance analysis because public historical stock datasets usually contain only one price source.

---

## Resume Summary

Built and deployed an AI-assisted market data QA system combining Looker Studio, Python, Streamlit, scikit-learn, and Gemini API to monitor equity market data quality, simulate vendor-source comparison, assign ML risk scores, and generate analyst review queues for discrepancy investigation and workflow automation.
