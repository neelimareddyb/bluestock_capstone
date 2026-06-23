-- =================================================================
-- BLUESTOCK MUTUAL FUND ANALYTICS PLATFORM - DAY 2 ANALYTICAL QUERIES
-- =================================================================

-- Query 1: Top 5 Funds by Asset Under Management (AUM)
-- Source Table: fact_aum, Target: Identify dominant fund houses
SELECT fund_house, MAX(aum_crore) as peak_aum_crore
FROM fact_aum
GROUP BY fund_house
ORDER BY peak_aum_crore DESC
LIMIT 5;

-- Query 2: Average Net Asset Value (NAV) per Month for a specific fund
-- Source Table: fact_nav, Target: Track monthly smooth transitions
SELECT amfi_code, strftime('%Y-%m', date) as month, ROUND(AVG(nav), 4) as avg_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY month DESC
LIMIT 10;

-- Query 3: Total SIP Inflow Records Ordered Chronologically
-- Source Table: fact_sip, Target: Trace dynamic month-wise macro flows
SELECT month_year, sip_inflow_crore
FROM fact_sip
ORDER BY month_year DESC;

-- Query 4: Total Transaction Volume and Value Grouped by State
-- Source Table: fact_transactions, Target: Track regional demographic penetration
SELECT state, COUNT(*) as total_transactions, SUM(amount_inr) as total_invested_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_invested_inr DESC;

-- Query 5: High-Value Lumpsum Transactions
-- Source Table: fact_transactions, Target: Isolate massive whale inflows
SELECT investor_id, amfi_code, amount_inr, state, city
FROM fact_transactions
WHERE transaction_type = 'Lumpsum' AND amount_inr >= 100000
ORDER BY amount_inr DESC
LIMIT 10;

-- Query 6: Distribution of Investors Across Geographic Tiers
-- Source Table: fact_transactions, Target: Compare T30 vs B30 regional contributions
SELECT city_tier, COUNT(DISTINCT investor_id) as unique_investor_count, SUM(amount_inr) as tier_total_inr
FROM fact_transactions
GROUP BY city_tier;

-- Query 7: Transaction Split by Gender and Age Group
-- Source Table: fact_transactions, Target: Demographic segmentation profile
SELECT age_group, gender, COUNT(*) as transaction_count, ROUND(AVG(amount_inr), 2) as avg_transaction_size
FROM fact_transactions
GROUP BY age_group, gender
ORDER BY age_group ASC;

-- Query 8: Active vs Pending KYC Status Impact on Invested Capital
-- Source Table: fact_transactions, Target: Compliance pipeline processing validation
SELECT kyc_status, COUNT(DISTINCT investor_id) as investor_count, SUM(amount_inr) as total_capital_inr
FROM fact_transactions
GROUP BY kyc_status;

-- Query 9: Preferred Payment Modes by Volume and Total Value
-- Source Table: fact_transactions, Target: Process infrastructure tracking
SELECT payment_mode, COUNT(*) as transaction_count, SUM(amount_inr) as total_processed_inr
FROM fact_transactions
GROUP BY payment_mode
ORDER BY transaction_count DESC;

-- Query 10: Summary Matrix of Funds and Associated Transaction Volatility
-- Source Table: dim_fund Inner Joined with fact_transactions
SELECT f.amfi_code, f.fund_name, f.category, COUNT(t.transaction_id) as total_txn_count
FROM dim_fund f
JOIN fact_transactions t ON f.amfi_code = t.amfi_code
GROUP BY f.amfi_code, f.fund_name
ORDER BY total_txn_count DESC
LIMIT 5;