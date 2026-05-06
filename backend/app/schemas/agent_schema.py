from typing import TypedDict, Dict, Any
from pydantic import BaseModel


class AgentRequest(BaseModel):
    input_text: str
    form_state: Dict[str, Any]

class AgentState(TypedDict, total=False):
    input: str
    form: Dict[str, Any]
    action: str
    payload: Dict[str, Any]
    message: str
    output: Dict[str, Any]
    ai_suggested_followups: list[str]
    artifact: Dict[str, Any]