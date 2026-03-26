import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

from main import run_once
from database import connect_db, create_table


# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="Space Intelligence Platform", layout="wide")

st.title("🚀 Space Intelligence Platform")
st.write("AI-powered real-time space industry insights")


# -------------------------------
# INIT (SAFE)
# -------------------------------
create_table()

# Run only once per session (prevents infinite reruns)
if "initialized" not in st.session_state:
    run_once()
    st.session_state.initialized = True


# -------------------------------
# TRANSLATION
# -------------------------------
def translate_to_malayalam(text):
    try:
        if len(text) > 120:
            text = text[:120]
        return GoogleTranslator(source='en', target='ml').translate(text)
    except:
        return text


# -------------------------------
# CONTROL PANEL
# -------------------------------
st.subheader("⚡ Control Panel")

col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Update Intelligence"):
        with st.spinner("Fetching latest space news..."):
            count = run_once()
        st.success(f"✅ {count} new articles added")
        st.cache_data.clear()   # 🔥 refresh cached DB
        st.rerun()

with col2:
    show_malayalam = st.toggle("🌐 Malayalam Translation")


# -------------------------------
# LOAD DATA (CACHED)
# -------------------------------
@st.cache_data
def load_data():
    conn = connect_db()
    df = pd.read_sql("SELECT * FROM articles", conn)
    conn.close()
    return df


df = load_data()


# -------------------------------
# EMPTY CHECK
# -------------------------------
if df.empty:
    st.warning("⚠️ No data available. Click Update.")
    st.stop()


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

search = st.text_input("🔎 Search news")

filtered_df = df.copy()

if importance_filter != "All":
    filtered_df = filtered_df[filtered_df["importance"] == importance_filter]

if topic_filter != "All":
    filtered_df = filtered_df[filtered_df["topic"] == topic_filter]

if search:
    filtered_df = filtered_df[
        filtered_df["title"].str.contains(search, case=False, na=False)
    ]


# -------------------------------
# HIGH IMPACT
# -------------------------------
st.subheader("🚨 High Impact News")

for _, row in filtered_df[filtered_df["importance"] == "HIGH"].head(5).iterrows():

    title = row["title"]

    if show_malayalam:
        title = translate_to_malayalam(title)

    date = pd.to_datetime(row["published"], errors='coerce')
    formatted_date = date.strftime("%d %b %Y") if pd.notna(date) else row["published"]

    st.markdown(f"🔥 **{title}**")
    st.write(f"📅 {formatted_date}")
    st.write(f"📊 Topic: {row['topic']}")
    st.markdown(f"[🔗 Read more]({row['link']})")
    st.markdown("---")


# -------------------------------
# MAIN FEED
# -------------------------------
st.subheader("📰 Intelligence Feed")

for _, row in filtered_df.head(50).iterrows():

    title = row["title"]

    if show_malayalam:
        title = translate_to_malayalam(title)

    date = pd.to_datetime(row["published"], errors='coerce')
    formatted_date = date.strftime("%d %b %Y") if pd.notna(date) else row["published"]

    if row["importance"] == "HIGH":
        st.markdown(f"### 🔥 {title}")
    else:
        st.markdown(f"### {title}")

    st.write(f"📅 {formatted_date}")
    st.write(f"📊 Topic: {row['topic']}")
    st.write(f"⚡ Importance: {row['importance']}")
    st.markdown(f"[🔗 Read more]({row['link']})")
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