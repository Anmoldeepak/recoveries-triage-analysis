# recoveries-triage-analysis
SQL-driven analysis to triage recoveries accounts and de-risk system migration using synthetic data.
> This project uses synthetic data generated for demonstration purposes only.
# Recoveries Triage & Migration Risk Analysis

## Objective
This project simulates how a business manager would use SQL and structured analysis
to triage recoveries data, identify where financial value and risk exist, and
support a phased migration of accounts to a new core system.

The focus is on:
- First-pass triage
- Dollar impact assessment
- Legal and data risk identification
- Explainable prioritization logic


## Business Context

The dataset represents post-default small business accounts being worked through
different recovery strategies:
- Direct collections
- Litigation
- Debt settlement
- Cash recoveries
- Special recoveries (bankruptcy and estate)

A subset of these accounts is being migrated from legacy systems to a new core
system ("Omega"). Poor data quality or legal constraints introduce material risk
during migration.

---

## Data Overview

### 1. accounts
Represents the financial state of each recovery account.

Key fields:
- `account_id`: Unique identifier for each account
- `customer_id`: Customer identifier (a customer may have multiple accounts)
- `strategy_type`: Current recovery strategy (DIRECT, LITIGATION, SETTLEMENT, CASH, SPECIAL)
- `balance`: Outstanding dollar amount
- `days_past_due`: Severity of delinquency
- `interest_accrual_flag`: Whether interest continues to accrue
- `account_status`: Charged-off / closed state

Purpose:
- Identify where outstanding dollars exist
- Segment value across recovery strategies

---

### 2. legal_status
Captures legal and regulatory constraints associated with accounts.

Key fields:
- `bankruptcy_flag`: Indicates bankruptcy protection
- `bankruptcy_type`: Chapter 7 / 11 / 13
- `estate_flag`: Customer deceased
- `litigation_flag`: Account involved in legal proceedings

Purpose:
- Identify Special Recoveries
- Quantify legally constrained balances
- Explain why some accounts require special handling

---

### 3. migration_status
Tracks readiness and risk associated with system migration.

Key fields:
- `source_system`: Legacy system where the record originates
- `target_system`: Destination system (Omega)
- `duplicate_flag`: Indicates duplicate or conflicting records
- `migration_ready_flag`: Indicates whether account is safe to migrate

Purpose:
- Identify migration risk
- Quantify dollar exposure due to data quality issues
- Support phased migration decisions

---

## Analysis Summary

### Value Segmentation
A first-pass aggregation shows that certain recovery strategies,
particularly Special Recoveries, represent a disproportionate share of
outstanding balance relative to account volume.

### Special Recoveries
- Special Recoveries include accounts in bankruptcy or estate.
- A significant portion of these accounts does not accrue interest.
- Legal constraints and opportunity cost justify isolating this group
  for careful handling prior to migration.

### Migration Risk & Duplication
- Duplicate records represent meaningful dollar exposure.
- A subset of Special Recoveries is both legally constrained and duplicated,
  making them the highest-risk candidates for migration.

### Triage & Prioritization
Accounts are bucketed into:
- Legal High Risk
- Data High Risk
- High Value (clean records)
- Low Priority

This framework enables moving fast by migrating clean, high-value accounts
while explicitly deferring high-risk accounts for remediation.

---

## Key Takeaway
This project demonstrates how SQL can be used to support business judgment,
risk-aware prioritization, and governance-friendly decision making in a
recoveries and system migration context.
