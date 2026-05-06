from typing import TypedDict, Dict, Any
from app.llm.groq_client import llm
from app.llm.prompts import SYSTEM_PROMPT


class AgentState(TypedDict):
    input: str
    form: Dict[str, Any]
    output: Dict[str, Any]


from app.llm.parser import parse_response

def llm_node(state: AgentState):
    user_input = state["input"]

    prompt = SYSTEM_PROMPT + f"\nUser Input: {user_input}"

    response = llm.invoke(prompt)

    parsed = parse_response(response.content)

    return {
        "output": parsed
    }