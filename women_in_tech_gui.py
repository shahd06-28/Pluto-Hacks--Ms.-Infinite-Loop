from flask import Flask, render_template, request, jsonify
from google_search_results import GoogleSearch
from dotenv import load_dotenv
import os, random

load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

app = Flask(__name__)

def fetch_articles(query, bucket=None):
    """Query SERP API and return 3 articles (past/present/future)."""
    search = GoogleSearch({
        "q": f"Women in {query} technology history OR future OR impact",
        "api_key": SERP_API_KEY,
        "num": 12
    })
    results = search.get_dict()
    articles = results.get("organic_results", [])
    random.shuffle(articles)
    selected = articles[:3]

    sections = ["past", "present", "future"]
    payload = []
    for i, art in enumerate(selected):
        payload.append({
            "bucket": sections[i],
            "title": art.get("title", "Untitled"),
            "link": art.get("link", ""),
            "snippet": art.get("snippet", "")
        })
    if bucket:
        payload = [a for a in payload if a["bucket"] == bucket]
    return payload

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/articles", methods=["POST"])
def get_articles():
    data = request.get_json()
    query = data.get("query", "").strip()
    bucket = data.get("bucket")
    if not query:
        return jsonify({"error": "Missing query"}), 400
    try:
        articles = fetch_articles(query, bucket)
        return jsonify({
            "summary": f"Results for '{query}'",
            "articles": articles
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)


