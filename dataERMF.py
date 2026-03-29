import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# =========================================================
# CONFIGURATION
# =========================================================

NUM_RECORDS = 500
OUTPUT_FILE = "enterprise_risk_register.csv"

DEPARTMENTS = [
    "Finance", "ICT", "Operations", "HR",
    "Compliance", "Internal Audit", "Strategy", "Procurement"
]

CATEGORIES = [
    "Financial Risk", "Operational Risk", "Cyber Risk",
    "Compliance Risk", "Strategic Risk", "Reputational Risk"
]

RISK_TITLES = {
    "Financial Risk": [
        "Liquidity Shortfall", "Exchange Rate Volatility",
        "Credit Default Risk", "Revenue Instability"
    ],
    "Operational Risk": [
        "Process Failure", "Human Error",
        "Supply Chain Disruption"
    ],
    "Cyber Risk": [
        "Data Breach", "System Hacking",
        "Ransomware Attack", "Phishing Attack"
    ],
    "Compliance Risk": [
        "Regulatory Breach", "AML Violation",
        "Reporting Non-compliance"
    ],
    "Strategic Risk": [
        "Policy Misalignment", "Market Competition",
        "Poor Strategic Decisions"
    ],
    "Reputational Risk": [
        "Negative Publicity", "Customer Complaints",
        "Service Failure"
    ]
}

CONTROL_EFFECTIVENESS = {
    "Weak": 0.25,
    "Moderate": 0.50,
    "Strong": 0.75,
    "Very Strong": 0.90
}

STATUSES = ["Open", "Under Review", "Mitigated", "Closed"]
TREATMENTS = ["Reduce", "Avoid", "Transfer", "Accept"]

OWNERS = [
    "Director Finance", "Head of ICT", "Operations Manager",
    "HR Manager", "Compliance Officer", "Internal Auditor"
]

# =========================================================
# HELPERS
# =========================================================

def classify_risk(score):
    if score <= 4:
        return "Low"
    elif score <= 9:
        return "Moderate"
    elif score <= 14:
        return "High"
    else:
        return "Extreme"

def random_date():
    start = datetime(2023, 1, 1)
    end = datetime(2026, 12, 31)
    return start + timedelta(days=random.randint(0, (end - start).days))

# =========================================================
# SIMULATION ENGINE
# =========================================================

records = []

for i in range(NUM_RECORDS):

    category = random.choice(CATEGORIES)
    title = random.choice(RISK_TITLES[category])
    department = random.choice(DEPARTMENTS)
    owner = random.choice(OWNERS)

    likelihood = np.random.choice([1,2,3,4,5], p=[0.1,0.2,0.3,0.25,0.15])
    impact = np.random.choice([1,2,3,4,5], p=[0.1,0.2,0.3,0.25,0.15])

    inherent = likelihood * impact

    ce_label = random.choice(list(CONTROL_EFFECTIVENESS.keys()))
    ce_score = CONTROL_EFFECTIVENESS[ce_label]

    residual = inherent * (1 - ce_score)

    record = {
        "Risk ID": f"ERM-{i+1:04d}",
        "Risk Title": title,
        "Risk Description": f"Simulated risk related to {title.lower()}",
        "Category": category,
        "Department": department,
        "Risk Owner": owner,
        "Date Identified": random_date().strftime("%Y-%m-%d"),
        "Likelihood": likelihood,
        "Impact": impact,
        "Inherent Risk Score": round(inherent,2),
        "Inherent Risk Level": classify_risk(inherent),
        "Existing Controls": "Standard internal controls in place",
        "Control Effectiveness Label": ce_label,
        "Control Effectiveness Score": ce_score,
        "Residual Risk Score": round(residual,2),
        "Residual Risk Level": classify_risk(residual),
        "Treatment Plan": random.choice(TREATMENTS),
        "Target Date": random_date().strftime("%Y-%m-%d"),
        "Status": random.choice(STATUSES),
        "KRI": f"{random.randint(0,50)} incidents/month",
        "Notes": "Simulated dataset"
    }

    records.append(record)

df = pd.DataFrame(records)

df.to_csv(OUTPUT_FILE, index=False)

print("✅ Simulation complete")
print(f"📁 File saved as: {OUTPUT_FILE}")
print(f"📊 Total risks generated: {len(df)}")