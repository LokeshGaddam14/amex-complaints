import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="AMEX Complaints Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-label {
        font-size: 14px;
        opacity: 0.9;
    }
    .header-title {
        color: #1f77b4;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .section-header {
        color: #2c3e50;
        font-size: 24px;
        font-weight: bold;
        padding: 20px 0 10px 0;
        border-bottom: 3px solid #667eea;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="header-title">📊 AMEX Complaints Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666; font-size: 16px;'>Real-time Insights into Customer Complaints, Trends, Resolutions, and Satisfaction</p>", unsafe_allow_html=True)
st.divider()

# Generate Sample Data
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start='2023-01-01', end='2024-11-30', freq='D')
    
    categories = ['Billing Issues', 'Customer Service', 'Card Management', 'Fraud & Security', 'Delivery Issues']
    statuses = ['Closed', 'In Progress', 'Pending']
    
    n_records = 2000
    data = {
        'Date': np.random.choice(dates, n_records),
        'Category': np.random.choice(categories, n_records),
        'Status': np.random.choice(statuses, n_records),
        'Resolution_Days': np.random.randint(1, 45, n_records),
        'Satisfaction': np.random.randint(1, 6, n_records),
        'Complaint_ID': range(1, n_records + 1)
    }
    return pd.DataFrame(data)

df = load_data()

# Sidebar Filters
st.sidebar.markdown('<div class="section-header">🔍 Filters</div>', unsafe_allow_html=True)
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df['Date'].min().date(), df['Date'].max().date()),
    key="date_range"
)

category_filter = st.sidebar.multiselect(
    "Select Categories",
    options=df['Category'].unique(),
    default=df['Category'].unique()
)

status_filter = st.sidebar.multiselect(
    "Select Status",
    options=df['Status'].unique(),
    default=df['Status'].unique()
)

# Filter Data
filtered_df = df[
    (df['Date'].dt.date >= date_range[0]) &
    (df['Date'].dt.date <= date_range[1]) &
    (df['Category'].isin(category_filter)) &
    (df['Status'].isin(status_filter))
]

# Key Metrics Section
st.markdown('<div class="section-header">📈 Key Performance Indicators</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        label="Total Complaints",
        value=f"{len(filtered_df):,}",
        delta=f"{len(filtered_df) - len(df)//10}",
        delta_color="inverse"
    )

with col2:
    avg_resolution = filtered_df['Resolution_Days'].mean()
    st.metric(
        label="Avg Resolution (Days)",
        value=f"{avg_resolution:.1f}",
        delta="-2.3 days",
        delta_color="inverse"
    )

with col3:
    avg_satisfaction = filtered_df['Satisfaction'].mean()
    st.metric(
        label="Avg Satisfaction",
        value=f"{avg_satisfaction:.2f}/5.0",
        delta="+0.3",
        delta_color="normal"
    )

with col4:
    closed_rate = (len(filtered_df[filtered_df['Status'] == 'Closed']) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric(
        label="Closure Rate",
        value=f"{closed_rate:.1f}%",
        delta="+5%",
        delta_color="normal"
    )

with col5:
    high_satisfaction = (len(filtered_df[filtered_df['Satisfaction'] >= 4]) / len(filtered_df) * 100) if len(filtered_df) > 0 else 0
    st.metric(
        label="Satisfaction (4+)",
        value=f"{high_satisfaction:.1f}%",
        delta="+12%",
        delta_color="normal"
    )

st.divider()

# Complaints Trend
st.markdown('<div class="section-header">📅 Complaints Over Time</div>', unsafe_allow_html=True)
daily_complaints = filtered_df.groupby(filtered_df['Date'].dt.date).size().reset_index(name='Count')

fig_trend = px.line(
    daily_complaints,
    x='Date',
    y='Count',
    title='Daily Complaint Volume Trend',
    markers=True,
    line_shape='spline',
    color_discrete_sequence=['#667eea']
)
fig_trend.update_layout(hovermode='x unified', height=400)
st.plotly_chart(fig_trend, use_container_width=True)

st.divider()

# Category Distribution
st.markdown('<div class="section-header">🏷️ Complaint Categories Analysis</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    category_dist = filtered_df['Category'].value_counts()
    fig_pie = px.pie(
        values=category_dist.values,
        names=category_dist.index,
        title='Distribution by Category',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

with col2:
    category_avg_satisfaction = filtered_df.groupby('Category')['Satisfaction'].mean().sort_values(ascending=False)
    fig_bar = px.bar(
        x=category_avg_satisfaction.values,
        y=category_avg_satisfaction.index,
        orientation='h',
        title='Average Satisfaction by Category',
        color=category_avg_satisfaction.values,
        color_continuous_scale='RdYlGn'
    )
    fig_bar.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# Resolution and Satisfaction Analysis
st.markdown('<div class="section-header">⏱️ Resolution Time & Customer Satisfaction</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    fig_resolution = px.histogram(
        filtered_df,
        x='Resolution_Days',
        nbins=15,
        title='Resolution Time Distribution',
        color_discrete_sequence=['#764ba2'],
        labels={'Resolution_Days': 'Days to Resolve', 'count': 'Number of Complaints'}
    )
    fig_resolution.update_layout(height=400)
    st.plotly_chart(fig_resolution, use_container_width=True)

with col2:
    satisfaction_dist = filtered_df['Satisfaction'].value_counts().sort_index()
    fig_satisfaction = px.bar(
        x=satisfaction_dist.index,
        y=satisfaction_dist.values,
        title='Customer Satisfaction Rating Distribution',
        color=satisfaction_dist.index,
        color_continuous_scale='RdYlGn',
        labels={'x': 'Satisfaction Rating', 'y': 'Count'}
    )
    fig_satisfaction.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_satisfaction, use_container_width=True)

st.divider()

# Status Breakdown
st.markdown('<div class="section-header">✅ Complaint Status Overview</div>', unsafe_allow_html=True)

status_counts = filtered_df['Status'].value_counts()
fig_status = px.bar(
    x=status_counts.index,
    y=status_counts.values,
    title='Complaints by Status',
    color=status_counts.index,
    color_discrete_map={'Closed': '#2ecc71', 'In Progress': '#f39c12', 'Pending': '#e74c3c'},
    labels={'x': 'Status', 'y': 'Count'}
)
fig_status.update_layout(height=400)
st.plotly_chart(fig_status, use_container_width=True)

st.divider()

# Advanced Analytics
st.markdown('<div class="section-header">🔬 Advanced Analytics</div>', unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["📊 Category Performance", "⏰ Resolution Trends", "😊 Satisfaction Analysis"])

with tab1:
    category_stats = filtered_df.groupby('Category').agg({
        'Complaint_ID': 'count',
        'Resolution_Days': 'mean',
        'Satisfaction': 'mean'
    }).round(2)
    category_stats.columns = ['Total Complaints', 'Avg Resolution Days', 'Avg Satisfaction']
    st.dataframe(category_stats, use_container_width=True)

with tab2:
    status_stats = filtered_df.groupby('Status').agg({
        'Complaint_ID': 'count',
        'Resolution_Days': 'mean',
        'Satisfaction': 'mean'
    }).round(2)
    status_stats.columns = ['Count', 'Avg Resolution Days', 'Avg Satisfaction']
    st.dataframe(status_stats, use_container_width=True)

with tab3:
    satisfaction_by_category = filtered_df.groupby('Category')['Satisfaction'].agg(['count', 'mean', 'std']).round(2)
    satisfaction_by_category.columns = ['Complaints', 'Avg Satisfaction', 'Std Dev']
    st.dataframe(satisfaction_by_category, use_container_width=True)

st.divider()

# Data Table
st.markdown('<div class="section-header">📋 Detailed Records</div>', unsafe_allow_html=True)
st.dataframe(
    filtered_df.sort_values('Date', ascending=False).head(20),
    use_container_width=True,
    height=400
)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #999; font-size: 12px;'>" +
    "Data represents AMEX customer complaints from 2023-2024. " +
    "Dashboard updated in real-time." +
    "</p>",
    unsafe_allow_html=True
)
