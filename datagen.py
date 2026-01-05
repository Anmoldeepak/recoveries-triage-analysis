import pandas as pd
import numpy as np
import random

np.random.seed(42)

N = 8000

strategy_types = ['DIRECT', 'LITIGATION', 'SETTLEMENT', 'CASH', 'SPECIAL']
strategy_probs = [0.4, 0.2, 0.15, 0.1, 0.15]

accounts = []

for i in range(N):
    strategy = np.random.choice(strategy_types, p=strategy_probs)

    if strategy == 'SPECIAL':
        balance = np.random.randint(20000, 150000)
        interest = 'N'
    elif strategy == 'LITIGATION':
        balance = np.random.randint(10000, 80000)
        interest = 'Y'
    else:
        balance = np.random.randint(1000, 30000)
        interest = 'Y'

    accounts.append({
        'account_id': i + 1,
        'customer_id': random.randint(1, int(N / 2)),
        'strategy_type': strategy,
        'balance': balance,
        'days_past_due': np.random.randint(90, 720),
        'interest_accrual_flag': interest,
        'account_status': 'CHARGED_OFF'
    })

accounts_df = pd.DataFrame(accounts)
accounts_df.to_csv('data/accounts.csv', index=False)
legal_rows = []

for _, row in accounts_df.iterrows():
    bankruptcy = 0
    estate = 0
    litigation = 0

    if row['strategy_type'] == 'SPECIAL':
        bankruptcy = np.random.choice([0,1], p=[0.3, 0.7])
        estate = np.random.choice([0,1], p=[0.8, 0.2])
    elif row['strategy_type'] == 'LITIGATION':
        litigation = 1

    legal_rows.append({
        'account_id': row['account_id'],
        'bankruptcy_flag': bankruptcy,
        'bankruptcy_type': np.random.choice(['CH7','CH11','CH13']) if bankruptcy else None,
        'estate_flag': estate,
        'litigation_flag': litigation
    })

legal_df = pd.DataFrame(legal_rows)
legal_df.to_csv('data/legal_status.csv', index=False)
migration_rows = []

for _, row in accounts_df.iterrows():
    duplicate = 0
    ready = 'Y'

    if row['strategy_type'] == 'SPECIAL':
        duplicate = np.random.choice([0,1], p=[0.6, 0.4])
        ready = 'N'
    elif row['strategy_type'] == 'LITIGATION':
        duplicate = np.random.choice([0,1], p=[0.85, 0.15])

    migration_rows.append({
        'account_id': row['account_id'],
        'source_system': np.random.choice(['LEGACY_A','LEGACY_B']),
        'target_system': 'OMEGA',
        'duplicate_flag': duplicate,
        'migration_ready_flag': ready
    })

migration_df = pd.DataFrame(migration_rows)
migration_df.to_csv('data/migration_status.csv', index=False)
print(accounts_df['strategy_type'].value_counts(normalize=True))
