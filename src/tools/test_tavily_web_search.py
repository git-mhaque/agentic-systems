# python ./tools/test_tavily_web_search.py 
from tools.tavily_web_search import tavily_web_search

def main():
    tavily_search_query = "Italian restaurants in Melbourne, Australia"  
    json_response = tavily_web_search(tavily_search_query)
    print("Tavily Search Response:", json_response)
    
if __name__ == "__main__":
    main()