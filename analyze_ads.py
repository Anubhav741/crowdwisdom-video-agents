import os
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "openai/gpt-4o-mini"


# ============================================================
# EXTRACT USEFUL DATA FROM APIFY AD
# ============================================================

def extract_ad(ad):

    snapshot = ad.get("snapshot", {})

    body = snapshot.get("body", {})

    if isinstance(body, dict):
        body_text = body.get("text", "")
    else:
        body_text = str(body)

    videos = snapshot.get("videos", [])

    return {
        "ad_archive_id": ad.get("ad_archive_id"),

        "page_name": ad.get(
            "page_name",
            snapshot.get("page_name", "")
        ),

        "page_category": (
            ad.get("_details", {})
            .get("advertiser", {})
            .get("ad_library_page_info", {})
            .get("page_info", {})
            .get("page_category", "")
        ),

        "body": body_text,

        "title": snapshot.get("title", ""),

        "cta": snapshot.get("cta_text", ""),

        "link_description": snapshot.get(
            "link_description", ""
        ),

        "display_format": snapshot.get(
            "display_format", ""
        ),

        "is_active": ad.get("is_active"),

        "start_date": ad.get("start_date"),

        "end_date": ad.get("end_date"),

        "has_video": len(videos) > 0
    }


# ============================================================
# OPENROUTER ANALYSIS
# ============================================================

def analyze_one_ad(ad, index):

    print(
        "\nAnalyzing ad {}/20 → {}".format(
            index,
            ad["page_name"]
        )
    )

    prompt = f"""
You are a senior performance marketing analyst.

Analyze this Meta advertisement for a trading/investment audience.

Return ONLY valid JSON using exactly these fields:

{{
  "hook": "",
  "pain_point": "",
  "target_icp": "",
  "promise": "",
  "mechanism": "",
  "CTA": "",
  "visual_pattern": "",
  "marketing_angle": "",
  "why_it_works": ""
}}

Rules:

- Read the actual advertisement carefully.
- Use the supplied advertisement text.
- Do not automatically use "unknown".
- Infer reasonable marketing insights from the ad.
- Do not invent statistics.
- Do not claim actual sales or revenue performance.
- Do not claim guaranteed trading results.
- Keep each field concise.
- Make the target ICP specific when possible.
- Identify the actual marketing angle used by the advertisement.
- Identify the likely visual/creative pattern from the available format information.

Advertisement:

Page:
{ad["page_name"]}

Page Category:
{ad["page_category"]}

Body:
{ad["body"]}

Title:
{ad["title"]}

CTA:
{ad["cta"]}

Link Description:
{ad["link_description"]}

Display Format:
{ad["display_format"]}

Has Video:
{ad["has_video"]}
"""

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

            "temperature": 0.1
        },

        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    content = (
        result["choices"][0]["message"]["content"]
        .strip()
    )

    # Remove markdown code fences if model returns them
    if content.startswith("```json"):
        content = content[len("```json"):].strip()

    elif content.startswith("```"):
        content = content[len("```"):].strip()

    if content.endswith("```"):
        content = content[:-3].strip()

    # Extract JSON object
    start = content.find("{")
    end = content.rfind("}")

    if start == -1 or end == -1:

        with open(
            "openrouter_debug.txt",
            "w"
        ) as f:
            f.write(content)

        raise ValueError(
            "Invalid JSON response. "
            "Check openrouter_debug.txt"
        )

    content = content[start:end + 1]

    return json.loads(content)


# ============================================================
# CREATIVE QUALITY SCORING
# ============================================================

def calculate_score(ad):

    hook = str(
        ad.get("hook", "")
    ).strip().lower()

    pain = str(
        ad.get("pain_point", "")
    ).strip().lower()

    icp = str(
        ad.get("target_icp", "")
    ).strip().lower()

    promise = str(
        ad.get("promise", "")
    ).strip().lower()

    mechanism = str(
        ad.get("mechanism", "")
    ).strip().lower()

    cta = str(
        ad.get("CTA", "")
    ).strip().lower()

    visual = str(
        ad.get("visual_pattern", "")
    ).strip().lower()


    # --------------------------------------------------------
    # Individual quality evaluator
    # --------------------------------------------------------

    def quality(text):

        if not text or text == "unknown":
            return 0.0

        score = 0.5

        # More detailed explanation
        if len(text) > 40:
            score += 0.15

        if len(text) > 80:
            score += 0.10

        # Useful trading/marketing vocabulary
        useful_words = [
            "trader",
            "trading",
            "market",
            "loss",
            "losing",
            "risk",
            "entry",
            "stop",
            "signal",
            "live",
            "data",
            "decision",
            "investor",
            "community",
            "setup",
            "strategy",
            "guidance",
            "profit",
            "analysis",
            "research",
            "support"
        ]

        matches = sum(
            1
            for word in useful_words
            if word in text
        )

        score += min(
            matches * 0.05,
            0.25
        )

        return min(score, 1.0)


    # --------------------------------------------------------
    # Calculate weighted dimensions
    # --------------------------------------------------------

    hook_score = quality(hook) * 15

    pain_score = quality(pain) * 15

    icp_score = quality(icp) * 15

    promise_score = quality(promise) * 15

    mechanism_score = quality(mechanism) * 10

    cta_score = quality(cta) * 10

    visual_score = quality(visual) * 20


    total = (
        hook_score
        + pain_score
        + icp_score
        + promise_score
        + mechanism_score
        + cta_score
        + visual_score
    )

    return round(
        min(total, 100)
    )


# ============================================================
# MAIN PIPELINE
# ============================================================

def main():

    print("========================================")
    print("CROWDWISDOM ADS ANALYSIS")
    print("========================================")


    # --------------------------------------------------------
    # Check OpenRouter API key
    # --------------------------------------------------------

    if not API_KEY:

        print(
            "ERROR: OPENROUTER_API_KEY missing."
        )

        return


    # --------------------------------------------------------
    # Check ads_raw.json
    # --------------------------------------------------------

    if not os.path.exists(
        "ads_raw.json"
    ):

        print(
            "ERROR: ads_raw.json not found."
        )

        print(
            "Run tools_apify.py first."
        )

        return


    # --------------------------------------------------------
    # Load raw ads
    # --------------------------------------------------------

    with open(
        "ads_raw.json",
        "r"
    ) as f:

        raw_ads = json.load(f)


    print(
        "Raw ads:",
        len(raw_ads)
    )


    analyzed = []


    # --------------------------------------------------------
    # Analyze every ad
    # --------------------------------------------------------

    for index, raw_ad in enumerate(
        raw_ads,
        1
    ):

        ad = extract_ad(raw_ad)


        # Skip ads with no usable text
        if (
            not ad["body"]
            and not ad["title"]
        ):

            print(
                "Skipping ad {} → no text".format(
                    index
                )
            )

            continue


        try:

            analysis = analyze_one_ad(
                ad,
                index
            )


            # ------------------------------------------------
            # Add metadata
            # ------------------------------------------------

            analysis["ad_archive_id"] = (
                ad["ad_archive_id"]
            )

            analysis["page_name"] = (
                ad["page_name"]
            )


            # ------------------------------------------------
            # Add creative score
            # ------------------------------------------------

            analysis["creative_score"] = (
                calculate_score(
                    analysis
                )
            )


            # ------------------------------------------------
            # Add ranking basis
            # ------------------------------------------------

            analysis["ranking_basis"] = (
                "creative_effectiveness_estimate"
            )


            analyzed.append(
                analysis
            )


            print(
                "   Score → {}/100".format(
                    analysis["creative_score"]
                )
            )


        except Exception as e:

            print(
                "   ERROR → {}".format(e)
            )


        # Small delay between API requests
        time.sleep(1)


    # --------------------------------------------------------
    # Sort highest score first
    # --------------------------------------------------------

    analyzed.sort(
        key=lambda x: x["creative_score"],
        reverse=True
    )


    # --------------------------------------------------------
    # Save output
    # --------------------------------------------------------

    with open(
        "successful_ads.json",
        "w"
    ) as f:

        json.dump(
            analyzed,
            f,
            indent=2
        )


    # --------------------------------------------------------
    # Final report
    # --------------------------------------------------------

    print("\n========================================")
    print("ANALYSIS COMPLETE")
    print("========================================")

    print(
        "Ads analyzed:",
        len(analyzed)
    )

    print(
        "Saved → successful_ads.json"
    )


    print("\nTOP 5 CREATIVE ADS:")


    for i, ad in enumerate(
        analyzed[:5],
        1
    ):

        print(
            "{}. {} → {}/100".format(
                i,
                ad["page_name"],
                ad["creative_score"]
            )
        )


    # --------------------------------------------------------
    # Validate JSON
    # --------------------------------------------------------

    print("\nJSON validation:")


    try:

        with open(
            "successful_ads.json",
            "r"
        ) as f:

            json.load(f)


        print(
            "successful_ads.json is valid ✅"
        )


    except Exception as e:

        print(
            "JSON validation failed ❌"
        )

        print(e)


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
