import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page Configuration
st.set_page_config(page_title="AMEX Complaints Dashboard", layout="wide")
st.title("📊 AMEX Complaints Analysis Dashboard")
st.markdown("Real-time insights into complaint trends, resolutions, and customer satisfaction")

# Sidebar Filters
st.sidebar.header("Filters")
date_range = st.sidebar.slider(
    "Select Date Range",
    min_value=datetime(2023, 1, 1),
    max_value=datetime(2024, 11, 30),
    value=(datetime(2024, 9, 1), datetime(2024, 11, 30)),
    format="YYYY-MM-DD"
)

category_filter = st.sidebar.multiselect(
    "Complaint Categories",
    ["Billing", "Service", "Account", "Product", "Fraud", "Other"],
    default=["Billing", "Service"]
)

# Mock Data Generation
np.random.seed(42)
date_range_data = pd.date_range(start=date_range[0], end=date_range[1], freq="D")
complaints_data = pd.DataFrame({
    'date': np.repeat(date_range_data, 30),
    'complaint_id': range(len(date_range_data) * 30),
    'category': np.random.choice(category_filter, len(date_range_data) * 30),
    'satisfaction': np.random.randint(1, 6, len(date_range_data) * 30),
    'resolution_days': np.random.randint(0, 20, len(date_range_data) * 30),
    'status': np.random.choice(['Closed', 'Open', 'In Progress'], len(date_range_data) * 30)
})

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Complaints",
        f"{len(complaints_data):,}",
        delta="-5%",
        delta_color="inverse"
    )

with col2:
    resolution_rate = (complaints_data['status'] == 'Closed').sum() / len(complaints_data) * 100
    st.metric(
        "Resolution Rate",
        f"{resolution_rate:.1f}%",
        delta="+2.3%",
        delta_color="normal"
    )

with col3:
    avg_satisfaction = complaints_data['satisfaction'].mean()
    st.metric(
        "Avg Satisfaction",
        f"{avg_satisfaction:.1f}/5",
        delta="-0.2",
        delta_color="inverse"
    )

with col4:
    avg_resolution = complaints_data['resolution_days'].mean()
    st.metric(
        "Avg Resolution (days)",
        f"{avg_resolution:.1f}",
        delta="-1.2",
        delta_color="inverse"
    )

st.markdown("---")

# Row 1: Charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Daily Complaint Trend")
    daily_complaints = complaints_data.groupby('date').size()
    fig_trend = px.line(x=daily_complaints.index, y=daily_complaints.values,
                        labels={'x': 'Date', 'y': 'Complaints'},
                        markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.subheader("📊 Complaints by Category")
    category_dist = complaints_data['category'].value_counts()
    fig_category = px.pie(values=category_dist.values, names=category_dist.index)
    st.plotly_chart(fig_category, use_container_width=True)

st.markdown("---")

# Row 2: More Analytics
col1, col2 = st.columns(2)

with col1:
    st.subheader("⭐ Satisfaction Distribution")
    satisfaction_dist = complaints_data['satisfaction'].value_counts().sort_index()
    fig_satisfaction = px.bar(x=satisfaction_dist.index, y=satisfaction_dist.values,
                              labels={'x': 'Rating', 'y': 'Count'},
                              color=satisfaction_dist.values)
    st.plotly_chart(fig_satisfaction, use_container_width=True)

with col2:
    st.subheader("🔄 Status Distribution")
    status_dist = complaints_data['status'].value_counts()
    fig_status = px.bar(x=status_dist.index, y=status_dist.values,
                        color=status_dist.index,
                        color_discrete_map={'Closed': '#2ecc71', 'Open': '#e74c3c', 'In Progress': '#f39c12'})
    st.plotly_chart(fig_status, use_container_width=True)

st.markdown("---")

# Data Table
st.subheader("📋 Detailed Complaint Data")
st.dataframe(complaints_data.head(50), use_container_width=True)

st.info("💡 This dashboard demonstrates data visualization capabilities and analytical insights")
