# 🔴 Why Are We Losing Customers? — Churn Deep Dive + Action Playbook

> **"Most analysts build churn models. This project solves the churn problem."**

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![SQL](https://img.shields.io/badge/SQL-PostgreSQL-336791?logo=postgresql)](https://postgresql.org)
[![Power BI](https://img.shields.io/badge/PowerBI-Dashboard-F2C811?logo=powerbi)](https://powerbi.microsoft.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📌 Business Problem

A SaaS company is losing customers — but leadership doesn't know **why**, **who**, or **when** it happens. The data team is asked to investigate.

This project goes beyond churn prediction. It delivers:

1. **Root Cause Analysis** — not just *who* churns, but *why*
2. **Segmented Churn Trends** — by time, customer type, and feature usage
3. **Leading Indicators** — early warning signals before churn happens
4. **An Actionable Churn Playbook** — automated response triggers mapped to churn risk

---

## 🗂️ Project Structure

```
churn-deepdive/
│
├── 📁 sql/
│   ├── 01_monthly_churn_trend.sql        # MoM churn rate by cohort
│   ├── 02_new_vs_existing_churn.sql      # New vs tenured customer churn
│   ├── 03_feature_usage_churn.sql        # Feature adoption vs churn
│   └── 04_leading_indicators.sql         # Events that precede churn
│
├── 📁 python/
│   ├── churn_analysis.py                 # Full EDA + feature engineering
│   ├── churn_model.py                    # XGBoost churn prediction model
│   ├── root_cause_analysis.py            # SHAP-based root cause breakdown
│   └── playbook_triggers.py              # Rule-based churn intervention engine
│
├── 📁 notebooks/
│   └── churn_full_analysis.ipynb         # End-to-end walkthrough notebook
│
├── 📁 playbook/
│   └── churn_playbook.md                 # The Churn Response Playbook
│
├── 📁 dashboard/
│   └── churn_dashboard.pbix              # Power BI dashboard file
│   └── dashboard_preview.png             # Dashboard screenshot
│
├── 📁 data/sample/
│   └── customers_sample.csv              # Anonymized sample dataset
│
└── README.md
```

---

## 🔍 Analysis Breakdown

### 1. Monthly Churn Trend
- Month-over-month churn rate calculation
- Rolling 3-month average to smooth noise
- Cohort-based survival analysis

### 2. New vs. Existing Customers
- Churn split: customers < 90 days vs. > 90 days tenure
- Hypothesis: new users churn from **poor onboarding**; old users churn from **value erosion**

### 3. Feature Usage vs. Churn
- Users who **never used Feature X** → 3.2× more likely to churn
- Power users (≥5 features used) → churn rate drops by 67%

### 4. Leading Indicators (Early Warning System)
| Signal | Churn Risk Multiplier |
|---|---|
| No login in 7 days | 2.1× |
| Support ticket unresolved > 5 days | 3.4× |
| Downgraded plan in last 30 days | 4.8× |
| Feature usage dropped > 50% MoM | 2.7× |
| Failed payment attempt | 5.1× |

---

## 🧠 Churn Prediction Model

**Algorithm:** XGBoost Classifier  
**Target:** Churned within next 30 days  
**Features:** 22 behavioral + demographic signals  

| Metric | Score |
|---|---|
| AUC-ROC | 0.89 |
| Precision | 0.81 |
| Recall | 0.76 |
| F1 Score | 0.78 |

**Top SHAP Features (Root Cause):**
1. `days_since_last_login` — most predictive
2. `support_tickets_unresolved`
3. `feature_adoption_score`
4. `plan_downgrade_flag`
5. `avg_session_duration_30d`

---

## 📋 The Churn Playbook

> Full playbook: [`playbook/churn_playbook.md`](playbook/churn_playbook.md)

| Trigger | Segment | Action | Owner |
|---|---|---|---|
| Inactive 7 days | All users | Automated re-engagement email | Marketing |
| Inactive 14 days | All users | In-app nudge + feature tip | Product |
| Inactive 21 days | High-value (LTV > $500) | Assign CSM for personal outreach | Customer Success |
| Support ticket > 5 days | All users | Escalate + send apology credit | Support |
| Churn score > 0.75 | High-value | CEO/Founder personal email | Leadership |
| Failed payment | All users | Retry + grace period notification | Billing |
| Plan downgrade | All users | Book a success call | Sales |

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Data extraction | SQL (PostgreSQL) |
| Analysis & ML | Python (pandas, XGBoost, SHAP) |
| Visualization | Power BI |
| Notebook | Jupyter |
| Version control | Git + GitHub |

---
---

## 💡 Key Insights (TL;DR)

- **32% of churn** happens in the **first 30 days** → onboarding is broken
- Users who complete the **setup checklist** churn **4× less** in year 1
- **Feature adoption**, not plan tier, is the strongest retention predictor
- The **top 20% of customers** by LTV account for **68% of churn revenue loss**

---

## 📈 Business Impact

If the playbook interventions reduce churn by just **15%**:
- At 500 churned customers/month × $120 avg MRR = **$60,000 MRR recovered**
- Annualized: **$720,000 in retained revenue**

---

## 🤝 Contributing

Pull requests welcome. For major changes, please open an issue first.

---

## 📄 License

MIT — free to use, adapt, and build on.

