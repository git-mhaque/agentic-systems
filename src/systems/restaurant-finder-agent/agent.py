from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from tools.tavily_web_search import tavily_web_search
from .nodes.finder_node import finder_node
from .agent_state import AgentState

def build_agent():
    graph = StateGraph(AgentState)
    graph.add_node("finder", finder_node)
    
    tool_node = ToolNode(tools=[tavily_web_search])
    graph.add_node("tavily_web_search", tool_node)
    
    graph.add_edge(START, "finder")

    graph.add_conditional_edges(
        "finder",
        tools_condition,
        {
            "tools": "tavily_web_search", 
            END: END
        } 
    )
    graph.add_edge("tavily_web_search", "finder")

    return graph.compile()
