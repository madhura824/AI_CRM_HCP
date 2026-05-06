from app.llm.parser import parse_response
from app.services.executor import apply_action
from app.schemas.agent_schema import AgentState
from app.llm.prompts import SYSTEM_PROMPT
from app.llm.groq_client import llm

def llm_node(state: AgentState):
    user_input = state["input"]

    prompt = SYSTEM_PROMPT + f"\nUser Input: {user_input}"

    response = llm.invoke(prompt)
    parsed = parse_response(response.content)

    return {
        "action": parsed.get("action"),
        "payload": parsed.get("payload", {}),
        "message": parsed.get("message", ""),
        "form": state["form"]
    }



def executor_node(state: AgentState):
    form = state["form"]
    action = state.get("action")
    payload = state.get("payload", {})

    updated_form = apply_action(form, action, payload)

    return {
        "form": updated_form,
        "message": state.get("message"),
        "action": action
    }