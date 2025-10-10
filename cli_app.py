import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
import openai

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")
openai.api_key = OPENAI_API_KEY


@tool(description="Search Google via SerpAPI")
def google_search(query):
    print("🔍 Searching...")
    params = {"engine": "google", "q": query, "api_key": SERP_API_KEY}
    results = GoogleSearch(params).get_dict().get("organic_results", [])
    return "\n\n".join(
        [f"Title: {r.get('title')}\nLink: {r.get('link')}" for r in results[:5]]
    )


@tool(description="Summarize with OpenAI")
def gpt_prompt(query):
    print("🧠 Thinking...")
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Be an expert curator on women in tech."},
            {"role": "user", "content": query},
        ],
    )
    return response["choices"][0]["message"]["content"]


llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
agent = create_react_agent(model=llm, tools=[google_search, gpt_prompt])

def agent_node(state):
    result = agent.invoke({"messages": [("human", state["query"])]})
    state["answer"] = result["messages"][-1].content
    return state

graph = StateGraph(dict)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)
app = graph.compile()

if __name__ == "__main__":
    while True:
        query = input("\n💬 Ask about women in tech > ").strip()
        if not query:
            break
        print("\n" + app.invoke({"query": query})["answer"])
