import streamlit as st
from utils.db_manager import get_db_manager
import pandas as pd
import os

st.title("Debug DB Manager")

db = get_db_manager()

st.write("Current Working Directory:", os.getcwd())
st.write("Files in dir:", os.listdir())

try:
    st.write("Attempting to fetch 'schedule' (lowercase)...")
    df = db.fetch_data("schedule")
    st.write("Result shape:", df.shape)
    st.dataframe(df)
except Exception as e:
    st.error(f"Error fetching 'schedule': {e}")

try:
    st.write("Attempting to fetch 'Schedule' (Capitalized)...")
    df_cap = db.fetch_data("Schedule")
    st.write("Result shape:", df_cap.shape)
    st.dataframe(df_cap)
except Exception as e:
    st.error(f"Error fetching 'Schedule': {e}")
