from langgraph.graph import StateGraph, END
from orchestration.state import SchedulingState
from agents.agents import (
    interpretation_agent,
    scheduler_agent,
    negotiation_agent
)

def route_after_scheduler(state: SchedulingState):
    if state.get("feasible"):
        return "end"
    return "negotiate"

def build_graph():
    graph = StateGraph(SchedulingState)

    graph.add_node("interpret", interpretation_agent)
    graph.add_node("schedule", scheduler_agent)
    graph.add_node("negotiate", negotiation_agent)

    graph.set_entry_point("interpret")
    graph.add_edge("interpret", "schedule")

    graph.add_conditional_edges(
        "schedule",
        route_after_scheduler,
        {
            "negotiate": "negotiate",
            "end": END
        }
    )

    # IMPORTANT: negotiation ENDS the graph
    graph.add_edge("negotiate", END)

    return graph.compile()

app = build_graph()
