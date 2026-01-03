from config.llm import negate_llm
from helpers.prompts import neg_prompt
def negotiate(order, infeasible_reason):
    negotiation_llm = negate_llm()
    negotiation_prompt = neg_prompt()
    chain = negotiation_prompt | negotiation_llm
    response = chain.invoke({
        "order": order,
        "reason": infeasible_reason
    })
    return response.content

