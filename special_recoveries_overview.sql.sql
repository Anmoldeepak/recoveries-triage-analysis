SELECT
    COUNT(*) AS special_accounts,
    SUM(a.balance) AS special_total_balance
FROM accounts a
JOIN legal_status l
  ON a.account_id = l.account_id
WHERE l.bankruptcy_flag = 1
   OR l.estate_flag = 1;
