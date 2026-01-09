from .agent import build_agent

def main():

    agent = build_agent()
    print(agent.get_graph().draw_ascii())

    user_query = "Welcome!"
    print("User query:", user_query)

    state = agent.invoke({"user_query": user_query})
    print("Translated output:", state["output_query"])

if __name__ == "__main__":
    main()
