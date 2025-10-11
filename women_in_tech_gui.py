from flask import Flask, render_template, request, jsonify
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os
import random

# --- Load environment variables ---
load_dotenv()
SERP_API_KEY = os.getenv("SERP_API_KEY")

# --- Initialize Flask app ---
app = Flask(__name__)

# --- Fetch Articles from SerpApi ---
def fetch_articles(query, bucket=None):
    """Query SerpApi and return articles categorized by Past, Present, and Future."""
    params = {
        "engine": "google",
        "q": f"Women in {query} technology history OR present OR future",
        "api_key": SERP_API_KEY,
        "num": 12
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    articles = results.get("organic_results", [])
    random.shuffle(articles)
    selected = articles[:9]

    sections = ["past", "present", "future"]
    payload = []

    for i, art in enumerate(selected):
        payload.append({
            "bucket": sections[i % 3],
            "title": art.get("title", "Untitled"),
            "link": art.get("link", "#"),
            "snippet": art.get("snippet", "No summary available.")
        })

    if bucket and bucket != "all":
        payload = [a for a in payload if a["bucket"] == bucket]

    return payload

# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/articles", methods=["POST"])
def get_articles():
    data = request.get_json()
    query = data.get("query", "").strip()
    bucket = data.get("bucket", None)

    if not query:
        return jsonify({"error": "Missing query"}), 400

    try:
        articles = fetch_articles(query, bucket)
        return jsonify({
            "summary": f"Results for '{query}' ({bucket or 'all'})",
            "articles": articles
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Run Server ---
if __name__ == "__main__":
    app.run(debug=True, port=5000)




