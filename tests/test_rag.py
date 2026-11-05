"""Tests for the RAG pieces that don't need the embedding model or network."""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.llm import build_prompt  # noqa: E402


def test_prompt_without_history_has_no_context_section():
    prompt = build_prompt("x = 1/0")
    assert "Similar bugs found and fixed earlier" not in prompt
    assert prompt.endswith("x = 1/0")


def test_prompt_includes_retrieved_fixes():
    past = [{"title": "Division by zero on empty list", "severity": "High",
             "description": "len(numbers) can be 0", "suggested_fix": "Return 0 when the list is empty"}]
    prompt = build_prompt("avg = total / len(items)", past)
    assert "Similar bugs found and fixed earlier" in prompt
    assert "Return 0 when the list is empty" in prompt
    assert prompt.index("Fix used") < prompt.index("Code to analyze")


def test_get_tickets_by_ids_keeps_retrieval_order(tmp_path, monkeypatch):
    import utils.db as db
    monkeypatch.setattr(db, "DB_PATH", str(tmp_path / "t.db"))
    db.init_db()
    a = db.save_ticket("A", "first", "Low", "Logic Error", "", "fix A")
    b = db.save_ticket("B", "second", "High", "Runtime Error", "", "fix B")
    rows = db.get_tickets_by_ids([b, a, 999])
    assert [r["suggested_fix"] for r in rows] == ["fix B", "fix A"]
