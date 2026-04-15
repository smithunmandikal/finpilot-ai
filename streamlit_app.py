import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FinPilot AI", page_icon="💰", layout="wide")

st.title("💰 FinPilot AI")
st.subheader("Smart Budget & Financial Advisor")
st.markdown("*Upload any financial CSV to get your personalized dashboard.*")
st.divider()

with st.sidebar:
    st.header("Your Profile")
    monthly_income = st.number_input(
        "Monthly take-home income ($)", min_value=0, value=4000
    )
    st.subheader("Your Goal")
    goal_name = st.text_input("Goal name", "Emergency Fund")
    goal_amount = st.number_input("Target amount ($)", value=3000)

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Normalize all column names to lowercase with underscores
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    st.success(f"Loaded {len(df)} rows and {len(df.columns)} columns")

    # Show the user what columns exist in their file
    st.markdown("### Step 1 — Map Your Columns")
    st.caption("Tell FinPilot which columns contain your amount and category data.")

    all_columns = ["-- select --"] + list(df.columns)

    col_amount = st.selectbox(
        "Which column has the transaction amount?",
        all_columns
    )
    col_category = st.selectbox(
        "Which column has the spending category?",
        all_columns
    )

    # Only proceed once both columns are selected
    if col_amount != "-- select --" and col_category != "-- select --":

        # Rename selected columns to standard names
        df = df.rename(columns={
            col_amount: "amount",
            col_category: "category"
        })

        # Convert amount to numeric in case it has $ signs or commas
        df["amount"] = pd.to_numeric(
            df["amount"].astype(str).str.replace("[$,]", "", regex=True),
            errors="coerce"
        ).fillna(0)

        st.divider()
        st.markdown("### Step 2 — Your Financial Dashboard")

        # Calculate metrics
        total_spend    = df["amount"].sum()
        surplus        = monthly_income - total_spend
        savings_rows   = df[df["category"].str.lower().str.contains("saving", na=False)]
        savings_spend  = savings_rows["amount"].sum()
        savings_rate   = round((savings_spend / max(monthly_income, 1)) * 100, 1)
        debt_rows      = df[df["category"].str.lower().str.contains("debt|loan|repay", na=False)]
        debt_spend     = debt_rows["amount"].sum()
        dti            = round((debt_spend / max(monthly_income, 1)) * 100, 1)
        ef_months      = round((total_spend * 3) / max(surplus, 1), 1)

        # 4 metric cards
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Spend", f"${total_spend:,.0f}")
        col2.metric("Monthly Surplus", f"${surplus:,.0f}")
        col3.metric("Savings Rate", f"{savings_rate}%")
        col4.metric("Months to Goal", f"{ef_months} mo")

        st.divider()

        left, right = st.columns(2)

        with left:
            st.subheader("Spending Breakdown")
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
            st.subheader("Goal Timeline")
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
        st.subheader("Category Breakdown")
        st.dataframe(category_totals, use_container_width=True)

        st.divider()
        st.subheader("Raw Data")
        st.dataframe(df.head(20), use_container_width=True)

    else:
        st.info("Please select your amount and category columns above to see your dashboard.")

    st.divider()
    st.caption(
        "Global Fusion Foundation on AI Hackathon | "
        "Track: Fintech | Personal Finance AI"
    )
