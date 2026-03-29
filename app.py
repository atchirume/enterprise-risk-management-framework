#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 29 11:45:00 2026

@author: USER

Enterprise Risk Management Framework (ERMF)
A Streamlit-based application for capturing, uploading, assessing,
measuring, monitoring, and reporting enterprise risks across departments,
functions, and the organisation as a whole.
"""

import os
from datetime import date

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Enterprise Risk Management Framework",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# CUSTOM STYLING
# =========================================================
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #f4f7fb 0%, #eef3f9 100%);
        color: #1f2937;
        font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
    }

    .main {
        background-color: transparent;
    }

    .block-container {
        padding-top: 1.2rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0b1f3a 0%, #102b52 55%, #123c73 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    section[data-testid="stSidebar"] .stRadio label,
    section[data-testid="stSidebar"] .stCheckbox label,
    section[data-testid="stSidebar"] .stSelectbox label,
    section[data-testid="stSidebar"] .stMultiSelect label,
    section[data-testid="stSidebar"] .stTextInput label,
    section[data-testid="stSidebar"] .stTextArea label,
    section[data-testid="stSidebar"] .stDateInput label {
        color: #f8fafc !important;
        font-weight: 600 !important;
    }
    
    section[data-testid="stSidebar"] .stTextInput > div > div,
    section[data-testid="stSidebar"] .stTextArea > div > div,
    section[data-testid="stSidebar"] .stDateInput > div > div,
    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: rgba(255,255,255,0.95) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 12px !important;
}

    section[data-testid="stSidebar"] .stExpander {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
        overflow: hidden;
    }

    .hero-box {
        background: linear-gradient(135deg, #0b1f3a 0%, #123c73 65%, #1f5aa6 100%);
        padding: 1.6rem 1.8rem;
        border-radius: 22px;
        color: white;
        margin-bottom: 1.2rem;
        box-shadow: 0 10px 30px rgba(11, 31, 58, 0.20);
        border: 1px solid rgba(255,255,255,0.10);
        position: relative;
        overflow: hidden;
    }

    .hero-box::after {
        content: "";
        position: absolute;
        top: -40px;
        right: -40px;
        width: 180px;
        height: 180px;
        background: radial-gradient(circle, rgba(212,175,55,0.28) 0%, rgba(212,175,55,0.00) 70%);
        border-radius: 50%;
    }

    .hero-title {
        font-size: 2.1rem;
        font-weight: 800;
        margin-bottom: 0.25rem;
        letter-spacing: 0.2px;
    }

    .hero-subtitle {
        font-size: 1rem;
        opacity: 0.96;
        line-height: 1.5;
    }

    .section-card {
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(6px);
        -webkit-backdrop-filter: blur(6px);
        padding: 1.15rem 1.15rem 1rem 1.15rem;
        border-radius: 20px;
        box-shadow: 0 8px 22px rgba(15, 23, 42, 0.07);
        border: 1px solid rgba(15, 23, 42, 0.05);
        margin-bottom: 1rem;
    }

    h1, h2, h3 {
        color: #0f172a !important;
        font-weight: 800 !important;
        letter-spacing: -0.3px;
    }

    h4, h5, h6 {
        color: #1e293b !important;
        font-weight: 700 !important;
    }

    .small-note {
        color: #64748b;
        font-size: 0.9rem;
    }

    .info-box {
        background: linear-gradient(90deg, #eff6ff 0%, #f8fbff 100%);
        border-left: 6px solid #2563eb;
        padding: 1rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        color: #1e3a8a;
    }

    .warning-box {
        background: linear-gradient(90deg, #fff8e6 0%, #fffdf5 100%);
        border-left: 6px solid #d4a017;
        padding: 1rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        color: #7c5a00;
    }

    .danger-box {
        background: linear-gradient(90deg, #fff1f2 0%, #fff8f8 100%);
        border-left: 6px solid #dc2626;
        padding: 1rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        color: #991b1b;
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 12px !important;
        font-weight: 700 !important;
        border: none !important;
        padding: 0.55rem 1rem !important;
        background: linear-gradient(135deg, #123c73 0%, #1f5aa6 100%) !important;
        color: white !important;
        box-shadow: 0 6px 16px rgba(18, 60, 115, 0.18);
        transition: all 0.2s ease-in-out;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 18px rgba(18, 60, 115, 0.24);
        background: linear-gradient(135deg, #0f2f59 0%, #184f95 100%) !important;
    }

    .stTextInput > div > div,
    .stTextArea > div > div,
    .stDateInput > div > div,
    .stSelectbox > div > div,
    .stMultiSelect > div > div {
        border-radius: 12px !important;
        border: 1px solid #d6deea !important;
        background: #ffffff !important;
        box-shadow: none !important;
    }

    .stTextInput input,
    .stTextArea textarea {
        color: #111827 !important;
    }

    div[data-testid="metric-container"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
        border: 1px solid #dbe7f3;
        padding: 1rem 1rem 0.9rem 1rem;
        border-radius: 18px;
        box-shadow: 0 6px 16px rgba(15, 23, 42, 0.05);
    }

    div[data-testid="metric-container"] label {
        color: #475569 !important;
        font-weight: 600 !important;
    }

    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #0b1f3a !important;
        font-weight: 800 !important;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
        border: 1px solid #dbe3ee;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
    }

    /* Main area expander headers */
  div[data-testid="stExpander"] summary {
    font-weight: 700 !important;
    color: #0f172a !important;
   }

/* Sidebar expander headers */
section[data-testid="stSidebar"] div[data-testid="stExpander"] summary {
    color: #f8fafc !important;
    font-weight: 700 !important;
    background: rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
    padding: 0.35rem 0.6rem !important;
}

 section[data-testid="stSidebar"] .block-container {
    padding-top: 1.2rem !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}

/* Sidebar expander content */
section[data-testid="stSidebar"] div[data-testid="stExpanderDetails"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 0 0 12px 12px !important;
    padding-top: 0.4rem !important;
}

    span[data-baseweb="tag"] {
        background-color: #dbeafe !important;
        color: #123c73 !important;
        border-radius: 999px !important;
        border: 1px solid #bfdbfe !important;
        font-weight: 600 !important;
    }

    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, rgba(0,0,0,0), rgba(148,163,184,0.5), rgba(0,0,0,0));
        margin: 1.2rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# CONSTANTS
# =========================================================
DATA_FILE = "enterprise_risk_register.csv"

RISK_CATEGORIES = [
    "Strategic Risk",
    "Financial Risk",
    "Operational Risk",
    "Compliance Risk",
    "Legal Risk",
    "Reputational Risk",
    "Cybersecurity Risk",
    "Project Risk",
    "Market Risk",
    "Liquidity Risk",
    "Technology Risk",
    "Environmental / ESG Risk",
]

DEPARTMENTS = [
    "Executive Office",
    "Finance",
    "Operations",
    "Human Resources",
    "ICT",
    "Risk Management",
    "Internal Audit",
    "Compliance",
    "Research and Strategy",
    "Statistics",
    "Procurement",
    "Administration",
    "Other",
]

STATUSES = ["Open", "Under Review", "Escalated", "Mitigated", "Closed"]
TREATMENTS = ["Reduce", "Avoid", "Transfer", "Accept"]

CONTROL_EFFECTIVENESS_MAP = {
    "Weak": 0.25,
    "Moderate": 0.50,
    "Strong": 0.75,
    "Very Strong": 0.90,
}

LIKELIHOOD_LABELS = {
    1: "Rare",
    2: "Unlikely",
    3: "Possible",
    4: "Likely",
    5: "Almost Certain",
}

IMPACT_LABELS = {
    1: "Insignificant",
    2: "Minor",
    3: "Moderate",
    4: "Major",
    5: "Severe",
}


# =========================================================
# HELPER FUNCTIONS
# =========================================================
def initialize_data() -> pd.DataFrame:
    columns = [
        "Risk ID",
        "Risk Title",
        "Risk Description",
        "Category",
        "Department",
        "Risk Owner",
        "Date Identified",
        "Likelihood",
        "Impact",
        "Inherent Risk Score",
        "Inherent Risk Level",
        "Existing Controls",
        "Control Effectiveness Label",
        "Control Effectiveness Score",
        "Residual Risk Score",
        "Residual Risk Level",
        "Treatment Plan",
        "Target Date",
        "Status",
        "KRI",
        "Notes",
    ]
    return pd.DataFrame(columns=columns)


def generate_template_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Risk ID": "ERM-001",
                "Risk Title": "Data Breach Risk",
                "Risk Description": "Unauthorized access to sensitive organisational data.",
                "Category": "Cybersecurity Risk",
                "Department": "ICT",
                "Risk Owner": "Head of ICT",
                "Date Identified": "2026-03-29",
                "Likelihood": 4,
                "Impact": 5,
                "Inherent Risk Score": "",
                "Inherent Risk Level": "",
                "Existing Controls": "Firewall, access controls, password policy",
                "Control Effectiveness Label": "Moderate",
                "Control Effectiveness Score": "",
                "Residual Risk Score": "",
                "Residual Risk Level": "",
                "Treatment Plan": "Reduce",
                "Target Date": "2026-06-30",
                "Status": "Open",
                "KRI": "Number of attempted intrusions per month",
                "Notes": "Template example row",
            },
            {
                "Risk ID": "ERM-002",
                "Risk Title": "Regulatory Reporting Delay",
                "Risk Description": "Late submission of statutory returns.",
                "Category": "Compliance Risk",
                "Department": "Compliance",
                "Risk Owner": "Compliance Officer",
                "Date Identified": "2026-03-29",
                "Likelihood": 3,
                "Impact": 4,
                "Inherent Risk Score": "",
                "Inherent Risk Level": "",
                "Existing Controls": "Reporting calendar and review checklist",
                "Control Effectiveness Label": "Strong",
                "Control Effectiveness Score": "",
                "Residual Risk Score": "",
                "Residual Risk Level": "",
                "Treatment Plan": "Reduce",
                "Target Date": "2026-05-31",
                "Status": "Under Review",
                "KRI": "Number of delayed submissions",
                "Notes": "Template example row",
            },
        ]
    )


def load_data() -> pd.DataFrame:
    if os.path.exists(DATA_FILE):
        try:
            return pd.read_csv(DATA_FILE)
        except Exception:
            return initialize_data()
    return initialize_data()


def save_data(df: pd.DataFrame):
    df.to_csv(DATA_FILE, index=False)


def classify_risk(score: float) -> str:
    if score <= 4:
        return "Low"
    elif score <= 9:
        return "Moderate"
    elif score <= 14:
        return "High"
    return "Extreme"


def compute_scores(likelihood: int, impact: int, control_effectiveness_score: float):
    inherent_risk = likelihood * impact
    residual_risk = inherent_risk * (1 - control_effectiveness_score)
    inherent_level = classify_risk(inherent_risk)
    residual_level = classify_risk(residual_risk)
    return inherent_risk, residual_risk, inherent_level, residual_level


def ensure_numeric(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols = [
        "Likelihood",
        "Impact",
        "Inherent Risk Score",
        "Control Effectiveness Score",
        "Residual Risk Score",
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def ensure_required_columns(df: pd.DataFrame) -> pd.DataFrame:
    template = initialize_data()
    for col in template.columns:
        if col not in df.columns:
            df[col] = ""
    return df[template.columns.tolist()]


def standardize_control_effectiveness(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "Control Effectiveness Label" in df.columns:
        df["Control Effectiveness Label"] = (
            df["Control Effectiveness Label"].fillna("").astype(str).str.strip()
        )

    if "Control Effectiveness Score" not in df.columns:
        df["Control Effectiveness Score"] = ""

    for i in df.index:
        label = str(df.at[i, "Control Effectiveness Label"]).strip()
        score = df.at[i, "Control Effectiveness Score"]

        if label in CONTROL_EFFECTIVENESS_MAP:
            df.at[i, "Control Effectiveness Score"] = CONTROL_EFFECTIVENESS_MAP[label]
        else:
            try:
                numeric_score = float(score)
                if 0 <= numeric_score <= 1:
                    df.at[i, "Control Effectiveness Score"] = numeric_score
                else:
                    df.at[i, "Control Effectiveness Score"] = 0.0
            except Exception:
                df.at[i, "Control Effectiveness Score"] = 0.0
                if not label:
                    df.at[i, "Control Effectiveness Label"] = "Weak"

    return df


def recompute_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if df.empty:
        return df

    df = ensure_required_columns(df)
    df = standardize_control_effectiveness(df)
    df = ensure_numeric(df)

    for i in df.index:
        likelihood = df.at[i, "Likelihood"] if pd.notna(df.at[i, "Likelihood"]) else 0
        impact = df.at[i, "Impact"] if pd.notna(df.at[i, "Impact"]) else 0
        ce = (
            df.at[i, "Control Effectiveness Score"]
            if pd.notna(df.at[i, "Control Effectiveness Score"])
            else 0
        )

        try:
            likelihood = int(float(likelihood))
        except Exception:
            likelihood = 0

        try:
            impact = int(float(impact))
        except Exception:
            impact = 0

        try:
            ce = float(ce)
        except Exception:
            ce = 0.0

        ce = min(max(ce, 0.0), 1.0)

        inherent = likelihood * impact
        residual = inherent * (1 - ce)

        df.at[i, "Likelihood"] = likelihood
        df.at[i, "Impact"] = impact
        df.at[i, "Control Effectiveness Score"] = round(ce, 2)
        df.at[i, "Inherent Risk Score"] = round(inherent, 2)
        df.at[i, "Residual Risk Score"] = round(residual, 2)
        df.at[i, "Inherent Risk Level"] = classify_risk(inherent)
        df.at[i, "Residual Risk Level"] = classify_risk(residual)

        if not str(df.at[i, "Control Effectiveness Label"]).strip():
            reverse_map = {v: k for k, v in CONTROL_EFFECTIVENESS_MAP.items()}
            df.at[i, "Control Effectiveness Label"] = reverse_map.get(round(ce, 2), "Weak")

    return df


def make_downloadable_csv(df: pd.DataFrame) -> bytes:
    return df.to_csv(index=False).encode("utf-8")


def get_top_risks(df: pd.DataFrame, n=10) -> pd.DataFrame:
    if df.empty:
        return df
    temp = df.copy()
    temp = ensure_numeric(temp)
    temp = temp.sort_values("Residual Risk Score", ascending=False)
    return temp.head(n)


def build_heatmap_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    heat_df = pd.DataFrame(0, index=[1, 2, 3, 4, 5], columns=[1, 2, 3, 4, 5])
    if df.empty:
        return heat_df

    temp = ensure_numeric(df.copy())
    for _, row in temp.iterrows():
        try:
            l = int(row["Likelihood"])
            i = int(row["Impact"])
            if l in heat_df.index and i in heat_df.columns:
                heat_df.loc[l, i] += 1
        except Exception:
            continue
    return heat_df


# =========================================================
# LOAD DATA
# =========================================================
df = load_data()
df = ensure_required_columns(df)
df = recompute_dataframe(df)
template_df = generate_template_dataframe()

# =========================================================
# HEADER
# =========================================================
st.markdown(
    """
    <div class="hero-box">
        <div class="hero-title">Enterprise Risk Management Framework</div>
        <div class="hero-subtitle">
            Executive risk intelligence platform for identifying, assessing, monitoring,
            and reporting enterprise-wide risks across departments and functions.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("ERM Control Panel")
st.sidebar.markdown("Choose how to input data, then filter and manage your risk register.")

input_mode = st.sidebar.radio(
    "Risk Data Input Mode",
    ["Manual Entry", "Upload Surveyed CSV"],
    index=0,
)

with st.sidebar.expander("Risk Data Template", expanded=False):
    st.markdown("Use this template structure when preparing risk data for CSV upload or guided manual entry.")
    st.download_button(
        label="Download Template CSV",
        data=make_downloadable_csv(template_df),
        file_name="erm_risk_data_template.csv",
        mime="text/csv",
        key="download_template_sidebar",
    )
    if st.button("Show Template Preview", key="show_template_sidebar"):
        st.session_state["show_template_preview"] = True

# =========================================================
# MANUAL ENTRY
# =========================================================
if input_mode == "Manual Entry":
    with st.sidebar.expander("Add New Risk Manually", expanded=True):
        with st.form("risk_entry_form", clear_on_submit=True):
            risk_id = st.text_input("Risk ID", placeholder="e.g. ERM-001")
            risk_title = st.text_input("Risk Title", placeholder="e.g. Data breach risk")
            risk_description = st.text_area("Risk Description", placeholder="Describe the nature of the risk.")
            category = st.selectbox("Risk Category", RISK_CATEGORIES)
            department = st.selectbox("Department / Business Unit", DEPARTMENTS)
            risk_owner = st.text_input("Risk Owner", placeholder="e.g. Head of ICT")
            date_identified = st.date_input("Date Identified", value=date.today())

            col_a, col_b = st.columns(2)
            with col_a:
                likelihood = st.slider("Likelihood", 1, 5, 3)
                st.caption(f"Selected: {likelihood} - {LIKELIHOOD_LABELS[likelihood]}")
            with col_b:
                impact = st.slider("Impact", 1, 5, 3)
                st.caption(f"Selected: {impact} - {IMPACT_LABELS[impact]}")

            existing_controls = st.text_area("Existing Controls", placeholder="Outline controls already in place.")
            ce_label = st.selectbox("Control Effectiveness", list(CONTROL_EFFECTIVENESS_MAP.keys()))
            treatment_plan = st.selectbox("Treatment Plan", TREATMENTS)
            target_date = st.date_input("Target Review / Action Date", value=date.today())
            status = st.selectbox("Status", STATUSES)
            kri = st.text_input("Key Risk Indicator (KRI)", placeholder="e.g. Number of unresolved incidents")
            notes = st.text_area("Additional Notes", placeholder="Optional comments or management notes.")

            submitted = st.form_submit_button("Add Risk")

            if submitted:
                if not risk_id.strip():
                    st.error("Risk ID is required.")
                elif not risk_title.strip():
                    st.error("Risk Title is required.")
                else:
                    ce_score = CONTROL_EFFECTIVENESS_MAP[ce_label]
                    inherent, residual, inherent_level, residual_level = compute_scores(
                        likelihood, impact, ce_score
                    )

                    new_row = pd.DataFrame(
                        [
                            {
                                "Risk ID": risk_id.strip(),
                                "Risk Title": risk_title.strip(),
                                "Risk Description": risk_description.strip(),
                                "Category": category,
                                "Department": department,
                                "Risk Owner": risk_owner.strip(),
                                "Date Identified": str(date_identified),
                                "Likelihood": likelihood,
                                "Impact": impact,
                                "Inherent Risk Score": round(inherent, 2),
                                "Inherent Risk Level": inherent_level,
                                "Existing Controls": existing_controls.strip(),
                                "Control Effectiveness Label": ce_label,
                                "Control Effectiveness Score": ce_score,
                                "Residual Risk Score": round(residual, 2),
                                "Residual Risk Level": residual_level,
                                "Treatment Plan": treatment_plan,
                                "Target Date": str(target_date),
                                "Status": status,
                                "KRI": kri.strip(),
                                "Notes": notes.strip(),
                            }
                        ]
                    )

                    if not df.empty and risk_id.strip() in df["Risk ID"].astype(str).tolist():
                        st.warning("Risk ID already exists. Please use a unique Risk ID.")
                    else:
                        df = pd.concat([df, new_row], ignore_index=True)
                        df = recompute_dataframe(df)
                        save_data(df)
                        st.success("Risk added successfully.")

# =========================================================
# CSV UPLOAD
# =========================================================
if input_mode == "Upload Surveyed CSV":
    with st.sidebar.expander("Upload Risk Register CSV", expanded=True):
        uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

        if uploaded_file is not None:
            try:
                uploaded_df = pd.read_csv(uploaded_file)
                uploaded_df = ensure_required_columns(uploaded_df)
                uploaded_df = recompute_dataframe(uploaded_df)
                df = uploaded_df.copy()
                save_data(df)
                st.success("CSV uploaded and processed successfully.")
            except Exception as e:
                st.error(f"Upload failed: {e}")

# =========================================================
# TEMPLATE PREVIEW
# =========================================================
if st.session_state.get("show_template_preview", False):
    with st.expander("Template Preview", expanded=True):
        st.dataframe(template_df, use_container_width=True)

# =========================================================
# FILTERS
# =========================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Risk Register Filters")

filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)

with filter_col1:
    selected_category = st.multiselect(
        "Category",
        options=sorted(df["Category"].dropna().astype(str).unique().tolist()) if not df.empty else [],
        default=[],
    )
with filter_col2:
    selected_department = st.multiselect(
        "Department",
        options=sorted(df["Department"].dropna().astype(str).unique().tolist()) if not df.empty else [],
        default=[],
    )
with filter_col3:
    selected_status = st.multiselect(
        "Status",
        options=sorted(df["Status"].dropna().astype(str).unique().tolist()) if not df.empty else [],
        default=[],
    )
with filter_col4:
    selected_level = st.multiselect(
        "Residual Risk Level",
        options=sorted(df["Residual Risk Level"].dropna().astype(str).unique().tolist()) if not df.empty else [],
        default=[],
    )

filtered_df = df.copy()

if selected_category:
    filtered_df = filtered_df[filtered_df["Category"].isin(selected_category)]
if selected_department:
    filtered_df = filtered_df[filtered_df["Department"].isin(selected_department)]
if selected_status:
    filtered_df = filtered_df[filtered_df["Status"].isin(selected_status)]
if selected_level:
    filtered_df = filtered_df[filtered_df["Residual Risk Level"].isin(selected_level)]

filtered_df = recompute_dataframe(filtered_df)
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# KPI METRICS
# =========================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Portfolio Overview")

if filtered_df.empty:
    total_risks = 0
    open_risks = 0
    extreme_risks = 0
    avg_residual = 0.0
else:
    total_risks = len(filtered_df)
    open_risks = filtered_df["Status"].astype(str).isin(["Open", "Under Review", "Escalated"]).sum()
    extreme_risks = (filtered_df["Residual Risk Level"].astype(str) == "Extreme").sum()
    avg_residual = pd.to_numeric(filtered_df["Residual Risk Score"], errors="coerce").fillna(0).mean()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Total Risks", f"{total_risks}")
k2.metric("Open / Active Risks", f"{open_risks}")
k3.metric("Extreme Residual Risks", f"{extreme_risks}")
k4.metric("Average Residual Score", f"{avg_residual:.2f}")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# MAIN VISUALS
# =========================================================
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Residual Risk by Category")

    if not filtered_df.empty:
        cat_df = (
            filtered_df.groupby("Category", as_index=False)["Residual Risk Score"]
            .mean()
            .sort_values("Residual Risk Score", ascending=False)
        )
        fig_cat = px.bar(
            cat_df,
            x="Category",
            y="Residual Risk Score",
            text="Residual Risk Score",
            color="Residual Risk Score",
            color_continuous_scale="Blues",
        )
        fig_cat.update_traces(texttemplate="%{text:.2f}", textposition="outside")
        fig_cat.update_layout(
            xaxis_title="Risk Category",
            yaxis_title="Average Residual Risk Score",
            xaxis_tickangle=-35,
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#1f2937"),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_cat, use_container_width=True, key="fig_cat")
    else:
        st.info("No data available for category analysis.")
    st.markdown('</div>', unsafe_allow_html=True)

with chart_col2:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Risks by Status")

    if not filtered_df.empty:
        status_df = filtered_df["Status"].value_counts().reset_index()
        status_df.columns = ["Status", "Count"]
        fig_status = px.pie(
            status_df,
            names="Status",
            values="Count",
            hole=0.45,
        )
        fig_status.update_layout(
            height=420,
            plot_bgcolor="white",
            paper_bgcolor="white",
            font=dict(color="#1f2937"),
        )
        st.plotly_chart(fig_status, use_container_width=True, key="fig_status")
    else:
        st.info("No data available for status analysis.")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# HEATMAP AND TOP RISKS
# =========================================================
heat_col, top_col = st.columns([1.1, 1])

with heat_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Risk Heatmap (Likelihood × Impact)")

    heat_data = build_heatmap_dataframe(filtered_df)
    heat_matrix = heat_data.values

    heat_fig = go.Figure(
        data=go.Heatmap(
            z=heat_matrix,
            x=[f"{x} - {IMPACT_LABELS[x]}" for x in heat_data.columns],
            y=[f"{y} - {LIKELIHOOD_LABELS[y]}" for y in heat_data.index],
            text=heat_matrix,
            texttemplate="%{text}",
            colorscale="YlOrRd",
            showscale=True,
        )
    )
    heat_fig.update_layout(
        xaxis_title="Impact",
        yaxis_title="Likelihood",
        height=460,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#1f2937"),
    )
    st.plotly_chart(heat_fig, use_container_width=True, key="heat_fig")
    st.markdown('</div>', unsafe_allow_html=True)

with top_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Top Residual Risks")

    top_risks_df = get_top_risks(filtered_df, n=10)
    if not top_risks_df.empty:
        display_top = top_risks_df[
            [
                "Risk ID",
                "Risk Title",
                "Department",
                "Residual Risk Score",
                "Residual Risk Level",
                "Status",
            ]
        ].copy()
        st.dataframe(display_top, use_container_width=True, height=460)
    else:
        st.info("No risks to display.")
    st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# DEPARTMENT VIEW
# =========================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Departmental Risk Exposure")

if not filtered_df.empty:
    dept_df = (
        filtered_df.groupby("Department", as_index=False)
        .agg(
            Risk_Count=("Risk ID", "count"),
            Avg_Residual_Risk=("Residual Risk Score", "mean"),
            Avg_Inherent_Risk=("Inherent Risk Score", "mean"),
        )
        .sort_values("Avg_Residual_Risk", ascending=False)
    )

    fig_dept = px.scatter(
        dept_df,
        x="Risk_Count",
        y="Avg_Residual_Risk",
        size="Avg_Inherent_Risk",
        hover_name="Department",
        text="Department",
        color="Avg_Residual_Risk",
        color_continuous_scale="Blues",
    )
    fig_dept.update_traces(textposition="top center")
    fig_dept.update_layout(
        xaxis_title="Number of Risks",
        yaxis_title="Average Residual Risk Score",
        height=500,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(color="#1f2937"),
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_dept, use_container_width=True, key="fig_dept")
else:
    st.info("No departmental risk data available.")
st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# RISK REGISTER TABLE
# =========================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Detailed Risk Register")

if not filtered_df.empty:
    st.dataframe(filtered_df, use_container_width=True, height=420)
else:
    st.info("The risk register is currently empty.")

download_col1, download_col2, download_col3 = st.columns(3)

with download_col1:
    st.download_button(
        label="Download Current Risk Register",
        data=make_downloadable_csv(filtered_df),
        file_name="enterprise_risk_register_filtered.csv",
        mime="text/csv",
        key="download_filtered_register",
    )

with download_col2:
    st.download_button(
        label="Download Full Risk Register",
        data=make_downloadable_csv(df),
        file_name="enterprise_risk_register_full.csv",
        mime="text/csv",
        key="download_full_register",
    )

with download_col3:
    if st.button("Reset Risk Register", key="reset_risk_register_btn"):
        df = initialize_data()
        save_data(df)
        st.success("Risk register has been reset. Refresh the app if needed.")

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# RISK INSIGHTS
# =========================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Risk Insights and Interpretation")

if filtered_df.empty:
    st.markdown(
        """
        <div class="info-box">
        No risks are currently available for analytical interpretation.
        Add risks manually or upload a CSV file to generate insights.
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    highest_risk = get_top_risks(filtered_df, 1)
    if not highest_risk.empty:
        top_row = highest_risk.iloc[0]
        st.markdown(
            f"""
            <div class="danger-box">
            <b>Highest residual risk:</b> {top_row['Risk Title']} ({top_row['Risk ID']}) in the
            <b>{top_row['Department']}</b> department, with a residual score of
            <b>{top_row['Residual Risk Score']:.2f}</b> classified as
            <b>{top_row['Residual Risk Level']}</b>.
            </div>
            """,
            unsafe_allow_html=True,
        )

    extreme_share = 0
    if len(filtered_df) > 0:
        extreme_share = (
            (filtered_df["Residual Risk Level"].astype(str) == "Extreme").sum() / len(filtered_df)
        ) * 100

    if extreme_share >= 20:
        st.markdown(
            """
            <div class="warning-box">
            A relatively large share of risks fall within the <b>Extreme</b> band.
            Management attention, escalation protocols, and accelerated treatment plans may be required.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="info-box">
            The portfolio does not currently show a dominant concentration of extreme residual risks,
            though ongoing monitoring remains necessary.
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# METHODOLOGY
# =========================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Risk Measurement Methodology")

st.markdown(
    """
    **1. Likelihood assessment**  
    Risks are scored on a 1–5 scale:
    - 1 = Rare
    - 2 = Unlikely
    - 3 = Possible
    - 4 = Likely
    - 5 = Almost Certain

    **2. Impact assessment**  
    Risks are scored on a 1–5 scale:
    - 1 = Insignificant
    - 2 = Minor
    - 3 = Moderate
    - 4 = Major
    - 5 = Severe

    **3. Inherent risk score**  
    Inherent risk reflects the gross exposure before considering controls:

    `Inherent Risk Score = Likelihood × Impact`

    **4. Control effectiveness**  
    Existing controls are translated into effectiveness weights:
    - Weak = 0.25
    - Moderate = 0.50
    - Strong = 0.75
    - Very Strong = 0.90

    **5. Residual risk score**  
    Residual risk reflects the exposure remaining after controls:

    `Residual Risk Score = Inherent Risk Score × (1 - Control Effectiveness Score)`

    **6. Risk classification bands**
    - Low: score ≤ 4
    - Moderate: score > 4 and ≤ 9
    - High: score > 9 and ≤ 14
    - Extreme: score > 14
    """
)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# DISCLAIMER AND OWNERSHIP
# =========================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Disclaimer and Ownership Notice")

st.markdown(
    """
    **Disclaimer**  
    This application is designed to support enterprise risk identification, documentation,
    scoring, monitoring, and reporting. The outputs generated by the framework are intended
    to assist management and risk practitioners in structured decision-making. They do not
    substitute for professional judgment, internal governance procedures, audit review, legal
    interpretation, or regulatory compliance assessments. Users should validate all inputs,
    assumptions, and interpretations before relying on outputs for official or strategic action.

    **Ownership Notice**  
    This Enterprise Risk Management Framework (ERMF) application and its underlying analytical
    structure, scoring logic, interface design, and reporting workflow are the intellectual work
    of the author.

    **Author:** Chirume A.T.  
    **Contact:** +263773369884  
    **Qualifications:** Ph.D*, MA, MSc, BSc (Hons)  
    **Copyright:** © 2026. All rights reserved.
    """
)

st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown(
    """
    <div class="small-note">
        Enterprise Risk Management Framework • Built in Python• 2026
    </div>
    """,
    unsafe_allow_html=True,
)