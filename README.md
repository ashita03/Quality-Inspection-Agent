---
title: QC Agent
emoji: 🔍
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
---

# QC Agent

A LangGraph agent that inspects manufacturing part images for defects,
identifies the equipment type, checks recent defect history, and decides
whether to pass a part or escalate it for human review.

## Architecture

React frontend → FastAPI backend → LangGraph agent → Ollama (LLaVA) for
vision, SQLite for logging.

## Known limitations

- Deployed on Hugging Face Spaces' free CPU tier — inference is slower here
  than on a local machine with a dedicated GPU.
- Storage on the free tier is not persistent — inspection history resets
  when the Space restarts.