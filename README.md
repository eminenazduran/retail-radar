# 🛰️ Retail Radar

Customer & product intelligence from raw e-commerce transaction data — built as a data science portfolio project using the [UCI Online Retail Dataset](https://archive.ics.uci.edu/dataset/352/online+retail) (541,909 transactions).

> **Status: 🚧 In Progress** — Data cleaning, EDA, visualization, feature engineering, RFM analysis, and customer segmentation are complete. The interactive dashboard is currently in development.

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
- [x] **Feature Engineering** — transaction-level data → customer-level features (Total Spending, Total Orders, Unique Products, Recency, Average Order Value)
- [x] **RFM Analysis** — Recency, Frequency, Monetary quintile scoring per customer
- [x] **Customer Segmentation (K-Means)** — unsupervised clustering into 4 behavioral segments
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
│   └── 05_feature_engineering.ipynb   # feature engineering, RFM, K-Means
├── src/
├── app/                                # Streamlit dashboard (planned)
└── visualizations/
```

## 🔍 Key Findings So Far

**Data cleaning & products**
- Cleaned dataset reduced from 541,909 raw rows by removing duplicates, cancelled orders, and invalid price/quantity entries.
- Identified top-selling products by quantity vs. by revenue — these rankings differ, showing volume ≠ value.
- Special non-product stock codes (`POST`, `DOT`, `M`, `BANK CHARGES`, etc.) were identified and excluded from product-level analysis, since they represent shipping/accounting entries rather than actual products.
- `POST` (shipping charge) entries appear alongside real product purchases in the majority of invoices (median 14 distinct products per invoice), confirming they represent customer-paid shipping costs and are **retained** in customer-level monetary calculations.

**Feature engineering & RFM**
- Built a customer-level feature table (4,338 unique customers) from transaction-level data: Total Spending, Total Orders, Unique Products, Recency, Average Order Value.
- Recency computed relative to the dataset's last transaction date, since the data predates the current date.
- Applied quintile-based RFM scoring (1–5) for Recency, Frequency, and Monetary dimensions.

**Customer segmentation (K-Means)**
- Applied log-transformation + `StandardScaler` to Recency/Frequency/Monetary features before clustering, to control for a highly skewed distribution (e.g. one wholesale-scale customer with a single 74,215-unit order).
- Used the Elbow Method to evaluate k=2 through k=10; compared k=2 and k=4 directly by cluster-level RFM averages before choosing **k=4**, since it produced business-interpretable segments rather than a coarse high/low split.
- Final segments:

| Segment | Customers | Avg. Recency | Avg. Orders | Avg. Spending |
|---|---|---|---|---|
| At Risk | 1,642 (38%) | 179 days | 1.3 | £348 |
| Regular | 1,203 (28%) | 68 days | 4.2 | £1,830 |
| Occasional | 808 (19%) | 17 days | 2.1 | £540 |
| High Value | 685 (16%) | 10 days | 14.0 | £8,290 |

- **38% of customers fall into "At Risk"** — the single largest segment — highlighting a significant re-engagement opportunity for a retention campaign.

## ▶️ Running the Notebooks

```bash
# from the project root
pip install -r requirements.txt
jupyter notebook notebooks/
```

---
*Part of a 20-day AI + Data Science portfolio program (Project 1 of 4: Retail Radar → Moodify AI → Fraud Hunter → AI Decision Lab).*