# 🪄 SlideMage: AI-Powered Research Assistant

SlideMage is an experimental project exploring how multi-agent AI workflows can assist in research summarization and presentation generation. The goal is to automate the process of transforming academic papers or text materials into structured summaries, notes, and presentation slides.

Try it here : https://slidemage-9ykktnu5wzy3bhclpkmvhn.streamlit.app/
##  Overview

SlideMage aims to bring together the power of Large Language Models, LangGraph-based orchestration, and Model Context Protocol (MCP) modularity to build an adaptive AI research assistant.

## Planned Capabilities

- Research Paper Ingestion – Extract key sections (abstract, methods, results) from academic PDFs or URLs.

- AI Summarization & Note Generation – Generate structured notes and short summaries using LLMs.

- Contextual Q&A – Ask questions about the paper content through RAG-based retrieval.

- Presentation Generation – Convert key findings into PowerPoint-style slides.

- Agentic Workflow – Coordinate specialized agents (Reader, Summarizer, Critic, Presenter) using LangGraph.

## Tech Stack
```
AI & Orchestration – LangGraph, Model Context Protocol (MCP), Gemini 2.5 Pro
Backend – FastAPI (Python)
Frontend – Streamlit (prototype interface)
Integrations – Wikipedia API, FAISS (planned for retrieval)
```

## Current Status

🚧 In active development.
Currently experimenting with multi-agent design patterns and LLM summarization pipelines.
Future updates will include end-to-end orchestration and PowerPoint export.

