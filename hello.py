from preswald import (
    connect, get_df, query, table, text, plotly, sidebar,
    selectbox, slider, tabs, collapse
)
import plotly.express as px
import pandas as pd

# --- 1. Load the Dataset ---
connect()
df = get_df("sleep_data")

# --- 2. Sidebar Filters ---
sidebar("## Filters")

occupations = ["All"] + sorted(df["Occupation"].dropna().unique().tolist())
selected_occupation = selectbox("Select Occupation", occupations)

min_sleep = int(df["Sleep_duration"].min())
max_sleep = int(df["Sleep_duration"].max())
sleep_threshold = slider("Minimum Sleep Duration (hrs)", min_sleep, max_sleep, 7)

# --- 3. Filtered Query ---
where_clauses = [f"Sleep_duration >= {sleep_threshold}"]
if selected_occupation != "All":
    safe_occ = selected_occupation.replace("'", "''")  # Escape single quotes for SQL
    where_clauses.append(f"Occupation = '{safe_occ}'")

sql = "SELECT * FROM sleep_data WHERE " + " AND ".join(where_clauses)
filtered_df = query(sql, "sleep_data")

# --- 4. Title & Introduction ---
text("# Sleep Health & Lifestyle Dashboard")
text("Use the sidebar to filter by occupation and minimum sleep duration.")

# --- 5. Summary Statistics ---
if filtered_df.empty:
    text("No data matches your filters. Try adjusting them.")
else:
    text("## Summary Statistics")
    avg_sleep = filtered_df["Sleep_duration"].mean()
    avg_stress = filtered_df["Stress Level"].mean()
    avg_activity = filtered_df["Physical Activity Level"].mean()

    text(f"- **Average Sleep Duration:** {avg_sleep:.2f} hrs")
    text(f"- **Average Stress Level:** {avg_stress:.2f}")
    text(f"- **Average Physical Activity:** {avg_activity:.2f}")

    # --- 6. Tabs for Charts ---
    tab1, tab2 = tabs(["📊 Scatter Plot", "📈 Sleep by Age & Gender"])

    with tab1:
        fig1 = px.scatter(
            filtered_df,
            x="Physical Activity Level",
            y="Sleep_duration",
            color="Occupation",
            size="Stress Level",
            hover_data=["Age", "Gender"],
            title="Sleep Duration vs Physical Activity",
            labels={
                "Physical Activity Level": "Physical Activity",
                "Sleep_duration": "Sleep Duration (hrs)",
                "Occupation": "Occupation"
            }
        )
        fig1.update_layout(template='plotly_white')
        plotly(fig1)

    with tab2:
        fig2 = px.box(
            filtered_df,
            x="Gender",
            y="Sleep_duration",
            color="Gender",
            title="Sleep Duration by Gender",
            labels={"Sleep_duration": "Sleep Duration (hrs)"}
        )
        plotly(fig2)

        fig3 = px.line(
            filtered_df.groupby("Age")["Sleep_duration"].mean().reset_index(),
            x="Age",
            y="Sleep_duration",
            title="Average Sleep Duration by Age",
            markers=True,
            labels={"Sleep_duration": "Avg Sleep Duration (hrs)"}
        )
        plotly(fig3)

    # --- 7. Collapsible Raw Data ---
    collapse("### View Full Dataset", table(filtered_df, title="Filtered Data Table"))
