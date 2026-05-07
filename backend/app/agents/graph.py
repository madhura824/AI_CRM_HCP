from langgraph.graph import StateGraph, END

from app.agents.nodes import llm_node, executor_node, followup_node
from app.schemas.agent_schema import AgentState


# Initialize state graph
builder = StateGraph(AgentState)

# Add nodes
builder.add_node("llm", llm_node)
builder.add_node("execute", executor_node)
builder.add_node("followup", followup_node)

# Define entry point
builder.set_entry_point("llm")

# Define edges (flow)
builder.add_edge("llm", "execute")
builder.add_edge("execute", "followup")
builder.add_edge("followup", END)

# Compile graph
graph = builder.compile()