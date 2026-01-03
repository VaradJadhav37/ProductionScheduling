from orchestration.state import SchedulingState
from scheduler.schedule_order import schedule_orders
from helpers.interpret import interpret_order
from helpers.negate import negotiate
def user_input_agent(state: SchedulingState):
    user_input = input("Enter order details: ")
    return {
        "user_input": user_input
    }
def interpretation_agent(state: SchedulingState):
    payload = interpret_order(state["user_input"])

    return {
        "orders": [o.model_dump() for o in payload.orders],
        "negotiation_round": 0
    }
def scheduler_agent(state: SchedulingState):
    result = schedule_orders(state["orders"], horizon=50)

    if result["feasible"]:
        return {
            "feasible": True,
            "schedule": result["schedule"]
        }

    return {
        "feasible": False,
        "reason": result["reason"]
    }
def negotiation_agent(state: SchedulingState):
    proposal = negotiate(
        order=state["orders"][0],
        infeasible_reason=state["reason"]
    )

    return {
        "proposal": proposal,
        "negotiation_round": state["negotiation_round"] + 1
    }


def user_update_agent(state: SchedulingState):
    MAX_ROUNDS = 3
    if state["negotiation_round"] >= MAX_ROUNDS:
        raise RuntimeError("Negotiation failed")

    updated_input = input(
        "Apply the changes suggested and enter updated order details: "
    )

    payload = interpret_order(updated_input)

    return {
        "user_input": updated_input,
        "orders": [o.model_dump() for o in payload.orders]
    }
