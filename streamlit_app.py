
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Health Business KPI Tracker", layout="wide")

# --- Load data ---
@st.cache_data
def load_data():
    kpi_monthly = pd.read_csv("kpi_monthly.csv")
    kpi_patients = pd.read_csv("kpi_patients.csv")
    return kpi_monthly, kpi_patients

kpi_monthly, kpi_patients = load_data()

# --- Summary Cards ---
st.title("🏥 Health Business KPI Tracker")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Patients (YTD)", int(kpi_monthly["total_patients"].sum()))
col2.metric("Revenue (YTD)", f"Rs {kpi_monthly['revenue'].sum():,}")
col3.metric("Appointments (YTD)", int(kpi_monthly["total_visits"].sum()))
col4.metric("Outstanding Payments", f"Rs {kpi_monthly['outstanding_payments'].sum():,}")

# --- Charts Row 1 ---
st.subheader("Monthly Revenue")
fig1 = px.bar(kpi_monthly, x="month", y="revenue", color="revenue",
              color_continuous_scale="blues", height=320)
fig1.update_layout(xaxis_title="", yaxis_title="Revenue (PKR)")
st.plotly_chart(fig1, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    st.subheader("Patient Growth")
    fig2 = px.line(kpi_monthly, x="month", y="total_patients", markers=True)
    fig2.update_traces(line_color="#29a3f3")
    fig2.update_layout(xaxis_title="", yaxis_title="Total Patients")
    st.plotly_chart(fig2, use_container_width=True)

with col6:
    st.subheader("No-show Rate")
    fig3 = px.line(kpi_monthly, x="month", y="no_show_count", markers=True)
    fig3.update_traces(line_color="#e06666")
    fig3.update_layout(xaxis_title="", yaxis_title="No-show Count")
    st.plotly_chart(fig3, use_container_width=True)

# --- Payer Mix Pie ---
st.subheader("Payer Mix")
payer_counts = kpi_patients['payer'].value_counts()
fig4 = px.pie(values=payer_counts.values, names=payer_counts.index, hole=0.4,
              color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig4, use_container_width=True)

# --- Recent Patient Activity Table ---
st.subheader("Recent Patient Activity")
st.dataframe(
    kpi_patients.sort_values("last_visit", ascending=False)[
        ["name", "doctor", "last_visit", "_]()
