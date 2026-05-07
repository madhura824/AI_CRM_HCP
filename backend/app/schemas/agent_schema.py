from typing import TypedDict, Dict, Any, Optional, List
from pydantic import BaseModel
from typing import Dict, Any

class AgentRequest(BaseModel):
    input_text: str
    form_state: Dict[str, Any]
class AgentState(TypedDict):
    input: str
    form: dict
    action: Optional[str]
    payload: dict
    message: Optional[str]
    followups: List[str]
    artifact_file: Optional[str]