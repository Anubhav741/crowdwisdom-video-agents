# CrowdWisdom Trading AI Video Agent Pipeline

An AI-powered multi-stage pipeline for researching trading audiences, analyzing recent Meta ads, generating advertising concepts, and producing short-form trading video ads.

## Overview

Built as an internship assessment for CrowdWisdomTrading.

The pipeline combines:

- **Hermes Agent** — workflow orchestration
- **Apify** — Meta/Facebook Ad Library data collection
- **OpenRouter** — LLM-based creative analysis
- **Tavily** — audience and market research
- **CrowdWisdom data** — proprietary trading insights supplied for the assessment
- **OpenMontage / Remotion** — programmatic video generation
- **Piper TTS** — voice narration
- **FFmpeg** — audio/media processing

## Pipeline

```text
Trigger / main.py
       ↓
Hermes Agent
       ↓
Ads Manager Agent → Apify
       ↓
ads_raw.json
       ↓
Ad Analysis Agent → OpenRouter
       ↓
successful_ads.json
       ↓
Tavily Research + CrowdWisdom Data
       ↓
Research Insights
       ↓
Script Agent → OpenRouter
       ↓
3 Ad Concepts
       ↓
OpenMontage / Remotion
       ↓
Piper TTS + FFmpeg
       ↓
Final MP4 Ads
