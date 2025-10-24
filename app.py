import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt



# --- Custom CSS styling for KPI cards ---
st.markdown("""
<style>
/* KPI Card Styling */
div[data-testid="metric-container"] {
    background-color: #1E1E2F;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 15px;
    padding: 15px 10px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
    transition: all 0.3s ease-in-out;
}
div[data-testid="metric-container"]:hover {
    transform: scale(1.02);
    border-color: #8ab4f8;
}

/* KPI Label and Value */
div[data-testid="stMetricValue"] {
    font-size: 1.8rem;
    font-weight: 600;
    color: #FFFFFF;
}
div[data-testid="stMetricLabel"] {
    font-size: 1.05rem;
    color: #BBBBBB;
    text-transform: uppercase;
    letter-spacing: 0.04em;
}
</style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="Smart Health Analytics", page_icon="🧬", layout="wide")

DATA_DIR = Path(__file__).parent / "data"
CURATED = DATA_DIR / "curated"
RAW = DATA_DIR / "raw_patients.csv"

st.title("🧬 Smart Health Analytics")
st.caption("ETL + QC + patient-safe analytics for healthcare intelligence")


with st.expander("Upload CSV (optional)", expanded=False):
    up = st.file_uploader("Upload a de-identified CSV", type=["csv"])    
    if up:
        df = pd.read_csv(up, parse_dates=[c for c in ["last_visit"] if c in pd.read_csv(up, nrows=0).columns])
        st.session_state["uploaded_df"] = df
        st.success("Uploaded! Scroll down for analytics.")

# Load curated if present else raw
def load_data():
    curated_csv = CURATED / "patients.csv"
    if curated_csv.exists():
        return pd.read_csv(curated_csv, parse_dates=["last_visit"])
    return pd.read_csv(RAW, parse_dates=["last_visit"])

df = st.session_state.get("uploaded_df", load_data())

# KPIs
import streamlit as st
import numpy as np

c1, c2, c3, c4 = st.columns(4)

# KPIs
total_rows = len(df)
avg_age = df["age"].mean()
avg_sys = df["systolic_bp"].mean()
avg_glu = df["glucose_mg_dL"].mean()

# Custom deltas and coloring
c1.metric(
    label="👩‍⚕️ Rows",
    value=f"{total_rows:,}",
    delta=f"{total_rows - 250:+d} vs baseline",
    delta_color="normal"
)

c2.metric(
    label="🎂 Avg Age",
    value=f"{avg_age:.1f}",
    delta="Stable",
    delta_color="off"
)

# Highlight if BP is high (>125) or low (<110)
bp_delta = "High" if avg_sys > 125 else ("Low" if avg_sys < 110 else "Normal")
bp_color = "inverse" if bp_delta == "High" else "normal"
c3.metric(
    label="❤️ Avg Systolic BP",
    value=f"{avg_sys:.1f}",
    delta=bp_delta,
    delta_color=bp_color
)

# Highlight glucose trend
glu_delta = "↑ Elevated" if avg_glu > 110 else "↓ Normal"
glu_color = "inverse" if avg_glu > 110 else "normal"
c4.metric(
    label="🍬 Avg Glucose",
    value=f"{avg_glu:.1f}",
    delta=glu_delta,
    delta_color=glu_color
)


# Filters
st.subheader("Filters")
colA, colB = st.columns(2)
sex = colA.multiselect("Sex", sorted(df['sex'].dropna().unique().tolist()), default=None)
dx = colB.multiselect("Diagnosis", sorted(df['diagnosis'].dropna().unique().tolist()), default=None)

f = df.copy()
if sex:
    f = f[f["sex"].isin(sex)]
if dx:
    f = f[f["diagnosis"].isin(dx)]

# Visualization 1: Age distribution
st.subheader("Age distribution")
fig1, ax1 = plt.subplots()
ax1.hist(f['age'].dropna(), bins=20)
ax1.set_xlabel("Age"); ax1.set_ylabel("Count")
st.pyplot(fig1)

# Visualization 2: BP trend over time
st.subheader("Blood pressure over time (mean by month)")
ts = f.set_index("last_visit").sort_index().groupby(pd.Grouper(freq='M'))[['systolic_bp','diastolic_bp']].mean()
fig2, ax2 = plt.subplots()
ts.plot(ax=ax2)
ax2.set_xlabel("Month"); ax2.set_ylabel("BP (mmHg)")
st.pyplot(fig2)

# Cohort table
st.subheader("Cohort summary by diagnosis and sex")
cohort = f.pivot_table(index="diagnosis", columns="sex", values="glucose_mg_dL", aggfunc="mean")
st.dataframe(cohort.round(1))

st.info("Run the ETL first (\`python -m etl.pipeline\`) for cleaned data and a QC report in `data/curated/`.")
