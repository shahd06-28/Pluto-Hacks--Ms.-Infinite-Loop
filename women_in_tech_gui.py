from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# --- Article Data ---
ARTICLES = {
    "past": [
        {"title": "Ada Lovelace and the Analytical Engine", "snippet": "The first computer programmer."},
        {"title": "Grace Hopper and the COBOL Revolution", "snippet": "Inventor of the compiler."},
        {"title": "Hedy Lamarr’s Frequency Hopping", "snippet": "Paved the way for modern Wi-Fi and Bluetooth."},
        {"title": "Katherine Johnson and NASA’s Flight Paths", "snippet": "Her math sent humans to space."}
    ],
    "present": [
        {"title": "Fei-Fei Li and AI Vision", "snippet": "Leader in computer vision and ethical AI."},
        {"title": "Reshma Saujani and Girls Who Code", "snippet": "Empowering women in tech worldwide."},
        {"title": "Gwynne Shotwell at SpaceX", "snippet": "Engineering the future of interplanetary travel."},
        {"title": "Whitney Wolfe Herd and Bumble", "snippet": "Redefining digital connection and safety online."}
    ],
    "future": [
        {"title": "Women Leading Quantum Computing", "snippet": "Pioneers shaping the next frontier."},
        {"title": "AI Ethics and the Next Generation", "snippet": "Guiding responsible machine intelligence."},
        {"title": "The Future of Women in Tech Leadership", "snippet": "A look ahead to equality in innovation."},
        {"title": "Neural Design: Women Innovating Brain-Computer Interfaces", "snippet": "Merging biology and code for a smarter world."}
    ]
}


# --- Routes ---
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/articles", methods=["POST"])
def get_articles():
    data = request.get_json()
    bucket = data.get("bucket", "all").lower()
    query = data.get("query", "").strip().lower()

    # Combine all categories if 'all'
    if bucket == "all":
        results = [art for cat in ARTICLES.values() for art in cat]
    else:
        results = ARTICLES.get(bucket, [])

    # Search filtering
    if query:
        results = [a for a in results if query in a["title"].lower() or query in a["snippet"].lower()]

    # Randomize order & subset
    random.shuffle(results)
    results = random.sample(results, min(len(results), random.randint(1, len(results)))) if results else []

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)



