import streamlit as st
import pandas as pd
import plotly.express as px
st.set_page_config(
    page_title="AMEX Complaints Dashboard",
    layout="wide"
)
st.title("AMEX Complaints Analysis Dashboard")
st.markdown(
    """
    **Objective:**  
    Analyze complaint trends and resolution efficiency to identify operational bottlenecks.
    """
)
@st.cache_data
def load_data():
    df = pd.read_excel(r"C:\Users\lokes\Downloads\complaints_amex.xlsx")

    # schema lock (DO NOT CHANGE NAMES LATER)
    df = df.rename(columns={
        "issue_category": "category",
        "resolution_status": "status"
    })

    df["complaint_date"] = pd.to_datetime(df["complaint_date"], errors="coerce")
    df["days_to_resolve"] = pd.to_numeric(df["days_to_resolve"], errors="coerce")

    return df

df = load_data()
total_complaints = len(df)
avg_resolution_days = df["days_to_resolve"].mean()
closure_rate = (df["status"].str.lower() == "closed").mean() * 100

col1, col2, col3 = st.columns(3)

col1.metric("Total Complaints", f"{total_complaints}")
col2.metric("Avg Resolution Days", f"{avg_resolution_days:.1f}")
col3.metric("Closure Rate", f"{closure_rate:.1f}%")
total_complaints = len(df)
avg_resolution_days = df["days_to_resolve"].mean()
closure_rate = (df["status"].str.lower() == "closed").mean() * 100

col1, col2, col3 = st.columns(3)

col1.metric("Total Complaints", f"{total_complaints}")
col2.metric("Avg Resolution Days", f"{avg_resolution_days:.1f}")
col3.metric("Closure Rate", f"{closure_rate:.1f}%")
st.sidebar.header("Filters")

date_range = st.sidebar.date_input(
    "Complaint Date Range",
    [df["complaint_date"].min(), df["complaint_date"].max()]
)

selected_categories = st.sidebar.multiselect(
    "Issue Category",
    options=df["category"].unique(),
    default=df["category"].unique()
)

filtered_df = df[
    (df["complaint_date"] >= pd.to_datetime(date_range[0])) &
    (df["complaint_date"] <= pd.to_datetime(date_range[1])) &
    (df["category"].isin(selected_categories))
]
def resolution_bucket(days):
    if pd.isna(days):
        return "Unknown"
    elif days <= 5:
        return "Fast"
    elif days <= 15:
        return "Medium"
    elif days <= 30:
        return "Slow"
    else:
        return "Very Slow"

filtered_df["resolution_bucket"] = filtered_df["days_to_resolve"].apply(resolution_bucket)
filtered_df["month"] = filtered_df["complaint_date"].dt.to_period("M").astype(str)

monthly_trend = (
    filtered_df.groupby("month")
    .size()
    .reset_index(name="complaints")
)

fig1 = px.line(
    monthly_trend,
    x="month",
    y="complaints",
    title="Monthly Complaint Trend"
)

st.plotly_chart(fig1, use_container_width=True)
status_dist = filtered_df["status"].value_counts().reset_index()
status_dist.columns = ["status", "count"]

fig2 = px.pie(
    status_dist,
    names="status",
    values="count",
    title="Complaint Status Distribution"
)

st.plotly_chart(fig2, use_container_width=True)
bucket_dist = filtered_df["resolution_bucket"].value_counts().reset_index()
bucket_dist.columns = ["bucket", "count"]

fig3 = px.bar(
    bucket_dist,
    x="bucket",
    y="count",
    title="Resolution Speed Distribution"
)

st.plotly_chart(fig3, use_container_width=True)
category_perf = (
    filtered_df.groupby("category")["days_to_resolve"]
    .mean()
    .reset_index()
    .sort_values("days_to_resolve", ascending=False)
)

fig4 = px.bar(
    category_perf,
    x="days_to_resolve",
    y="category",
    orientation="h",
    title="Average Resolution Time by Issue Category"
)

st.plotly_chart(fig4, use_container_width=True)
category_bucket = (
    filtered_df.groupby(["category", "resolution_bucket"])
    .size()
    .reset_index(name="count")
)

fig5 = px.bar(
    category_bucket,
    x="resolution_bucket",
    y="count",
    color="category",
    barmode="group",
    title="Resolution Speed Distribution by Issue Category"
)

st.plotly_chart(fig5, use_container_width=True)
st.subheader("Key Insights")

st.markdown("""
- Complaint volume is largely stable with periodic spikes, indicating event-driven issues.
- Medium resolution timelines dominate, but slow and very slow cases present operational risk.
- Certain issue categories consistently take longer to resolve, indicating systemic bottlenecks.
- Improving resolution workflows for the slowest category would deliver the highest impact.
""")
