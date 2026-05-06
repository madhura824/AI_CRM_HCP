from langgraph.graph import StateGraph, END
from app.agents.nodes import AgentState, llm_node

builder = StateGraph(AgentState)

builder.add_node("llm", llm_node)

builder.set_entry_point("llm")
builder.add_edge("llm", END)

graph = builder.compile()