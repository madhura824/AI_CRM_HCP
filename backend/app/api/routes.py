from fastapi import APIRouter
from app.agents.graph import graph
from app.schemas.agent_schema import AgentRequest

router = APIRouter()

@router.post("/agent")
def run_agent(request: AgentRequest):
    result = graph.invoke({
        "input": request.input_text,
        "form": request.form_state
    })

    return result