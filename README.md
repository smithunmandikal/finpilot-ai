# 💰 FinPilot AI — Smart Budget & Financial Advisor

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML%20Pipeline-orange?style=flat-square)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-green?style=flat-square)
![Claude API](https://img.shields.io/badge/Claude-AI%20Advisor-purple?style=flat-square)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-red?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-brightgreen?style=flat-square)

---

## 📌 Project Overview

**FinPilot AI** is an end-to-end machine learning pipeline and 
AI-powered financial advisor built on a real-world personal finance 
dataset of 32,424 users across 5 global regions.

The project combines supervised learning (regression + multi-class 
classification), rich exploratory data analysis, a rule-based budget 
recommendation engine, and Claude AI to generate personalized 
plain-English financial plans from a single CSV upload.

> *"What if an AI could look at your finances and tell you exactly 
> what to do next month? Not a generic tip. A real plan built just 
> for you."*

---

## 🚀 What It Does

1. **Upload** a transaction CSV or bank statement
2. **Categorize** every transaction automatically using Naive Bayes
3. **Score** 4 financial health metrics against benchmarks from 
   32,424 real users
4. **Generate** a plain-English 5-part financial plan using Claude AI
5. **Visualize** spending breakdown, goal timeline and health dashboard

---

## 📊 Dataset

**Kaggle Personal Finance ML Dataset**
- 32,424 users across Africa, Asia, Europe, North America and Other
- Key finding: 50.7% of users have poor credit scores below 580
- Median savings rate: only 5% of income

---

## 🤖 ML Models

| Task | Models Used | Best Result |
|---|---|---|
| Expenses Prediction (Regression) | Ridge, Lasso, Random Forest, Extra Trees, Gradient Boosting | R² = 0.99+ |
| Loan Risk Classification (Binary) | Logistic Regression, Decision Tree, Random Forest, MLP Neural Net | ROC-AUC = 0.99+ |
| Savings Tier (Multi-Class) | Random Forest, Extra Trees, HistGradient Boosting | Accuracy = 0.99+ |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.8+ |
| ML | scikit-learn, scipy |
| Data | pandas, numpy |
| Visualization | matplotlib, seaborn, Plotly |
| AI Advisor | Anthropic Claude API |
| Backend | FastAPI + uvicorn |
| Dashboard | Streamlit |
| Database | SQLite |
| Environment | Google Colab / Jupyter Notebook |

---

## 📁 Repository Structure

```
finpilot-ai/
├── Finpilot_AI.ipynb          # Main ML pipeline notebook
├── generate_data.py           # Synthetic transaction data generator
├── Personal_Finance_Dataset_1.csv  # Kaggle dataset
└── README.md
```

---

## 💡 Key Features

- **3 ML models** covering regression, binary and multi-class tasks
- **26 visualizations** including distributions, correlation heatmaps, 
  ROC curves, learning curves and financial health dashboards
- **Rule-based recommendation engine** with personalized financial advice
- **Claude AI integration** for plain-English 5-part financial plans
- **What-If scenario engine** — change one input, see the full impact
- **Benchmarks from real data** — every threshold derived from 32,424 users

---

## 🌍 Global Fusion Foundation on AI Hackathon

**Track:** Fintech | **Category:** Personal Finance AI

*Built for the 3.5 billion people who have never had a financial advisor.*

---

## 👥 Team

- **Shwetha Mithun** — Financial analytics, AML compliance background, 
  business strategy
- **Dhrumil Shah** — ML pipeline, model training, technical implementation

---

## 📄 License

MIT License
