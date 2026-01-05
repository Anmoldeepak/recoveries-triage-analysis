SELECT
    a.interest_accrual_flag,
    COUNT(*) AS accounts,
    SUM(a.balance) AS total_balance
FROM accounts a
JOIN legal_status l
  ON a.account_id = l.account_id
WHERE l.bankruptcy_flag = 1
   OR l.estate_flag = 1
GROUP BY a.interest_accrual_flag;
