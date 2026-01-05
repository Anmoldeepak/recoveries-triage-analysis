import duckdb
import pandas as pd

print("Starting analysis script...")

con = duckdb.connect(database='recoveries.duckdb', read_only=False)

# DROP existing tables (safe in sandbox)
con.execute("DROP TABLE IF EXISTS accounts")
con.execute("DROP TABLE IF EXISTS legal_status")
con.execute("DROP TABLE IF EXISTS migration_status")

# Recreate tables
con.execute("""
    CREATE TABLE accounts AS
    SELECT * FROM read_csv_auto('data/accounts.csv')
""")

con.execute("""
    CREATE TABLE legal_status AS
    SELECT * FROM read_csv_auto('data/legal_status.csv')
""")

con.execute("""
    CREATE TABLE migration_status AS
    SELECT * FROM read_csv_auto('data/migration_status.csv')
""")

# Sanity checks
print(con.execute("SELECT COUNT(*) FROM accounts").fetchall())
print(con.execute("SELECT COUNT(*) FROM legal_status").fetchall())
print(con.execute("SELECT COUNT(*) FROM migration_status").fetchall())

# First business query
df = con.execute("""
    SELECT
        strategy_type,
        COUNT(*) AS accounts,
        SUM(balance) AS total_balance
    FROM accounts
    GROUP BY strategy_type
    ORDER BY total_balance DESC
""").fetchdf()

print(df)
special_df = con.execute("""
    SELECT
        COUNT(*) AS special_accounts,
        SUM(a.balance) AS special_total_balance
    FROM accounts a
    JOIN legal_status l
      ON a.account_id = l.account_id
    WHERE l.bankruptcy_flag = 1
       OR l.estate_flag = 1
""").fetchdf()

print("\nSpecial Recoveries Overview")
print(special_df)

# segment_df = con.execute("""SELECT strategy_type,
#     COUNT(*) AS account_count,
#     SUM(balance) AS total_balance
# FROM accounts
# GROUP BY strategy_type
# ORDER BY total_balance DESC;
#       """).fetchdf()

# print("\nSegmentation")
# print(segment_df)
# print("\nSegmentation done")

interest_df = con.execute("""
    SELECT
        a.interest_accrual_flag,
        COUNT(*) AS accounts,
        SUM(a.balance) AS total_balance
    FROM accounts a
    JOIN legal_status l
      ON a.account_id = l.account_id
    WHERE l.bankruptcy_flag = 1
       OR l.estate_flag = 1
    GROUP BY a.interest_accrual_flag
""").fetchdf()

print("\nInterest Accrual in Special Recoveries")
print(interest_df)
dup_df = con.execute("""
    SELECT
        m.duplicate_flag,
        COUNT(*) AS accounts,
        SUM(a.balance) AS total_balance
    FROM migration_status m
    JOIN accounts a
      ON m.account_id = a.account_id
    GROUP BY m.duplicate_flag
""").fetchdf()

print("\nDuplicate Record Risk")
print(dup_df)
special_dup_df = con.execute("""
    SELECT
        COUNT(*) AS accounts,
        SUM(a.balance) AS total_balance
    FROM accounts a
    JOIN legal_status l
      ON a.account_id = l.account_id
    JOIN migration_status m
      ON a.account_id = m.account_id
    WHERE (l.bankruptcy_flag = 1 OR l.estate_flag = 1)
      AND m.duplicate_flag = 1
""").fetchdf()

print("\nSpecial Recoveries with Duplicate Records")
print(special_dup_df)

triage_df = con.execute("""
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
      ON a.account_id = m.account_id
""").fetchdf()

print("\nSample Triage Output")
print(triage_df.head(10))
summary_df = con.execute("""
    SELECT
        triage_bucket,
        COUNT(*) AS accounts,
        SUM(balance) AS total_balance
    FROM (
        SELECT
            a.balance,
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
          ON a.account_id = m.account_id
    )
    GROUP BY triage_bucket
    ORDER BY total_balance DESC
""").fetchdf()

print("\nTriage Summary")
print(summary_df)
