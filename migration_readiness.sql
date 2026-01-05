SELECT
    migration_ready_flag,
    COUNT(*) AS accounts,
    SUM(a.balance) AS total_balance
FROM migration_status m
JOIN accounts a
  ON m.account_id = a.account_id
GROUP BY migration_ready_flag;
