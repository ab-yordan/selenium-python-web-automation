import streamlit as st
import pandas as pd
import sqlite3
import os

# Get absolute DB path
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../db/test_results.db"))
conn = sqlite3.connect(db_path)

# Load data
df = pd.read_sql_query("SELECT * FROM test_runs ORDER BY run_time DESC", conn)
df['run_time'] = pd.to_datetime(df['run_time'])
df['date'] = df['run_time'].dt.date

# Page setup
st.set_page_config(page_title="Automation Test Dashboard", layout="wide")
st.title("📊 Automation Test Dashboard")

# Summary
col1, col2, col3 = st.columns(3)
col1.metric("Total Runs", len(df))
col2.metric("Passes", len(df[df.status == "PASSED"]))
col3.metric("Failures/Errors", len(df[df.status.isin(["FAILED", "ERROR"])]))

# Filters
with st.sidebar:
    st.header("🔍 Filters")
    run_id_filter = st.selectbox("Select Run ID", options=["All"] + sorted(df['run_id'].unique(), reverse=True))
    env_values = [v for v in df['environment'].unique() if v is not None]
    trigger_values = [v for v in df['triggered_by'].unique() if v is not None]

    env_filter = st.selectbox("Environment", options=["All"] + sorted(env_values))
    trigger_filter = st.selectbox("Triggered By", options=["All"] + sorted(trigger_values))

# Apply filters
filtered_df = df.copy()
if run_id_filter != "All":
    filtered_df = filtered_df[filtered_df['run_id'] == run_id_filter]
if env_filter != "All":
    filtered_df = filtered_df[filtered_df['environment'] == env_filter]
if trigger_filter != "All":
    filtered_df = filtered_df[filtered_df['triggered_by'] == trigger_filter]

# Daily pass rate
st.subheader("📈 Daily Pass Rate")
summary = filtered_df.groupby(['date', 'status']).size().unstack(fill_value=0)
summary['total'] = summary.sum(axis=1)
summary['pass_rate'] = summary.get('PASSED', 0) / summary['total'] * 100
st.area_chart(summary['pass_rate'])

# Duration per test
st.subheader("⏱️ Average Duration per Test")
durations = filtered_df.groupby('test_name')['duration'].mean().sort_values(ascending=False)
st.bar_chart(durations, horizontal=True)

# Top failing tests
st.subheader("❌ Most Failing/Error-Prone Tests")
failures_df = (
    filtered_df[filtered_df['status'].isin(['FAILED', 'ERROR'])]
    .groupby('test_name').size()
    .reset_index(name='Fail Count')
    .sort_values(by='Fail Count', ascending=False)
    .rename(columns={'test_name': 'Test Name'})
    )
st.table(failures_df)

# Show raw data
st.subheader("📋 Test Execution Records")
st.dataframe(filtered_df[[
    'run_time', 'run_id', 'test_name', 'status', 'duration',
    'error_message', 'environment', 'triggered_by'
]])
