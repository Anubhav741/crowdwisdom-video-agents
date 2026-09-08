import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


def main():

    with open("research.json", "r") as f:
        research = json.load(f)

    prompt = f"""
You are a senior market research and performance marketing strategist
for a trading intelligence company.

Analyze the following recent research.

Extract ONLY insights supported by the research.

Return valid JSON with exactly these sections:

{{
  "top_pain_points": [],
  "target_icp": [],
  "desires": [],
  "objections": [],
  "market_language": [],
  "marketing_opportunities": []
}}

Rules:
- Do not invent statistics.
- Do not make unsupported claims.
- Focus on retail traders/investors.
- Prefer specific insights over generic statements.
- Keep each item concise.
- Return ONLY JSON.

RESEARCH:
{json.dumps(research, indent=2)}
"""

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.2
        },
        timeout=120
    )

    response.raise_for_status()

    content = response.json()["choices"][0]["message"]["content"]

    # Handle markdown code fences if model adds them
    content = content.strip()

    if content.startswith("```"):
        content = content.split("\n", 1)[1]
        content = content.rsplit("```", 1)[0]

    insights = json.loads(content)

    with open("research_insights.json", "w") as f:
        json.dump(insights, f, indent=2)

    print("Research insights generated ✅")
    print("Saved → research_insights.json")


if __name__ == "__main__":
    main()
