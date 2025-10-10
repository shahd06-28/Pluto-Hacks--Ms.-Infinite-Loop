import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.graph import StateGraph, END
from serpapi import GoogleSearch
import openai

# --- LOAD KEYS ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

openai.api_key = OPENAI_API_KEY

# --- SERPAPI TOOL ---
@tool(description="Search using Google via SerpAPI")
def google_search(query):
    print("🔍 Using SerpAPI Google Search...")
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERP_API_KEY,
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    organic = results.get("organic_results", [])
    formatted = []
    for item in organic[:5]:
        title = item.get("title", "")
        link = item.get("link", "")
        snippet = item.get("snippet", "")
        formatted.append(f"Title: {title}\nLink: {link}\nSnippet: {snippet}")
    return "\n\n".join(formatted)


@tool(description="Search Reddit via Google")
def reddit_search(query):
    print("🔍 Searching Reddit...")
    params = {
        "engine": "google",
        "q": f"site:reddit.com {query}",
        "api_key": SERP_API_KEY,
    }
    search = GoogleSearch(params)
    results = search.get_dict().get("organic_results", [])
    formatted = []
    for item in results[:5]:
        formatted.append(f"Title: {item.get('title','')}\nLink: {item.get('link','')}")
    return "\n\n".join(formatted)


@tool(description="Search X (Twitter) via Google")
def x_search(query):
    print("🔍 Searching X (Twitter)...")
    params = {
        "engine": "google",
        "q": f"site:x.com {query}",
        "api_key": SERP_API_KEY,
    }
    search = GoogleSearch(params)
    results = search.get_dict().get("organic_results", [])
    formatted = []
    for item in results[:5]:
        formatted.append(f"Title: {item.get('title','')}\nLink: {item.get('link','')}")
    return "\n\n".join(formatted)


# --- OPENAI TOOL ---
@tool(description="Use OpenAI GPT to summarize and generate answers")
def gpt_prompt(query):
    print("🧠 Using OpenAI GPT...")
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are an insightful assistant who curates content about women in technology — past, present, and future.",
            },
            {"role": "user", "content": query},
        ],
        temperature=0.7,
    )
    return response["choices"][0]["message"]["content"]


# --- BUILD AGENT ---
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
agent = create_react_agent(
    model=llm,
    tools=[google_search, reddit_search, x_search, gpt_prompt],
    debug=False,
    prompt=(
        "Use SerpAPI and OpenAI tools to find and summarize the best information "
        "about women in technology. Always aggregate sources and list all links at the end."
    ),
)

def agent_node(state):
    result = agent.invoke({"messages": [("human", state["query"])]})
    state["answer"] = result["messages"][-1].content
    return state


graph = StateGraph(dict)
graph.add_node("agent", agent_node)
graph.set_entry_point("agent")
graph.add_edge("agent", END)

langgraph_app = graph.compile()
flask_app = Flask(__name__)

# --- FLASK ROUTES ---
@flask_app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.is_json:
            query = request.get_json(silent=True).get("query", "").strip()
            if not query:
                return jsonify({"error": "No query provided"}), 400
            answer = langgraph_app.invoke({"query": query})["answer"]
            return jsonify({"answer": answer})

        query = request.form.get("query", "").strip()
        if not query:
            return render_template("index.html", error="Please enter a query")
        answer = langgraph_app.invoke({"query": query})["answer"]
        return render_template("index.html", query=query, answer=answer)

    return render_template("index.html")


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000, debug=True)
