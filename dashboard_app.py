import pandas as pd
import plotly.express as px
import streamlit as st

# -----------------------------
# Page setup
# -----------------------------
st.set_page_config(
    page_title="Interactive KPI Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv("online_retail_uk_cleaned.csv")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

monthly_summary = pd.read_csv("monthly_summary.csv")
top_products = pd.read_csv("top_products.csv")
top_customers = pd.read_csv("top_customers.csv")

top_customers["CustomerID"] = top_customers["CustomerID"].astype(str)

# -----------------------------
# KPI calculations
# -----------------------------
total_revenue = df["Revenue"].sum()
total_orders = df["InvoiceNo"].nunique()
total_units_sold = df["Quantity"].sum()
average_order_value = total_revenue / total_orders
active_customers = df["CustomerID"].nunique()

# -----------------------------
# Dashboard title
# -----------------------------
st.title("Interactive KPI Dashboard")
st.markdown("Retail sales performance dashboard for UK transactions from Jan 2011 to Jun 2011.")

# -----------------------------
# KPI row
# -----------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Units Sold", f"{total_units_sold:,}")
col4.metric("Avg Order Value", f"${average_order_value:,.2f}")
col5.metric("Active Customers", f"{active_customers:,}")

# -----------------------------
# Shared chart style
# -----------------------------
common_layout = dict(
    template="plotly_dark",
    font=dict(family="Arial", size=14),
    title=dict(x=0.05, xanchor="left"),
    plot_bgcolor="#111111",
    paper_bgcolor="#111111",
    margin=dict(l=60, r=30, t=60, b=50)
)

# -----------------------------
# Monthly revenue chart
# -----------------------------
fig_monthly = px.line(
    monthly_summary,
    x="YearMonth",
    y="Revenue",
    title="Monthly Revenue Trend",
    markers=True
)

fig_monthly.update_traces(
    line=dict(width=4),
    marker=dict(size=8)
)

fig_monthly.update_layout(
    **common_layout,
    xaxis_title="Month",
    yaxis_title="Revenue ($)",
    yaxis_tickprefix="$"
)

# -----------------------------
# Top products chart
# -----------------------------
top_products_sorted = top_products.sort_values("Revenue", ascending=True)

fig_products = px.bar(
    top_products_sorted,
    x="Revenue",
    y="Description",
    orientation="h",
    title="Top 10 Products by Revenue",
    text="Revenue"
)

fig_products.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig_products.update_layout(
    **common_layout,
    xaxis_title="Revenue ($)",
    yaxis_title="Product",
    xaxis_tickprefix="$",
    height=500
)

# -----------------------------
# Top customers chart
# -----------------------------
top_customers_sorted = top_customers.sort_values("Revenue", ascending=True)

fig_customers = px.bar(
    top_customers_sorted,
    x="Revenue",
    y="CustomerID",
    orientation="h",
    title="Top 10 Customers by Revenue",
    text="Revenue"
)

fig_customers.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig_customers.update_layout(
    **common_layout,
    xaxis_title="Revenue ($)",
    yaxis_title="Customer ID",
    xaxis_tickprefix="$",
    height=500
)

# -----------------------------
# Show charts
# -----------------------------
st.plotly_chart(fig_monthly, use_container_width=True)

left_col, right_col = st.columns(2)

with left_col:
    st.plotly_chart(fig_products, use_container_width=True)

with right_col:
    st.plotly_chart(fig_customers, use_container_width=True)