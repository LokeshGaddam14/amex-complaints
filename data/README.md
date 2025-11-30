# Data Directory

## Overview
This directory contains American Express customer complaint data used for exploratory data analysis and insights generation.

## Dataset Information

### Data Source
- **Source**: Public AMEX complaints dataset or internal customer feedback
- **Type**: Customer service complaints and issues
- **Period**: Time-series data from multiple years
- **Records**: Varies by dataset size

### Data Structure
```
data/
├── raw/
│   ├── complaints_raw.csv
│   └── customer_feedback.json
├── processed/
│   ├── cleaned_complaints.csv
│   └── categorized_complaints.csv
└── analysis/
    └── insights_report.json
```

## Data Fields
- **Complaint Date**: When complaint was filed
- **Issue**: Type or category of complaint
- **Sub-issue**: Detailed issue categorization
- **Complaint Text**: Full complaint description
- **Resolution**: How the complaint was resolved
- **Resolution Date**: When issue was resolved
- **Status**: Open, In Progress, Closed

## Analysis Dimensions
- **Temporal**: Complaint volume over time, seasonal patterns
- **Categorical**: Issue types, complaint categories distribution
- **Resolution**: Time to resolution, resolution rates
- **Text**: Sentiment analysis, common complaint themes

## Data Preprocessing
1. Remove duplicates and null values
2. Standardize text (lowercase, stemming)
3. Categorize complaints using keyword matching
4. Calculate resolution times
5. Generate temporal aggregations

## Usage
The `ComplaintsAnalyzer` class loads and processes data from this directory.

## Privacy & Compliance
All customer data is anonymized and complies with data protection regulations.
