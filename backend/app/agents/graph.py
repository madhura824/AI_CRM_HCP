from langgraph.graph import StateGraph, END
from app.agents.nodes import  llm_node, executor_node
from app.schemas.agent_schema import AgentState

builder = StateGraph(AgentState)

builder.add_node("llm", llm_node)
builder.add_node("execute", executor_node)

builder.set_entry_point("llm")
builder.add_edge("llm", "execute")
builder.add_edge("execute", END)

graph = builder.compile()