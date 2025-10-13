from flask import Flask, render_template, jsonify, request
from serpapi import GoogleSearch
import os, random
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

SERP_API_KEY = os.getenv("SERP_API_KEY")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/articles", methods=["POST"])
def get_articles():
    data = request.get_json()
    bucket = data.get("bucket", "all").lower()
    query = data.get("query", "").strip().lower()

    if not query:
        return jsonify([])

    params = {
        "engine": "google",
        "q": f"women in tech {query} {bucket} {random.choice(['innovation','leadership','future','research','success','inspiration'])}",
        "num": 3,
        "api_key": SERP_API_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    articles = []
    for item in results.get("organic_results", [])[:3]:
        title = item.get("title", "No title")
        link = item.get("link", "#")
        snippet = item.get("snippet", "No description available.")
        articles.append({
            "title": title,
            "snippet": snippet,
            "link": link
        })

    random.shuffle(articles)
    return jsonify(articles)

if __name__ == "__main__":
    app.run(debug=True)






