<div align="center">

  # 🎬 MavenFlix — Subscription Cohort & Retention Analytics
  ### End-to-End Python Data Pipeline & Mobile-Optimized Executive HTML Dashboard
  
  [![Live Interactive Dashboard](https://img.shields.io/badge/🚀_LIVE_DEMO-Launch_Interactive_Dashboard-blueviolet?style=for-the-badge&logo=githubpages&logoColor=white)](https://aly-hossam.github.io/saas-cohort-retention-dashboard/)

  <p align="center">
    <a href="#-executive-summary--key-kpis">Executive Summary</a> •
    <a href="#-key-business-insights">Key Insights</a> •
    <a href="#-analytical-rigor--methodology">Methodology</a> •
    <a href="#-data-pipeline--architecture">Pipeline Architecture</a> •
    <a href="#-installation--how-to-run">Installation</a>
  </p>

  <!-- Badges -->
  <p align="center">
    <img src="https://img.shields.io/badge/Python_3.8+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python" />
    <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas" />
    <img src="https://img.shields.io/badge/Tailwind_CSS-38BDF8?style=flat-square&logo=tailwind-css&logoColor=white" alt="Tailwind CSS" />
    <img src="https://img.shields.io/badge/Chart.js_v4-FF6384?style=flat-square&logo=chart.js&logoColor=white" alt="Chart.js" />
    <img src="https://img.shields.io/badge/Analysis-SaaS_Cohort_Retention-blueviolet?style=flat-square" alt="SaaS Cohort Analysis" />
    <img src="https://img.shields.io/badge/License-MIT-green?style=flat-square" alt="License" />
  </p>

</div>

---

## 💡 Project Overview

This repository features an automated Python-driven data pipeline and executive dashboard built for **MavenFlix** (a fictitious video streaming platform). 

The platform handles raw data extraction, exploratory profiling, data cleaning (resolving unpaid subscriptions & right-censoring biases), and compiles an interactive, mobile-optimized HTML report featuring dynamic **Chart.js** trends and a complete **Cohort Retention Heatmap Matrix ($M_0 - M_{12}$)**.

---

## 🖥️ Interactive Dashboard Demo

<div align="center">
  <a href="https://aly-hossam.github.io/saas-cohort-retention-dashboard/">
    <img src="assets/dashboard-demo.gif" width="100%" alt="MavenFlix Executive Dashboard Demo" style="border-radius: 10px; border: 1px solid #30363d;" />
  </a>

  <br/><br/>

  [![Launch Live Dashboard](https://img.shields.io/badge/▶_LAUNCH_INTERACTIVE_DASHBOARD-MavenFlix_Analytics-blueviolet?style=for-the-badge&logoColor=white)](https://aly-hossam.github.io/saas-cohort-retention-dashboard/)
</div>

---

## 📊 Executive Summary & Key KPIs

Analyzing subscriber records across a 13-month lifecycle (**September 2022 through September 2023**):

<div align="center">
  <img src="assets/00-kpis.png" width="100%" alt="Key Performance Indicators" style="border-radius: 10px; border: 1px solid #30363d;" />
</div>

<br/>

### 🎯 Key Commercial Benchmarks Evaluated:
- 👥 **Unique Paid Subscribers:** `2,744` active accounts (filtered from $3,069$ raw transaction attempts).
- 🔄 **5+ Months Active Retention Rate:** `23.99%` *(Eligible cohort window: Joined $\le$ May 2023).*
- 📅 **Peak Acquisition Month:** **July 2023** with `293` brand-new paid subscribers.
- 🏆 **Top Month-1 ($M_1$) Retention:** **January 2023** cohort achieving **82.88%** retention.

---

## 🎯 Key Business Insights

### 1. Subscription Acquisition Growth
> Subscriptions experienced steady expansion through mid-2023, hitting an all-time peak of **293 new subscribers** in **July 2023**.

<div align="center">
  <img src="assets/01-subscriptions-trend.png" width="100%" alt="Subscriptions Trend Over Time" style="border-radius: 10px; border: 1px solid #30363d;" />
</div>

*Note: The drop in late September 2023 represents the dataset extraction cutoff date rather than natural churn.*

---

### 2. Customer Lifetime Retention ($5+$ Months Window)
> **23.99%** ($479 / 1,997$) of eligible subscribers who joined on or before May 2023 remained active for 5+ months.

<div align="center">
  <img src="assets/02-customer-retention-5months.png" width="100%" alt="Customer Retention 5 Plus Months" style="border-radius: 10px; border: 1px solid #30363d;" />
</div>

- **Analytical Rigor:** Reactivated/re-subscribed users are grouped under unified `customer_id` records to measure true lifetime customer value rather than superficial account spikes.

---

### 3. Cohort Retention Heatmap Matrix ($M_0 - M_{12}$)
> Month-1 retention ($M_1 \ge 30\text{ days active}$) across mature cohorts fluctuates within a healthy, stable corridor between **75.85%** and **82.88%**.

<div align="center">
  <img src="assets/03-cohort-retention-heatmap-matrix.png" width="100%" alt="Cohort Retention Heatmap Matrix" style="border-radius: 10px; border: 1px solid #30363d;" />
</div>

---

## 🔍 Analytical Rigor & Methodology

To deliver C-suite level analytics, several data pipeline corrections were automated:

- **Unpaid Subscription Filtering:** Stripped failed transactions (`was_subscription_paid == 'Yes'`), cleansing $3,069$ raw attempts into $2,936$ verified revenue records.
- **Customer Lifetime Consolidation:** Aggregated multi-period transactions by unique `customer_id` ($2,877$ total unique customers) to accurately sum lifetime active days.
- **Right-Censoring Bias Mitigation:** Immature cohorts (subscribers acquired near the extraction cutoff of Sept 30, 2023) were excluded from Month-1 min/max ranking logic to eliminate artificially suppressed retention figures.
- **Dynamic Heatmap Visualization:** Rendered a full $M_0 - M_{12}$ interactive HTML/Tailwind matrix with automated color-gradient intensity thresholds.

---

## 🛠️ Data Pipeline & Architecture

The analytical workflow is driven by 3 modular, zero-dependency Python scripts:

```text
.
├── assets/                                    # Screenshots and demo GIFs
│   ├── dashboard-demo.gif
│   ├── 00-kpis.png
│   ├── 01-subscriptions-trend.png
│   ├── 02-customer-retention-5months.png
│   └── 03-cohort-retention-heatmap-matrix.png
├── extracted_files/                          # Cleaned CSV data output
│   ├── Subscription Cohort Analysis Data Dictionary.csv
│   └── Subscription Cohort Analysis Data.csv
├── unzip_files.py                             # Archive extractor & macOS metadata cleaner
├── inspect_data.py                            # Automated EDA & profiling generator
├── generate_html_report.py                    # Core pipeline & HTML dashboard compiler
├── data_overview_report.md                    # Auto-generated EDA profile report
├── mavenflix_report.html                      # Standalone interactive dashboard
└── README.md                                  # Project documentation
```

### ⚙️ Script Execution Workflow:
1. **`unzip_files.py`**: Automated extraction of `.zip`/`.tar` archives while purging hidden OS files (`__MACOSX`).
2. **`inspect_data.py`**: Generates a comprehensive Markdown Exploratory Data Analysis report (`data_overview_report.md`).
3. **`generate_html_report.py`**: Executes business rules, matrix transformations, and outputs `mavenflix_report.html`.

---

## ⚡ Installation & How to Run

### Prerequisites
- Python 3.8 or higher
- `pandas` library

```bash
pip install pandas
```

### Run the End-to-End Pipeline

1. **Extract Archives:**
   ```bash
   python3 unzip_files.py
   ```

2. **Generate Data Profiling Report:**
   ```bash
   python3 inspect_data.py
   ```

3. **Build Interactive Executive HTML Dashboard:**
   ```bash
   python3 generate_html_report.py
   ```

4. **View Results:**
   Open `mavenflix_report.html` (or `index.html`) in any modern desktop or mobile browser.

---

## 👤 Author & Contact

**Aly Hossam**  
*Data Analytics Engineer | Building 100% Offline, Secure Executive Dashboards*

- 💼 **LinkedIn:** [linkedin.com/in/aly-hossam](https://linkedin.com/in/aly-hossam)
- 🛒 **Gumroad:** [alyhossam.gumroad.com](https://alyhossam.gumroad.com)
- 📧 **Email:** `aly.hossam.2002@gmail.com`

---
<div align="center">
  <sub>Dataset Source: Public Domain Maven Analytics. Built for SaaS Analytics & Data Engineering Portfolio.</sub>
</div>
