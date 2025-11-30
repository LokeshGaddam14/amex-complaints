-- AMEX COMPLAINTS ANALYSIS - SQL QUERIES
-- These queries provide actionable insights for complaint analysis
-- and customer satisfaction metrics

-- Query 1: Monthly Complaint Volume Trend
-- Shows complaint trends to identify seasonal patterns
SELECT 
    DATE_TRUNC('month', complaint_date)::DATE AS complaint_month,
    COUNT(*) AS total_complaints,
    COUNT(CASE WHEN status = 'Closed' THEN 1 END) AS resolved_complaints,
    ROUND(COUNT(CASE WHEN status = 'Closed' THEN 1 END)::NUMERIC / COUNT(*) * 100, 2) AS resolution_rate_pct
FROM complaints
GROUP BY DATE_TRUNC('month', complaint_date)
ORDER BY complaint_month DESC;

-- Query 2: Top 10 Complaint Categories
SELECT 
    category,
    COUNT(*) AS complaint_count,
    ROUND(COUNT(*)::NUMERIC / (SELECT COUNT(*) FROM complaints) * 100, 2) AS percentage,
    AVG(EXTRACT(DAY FROM (resolved_date - complaint_date))) AS avg_resolution_days
FROM complaints
WHERE resolved_date IS NOT NULL
GROUP BY category
ORDER BY complaint_count DESC
LIMIT 10;

-- Query 3: Customer Lifetime Complaint Count
SELECT 
    customer_id,
    COUNT(*) AS total_complaints,
    ROUND(AVG(satisfaction_rating), 2) AS avg_satisfaction
FROM complaints
GROUP BY customer_id
HAVING COUNT(*) >= 3
ORDER BY total_complaints DESC
LIMIT 20;

-- Query 4: Resolution Time Analysis
SELECT 
    department,
    COUNT(*) AS complaints_handled,
    ROUND(AVG(EXTRACT(DAY FROM (resolved_date - complaint_date))), 1) AS avg_days_to_resolve
FROM complaints
WHERE resolved_date IS NOT NULL
GROUP BY department
ORDER BY avg_days_to_resolve ASC;
