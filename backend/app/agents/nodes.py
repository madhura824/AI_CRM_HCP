from app.llm.parser import parse_response
from app.services.executor import apply_action
from app.schemas.agent_schema import AgentState
from app.llm.prompts import SYSTEM_PROMPT
from app.llm.groq_client import llm
from app.services.post_processor import enforce_action_rules
from typing import TypedDict, Dict, Any, List
from app.llm.prompts import FOLLOWUP_PROMPT
from app.services.sentiment import fallback_sentiment
from app.services.pdf_generator import generate_samples_pdf

import json

def llm_node(state: AgentState):
    user_input = state["input"]

    prompt = SYSTEM_PROMPT + f"""

USER INPUT:
{user_input}

IMPORTANT:
Always include sentiment in payload.
"""

    response = llm.invoke(prompt)
    parsed = parse_response(response.content)

    action = parsed.get("action")
    payload = parsed.get("payload", {})
    message = parsed.get("message") or "Interaction processed successfully"

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

    artifact_file = None

    # 🔥 THIS IS WHERE YOU PUT IT
    artifact = updated_form.get("artifact")

    if artifact and artifact.get("type") == "samples_pdf":
        artifact = updated_form.get("artifact")

        if artifact and artifact.get("type") == "samples_pdf":
            pdf_buffer = generate_samples_pdf(artifact["data"])

            import uuid, os
            import uuid, os
            from datetime import datetime

            os.makedirs("files", exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_id = f"samples_{timestamp}_{uuid.uuid4().hex[:6]}.pdf"
            file_path = f"files/{file_id}"

            with open(file_path, "wb") as f:
                f.write(pdf_buffer.getvalue())

            artifact_file = f"http://127.0.0.1:8000/files/{file_id}"

    return {
        **state,
        "form": updated_form,
        "message": state.get("message"),
        "action": action,
        "artifact_file": artifact_file
    }
        
def followup_node(state: AgentState):
    form_data = state.get("form", {})

    prompt = FOLLOWUP_PROMPT + f"\nForm Data: {form_data}"

    response = llm.invoke(prompt)
    parsed = parse_response(response.content)
    if not parsed.get("payload", {}).get("sentiment") and  parsed.get("input", ""):
        parsed.setdefault("payload", {})["sentiment"] = fallback_sentiment(parsed.get("input"))

    raw_followups = parsed.get("followups", [])

    #  Convert to list of strings
    clean_followups = []

    for item in raw_followups:
        if isinstance(item, dict):
            # Prefer 'action', fallback to 'description'
            clean_followups.append(item.get("action") or item.get("description"))
        elif isinstance(item, str):
            clean_followups.append(item)

    return {
        **state,
        "ai_suggested_followups": clean_followups
    }