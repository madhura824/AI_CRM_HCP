import json
import uuid
import os
from datetime import datetime
from typing import TypedDict, Dict, Any, List

from app.llm.parser import parse_response
from app.services.executor import apply_action
from app.schemas.agent_schema import AgentState
from app.llm.prompts import SYSTEM_PROMPT, FOLLOWUP_PROMPT
from app.llm.groq_client import llm
from app.services.post_processor import enforce_action_rules
from app.services.sentiment import fallback_sentiment
from app.services.pdf_generator import generate_samples_pdf
import json
import re

def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group())
    except:
        return None

def llm_node(state: AgentState):
    

    user_input = state["input"]

    prompt = SYSTEM_PROMPT + f"""
USER INPUT: {user_input}
"""

    response = llm.invoke(prompt)

    raw = response.content
    print("RAW LLM RESPONSE:", raw)

    parsed = extract_json(raw)

    if not parsed:
        return {
            "form": state.get("form", {}),
            "action": None,
            "payload": {},
            "message": "LLM parsing failed"
        }

    action = parsed.get("action")
    payload = parsed.get("payload", {})
    message = parsed.get("message", "Processed")
    print("RAW LLM RESPONSE:", response.content)
    print("PARSED:", parsed)

    return {
        **state,
        "action": action,
        "payload": payload,
        "message": message,
    }
def executor_node(state: AgentState):

    form = state.get("form", {})
    action = state.get("action")
    payload = state.get("payload", {})

    updated_form = apply_action(form, action, payload)

    artifact_file = None

    artifact = updated_form.get("artifact")
    if artifact and artifact.get("type") == "samples_pdf":
        pdf_buffer = generate_samples_pdf(artifact["data"])

        os.makedirs("files", exist_ok=True)

        file_id = f"{uuid.uuid4().hex}.pdf"
        file_path = f"files/{file_id}"

        with open(file_path, "wb") as f:
            f.write(pdf_buffer.getvalue())

        artifact_file = f"http://127.0.0.1:8000/files/{file_id}"
    print("ACTION:", action)
    print("PAYLOAD:", payload)
    print("UPDATED FORM:", updated_form)

    return {
    **state,
    "form": updated_form,
    "artifact_file": artifact_file,
}


def followup_node(state: AgentState):
    form_data = state.get("form", {})

    prompt = FOLLOWUP_PROMPT + f"\nForm Data: {form_data}"
    response = llm.invoke(prompt)

    parsed = parse_response(response.content)

    raw_followups = parsed.get("followups", [])

    clean_followups = []
    for item in raw_followups:
        if isinstance(item, dict):
            clean_followups.append(item.get("action") or item.get("description"))
        else:
            clean_followups.append(item)

    return {
    "form": form_data,
    "followups": clean_followups,
}