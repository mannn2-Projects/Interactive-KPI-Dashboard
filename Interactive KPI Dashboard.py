import pandas as pd
import plotly.express as px

# Load summary tables
monthly_summary = pd.read_csv("monthly_summary.csv")
top_products = pd.read_csv("top_products.csv")
top_customers = pd.read_csv("top_customers.csv")

# Convert CustomerID to string so Plotly treats it like categories
top_customers["CustomerID"] = top_customers["CustomerID"].astype(str)

# -----------------------------
# Shared layout styling
# -----------------------------
common_layout = dict(
    template="plotly_dark",
    font=dict(family="Arial", size=14),
    title=dict(x=0.05, xanchor="left"),
    plot_bgcolor="#111111",
    paper_bgcolor="#111111",
    margin=dict(l=70, r=40, t=70, b=60)
)

# -----------------------------
# Chart 1: Monthly Revenue Trend
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
    marker=dict(size=9)
)

fig_monthly.update_layout(
    **common_layout,
    xaxis_title="Month",
    yaxis_title="Revenue ($)",
    yaxis_tickprefix="$"
)

fig_monthly.show()

# -----------------------------
# Chart 2: Top 10 Products by Revenue
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
    xaxis_tickprefix="$"
)

fig_products.show()

# -----------------------------
# Chart 3: Top 10 Customers by Revenue
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
    xaxis_tickprefix="$"
)

fig_customers.show()


