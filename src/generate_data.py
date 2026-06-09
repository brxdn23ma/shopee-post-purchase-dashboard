import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# ==========================================
# CONFIG
# ==========================================

N_DISPUTES = 2000

np.random.seed(42)

# ==========================================
# CATEGORIES
# ==========================================

categories = [
    "Electronics",
    "Fashion",
    "Beauty",
    "Home",
    "Sports"
]

seller_types = [
    "Shopee Mall",
    "Local SME",
    "Cross-Border"
]

logistics_providers = [
    "SPX",
    "J&T",
    "Ninja Van",
    "Others"
]

complaint_types = [
    "Damaged Item",
    "Wrong Item",
    "Missing Item",
    "Late Delivery",
    "Refund Issue"
]

# ==========================================
# PROBABILITIES
# ==========================================

refund_probabilities = {
    "Damaged Item": 0.85,
    "Wrong Item": 0.90,
    "Missing Item": 0.80,
    "Late Delivery": 0.60,
    "Refund Issue": 0.50
}

# ==========================================
# GENERATION
# ==========================================

records = []

start_date = datetime(2025, 1, 1)

for i in range(N_DISPUTES):

    order_id = f"ORD{i+1:06d}"

    customer_id = f"CUST{np.random.randint(1, 800):04d}"

    order_date = start_date + timedelta(
        days=np.random.randint(0, 365)
    )

    category = np.random.choice(categories)

    seller_type = np.random.choice(
        seller_types,
        p=[0.35, 0.45, 0.20]
    )

    logistics_provider = np.random.choice(
        logistics_providers
    )

    complaint_type = np.random.choice(
        complaint_types
    )

    # ======================================
    # CASE OPEN
    # ======================================

    case_open_date = order_date + timedelta(
        days=np.random.randint(1, 10)
    )

    evidence_collection_date = case_open_date + timedelta(
        days=np.random.randint(0, 2)
    )

    # ======================================
    # SELLER RESPONSE
    # ======================================

    if seller_type == "Shopee Mall":
        seller_delay = np.random.randint(1, 4)

    elif seller_type == "Local SME":
        seller_delay = np.random.randint(2, 6)

    else:
        seller_delay = np.random.randint(5, 11)

    seller_response_date = (
        evidence_collection_date
        + timedelta(days=seller_delay)
    )

    # ======================================
    # INVESTIGATION
    # ======================================

    investigation_delay = 1

    if complaint_type == "Damaged Item":
        investigation_delay += np.random.randint(2, 5)

    elif complaint_type == "Missing Item":
        investigation_delay += np.random.randint(1, 4)

    else:
        investigation_delay += np.random.randint(0, 2)

    investigation_date = (
        seller_response_date
        + timedelta(days=investigation_delay)
    )

    # ======================================
    # DECISION
    # ======================================

    decision_delay = 1

    if complaint_type == "Refund Issue":
        decision_delay += np.random.randint(2, 5)

    decision_date = (
        investigation_date
        + timedelta(days=decision_delay)
    )

    # ======================================
    # REFUND APPROVAL
    # ======================================

    refund_approved = np.random.rand() < (
        refund_probabilities[complaint_type]
    )

    refund_date = decision_date + timedelta(
        days=np.random.randint(1, 4)
    )

    close_date = refund_date + timedelta(
        days=np.random.randint(0, 2)
    )

    # ======================================
    # RESOLUTION DAYS
    # ======================================

    resolution_days = (
        close_date - case_open_date
    ).days

    # ======================================
    # CSAT
    # ======================================

    if resolution_days <= 3:

        csat = np.random.choice(
            [4, 5],
            p=[0.4, 0.6]
        )

    elif resolution_days <= 7:

        csat = np.random.choice(
            [3, 4],
            p=[0.5, 0.5]
        )

    else:

        csat = np.random.choice(
            [1, 2, 3],
            p=[0.4, 0.4, 0.2]
        )

    # ======================================
    # REOPEN
    # ======================================

    if (
        (not refund_approved)
        or resolution_days > 10
    ):
        reopen_prob = 0.25
    else:
        reopen_prob = 0.05

    reopened = np.random.rand() < reopen_prob

    # ======================================
    # RETENTION
    # ======================================

    if reopened:

        retained_90d = np.random.rand() < 0.20

    elif resolution_days <= 3:

        retained_90d = np.random.rand() < 0.85

    elif resolution_days <= 7:

        retained_90d = np.random.rand() < 0.65

    else:

        retained_90d = np.random.rand() < 0.45

    retained_30d = np.random.rand() < min(
        0.95,
        (0.20 + retained_90d)
    )

    # ======================================
    # RECORD
    # ======================================

    records.append({
        "order_id": order_id,
        "customer_id": customer_id,
        "order_date": order_date,

        "category": category,
        "seller_type": seller_type,
        "logistics_provider": logistics_provider,
        "complaint_type": complaint_type,

        "case_open_date": case_open_date,
        "evidence_collection_date": evidence_collection_date,
        "seller_response_date": seller_response_date,
        "investigation_date": investigation_date,
        "decision_date": decision_date,
        "refund_date": refund_date,
        "close_date": close_date,

        "refund_approved": refund_approved,
        "reopened": reopened,

        "resolution_days": resolution_days,

        "csat": csat,

        "retained_30d": retained_30d,
        "retained_90d": retained_90d
    })

# ==========================================
# SAVE
# ==========================================

df = pd.DataFrame(records)

os.makedirs("data", exist_ok=True)

df.to_csv(
    "data/disputes.csv",
    index=False
)

print("=" * 50)
print("Dataset generated successfully.")
print(f"Rows: {len(df):,}")
print("Saved to: data/disputes.csv")
print("=" * 50)

print(df.head())