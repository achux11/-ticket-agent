# 🐛 Bug Ticket Agent

An AI-powered bug detection and auto ticket raising agent.

## What it does
- Paste buggy code → AI detects bugs automatically
- Checks for duplicate tickets using FAISS
- Saves tickets locally in SQLite
- Creates GitHub Issues automatically

## Tech Stack
- **UI** — Streamlit
- **LLM** — HuggingFace API + llama-3.1-8b
- **Duplicate Check** — FAISS + sentence-transformers
- **Database** — SQLite
- **Tickets** — GitHub Issues API

## How to run
1. Add your keys to .env file:
   - HF_TOKEN=your_huggingface_token
   - GITHUB_TOKEN=your_github_token
   - GITHUB_REPO=username/repo-name

2. Install dependencies:
   pip install -r requirements.txt

3. Run:
   export GITHUB_TOKEN=your_token
   streamlit run app.py

## Pipeline
Code Input → HuggingFace LLM → FAISS Duplicate Check → SQLite → GitHub Issues

## Author
Built by [achux11](https://github.com/achux11)
