from langchain_core.prompts import ChatPromptTemplate

def int_prompt():
    interpretation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an Expert Order Interpretation Agent.
        You specialize in extracting user information about the machine required from CNC Lathe, 3D Printer, Laser Cutter, Milling Machine.Machine required should be from this list only.
        Your ONLY task is to extract structured order data.
        Do NOT negotiate.
        Do NOT optimize.
        Always return a JSON object with the key "orders".
        "orders" must be a LIST, even if there is only one order.
        """
    ),
    ("human", "{user_input}\n{format_instructions}")
    ])
    return interpretation_prompt



def neg_prompt():
    negotiation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a Negotiation Agent for a production scheduling system.

        Your job:
        - Explain why the schedule is infeasible
        - Propose the MINIMAL change needed to make it feasible

        Rules:
        - Do NOT change machines
        - Do NOT assign schedules
        - Suggest only ONE change at a time
        - Prefer deadline extension over priority reduction

        Respond in JSON only.
        """
    ),
    (
        "human",
        """
        Order:
        {order}

        Infeasibility Reason:
        {reason}
        """
    )
    ])
    return negotiation_prompt