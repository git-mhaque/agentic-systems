from agent import build_agent
from langchain_core.messages import HumanMessage

def main():

    agent = build_agent()
    print(agent.get_graph().draw_ascii())

    prompt = "Translate the following English text to French: 'Welcome! How are you today?'"
    input = {"messages": [HumanMessage(prompt)]}
    for chunk in agent.stream(input):
        print(chunk)

    prompt = "Translate the following English text to French: 'Have a great day!'"
    state = agent.invoke({"messages": prompt})
    print("AI Agent says:", state)

if __name__ == "__main__":
    main()
