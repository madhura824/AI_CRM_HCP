from app.llm.parser import parse_response
from app.services.executor import apply_action
from app.schemas.agent_schema import AgentState
from app.llm.prompts import SYSTEM_PROMPT
from app.llm.groq_client import llm
from app.services.post_processor import enforce_action_rules

import json

def llm_node(state: AgentState):
    user_input = state["input"]

    prompt = SYSTEM_PROMPT + f"\nUser Input: {user_input}"

    response = llm.invoke(prompt)
    parsed = parse_response(response.content)

    action = parsed.get("action")
    payload = parsed.get("payload", {})
    message = parsed.get("message", "")

    action = enforce_action_rules(action, payload, user_input)

    return {
        "action": action,
        "payload": payload,
        "message": message,
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

def followup_node(state: AgentState):
    form = state["form"]

    prompt = f"""
    Based on this interaction data, suggest 3 follow-up actions.

    {form}

    Return ONLY JSON array.
    """

    response = llm.invoke(prompt)

    try:
        followups = json.loads(response.content)
    except:
        followups = []

    form["ai_suggested_followups"] = followups

    return {
        "form": form
    }