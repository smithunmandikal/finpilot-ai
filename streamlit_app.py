import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FinPilot AI", page_icon="💰")

st.title("💰 FinPilot AI")
st.subheader("Smart Budget & Financial Advisor")

st.markdown("""
FinPilot AI is an AI-powered personal financial advisor 
built on 32,424 real users across 5 global regions.

Upload your transaction CSV to get a personalized 
plain-English financial plan.
""")

uploaded = st.file_uploader("Upload your transaction CSV", 
                             type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    st.success(f"Loaded {len(df)} transactions")
    st.dataframe(df.head(10))
    
    if 'monthly_income_usd' in df.columns:
        fig = px.histogram(df, x='monthly_income_usd', 
                          title='Income Distribution',
                          color_discrete_sequence=['#0B6E4F'])
        st.plotly_chart(fig)
        
        avg_income = df['monthly_income_usd'].mean()
        avg_expenses = df['monthly_expenses_usd'].mean()
        surplus = avg_income - avg_expenses
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Avg Income", f"${avg_income:,.0f}")
        col2.metric("Avg Expenses", f"${avg_expenses:,.0f}")
        col3.metric("Avg Surplus", f"${surplus:,.0f}")

st.markdown("---")
st.caption("Global Fusion Foundation on AI Hackathon | Track: Fintech")
