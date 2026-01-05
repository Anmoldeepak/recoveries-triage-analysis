SELECT
    COUNT(*) AS accounts,
    SUM(a.balance) AS total_balance
FROM accounts a
JOIN legal_status l
  ON a.account_id = l.account_id
JOIN migration_status m
  ON a.account_id = m.account_id
WHERE (l.bankruptcy_flag = 1 OR l.estate_flag = 1)
  AND m.duplicate_flag = 1;
