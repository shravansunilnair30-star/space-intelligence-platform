import streamlit as st
import sqlite3
import pandas as pd
import os
from analyzer import detect_trends, generate_trend_insight

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Space Intelligence Platform", layout="wide")

st.title("🚀 Space Intelligence Platform")
st.write("AI-powered real-time space industry insights")

# -------------------------------
# DATABASE
# -------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "space_news.db")

conn = sqlite3.connect(DB_PATH)
df = pd.read_sql("SELECT * FROM articles", conn)

# -------------------------------
# SAFETY CHECK
# -------------------------------
if df.empty:
    st.warning("⚠️ No data available. Run main.py first.")
    st.stop()

# -------------------------------
# KPI SECTION
# -------------------------------
st.subheader("📊 Key Metrics")

col1, col2, col3 = st.columns(3)

col1.metric("Total Articles", len(df))
col2.metric("High Importance", (df["importance"] == "HIGH").sum())
col3.metric("Topics Covered", df["topic"].nunique())

# -------------------------------
# FILTERS
# -------------------------------
st.sidebar.title("🔍 Filters")

importance_filter = st.sidebar.selectbox(
    "Importance",
    ["All"] + sorted(df["importance"].dropna().unique())
)

topic_filter = st.sidebar.selectbox(
    "Topic",
    ["All"] + sorted(df["topic"].dropna().unique())
)

# -------------------------------
# SEARCH
# -------------------------------
search = st.text_input("🔎 Search news")

filtered_df = df.copy()

if importance_filter != "All":
    filtered_df = filtered_df[filtered_df["importance"] == importance_filter]

if topic_filter != "All":
    filtered_df = filtered_df[filtered_df["topic"] == topic_filter]

if search:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search, case=False)
    ]

# -------------------------------
# TREND SIGNALS
# -------------------------------
st.subheader("📈 Trend Signals")

trends = detect_trends(df)

cols = st.columns(len(trends))

for i, (key, value) in enumerate(trends.items()):
    cols[i].metric(key.upper(), value)

# -------------------------------
# AI INSIGHT
# -------------------------------
st.subheader("🧠 AI Insight")

insight = generate_trend_insight(trends)
st.info(insight)

# -------------------------------
# HIGH ALERTS
# -------------------------------
st.subheader("🚨 High Impact News")

high_df = filtered_df[filtered_df["importance"] == "HIGH"].head(5)

for _, row in high_df.iterrows():
    st.markdown(f"🔥 **{row['title']}**")
    st.write(f"📊 Topic: {row['topic']}")
    st.write(f"🔗 {row['link']}")
    st.markdown("---")

# -------------------------------
# MAIN FEED
# -------------------------------
st.subheader("📰 Intelligence Feed")

for _, row in filtered_df.head(50).iterrows():

    if row["importance"] == "HIGH":
        st.markdown(f"### 🔥 {row['title']}")
    else:
        st.markdown(f"### {row['title']}")

    st.write(f"📊 Topic: {row['topic']}")
    st.write(f"⚡ Importance: {row['importance']}")
    st.write(f"🔗 {row['link']}")
    st.markdown("---")

# -------------------------------
# EXPORT
# -------------------------------
st.subheader("📥 Export Data")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="space_intelligence.csv",
    mime="text/csv",
)