-- Purpose:
-- First-pass triage to understand where total outstanding balance sits
-- across recovery strategies. This informs where to focus deeper analysis.

SELECT
    strategy_type,
    COUNT(*) AS account_count,
    SUM(balance) AS total_balance
FROM accounts
GROUP BY strategy_type
ORDER BY total_balance DESC;
