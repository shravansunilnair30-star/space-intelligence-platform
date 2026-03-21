import pandas as pd

# -------------------------------
# IMPORTANCE DETECTION
# -------------------------------
def get_importance(title):

    high_keywords = [
        "launch", "mission", "rocket", "satellite",
        "isro", "nasa", "spacex", "esa",
        "artemis", "gaganyaan"
    ]

    title_lower = title.lower()

    for word in high_keywords:
        if word in title_lower:
            return "HIGH"

    return "LOW"


# -------------------------------
# TOPIC CLASSIFICATION
# -------------------------------
def classify_topic(title):

    title = title.lower()

    if "rocket" in title or "launch" in title:
        return "Launch"

    if "satellite" in title:
        return "Satellite"

    if "nasa" in title or "isro" in title or "esa" in title:
        return "Agency"

    if "research" in title or "study" in title:
        return "Research"

    return "General"


# -------------------------------
# TREND DETECTION (SMART VERSION)
# -------------------------------
def detect_trends(df):

    if df.empty or "title" not in df.columns:
        return {}

    keywords = ["launch", "satellite", "spacex", "nasa", "isro"]
    trends = {}

    for word in keywords:
        subset = df[
            df["title"].astype(str).str.contains(rf"\b{word}\b", case=False, na=False)
        ]

        # weighted scoring
        score = (
            (subset["importance"] == "HIGH").sum() * 2 +
            (subset["importance"] == "LOW").sum()
        )

        trends[word] = score

    return trends


# -------------------------------
# AI INSIGHT GENERATION
# -------------------------------
def generate_trend_insight(trends):

    if not trends:
        return "No significant activity detected."

    top_trend = max(trends, key=trends.get)
    value = trends[top_trend]

    if value == 0:
        return "No major space activity detected."

    if top_trend == "launch":
        return f"🚀 Surge in launch activity ({value} signals). Indicates strong operational momentum."

    if top_trend == "satellite":
        return f"🛰️ Increased satellite developments ({value} signals). Expansion in communication systems likely."

    if top_trend == "spacex":
        return f"📈 SpaceX activity rising ({value} signals). Private sector competition intensifying."

    if top_trend == "nasa":
        return f"🇺🇸 NASA-driven developments ({value} signals). Government-backed missions accelerating."

    if top_trend == "isro":
        return f"🇮🇳 ISRO activity detected ({value} signals). Strategic growth in Indian space sector."

    return "General space industry activity detected."


def generate_insight(title):

    title_lower = title.lower()

    if "launch" in title_lower:
        return "🚀 Indicates upcoming mission activity and operational readiness"

    if "satellite" in title_lower:
        return "🛰️ Suggests expansion in space-based communication or surveillance"

    if "spacex" in title_lower:
        return "📈 Reflects increased private sector competition"

    if "nasa" in title_lower:
        return "🇺🇸 Shows progress in US-led space exploration programs"

    if "isro" in title_lower:
        return "🇮🇳 Highlights India's strategic growth in space capabilities"

    if "rocket" in title_lower:
        return "🔥 Rocket development indicates propulsion and launch readiness"

    return "ℹ️ General update in the space industry"