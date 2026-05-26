-- ============================================================================
-- CUSTOMER CHURN ANALYTICS & BEHAVIORAL DEEP DIVE ENGINE
-- Database Schema, Data Simulation, and Metric Multiplier Views
-- ============================================================================

-- 1. SETUP SIMULATED ENVIRONMENT STRUCTURES
DROP TABLE IF EXISTS customer_telemetry_snapshot;
DROP TABLE IF EXISTS billing_history;
DROP TABLE IF EXISTS support_tickets;
DROP TABLE IF EXISTS feature_interactions;
DROP TABLE IF EXISTS customer_master;

CREATE TABLE customer_master (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    ltv NUMERIC(10, 2) NOT NULL,
    current_tier VARCHAR(20) CHECK (current_tier IN ('Basic', 'Pro', 'Enterprise')),
    signup_date DATE NOT NULL,
    churn_date DATE,
    account_status VARCHAR(20) DEFAULT 'Active' CHECK (account_status IN ('Active', 'Churned'))
);

CREATE TABLE feature_interactions (
    log_id SERIAL PRIMARY KEY,
    customer_id VARCHAR(20) REFERENCES customer_master(customer_id),
    feature_name VARCHAR(50),
    interaction_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE support_tickets (
    ticket_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) REFERENCES customer_master(customer_id),
    date_created DATE NOT NULL,
    is_unresolved INT DEFAULT 1, -- 1 = True, 0 = False
    age_days INT NOT NULL
);

CREATE TABLE billing_history (
    invoice_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) REFERENCES customer_master(customer_id),
    invoice_date DATE NOT NULL,
    failed_payment_flag INT DEFAULT 0,
    plan_downgraded_flag INT DEFAULT 0
);

-- 2. SEED MOCK ENTERPRISE USER LOGS
INSERT INTO customer_master (customer_id, customer_name, email, ltv, current_tier, signup_date, churn_date, account_status) VALUES
('CUST-1001', 'Alpha Corp', 'alpha@corp.com', 1200.00, 'Enterprise', '2025-06-01', NULL, 'Active'),
('CUST-1002', 'Beta LLC', 'beta@llc.com', 150.00, 'Pro', '2026-01-10', '2026-01-24', 'Churned'),
('CUST-1003', 'Gamma Inc', 'gamma@inc.com', 850.00, 'Enterprise', '2025-05-15', '2026-01-15', 'Churned'),
('CUST-1004', 'Delta Co', 'delta@co.com', 45.00, 'Basic', '2026-01-02', '2026-01-10', 'Churned'),
('CUST-1005', 'Epsilon Org', 'epsilon@org.com', 2100.00, 'Enterprise', '2024-11-20', NULL, 'Active');

INSERT INTO feature_interactions (customer_id, feature_name) VALUES
('CUST-1001', 'Feature X'), ('CUST-1001', 'Dashboard API'),
('CUST-1003', 'Setup Checklist'),
('CUST-1005', 'Feature X'), ('CUST-1005', 'Setup Checklist'), ('CUST-1005', 'Advanced Analytics');

INSERT INTO support_tickets (ticket_id, customer_id, date_created, is_unresolved, age_days) VALUES
('TCK-99', 'CUST-1002', '2026-01-12', 1, 6),
('TCK-88', 'CUST-1003', '2026-01-02', 1, 8);

INSERT INTO billing_history (invoice_id, customer_id, invoice_date, failed_payment_flag, plan_downgraded_flag) VALUES
('INV-501', 'INV-501', '2026-01-05', 1, 0),
('INV-502', 'CUST-1003', '2025-12-28', 0, 1);


-- ============================================================================
-- ANALYTICAL QUERIES
-- ============================================================================

-- QUERY 1: MONTH-OVER-MONTH CHURN TREND WITH ROLLING 3-MONTH AVERAGE
SELECT 
    DATE_TRUNC('month', churn_date)::DATE AS reporting_month,
    COUNT(customer_id) AS churned_customer_count,
    ROUND(
        (COUNT(customer_id)::NUMERIC / (SELECT COUNT(*) FROM customer_master WHERE signup_date <= '2026-01-31')) * 100, 2
    ) AS mom_churn_rate,
    ROUND(
        AVG(COUNT(customer_id)) OVER(ORDER BY DATE_TRUNC('month', churn_date) ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2
    ) AS rolling_3_month_avg_volume
FROM customer_master
WHERE account_status = 'Churned'
GROUP BY 1
ORDER BY reporting_month DESC;


-- QUERY 2: NEW VS TENURED CUSTOMER RETENTION PROFILES
SELECT 
    CASE 
        WHEN (churn_date - signup_date) <= 90 THEN 'New (<90 Days - Poor Onboarding Risk)'
        ELSE 'Existing (>90 Days - Value Erosion Risk)'
    END AS churn_tenure_segment,
    COUNT(customer_id) AS total_lost_accounts,
    ROUND(AVG(churn_date - signup_date), 1) AS average_days_to_attrition
FROM customer_master
WHERE account_status = 'Churned'
GROUP BY 1;


-- QUERY 3: FEATURE ADOPTION CORRELATION STUDY
SELECT 
    CASE 
        WHEN fx.customer_id IS NULL THEN 'Never Handled Feature X'
        ELSE 'Active Feature X Adoption'
    END AS feature_adoption_profile,
    COUNT(cm.customer_id) AS total_tracked_base,
    SUM(CASE WHEN cm.account_status = 'Churned' THEN 1 ELSE 0 END) AS total_churned,
    ROUND((SUM(CASE WHEN cm.account_status = 'Churned' THEN 1 ELSE 0 END)::NUMERIC / COUNT(cm.customer_id)) * 100, 2) AS churn_rate_pct
FROM customer_master cm
LEFT JOIN (
    SELECT DISTINCT customer_id FROM feature_interactions WHERE feature_name = 'Feature X'
) fx ON cm.customer_id = fx.customer_id
GROUP BY 1;
