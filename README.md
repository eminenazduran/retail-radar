# 🛰️ Retail Radar

Customer & product intelligence from raw e-commerce transaction data — built as a data science portfolio project using the [UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail) (541,909 transactions).

> **Status: 🚧 In Progress** — Data cleaning, EDA, and visualization are complete. Feature engineering, RFM analysis, clustering, and the dashboard are currently in development.

## 🎯 Goal

Turn raw retail transaction data into actionable customer and product insights:
- **Customer Intelligence** — who are the high-value, loyal, and at-risk customers?
- **Product Intelligence** — which products drive volume vs. revenue?
- **Sales Intelligence** — how do sales trends vary over time and geography?

## 📊 Dataset

| Column | Description |
|---|---|
| InvoiceNo | Transaction/invoice identifier |
| StockCode | Product code |
| Description | Product name |
| Quantity | Units purchased |
| InvoiceDate | Date and time of transaction |
| UnitPrice | Price per unit |
| CustomerID | Unique customer identifier |
| Country | Customer's country |

## 🗺️ Roadmap & Progress

- [x] **Data Understanding** — shape, dtypes, missing values, cancelled orders, invalid records
- [x] **Data Cleaning** — duplicate removal, negative/zero price & quantity handling, invalid invoice filtering
- [x] **Exploratory Data Analysis** — top products, revenue by country, order patterns by hour, top customers
- [x] **Data Visualization** — product & revenue distributions, price histograms
- [ ] **Feature Engineering** — transaction-level data → customer-level features (Total Spending, Frequency, AOV, Recency, Unique Products)
- [ ] **RFM Analysis** — Recency, Frequency, Monetary scoring per customer
- [ ] **Customer Segmentation (K-Means)** — unsupervised clustering into behavioral segments
- [ ] **Streamlit Dashboard** — interactive view of revenue, customer segments, sales trends, top products

## 🛠️ Tech Stack

Python · Pandas · NumPy · Matplotlib · Seaborn · Scikit-learn · Streamlit · Jupyter

## 📁 Project Structure

```
retail-radar/
├── data/
│   └── raw/
│       └── Online Retail.xlsx
├── notebooks/
│   ├── 01_data_understanding.ipynb
│   ├── 02_data_cleaning_eda.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_data_visualization.ipynb
│   └── 05_feature_engineering.ipynb   # in progress
├── src/
├── app/                                # Streamlit dashboard (planned)
└── visualizations/
```

## 🔍 Key Findings So Far

- Cleaned dataset reduced from 541,909 raw rows by removing duplicates, cancelled orders, and invalid price/quantity entries.
- Identified top-selling products by quantity vs. by revenue — these rankings differ, showing volume ≠ value.
- Special non-product stock codes (`POST`, `DOT`, `M`, `BANK CHARGES`, etc.) were identified and excluded from product-level analysis, since they represent shipping/accounting entries rather than actual products.
- `POST` (shipping charge) entries appear alongside real product purchases in the majority of invoices (median 14 distinct products per invoice), confirming they represent customer-paid shipping costs and should be **retained** in customer-level monetary calculations.

## ▶️ Running the Notebooks

```bash
# from the project root
pip install -r requirements.txt
jupyter notebook notebooks/
```

---
*Part of a 20-day AI + Data Science portfolio program (Project 1 of 4: Retail Radar → Moodify AI → Fraud Hunter → AI Decision Lab).*
