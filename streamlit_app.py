import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FinPilot AI", page_icon="💰", layout="wide")

st.title("💰 FinPilot AI")
st.subheader("Smart Budget & Financial Advisor")
st.markdown("*Upload your transaction CSV to get your personalized financial dashboard.*")
st.divider()

with st.sidebar:
    st.header("Your Profile")
    monthly_income = st.number_input("Monthly take-home income ($)", min_value=0, value=4000)
    st.subheader("Your Goal")
    goal_name = st.text_input("Goal name", "Emergency Fund")
    goal_amount = st.number_input("Target amount ($)", value=3000)

uploaded_file = st.file_uploader("Upload your transaction CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.success(f"Loaded {len(df)} transactions successfully")

    total_spend = df["amount"].sum()
    surplus = monthly_income - total_spend
    savings_spend = df[df["category"] == "Savings"]["amount"].sum()
    savings_rate = round((savings_spend / monthly_income) * 100, 1)
    debt_spend = df[df["category"] == "Debt repayment"]["amount"].sum()
    dti = round((debt_spend / monthly_income) * 100, 1)
    ef_months = round((total_spend * 3) / max(surplus, 1), 1)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Monthly Surplus", f"${surplus:,.0f}")
    col2.metric("Savings Rate", f"{savings_rate}%")
    col3.metric("Debt to Income", f"{dti}%")
    col4.metric("Months to Emergency Fund", f"{ef_months} mo")

    st.divider()

    left, right = st.columns(2)

    with left:
        st.subheader("Spending Breakdown")
        category_totals = df.groupby("category")["amount"].sum().reset_index()
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
            x=["Months to Goal"],
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
    st.subheader("Your Transactions")
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.caption("Global Fusion Foundation on AI Hackathon | Track: Fintech | Personal Finance AI")
