import streamlit as st
import pandas as pd


def render_defect_trend(Data):
     df = pd.DataFrame(Data, columns=['run_id', 'Total_Defect'])
     st.bar_chart(df, x = 'run_id', y = 'Total_Defect')
