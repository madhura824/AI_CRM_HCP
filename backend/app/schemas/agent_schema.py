from typing import TypedDict, Dict, Any


class AgentState(TypedDict, total=False):
    input: str
    form: Dict[str, Any]
    action: str
    payload: Dict[str, Any]
    message: str
    output: Dict[str, Any]