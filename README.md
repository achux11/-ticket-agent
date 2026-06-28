# 🐛 Bug Ticket Agent
> Paste your code → AI detects bugs → GitHub ticket created in 30 seconds

![Python](https://img.shields.io/badge/Python-3.11-blue)
![HuggingFace](https://img.shields.io/badge/HuggingFace-llama--3.1--8b-orange)
![FAISS](https://img.shields.io/badge/Vector_DB-FAISS-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightblue)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-red)

---

## 🔄 Pipeline

Code Input (Streamlit) → Bug Analysis (HuggingFace + llama-3.1-8b) → Duplicate Check (FAISS) → Local Storage (SQLite) → GitHub Issues API → Dashboard ✅

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| UI | Streamlit | Web interface and dashboard |
| LLM | HuggingFace + llama-3.1-8b | Bug detection and analysis |
| Vector DB | FAISS | Semantic duplicate detection |
| Embeddings | sentence-transformers | Text to vectors |
| Database | SQLite | Local ticket storage |
| Ticket Platform | GitHub Issues API | Auto ticket creation |
| Language | Python | Everything — no frameworks |

---

## 🔮 Future Planning

### Phase 1 — Better AI (Short Term)
- Switch to Claude API for better accuracy
- Support JavaScript, Java, C++, SQL
- Detect security vulnerabilities
- Add confidence score per bug

### Phase 2 — Better Integration (Medium Term)
- GitHub Actions — auto scan every commit
- Jira integration for enterprise teams
- Slack notifications for Critical bugs
- VS Code extension

### Phase 3 — Smarter Agent (Long Term)
- Auto-fix bugs and create pull requests
- Assign tickets to right developer automatically
- Natural language bug reporting
- Multi-repo support

### Phase 4 — Analytics (Advanced)
- Bug trend dashboard over time
- Which part of codebase is most buggy
- Sprint planning based on bug data

---

## 👤 Author

Achintya Vamshi Nudurupati
- GitHub: @achux11

Built from scratch in pure Python — no LangChain, no frameworks.
