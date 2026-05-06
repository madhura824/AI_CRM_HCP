from fastapi import APIRouter
from app.agents.graph import graph

router = APIRouter()

@router.post("/agent")
def run_agent(input_text: str, form_state: dict):
    result = graph.invoke({
        "input": input_text,
        "form": form_state
    })
    return result