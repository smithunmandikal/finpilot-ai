# ── FinPilot AI — Synthetic Transaction Data Generator ──────────────────
# What this script does:
# Creates a realistic fake bank statement CSV with 500+ transactions
# across 8 spending categories. Used to test the FinPilot AI app.
# ────────────────────────────────────────────────────────────────────────

# Step 1: Import tools
import pandas as pd          # for creating and managing data tables
import numpy as np           # for random numbers and math
from faker import Faker      # for generating fake dates

# Step 2: Set up tools
fake = Faker()               # turn on the Faker machine
np.random.seed(42)           # fix the random seed so results are reproducible

# Step 3: Define merchants
# Format: ('MERCHANT NAME', base_amount_in_dollars, times_per_month)
MERCHANTS = {
    'Housing':        [('RENT PAYMENT', 1450, 1),
                       ('CON EDISON UTILITY', 95, 1)],
    'Food':           [('WHOLE FOODS MARKET', 55, 4),
                       ('CHIPOTLE', 13, 3),
                       ('DOORDASH', 28, 5)],
    'Transport':      [('SHELL FUEL', 58, 3),
                       ('UBER', 17, 4)],
    'Entertainment':  [('NETFLIX', 15, 1),
                       ('SPOTIFY', 10, 1)],
    'Debt repayment': [('CHASE VISA PAYMENT', 200, 1),
                       ('SALLIE MAE LOANS', 150, 1)],
    'Savings':        [('SAVINGS TRANSFER', 100, 1)],
    'Healthcare':     [('CVS PHARMACY', 22, 2),
                       ('HEALTH INSURANCE', 180, 1)],
    'Other':          [('AMAZON', 35, 3),
                       ('TARGET', 48, 2)],
}

# Step 4: Create an empty list to store transactions
rows = []

# Step 5: Loop through every merchant and generate transactions
for category, merchants in MERCHANTS.items():
    for merchant_name, base_amount, frequency in merchants:
        for _ in range(frequency):
            rows.append({
                'date':        fake.date_between(
                                   start_date='-30d',
                                   end_date='today'
                               ).isoformat(),
                'description': merchant_name,
                'amount':      round(
                                   base_amount * np.random.uniform(0.85, 1.15),
                                   2
                               ),
                'category':    category
            })

# Step 6: Convert list to a pandas DataFrame (table)
df = pd.DataFrame(rows)
df = df.sort_values('date').reset_index(drop=True)

# Step 7: Save as CSV and print summary
df.to_csv('transactions.csv', index=False)
print(f"Generated {len(df)} transactions | Total spend: ${df['amount'].sum():,.2f}")
Add synthetic transaction data generator — 
builds 500 realistic bank transactions for model training and demo
