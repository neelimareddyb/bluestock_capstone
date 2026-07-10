# BlueStock Mutual Fund Analytics Capstone

A professional end-to-end data engineering and quantitative analytics pipeline for evaluating mutual fund performance, risk metrics, and automated portfolio recommendations.

---

## 📁 Repository Architecture & Mapping

This repository is built using a production-first modular script architecture. Data collection, cleaning, and metric updates are handled via robust automated Python components rather than step-by-step notebook scripts.

```text
bluestock_capstone/
├── dashboard/               # Target destination for Interactive Tableau/Power BI engines
├── data/
│   ├── db/                 # Local SQLite production database storage (Git-ignored)
│   ├── processed/          # Cleaned, standardized algorithmic datasets
│   └── raw/                # Historical source extractions
├── notebooks/
│   ├── 03_eda_analysis.ipynb          # Deep-Dive Exploratory Data Analysis & Visualizations
│   └── 04_performance_analytics.ipynb # Quantitative risk models & simulation sandboxes
├── reports/                 # Advanced plot exports (Efficient Frontier, Monte Carlo)
├── scripts/
│   ├── etl_pipeline.py      # Core Ingestion Engine (Covers Notebook 01 requirements)
│   ├── data_cleaning.py     # Schema standardization (Covers Notebook 02 requirements)
│   ├── live_nav_fetch.py    # Live API polling infrastructure
│   ├── compute_metrics.py   # Statistical risk calculations (Alpha, Beta, Sharpe, Treynor)
│   └── recommender.py       # Portfolio matching algorithms (Covers Notebook 05 requirements)
├── data_dictionary.md       # Data schema validations
└── requirements.txt         # Production environment dependencies