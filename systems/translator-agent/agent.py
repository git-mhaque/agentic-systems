from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from nodes.translator_node import translator_node


def build_agent():
    class State(TypedDict):
        messages: Annotated[list, add_messages]

    graph = StateGraph(State)
    graph.add_node("translator", translator_node)
    graph.add_edge(START, "translator")
    graph.add_edge("translator", END)

    return graph.compile()
