"""Tests for the custom-LLM server. Run with: uv run pytest

No FISH_API_KEY needed — these hit server.py directly with a Fish-shaped request
(session_id, fishaudio_extra_body, messages, tools) and check the SSE contract.
"""

import os

os.environ.setdefault("CUSTOM_LLM_API_KEY", "test-key")

from fastapi.testclient import TestClient

import game
import server

client = TestClient(server.app)

AUTH = {"Authorization": "Bearer test-key"}

FISH_REQUEST = {
    "model": "game-master",
    "stream": True,
    "messages": [
        {"role": "system", "content": "You are Brom, a bridge guard."},
        {"role": "user", "content": "Hello there, guard."},
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "pay_toll",
                "description": "Pay the bridge toll",
                "parameters": {"type": "object", "properties": {}},
            },
        }
    ],
    "session_id": "sess_test123",
    "user_id": "user_test123",
    "fishaudio_extra_body": {"game_session_id": "game_test123"},
}


def _parse_sse(text: str) -> list[str]:
    """Return the raw `data: ...` lines of an SSE body."""
    return [line for line in text.splitlines() if line.startswith("data:")]


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


def test_chat_completions_requires_auth():
    resp = client.post("/v1/chat/completions", json=FISH_REQUEST)
    assert resp.status_code == 401

    resp = client.post(
        "/v1/chat/completions", json=FISH_REQUEST, headers={"Authorization": "Bearer wrong"}
    )
    assert resp.status_code == 401


def test_chat_completions_streams_valid_sse_chunks():
    resp = client.post("/v1/chat/completions", json=FISH_REQUEST, headers=AUTH)
    assert resp.status_code == 200
    assert resp.headers["content-type"].startswith("text/event-stream")

    lines = _parse_sse(resp.text)
    assert lines[-1] == "data: [DONE]"

    # Every chunk except the terminal [DONE] marker must be valid OpenAI-chunk JSON.
    import json

    saw_content = False
    saw_finish_stop = False
    for line in lines[:-1]:
        chunk = json.loads(line.removeprefix("data: "))
        assert chunk["object"] == "chat.completion.chunk"
        delta = chunk["choices"][0]["delta"]
        if delta.get("content"):
            saw_content = True
        if chunk["choices"][0]["finish_reason"] == "stop":
            saw_finish_stop = True
    assert saw_content
    assert saw_finish_stop


def test_game_event_changes_mock_reply():
    session_id = "game_sword_test"
    before = game.get_state(session_id)
    assert before["player_has_sword"] is False

    event_resp = client.post(f"/game/{session_id}/event", json={"event": "sword_drawn"})
    assert event_resp.status_code == 200
    assert event_resp.json()["state"]["player_has_sword"] is True

    request_body = {**FISH_REQUEST, "fishaudio_extra_body": {"game_session_id": session_id}}
    resp = client.post("/v1/chat/completions", json=request_body, headers=AUTH)
    lines = _parse_sse(resp.text)

    import json

    first_chunk = json.loads(lines[0].removeprefix("data: "))
    content = first_chunk["choices"][0]["delta"]["content"]
    assert "sword" in content.lower() or "wary" in content.lower()
