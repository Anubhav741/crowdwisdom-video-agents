# CrowdWisdom Trading AI Video Agent Pipeline

An AI-powered multi-stage pipeline for researching trading audiences, analyzing successful Meta ads, generating advertising concepts, and producing short-form trading video ads.

## Overview

This project was built as an internship assessment for CrowdWisdomTrading.

The pipeline combines:

- **Apify** — Meta/Facebook Ad Library data collection
- **OpenRouter** — LLM-based creative analysis
- **Tavily** — audience and market research
- **CrowdWisdom data** — proprietary trading insights supplied for the assessment
- **OpenMontage / Remotion** — programmatic cinematic video generation
- **Piper TTS** — voice narration generation
- **FFmpeg** — audio assembly and media processing

## Pipeline

```text
                    ┌─────────────────────┐
                    │       Trigger       │
                    │   main.py / scripts │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Ads Manager      │
                    │   Agent / Apify      │
                    └──────────┬──────────┘
                               │
                               ▼
                       ads_raw.json
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Ad Analysis      │
                    │      OpenRouter      │
                    └──────────┬──────────┘
                               │
                               ▼
                     successful_ads.json
                               │
                    ┌──────────┴──────────┐
                    ▼                     ▼
             Tavily Research       CrowdWisdom Data
                    │                     │
                    ▼                     ▼
          research_insights.json    unique_data.json
                    │                     │
                    └──────────┬──────────┘
                               ▼
                    ┌─────────────────────┐
                    │    Script Agent     │
                    │    3 Ad Concepts    │
                    └──────────┬──────────┘
                               │
                               ▼
                       scripts/*.json
                               │
                               ▼
                    ┌─────────────────────┐
                    │    Video Agent      │
                    │ OpenMontage/Remotion │
                    │    + Piper + FFmpeg │
                    └──────────┬──────────┘
                               │
                               ▼
                         Final MP4 Ads

eof
