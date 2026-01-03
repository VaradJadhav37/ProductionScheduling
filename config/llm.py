from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

def interpret_llm():
    load_dotenv()
    GROK_API_KEY = os.getenv('GROK_API_KEY')
    interpretation_llm = ChatGroq(
    api_key=GROK_API_KEY,
    model="openai/gpt-oss-120b",
    temperature=0 
    )
    return interpretation_llm

def negate_llm():
    load_dotenv()
    GROK_API_KEY = os.getenv('GROK_API_KEY')
    negotiation_llm = ChatGroq(
    api_key=GROK_API_KEY,
    model="openai/gpt-oss-120b",
    temperature=0.2  
    )
    return negotiation_llm

