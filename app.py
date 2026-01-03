import streamlit as st
from orchestration.graph import app as scheduling_graph
import plotly.express as px
import pandas as pd

import plotly.graph_objects as go

def plot_gantt(schedule):
    color_map = {
        "A": "#1f77b4",   # blue
        "B": "#ff7f0e",   # orange
        "C": "#2ca02c",   # green
        "D": "#d62728",   # red
    }

    fig = go.Figure()

    for task in schedule:
        fig.add_trace(
            go.Bar(
                x=[task["end"] - task["start"]],
                y=[task["machine"]],
                base=[task["start"]],
                orientation="h",
                name=f"Order {task['order_id']}",
                marker=dict(
                    color=color_map.get(task["order_id"], "#7f7f7f")
                ),
                hovertemplate=(
                    f"<b>Order:</b> {task['order_id']}<br>"
                    f"<b>Machine:</b> {task['machine']}<br>"
                    f"<b>Start:</b> {task['start']}<br>"
                    f"<b>End:</b> {task['end']}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title="Production Schedule (Gantt Chart)",
        xaxis_title="Time (hours)",
        yaxis_title="Machine",
        barmode="overlay",
        legend_title="Orders",
        height=400,
    )

    return fig

    """
    schedule: List[dict] with keys:
    order_id, machine, start, end
    """
    df = pd.DataFrame(schedule)

    df["Start"] = df["start"]
    df["Finish"] = df["end"]
    df["Task"] = df["order_id"]
    df["Machine"] = df["machine"]

    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Machine",
        color="Task",
        title="Production Schedule (Gantt Chart)",
    )

    fig.update_yaxes(autorange="reversed")
    fig.update_layout(
        xaxis_title="Time",
        yaxis_title="Machine",
        legend_title="Order ID",
        height=400,
    )

    return fig

st.set_page_config(page_title="Production Scheduling", layout="centered")
st.title("🛠️ Multi-Agent Production Scheduling")

if "state" not in st.session_state:
    st.session_state.state = {}

if "result" not in st.session_state:
    st.session_state.result = None

user_input = st.text_area(
    "Enter order details",
    placeholder="Order A needs turning, 5 hours, deadline 20, high priority"
)

if st.button("Run Scheduler"):
    if not user_input.strip():
        st.warning("Please enter order details.")
    else:
        st.session_state.state = {"user_input": user_input}
        st.session_state.result = scheduling_graph.invoke(
            st.session_state.state
        )

if st.session_state.result:
    result = st.session_state.result

    if result.get("feasible"):
        st.success("✅ Schedule Feasible")
        st.json(result["schedule"])
        st.success("✅ Schedule Feasible")
        st.subheader("📅 Schedule (Table)")
        st.json(result["schedule"])
        st.subheader("📊 Gantt Chart")
        gantt_fig = plot_gantt(result["schedule"])
        st.plotly_chart(gantt_fig, use_container_width=True)

   
    else:
        st.error("❌ Schedule Infeasible")

    st.subheader("⚠️ Reason")
    st.write(result.get("reason", "Unknown"))

    st.subheader("🤝 Negotiation Suggestion")
    st.json(result.get("proposal", {}))

    st.divider()

    # ---------- Update Input ----------
    st.subheader("✏️ Update Order and Retry")

    updated_input = st.text_area(
        "Modify the order based on the suggestion",
        placeholder="Extend deadline to 10 hours",
        key="updated_input_box"
    )

    col1, col2 = st.columns([1, 3])

    with col1:
        apply_clicked = st.button("🔄 Apply Changes")

    # ---------- Apply Changes Logic ----------
    if apply_clicked:
        if not updated_input.strip():
            st.warning("Please enter updated order details.")
        else:
            with st.spinner("Re-running scheduler with updated input..."):
                # Preserve previous result for comparison
                st.session_state.previous_result = result

                # Update state
                st.session_state.state["user_input"] = updated_input

                # Re-run LangGraph
                st.session_state.last_result = scheduling_graph.invoke(
                    st.session_state.state
                )

            st.success("✅ Scheduler re-run completed")

            st.divider()

            # ---------- Updated Result ----------
            updated_result = st.session_state.last_result

            st.subheader("📌 Updated Result")

            if updated_result.get("feasible"):
                st.success("🎉 Updated schedule is feasible")
                st.json(updated_result["schedule"])

                st.subheader("📊 Updated Gantt Chart")
                fig = plot_gantt(updated_result["schedule"])
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.error("❌ Still infeasible after update")
                st.write(updated_result.get("reason", "Unknown"))

                st.subheader("🤝 New Negotiation Suggestion")
                st.json(updated_result.get("proposal", {}))