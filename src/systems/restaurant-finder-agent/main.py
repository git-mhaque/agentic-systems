from .agent import build_agent
from langchain_core.messages import HumanMessage

def main():

    agent = build_agent()
    print(agent.get_graph().draw_ascii())

    user_query = """
        Find top 5 sushi restaurants in the Melbourne city, Australia. 
        For each restaurant, provide the name, rating, address, and a brief description.
    """ 
    print("User query:", user_query)

    state = agent.invoke({"user_query": user_query})
    print("Agent response:", state["output_query"])
    
if __name__ == "__main__":
    main()
