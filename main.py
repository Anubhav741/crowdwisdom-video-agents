import os
import sys
import subprocess
from pathlib import Path

# Hermes is installed in the dedicated Hermes environment.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hermes-agent"))

from dotenv import load_dotenv
from run_agent import AIAgent


ROOT = Path(__file__).resolve().parent


def run_script(name, script):
    print("\n" + "=" * 60)
    print(f"AGENT: {name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(ROOT / script)],
        cwd=ROOT,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{name} failed with exit code {result.returncode}"
        )

    print(f"✅ {name} completed")


def require_file(path):
    file_path = ROOT / path

    if not file_path.exists():
        raise FileNotFoundError(
            f"Expected output not found: {path}"
        )

    print(f"✓ {path}")


def hermes_stage(stage, instruction):
    print("\n" + "=" * 60)
    print(f"HERMES AGENT: {stage}")
    print("=" * 60)

    agent = AIAgent(
        provider="OpenRouter",
        model="openai/gpt-4o-mini",
        max_iterations=3,
        quiet_mode=True,
    )

    result = agent.run_conversation(
        instruction,
        system_message=(
            "You are an orchestration agent for the CrowdWisdom "
            "Trading video-ad pipeline. "
            "Do not fabricate data. "
            "Return a concise execution acknowledgement."
        ),
    )

    print("Hermes response:", result.get("content", result))
    print(f"✅ Hermes completed: {stage}")


def main():
    load_dotenv(ROOT / ".env")

    print("""
============================================================
       CROWDWISDOM HERMES VIDEO AD PIPELINE
============================================================
""")

    required_keys = [
        "OPENROUTER_API_KEY",
        "APIFY_API_TOKEN",
        "TAVILY_API_KEY",
    ]

    missing = [key for key in required_keys if not os.getenv(key)]

    if missing:
        print("❌ Missing environment variables:")
        for key in missing:
            print(f"   {key}")
        sys.exit(1)

    print("✅ Environment variables loaded")

    # ---------------------------------------------------------
    # Hermes orchestration layer
    # ---------------------------------------------------------
    hermes_stage(
        "Pipeline Planning",
        """
Plan the execution order for this CrowdWisdom advertising
pipeline:

1. Scrape recent Meta trading ads with Apify.
2. Analyze creative effectiveness using OpenRouter.
3. Research retail-trader pain points using Tavily.
4. Combine research with CrowdWisdom unique data.
5. Generate three advertising concepts.
6. Render the concepts using OpenMontage/Remotion.

Confirm that this sequence is logically valid.
""",
    )

    # ---------------------------------------------------------
    # Ads Manager Agent
    # ---------------------------------------------------------
    run_script(
        "Ads Manager Agent / Apify",
        "tools_apify.py",
    )
    require_file("ads_raw.json")

    # ---------------------------------------------------------
    # Ad Analysis Agent
    # ---------------------------------------------------------
    run_script(
        "Ad Analysis Agent / OpenRouter",
        "analyze_ads.py",
    )
    require_file("successful_ads.json")

    # ---------------------------------------------------------
    # Research Agent
    # ---------------------------------------------------------
    run_script(
        "Market Research Agent / Tavily",
        "research_agent.py",
    )
    require_file("research.json")

    # ---------------------------------------------------------
    # Research Insights
    # ---------------------------------------------------------
    run_script(
        "Research Insights Agent",
        "research_insights.py",
    )
    require_file("research_insights.json")

    # ---------------------------------------------------------
    # Script Agent
    # ---------------------------------------------------------
    run_script(
        "Script Agent / OpenRouter",
        "script_agent.py",
    )

    require_file("scripts/concept_1.json")
    require_file("scripts/concept_2.json")
    require_file("scripts/concept_3.json")

    # ---------------------------------------------------------
    # Video Agent
    # ---------------------------------------------------------
    print("\n" + "=" * 60)
    print("VIDEO AGENT / OPENMONTAGE")
    print("=" * 60)

    videos = [
        "output/videos/concept_1_the_noise.mp4",
        "output/videos/concept_2_from_data_to_decision.mp4",
        "output/videos/concept_3_find_the_signal.mp4",
    ]

    for video in videos:
        if (ROOT / video).exists():
            print(f"✓ {video}")
        else:
            print(f"⚠ Missing: {video}")

    hermes_stage(
        "Final QA",
        """
Verify the CrowdWisdom pipeline outputs.

Expected:
- successful_ads.json
- research_insights.json
- three script concepts
- three rendered MP4 advertisements

Check that the pipeline produced the expected artifacts.
""",
    )

    print("""
============================================================
              PIPELINE COMPLETED ✅
============================================================
""")


if __name__ == "__main__":
    main()
PYcat > main.py <<'PY'
import os
import sys
import subprocess
from pathlib import Path

# Hermes is installed in the dedicated Hermes environment.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "hermes-agent"))

from dotenv import load_dotenv
from run_agent import AIAgent


ROOT = Path(__file__).resolve().parent


def run_script(name, script):
    print("\n" + "=" * 60)
    print(f"AGENT: {name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(ROOT / script)],
        cwd=ROOT,
        check=False,
    )

    if result.returncode != 0:
        raise RuntimeError(
            f"{name} failed with exit code {result.returncode}"
        )

    print(f"✅ {name} completed")


def require_file(path):
    file_path = ROOT / path

    if not file_path.exists():
        raise FileNotFoundError(
            f"Expected output not found: {path}"
        )

    print(f"✓ {path}")


def hermes_stage(stage, instruction):
    print("\n" + "=" * 60)
    print(f"HERMES AGENT: {stage}")
    print("=" * 60)

    agent = AIAgent(
        provider="OpenRouter",
        model="openai/gpt-4o-mini",
        max_iterations=3,
        quiet_mode=True,
    )

    result = agent.run_conversation(
        instruction,
        system_message=(
            "You are an orchestration agent for the CrowdWisdom "
            "Trading video-ad pipeline. "
            "Do not fabricate data. "
            "Return a concise execution acknowledgement."
        ),
    )

    print("Hermes response:", result.get("content", result))
    print(f"✅ Hermes completed: {stage}")


def main():
    load_dotenv(ROOT / ".env")

    print("""
============================================================
       CROWDWISDOM HERMES VIDEO AD PIPELINE
============================================================
""")

    required_keys = [
        "OPENROUTER_API_KEY",
        "APIFY_API_TOKEN",
        "TAVILY_API_KEY",
    ]

    missing = [key for key in required_keys if not os.getenv(key)]

    if missing:
        print("❌ Missing environment variables:")
        for key in missing:
            print(f"   {key}")
        sys.exit(1)

    print("✅ Environment variables loaded")

    # ---------------------------------------------------------
    # Hermes orchestration layer
    # ---------------------------------------------------------
    hermes_stage(
        "Pipeline Planning",
        """
Plan the execution order for this CrowdWisdom advertising
pipeline:

1. Scrape recent Meta trading ads with Apify.
2. Analyze creative effectiveness using OpenRouter.
3. Research retail-trader pain points using Tavily.
4. Combine research with CrowdWisdom unique data.
5. Generate three advertising concepts.
6. Render the concepts using OpenMontage/Remotion.

Confirm that this sequence is logically valid.
""",
    )

    # ---------------------------------------------------------
    # Ads Manager Agent
    # ---------------------------------------------------------
    run_script(
        "Ads Manager Agent / Apify",
        "tools_apify.py",
    )
    require_file("ads_raw.json")

    # ---------------------------------------------------------
    # Ad Analysis Agent
    # ---------------------------------------------------------
    run_script(
        "Ad Analysis Agent / OpenRouter",
        "analyze_ads.py",
    )
    require_file("successful_ads.json")

    # ---------------------------------------------------------
    # Research Agent
    # ---------------------------------------------------------
    run_script(
        "Market Research Agent / Tavily",
        "research_agent.py",
    )
    require_file("research.json")

    # ---------------------------------------------------------
    # Research Insights
    # ---------------------------------------------------------
    run_script(
        "Research Insights Agent",
        "research_insights.py",
    )
    require_file("research_insights.json")

    # ---------------------------------------------------------
    # Script Agent
    # ---------------------------------------------------------
    run_script(
        "Script Agent / OpenRouter",
        "script_agent.py",
    )

    require_file("scripts/concept_1.json")
    require_file("scripts/concept_2.json")
    require_file("scripts/concept_3.json")

    # ---------------------------------------------------------
    # Video Agent
    # ---------------------------------------------------------
    print("\n" + "=" * 60)
    print("VIDEO AGENT / OPENMONTAGE")
    print("=" * 60)

    videos = [
        "output/videos/concept_1_the_noise.mp4",
        "output/videos/concept_2_from_data_to_decision.mp4",
        "output/videos/concept_3_find_the_signal.mp4",
    ]

    for video in videos:
        if (ROOT / video).exists():
            print(f"✓ {video}")
        else:
            print(f"⚠ Missing: {video}")

    hermes_stage(
        "Final QA",
        """
Verify the CrowdWisdom pipeline outputs.

Expected:
- successful_ads.json
- research_insights.json
- three script concepts
- three rendered MP4 advertisements

Check that the pipeline produced the expected artifacts.
""",
    )

    print("""
============================================================
              PIPELINE COMPLETED ✅
============================================================
""")


if __name__ == "__main__":
    main()
