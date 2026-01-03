from typing import TypedDict, List, Dict, Any
class SchedulingState(TypedDict):
    user_input: str
    orders: List[Dict[str, Any]]
    feasible: bool
    reason: str
    schedule: List[Dict[str, Any]]
    proposal: Dict[str, Any]
    negotiation_round: int
