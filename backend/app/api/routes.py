# from fastapi import APIRouter
# from app.agents.graph import graph

# router = APIRouter()

# @router.post("/agent")
# def run_agent(input_text: str, form_state: dict):
#     result = graph.invoke({
#         "input": input_text,
#         "form": form_state
#     })
#     return result

from fastapi import APIRouter
from app.schemas.agent_schema import AgentRequest
from app.agents.graph import graph

router = APIRouter()

@router.post("/agent")
def run_agent(request: AgentRequest):

    result = graph.invoke({
        "input": request.input_text,
        "form": request.form_state
    })

    return {
        "form": result.get("form"),
        "message": result.get("message"),
        "action": result.get("action"),
        "ai_suggested_followups": result.get("ai_suggested_followups"),
        "artifact_file": result.get("artifact_file")  # 🔥 THIS WAS MISSING
    }