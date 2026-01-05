-- Purpose:
-- Create a first-round triage framework to prioritize accounts
-- based on legal risk, data risk, and dollar value.

SELECT
    a.account_id,
    a.customer_id,
    a.strategy_type,
    a.balance,
    a.interest_accrual_flag,
    l.bankruptcy_flag,
    l.estate_flag,
    m.duplicate_flag,
    m.migration_ready_flag,
    CASE
        WHEN l.bankruptcy_flag = 1 OR l.estate_flag = 1
            THEN 'LEGAL_HIGH_RISK'
        WHEN m.duplicate_flag = 1
            THEN 'DATA_HIGH_RISK'
        WHEN a.balance >= 50000
            THEN 'HIGH_VALUE'
        ELSE 'LOW_PRIORITY'
    END AS triage_bucket
FROM accounts a
LEFT JOIN legal_status l
  ON a.account_id = l.account_id
LEFT JOIN migration_status m
  ON a.account_id = m.account_id;
