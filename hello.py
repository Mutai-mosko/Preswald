from preswald import (
    connect, table, text, plotly, sidebar,
    selectbox, slider
)
import plotly.express as px
import pandas as pd

# --- 1. Load the Dataset ---
connect()
df = pd.read_csv("data/Sleep_health_and_lifestyle_dataset.csv")

if df is None or df.empty:
    text("Error: Failed to load dataset.")
else:
    # --- 2. Sidebar Filters ---
    sidebar("## Filters")

    occupations = ["All"] + sorted(df["Occupation"].dropna().unique().tolist())
    selected_occupation = selectbox("Select Occupation", occupations)

    min_sleep = int(df["Sleep Duration"].min())
    max_sleep = int(df["Sleep Duration"].max())
    sleep_threshold = slider("Minimum Sleep Duration (hrs)", min_sleep, max_sleep, 7)

    # --- 3. Filter Data with Pandas ---
    filtered_df = df[df["Sleep Duration"] >= sleep_threshold]
    if selected_occupation != "All":
        filtered_df = filtered_df[filtered_df["Occupation"] == selected_occupation]

    if filtered_df.empty:
        text("No data matches your filters. Try adjusting them.")
    else:
        # --- 4. Title & Introduction ---
        text("# Sleep Health & Lifestyle Dashboard")
        text("Use the sidebar to filter by occupation and minimum sleep duration.")

        # --- 5. Summary Statistics ---
        avg_sleep = filtered_df["Sleep Duration"].mean()
        avg_stress = filtered_df["Stress Level"].mean()
        avg_activity = filtered_df["Physical Activity Level"].mean()

        text(f"- **Average Sleep Duration:** {avg_sleep:.2f} hrs")
        text(f"- **Average Stress Level:** {avg_stress:.2f}")
        text(f"- **Average Physical Activity:** {avg_activity:.2f}")

        # --- 6. Select View Instead of Tabs ---
        view = selectbox("Choose Visualization", ["📊 Scatter Plot", "📈 Sleep by Age & Gender"])

        if view == "📊 Scatter Plot":
            fig1 = px.scatter(
                filtered_df,
                x="Physical Activity Level",
                y="Sleep Duration",
                color="Occupation",
                size="Stress Level",
                hover_data=["Age", "Gender"],
                title="Sleep Duration vs Physical Activity",
                labels={
                    "Physical Activity Level": "Physical Activity",
                    "Sleep Duration": "Sleep Duration (hrs)",
                    "Occupation": "Occupation"
                }
            )
            fig1.update_layout(template='plotly_white')
            plotly(fig1)

        elif view == "📈 Sleep by Age & Gender":
            fig2 = px.box(
                filtered_df,
                x="Gender",
                y="Sleep Duration",
                color="Gender",
                title="Sleep Duration by Gender",
                labels={"Sleep Duration": "Sleep Duration (hrs)"}
            )
            plotly(fig2)

            fig3 = px.line(
                filtered_df.groupby("Age")["Sleep Duration"].mean().reset_index(),
                x="Age",
                y="Sleep Duration",
                title="Average Sleep Duration by Age",
                markers=True,
                labels={"Sleep Duration": "Avg Sleep Duration (hrs)"}
            )
            plotly(fig3)

        # --- 7. Show Full Dataset ---
        text("### View Full Dataset")
        table(filtered_df, title="Filtered Data Table")
