import tkinter as tk
from tkinter import messagebox
import webbrowser
import openai
import os
from serpapi import GoogleSearch
from dotenv import load_dotenv

# --- Load keys ---
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

openai.api_key = OPENAI_API_KEY


# --- Functions ---

def generate_articles():
    try:
        query_past = "Women in technology pioneers history"
        query_present = "Modern women in AI and computer science 2025"
        query_future = "Future of women in quantum computing and space tech"

        results = {
            "Past": serp_search(query_past),
            "Present": serp_search(query_present),
            "Future": serp_search(query_future),
        }

        display_results(results)

    except Exception as e:
        messagebox.showerror("Error", f"Something went wrong: {e}")


def serp_search(query):
    params = {"engine": "google", "q": query, "api_key": SERP_API_KEY}
    search = GoogleSearch(params)
    data = search.get_dict()
    results = data.get("organic_results", [])
    if not results:
        return [("No results found", "")]
    top = []
    for item in results[:3]:
        title = item.get("title", "No title")
        link = item.get("link", "")
        top.append((title, link))
    return top


def display_results(results):
    for widget in frame_links.winfo_children():
        widget.destroy()

    for era, links in results.items():
        tk.Label(frame_links, text=f"--- {era.upper()} ---", font=("Helvetica", 12, "bold")).pack(pady=(10, 0))
        for title, url in links:
            lbl = tk.Label(frame_links, text=title, fg="blue", cursor="hand2", wraplength=460, justify="left")
            lbl.pack(anchor="w", padx=10)
            lbl.bind("<Button-1>", lambda e, link=url: webbrowser.open(link))


# --- UI Setup ---
root = tk.Tk()
root.title("Women in Tech Article Generator")
root.geometry("520x480")
root.resizable(False, False)
root.configure(bg="#f9fafb")

title = tk.Label(root, text="💡 Women in Tech: Past, Present & Future", font=("Helvetica", 14, "bold"), bg="#f9fafb")
title.pack(pady=15)

desc = tk.Label(root, text="Click the button below to generate informative articles about women in technology.",
                font=("Helvetica", 10), bg="#f9fafb", wraplength=460, justify="center")
desc.pack(pady=5)

generate_button = tk.Button(root, text="Generate Articles", command=generate_articles, font=("Helvetica", 12, "bold"),
                            bg="#007bff", fg="white", padx=10, pady=5, relief="raised", cursor="hand2")
generate_button.pack(pady=15)

frame_links = tk.Frame(root, bg="#f9fafb")
frame_links.pack(pady=10, fill="both", expand=True)

tk.Label(root, text="Powered by OpenAI + SerpAPI", font=("Helvetica", 8), bg="#f9fafb", fg="gray").pack(side="bottom", pady=10)

root.mainloop()

