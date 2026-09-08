import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

SEARCHES = [
    "retail traders biggest problems trading decisions",
    "trader information overload market signals",
    "retail investors trading decision making",
    "trading psychology decision fatigue retail traders"
]


def tavily_search(query):

    response = requests.post(
        "https://api.tavily.com/search",
        json={
            "api_key": TAVILY_API_KEY,
            "query": query,
            "topic": "news",
            "days": 30,
            "max_results": 5,
            "include_answer": True
        },
        timeout=60
    )

    response.raise_for_status()

    return response.json()


def main():

    all_research = []

    for query in SEARCHES:

        print(f"Researching: {query}")

        data = tavily_search(query)

        results = []

        for item in data.get("results", []):
            results.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content"),
                "published_date": item.get("published_date")
            })

        all_research.append({
            "query": query,
            "answer": data.get("answer"),
            "results": results
        })

    with open("research.json", "w") as f:
        json.dump(all_research, f, indent=2)

    print("\nResearch complete ✅")
    print("Saved → research.json")


if __name__ == "__main__":
    main()
