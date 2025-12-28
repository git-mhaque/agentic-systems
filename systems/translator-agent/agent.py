from langgraph.graph import StateGraph, START, END
from nodes.translator_node import translator_node
from agent_state import AgentState

def build_agent():
    graph = StateGraph(AgentState)
    graph.add_node("translator", translator_node)
    graph.add_edge(START, "translator")
    graph.add_edge("translator", END)

    return graph.compile()
