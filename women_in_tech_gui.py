import tkinter as tk
import random
import webbrowser
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

# API key
SERP_API_KEY = os.getenv("SERP_API_KEY", "8626734a396ccad9ac95f5d04b9d9dae0277d536bc7089e61dc1a1b2004593e7")

# GUI setup
root = tk.Tk()
root.title("Women in Tech - Article Explorer")
root.geometry("1000x700")  # Bigger window
root.config(bg="#f9f9f9")

# Title
title_label = tk.Label(
    root,
    text="🌸 Women in Tech: Article Explorer",
    font=("Arial", 22, "bold"),
    bg="#f9f9f9",
    fg="#ba7a9a"
)
title_label.pack(pady=15)

# Keyword search area
keyword_frame = tk.Frame(root, bg="#f9f9f9")
keyword_frame.pack(pady=10)

keyword_label = tk.Label(keyword_frame, text="🔍 Enter a keyword:", font=("Arial", 14), bg="#f9f9f9")
keyword_label.pack(side=tk.LEFT, padx=10)

keyword_entry = tk.Entry(keyword_frame, width=40, font=("Arial", 14))
keyword_entry.pack(side=tk.LEFT, padx=10)

# Output area
output_box = tk.Text(root, height=25, width=115, font=("Arial", 12), wrap="word", bg="#ffffff", fg="#222222")
output_box.pack(padx=20, pady=20)
output_box.config(state=tk.DISABLED)

# Function to make links clickable
def open_link(event):
    idx = output_box.index("@%s,%s" % (event.x, event.y))
    line = output_box.get(idx + " linestart", idx + " lineend")
    if line.startswith("🔗 "):
        link = line.replace("🔗 ", "").strip()
        webbrowser.open(link)

output_box.bind("<Button-1>", open_link)

# Fetch articles
def generate_articles():
    keyword = keyword_entry.get().strip()
    if not keyword:
        output_box.config(state=tk.NORMAL)
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, "⚠️ Please enter a keyword first.\n")
        output_box.config(state=tk.DISABLED)
        return

    search = GoogleSearch({
        "q": f"Women in {keyword} technology history OR future OR impact",
        "api_key": SERP_API_KEY,
        "num": 12
    })
    results = search.get_dict()
    articles = results.get("organic_results", [])

    if not articles:
        output_box.config(state=tk.NORMAL)
        output_box.delete(1.0, tk.END)
        output_box.insert(tk.END, "❌ No articles found. Try a different keyword.\n")
        output_box.config(state=tk.DISABLED)
        return

    random.shuffle(articles)
    selected = articles[:3]

    sections = ["🌺 Past", "🌼 Present", "🌻 Future"]

    output_box.config(state=tk.NORMAL)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, f"✨ Results for: **{keyword}**\n\n")

    for i, article in enumerate(selected):
        title = article.get("title", "Untitled")
        link = article.get("link", "")
        snippet = article.get("snippet", "")

        output_box.insert(tk.END, f"{sections[i]}\n", "section")
        output_box.insert(tk.END, f"• {title}\n", "bold")
        output_box.insert(tk.END, f"{snippet}\n", "normal")
        output_box.insert(tk.END, f"🔗 {link}\n\n")

    output_box.config(state=tk.DISABLED)

# Button
generate_button = tk.Button(
    root,
    text="✨ Generate Articles",
    command=generate_articles,
    font=("Arial", 14, "bold"),
    bg="#d63384",
    fg="white",
    padx=15,
    pady=5,
    relief="ridge"
)
generate_button.pack(pady=10)

# Text styling
output_box.tag_configure("bold", font=("Arial", 13, "bold"))
output_box.tag_configure("section", font=("Arial", 14, "bold"), foreground="#d63384")

# Run app
root.mainloop()

