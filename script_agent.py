import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-4o-mini"


# ============================================================
# LOAD JSON FILE
# ============================================================

def load_json(filename):

    if not os.path.exists(filename):
        raise FileNotFoundError(
            f"{filename} not found"
        )

    with open(filename, "r") as f:
        return json.load(f)


# ============================================================
# OPENROUTER
# ============================================================

def generate_script(prompt):

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",

        headers={
            "Authorization": "Bearer " + API_KEY,
            "Content-Type": "application/json"
        },

        json={
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7
        },

        timeout=180
    )

    response.raise_for_status()

    data = response.json()

    content = (
        data["choices"][0]["message"]["content"]
        .strip()
    )

    # Remove markdown fences
    if content.startswith("```json"):
        content = content[len("```json"):].strip()

    elif content.startswith("```"):
        content = content[len("```"):].strip()

    if content.endswith("```"):
        content = content[:-3].strip()

    # Find JSON
    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            "OpenRouter did not return valid JSON"
        )

    return json.loads(
        content[start:end + 1]
    )


# ============================================================
# CREATE PROMPT
# ============================================================

def build_prompt(
    concept_name,
    successful_ads,
    research,
    unique_data
):

    # Top creative examples
    top_ads = successful_ads[:5]

    prompt = f"""
You are a senior creative director and direct-response
advertising scriptwriter.

You are creating a cinematic short-form video advertisement
for CrowdWisdom, a trading intelligence platform.

IMPORTANT:
- Do not promise profits.
- Do not guarantee trading success.
- Do not invent statistics.
- Do not invent CrowdWisdom features that are not supported
  by the supplied data.
- Treat the supplied CrowdWisdom WeeklyBlog analysis as
  analysis/data, not as a guaranteed prediction.
- Include a clear trading-risk disclaimer.
- The final video should feel premium, cinematic and modern,
  not like a generic AI advertisement.

TARGET VIDEO:
- Duration: 30–60 seconds
- Format: 9:16 vertical
- Scenes: 6–8
- Audience: retail traders/investors
- Style: cinematic fintech advertisement
- Strong visual hook in first 2–3 seconds
- Clear CTA at the end

REFERENCE SUCCESSFUL ADS:

{json.dumps(top_ads, indent=2)}

RESEARCH INSIGHTS:

{json.dumps(research, indent=2)}

CROWDWISDOM UNIQUE DATA:

{json.dumps(unique_data, indent=2)}


CREATE THIS CONCEPT:

{concept_name}


RETURN ONLY VALID JSON WITH EXACTLY THIS STRUCTURE:

{{
  "concept_name": "",
  "objective": "",
  "target_icp": "",
  "hook": "",
  "voiceover_style": "",
  "total_duration_seconds": 45,

  "scenes": [
    {{
      "scene_number": 1,
      "duration_seconds": 5,
      "visual": "",
      "camera": "",
      "lighting": "",
      "sound": "",
      "voiceover": "",
      "on_screen_text": "",
      "asset_prompt": ""
    }}
  ],

  "cta": "",
  "disclaimer": ""
}}

SCENE REQUIREMENTS:

Scene 1:
Create an extremely strong visual hook.
The viewer should immediately understand the problem.

Middle scenes:
Build tension/problem → insight → solution.

Final scenes:
Show how CrowdWisdom can help the trader make more
informed decisions, followed by CTA.

VISUAL REQUIREMENTS:

Use cinematic visuals such as:
- trading screens
- charts
- market data
- notifications
- crowded information feeds
- trader reaction
- abstract data visualization
- signal/noise visual metaphors
- clean fintech interface
- dramatic close-ups
- cinematic transitions

Avoid:
- cheesy stock footage
- unrealistic guaranteed-profit imagery
- piles of money
- Lamborghinis
- fake "100% win rate" claims
- impossible trading screenshots

VOICEOVER:
Natural human language.
Short sentences.
Confident but not exaggerated.

ON-SCREEN TEXT:
Keep it short.
Prefer 3–7 words per screen.

ASSET PROMPT:
Write a detailed prompt that can be used by a
video/image generation system.

The scenes must collectively fit within 30–60 seconds.
"""


    return prompt


# ============================================================
# MAIN
# ============================================================

def main():

    print("========================================")
    print("CROWDWISDOM SCRIPT AGENT")
    print("========================================")


    if not API_KEY:

        print(
            "ERROR: OPENROUTER_API_KEY missing."
        )

        return


    # --------------------------------------------------------
    # Load files
    # --------------------------------------------------------

    print("\nLoading project data...")


    successful_ads = load_json(
        "successful_ads.json"
    )

    research = load_json(
        "research_insights.json"
    )

    unique_data = load_json(
        "unique_data.json"
    )


    print(
        "Successful ads:",
        len(successful_ads)
    )

    print("Research insights: loaded")

    print("CrowdWisdom data: loaded")


    # --------------------------------------------------------
    # Create output directory
    # --------------------------------------------------------

    os.makedirs(
        "scripts",
        exist_ok=True
    )


    # --------------------------------------------------------
    # Three concepts
    # --------------------------------------------------------

    concepts = [

        (
            "Concept 1 — Pain + ICP: "
            "The Noise"
        ),

        (
            "Concept 2 — Unique CrowdWisdom Data: "
            "From Data to Decision"
        ),

        (
            "Concept 3 — How CrowdWisdom Helps: "
            "Find the Signal"
        )
    ]


    generated_scripts = []


    # --------------------------------------------------------
    # Generate each concept
    # --------------------------------------------------------

    for index, concept in enumerate(
        concepts,
        1
    ):

        print(
            "\nGenerating concept {}/3 → {}".format(
                index,
                concept
            )
        )


        prompt = build_prompt(
            concept,
            successful_ads,
            research,
            unique_data
        )


        try:

            script = generate_script(
                prompt
            )


            script["concept_number"] = index


            # Save individual concept
            filename = (
                f"scripts/concept_{index}.json"
            )


            with open(
                filename,
                "w"
            ) as f:

                json.dump(
                    script,
                    f,
                    indent=2
                )


            generated_scripts.append(
                script
            )


            print(
                "Saved →",
                filename
            )


        except Exception as e:

            print(
                "ERROR:",
                e
            )


    # --------------------------------------------------------
    # Save master file
    # --------------------------------------------------------

    master = {
        "project": "CrowdWisdom Trading Video Ads",
        "format": "9:16",
        "duration": "30-60 seconds",
        "concept_count": len(generated_scripts),
        "concepts": generated_scripts
    }


    with open(
        "scripts/scripts.json",
        "w"
    ) as f:

        json.dump(
            master,
            f,
            indent=2
        )


    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    print("\n========================================")
    print("SCRIPT GENERATION COMPLETE")
    print("========================================")

    print(
        "Scripts generated:",
        len(generated_scripts)
    )

    print(
        "Master file → scripts/scripts.json"
    )


    try:

        with open(
            "scripts/scripts.json",
            "r"
        ) as f:

            json.load(f)


        print(
            "JSON validation: PASSED ✅"
        )


    except Exception as e:

        print(
            "JSON validation: FAILED ❌"
        )

        print(e)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
