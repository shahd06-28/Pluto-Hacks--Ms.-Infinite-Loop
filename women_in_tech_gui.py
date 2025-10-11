from flask import Flask, render_template, jsonify, request 

app = Flask(__name__)

# Simple fake data
ARTICLES = {
    "past": [
        {"title": "Ada Lovelace and the Analytical Engine", "snippet": "The first computer programmer."},
        {"title": "Grace Hopper and the COBOL Revolution", "snippet": "Inventor of the compiler."}
    ],
    "present": [
        {"title": "Fei-Fei Li and AI Vision", "snippet": "Leader in computer vision and ethical AI."},
        {"title": "Reshma Saujani and Girls Who Code", "snippet": "Empowering women in tech worldwide."}
    ],
    "future": [
        {"title": "Women Leading Quantum Computing", "snippet": "Pioneers shaping the next frontier."},
        {"title": "The Future of Women in Tech Leadership", "snippet": "A look ahead to equality in innovation."}
    ]
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/articles", methods=["POST"])
def get_articles():
    data = request.get_json()
    bucket = data.get("bucket", "all").lower()
    if bucket == "all":
        results = [art for cat in ARTICLES.values() for art in cat]
    else:
        results = ARTICLES.get(bucket, [])
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)



