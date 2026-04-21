import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FinPilot AI", page_icon="💰", layout="wide")

# ── HEADER ────────────────────────────────────────────────────────────────
st.title("💰 FinPilot AI")
st.subheader("Smart Budget & Financial Advisor")
st.caption("Upload any financial CSV to get your personalized dashboard.")

# ── ONBOARDING: HOW IT WORKS ─────────────────────────────────────────────
with st.expander("📘 How it works — click to expand", expanded=True):
    st.markdown("""
    ### Step 1 — Enter your profile in the sidebar
    Set your monthly income and savings goal on the left.

    ### Step 2 — Upload any financial CSV
    FinPilot accepts two kinds of data:
    - **Transaction data** — rows of individual purchases with date, description, amount, category
    - **Profile data** — rows of users with income, expenses, credit score, debt ratio

    FinPilot detects which one you uploaded automatically.

    ### Step 3 — Get your dashboard
    See your spending breakdown, financial health metrics, and goal timeline.

    ### No data? Try our demo dataset
    Download the sample CSV below to see the app working.
    """)

    # Sample CSV download
    sample_csv = """date,description,amount,category
2024-03-01,WHOLE FOODS MARKET,54.32,Food
2024-03-01,RENT PAYMENT,1450.00,Housing
2024-03-02,SHELL FUEL,58.21,Transport
2024-03-03,NETFLIX,15.99,Entertainment
2024-03-04,CHASE VISA PAYMENT,200.00,Debt repayment
2024-03-05,SAVINGS TRANSFER,100.00,Savings
2024-03-06,CHIPOTLE,13.45,Food
2024-03-07,CVS PHARMACY,22.10,Healthcare
2024-03-08,UBER,17.25,Transport
2024-03-09,AMAZON,35.99,Other
"""
    st.download_button(
        label="⬇️ Download sample transactions.csv",
        data=sample_csv,
        file_name="sample_transactions.csv",
        mime="text/csv"
    )

st.divider()

# ── SIDEBAR: USER PROFILE ────────────────────────────────────────────────
with st.sidebar:
    st.header("📋 Your Profile")
    monthly_income = st.number_input(
        "Monthly take-home income ($)", min_value=0, value=4000
    )
    st.subheader("🎯 Your Goal")
    goal_name = st.text_input("Goal name", "Emergency Fund")
    goal_amount = st.number_input("Target amount ($)", value=3000)

    st.divider()
    st.caption(
        "Global Fusion Foundation on AI Hackathon\n\n"
        "Track: Fintech | Personal Finance AI"
    )

# ── FILE UPLOAD ──────────────────────────────────────────────────────────
st.markdown("### 📁 Upload Your CSV")
uploaded_file = st.file_uploader(
    "Drag and drop your CSV here or click to browse",
    type=["csv"]
)

if not uploaded_file:
    st.info("👆 Upload a CSV above to see your dashboard. No file? Download the sample CSV from the guide above.")
    st.stop()

# ── READ AND NORMALIZE ───────────────────────────────────────────────────
df = pd.read_csv(uploaded_file)
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

st.success(f"✅ Loaded {len(df)} rows and {len(df.columns)} columns")

# ── DETECT DATASET TYPE ──────────────────────────────────────────────────
transaction_signals = {"amount", "description", "category", "merchant", "transaction"}
profile_signals = {"monthly_income_usd", "monthly_expenses_usd", "credit_score", "savings_usd"}

found_txn = transaction_signals.intersection(set(df.columns))
found_profile = profile_signals.intersection(set(df.columns))

if len(found_profile) >= 2:
    dataset_type = "profile"
elif len(found_txn) >= 1:
    dataset_type = "transaction"
else:
    dataset_type = "unknown"

# ── PROFILE DATASET BRANCH ───────────────────────────────────────────────
if dataset_type == "profile":
    st.markdown("### 🔍 Detected: Profile Dataset")
    st.caption(
        "This dataset contains one row per user. FinPilot will show you "
        "aggregate financial health insights across all users."
    )

    # Sample size selector
    n_show = st.slider(
        "How many users to analyze",
        min_value=100,
        max_value=min(len(df), 10000),
        value=1000
    )
    df_sample = df.head(n_show)

    # Compute key stats
    if "monthly_income_usd" in df.columns and "monthly_expenses_usd" in df.columns:
        df_sample["surplus"] = df_sample["monthly_income_usd"] - df_sample["monthly_expenses_usd"]
        avg_income = df_sample["monthly_income_usd"].mean()
        avg_expenses = df_sample["monthly_expenses_usd"].mean()
        avg_surplus = df_sample["surplus"].mean()

        col1, col2, col3 = st.columns(3)
        col1.metric("Average Income", f"${avg_income:,.0f}")
        col2.metric("Average Expenses", f"${avg_expenses:,.0f}")
        col3.metric("Average Surplus", f"${avg_surplus:,.0f}")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("💳 Credit Score Distribution")
        if "credit_score" in df.columns:
            fig_credit = px.histogram(
                df_sample,
                x="credit_score",
                nbins=20,
                color_discrete_sequence=["#0B6E4F"],
                title="Credit Scores Across Users"
            )
            fig_credit.add_vline(x=580, line_dash="dash", line_color="red",
                                 annotation_text="Poor")
            fig_credit.add_vline(x=740, line_dash="dash", line_color="green",
                                 annotation_text="Excellent")
            st.plotly_chart(fig_credit, use_container_width=True)

    with right:
        st.subheader("🌍 Users by Region")
        if "region" in df.columns:
            region_counts = df_sample["region"].value_counts().reset_index()
            region_counts.columns = ["region", "count"]
            fig_region = px.pie(
                region_counts,
                values="count",
                names="region",
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Greens_r,
                title="Global Distribution"
            )
            st.plotly_chart(fig_region, use_container_width=True)

    st.divider()
    st.subheader("📊 Full Dataset Preview")
    st.dataframe(df_sample.head(20), use_container_width=True)

# ── TRANSACTION DATASET BRANCH ───────────────────────────────────────────
elif dataset_type == "transaction":
    st.markdown("### 🔍 Detected: Transaction Dataset")
    st.caption(
        "This dataset contains individual transactions. "
        "FinPilot will categorize spending and score your financial health."
    )

    # Column mapping
    st.markdown("#### Step — Map Your Columns")
    all_columns = ["-- select --"] + list(df.columns)
    auto_amount = next((c for c in df.columns if "amount" in c), "-- select --")
    auto_cat = next((c for c in df.columns if "categ" in c), "-- select --")

    col_a, col_b = st.columns(2)
    with col_a:
        col_amount = st.selectbox(
            "Which column has the amount?",
            all_columns,
            index=all_columns.index(auto_amount) if auto_amount in all_columns else 0
        )
    with col_b:
        col_category = st.selectbox(
            "Which column has the category?",
            all_columns,
            index=all_columns.index(auto_cat) if auto_cat in all_columns else 0
        )

    if col_amount == "-- select --" or col_category == "-- select --":
        st.info("👆 Select your amount and category columns to see the dashboard.")
        st.stop()

    # Rename
    df = df.rename(columns={col_amount: "amount", col_category: "category"})

    # Clean amount
    df["amount"] = pd.to_numeric(
        df["amount"].astype(str).str.replace("[$,]", "", regex=True),
        errors="coerce"
    ).fillna(0)

    st.divider()
    st.markdown("### 📊 Your Financial Dashboard")

    total_spend = df["amount"].sum()
    surplus = monthly_income - total_spend
    savings_rows = df[df["category"].astype(str).str.lower().str.contains("saving", na=False)]
    savings_spend = savings_rows["amount"].sum()
    savings_rate = round((savings_spend / max(monthly_income, 1)) * 100, 1)
    debt_rows = df[df["category"].astype(str).str.lower().str.contains("debt|loan|repay", na=False)]
    debt_spend = debt_rows["amount"].sum()
    dti = round((debt_spend / max(monthly_income, 1)) * 100, 1)
    ef_months = round((total_spend * 3) / max(surplus, 1), 1)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💵 Total Spend", f"${total_spend:,.0f}")
    col2.metric("💰 Monthly Surplus", f"${surplus:,.0f}")
    col3.metric("📈 Savings Rate", f"{savings_rate}%")
    col4.metric("🎯 Months to Goal", f"{ef_months} mo")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("🍩 Spending Breakdown")
        category_totals = (
            df.groupby("category")["amount"]
            .sum()
            .reset_index()
            .sort_values("amount", ascending=False)
        )
        fig_donut = px.pie(
            category_totals,
            values="amount",
            names="category",
            hole=0.4,
            color_discrete_sequence=px.colors.sequential.Greens_r,
            title="Where Your Money Goes"
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with right:
        st.subheader("📅 Goal Timeline")
        months_needed = round(goal_amount / max(surplus, 1), 1)
        fig_bar = px.bar(
            x=[goal_name],
            y=[months_needed],
            color_discrete_sequence=["#0B6E4F"],
            title=f"{goal_name}: {months_needed} months away",
            labels={"y": "Months", "x": ""}
        )
        fig_bar.add_hline(
            y=6,
            line_dash="dash",
            line_color="#E8A020",
            annotation_text="6 month target"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    st.divider()
    st.subheader("📑 Category Breakdown Table")
    st.dataframe(category_totals, use_container_width=True)

    st.divider()
    st.subheader("📋 Raw Data (first 20 rows)")
    st.dataframe(df.head(20), use_container_width=True)

# ── UNKNOWN DATASET BRANCH ───────────────────────────────────────────────
else:
    st.warning(
        "⚠️ We could not detect the dataset type. FinPilot expects either:\n\n"
        "- **Transaction data** with columns like `amount`, `description`, `category`\n"
        "- **Profile data** with columns like `monthly_income_usd`, `credit_score`\n\n"
        "Please check your CSV and try again, or download our sample CSV."
    )
    st.markdown("#### Columns detected in your file:")
    st.write(list(df.columns))
    st.markdown("#### Preview:")
    st.dataframe(df.head(10), use_container_width=True)
