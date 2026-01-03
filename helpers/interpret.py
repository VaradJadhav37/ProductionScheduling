from schemas.order_schema import OrdersPayload
from config.llm import interpret_llm
from langchain_core.output_parsers import PydanticOutputParser
from helpers.prompts import int_prompt

def interpret_order(user_input: str):
    parser = PydanticOutputParser(pydantic_object=OrdersPayload)
    interpretation_llm = interpret_llm()
    prompt = int_prompt()
    chain = prompt | interpretation_llm | parser
    return chain.invoke({
        "user_input": user_input,
        "format_instructions": parser.get_format_instructions()
    })

