def generate_daily_report(df):

    report = "🚀 DAILY SPACE INTELLIGENCE REPORT\n\n"

    # Filter only important news
    high_df = df[df["importance"] == "HIGH"]

    if high_df.empty:
        return report + "No high importance news today."

    for i, row in high_df.head(5).iterrows():
        report += f"{i+1}. {row['title']}\n"

    return report