import sys
import os
from charts import render_defect_trend

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

try:
    from dashboard.charts import render_defect_trend
except ModuleNotFoundError:
    from charts import render_defect_trend


import streamlit as st
import pandas as pd
import sqlite3
from database.models import InspectionDatabase



#Configuration of page and header
st.set_page_config(page_title="IPIR Operator Console", page_icon="🤖", layout="wide")
st.title("IPIR Pipeline Inspection Robot - Operator Console")
st.markdown("---")

# 1. Instantiate database (this automatically runs _create_Tables() if the DB is fresh!)
db = InspectionDatabase()

#initializatio of variable to get the inspection data
run = db.get_inspection_runs()

#fetches the data from the database to get total defects
T_defect = db.total_defect()

#draws the chart of total defects
render_defect_trend(T_defect)

#Sidebar Run Selection
st.sidebar.header("🕹️ Controls")
if run:
    selected_run = st.sidebar.selectbox("Select Inspection Run", run)

    # 1. Fetch Defects for Selected Run
    defects = db.get_defects_for_runs(selected_run)

    # 2. Compute counts
    crack_count = sum(1 for row in defects if row[2] == "CRACK")
    rust_count = sum(1 for row in defects if row[2] == "RUST")

    # 3. Render 3 Metric Columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Defects", len(defects))
    col2.metric("Cracks", crack_count)
    col3.metric("Rust Patches", rust_count)

    st.markdown("---")

    # 4. Render Pandas DataFrame Table
    df = pd.DataFrame(defects, columns=['ID', 'Timestamp', 'Type', 'X', 'Y', 'Width', 'Height', 'Distance (m)'])
    st.dataframe(df, use_container_width=True)
else:
    st.info("No inspection runs found in database. Run 'python3 kratos.py' first!")