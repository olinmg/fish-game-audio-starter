# Conventions

These rules keep every example easy to copy into a game and easy for an LLM to extend.

## 1. Each example is self-contained

Each `examples/NN-name/` folder can be copied out of the repo on its own. It has:

- `README.md`: starts with a one-line "Coding agent? Run `npx skills add https://docs.fish.audio` and read
  [AGENTS.md](../../AGENTS.md)" note, then what it shows, how to run it (one command), which Fish docs it relies on (links), and
  "Where to put your game code".
- Its own dependency file (`pyproject.toml` for uv, `package.json` for Node).
- A `game.py` / `game.ts` / `game.js` file holding **all** game-side logic. Everything else is audio plumbing.

No shared library code between examples. Duplicating a 20-line helper beats a cross-folder import.

## 2. Mark where the game goes

```python
# GAME HOOK: <what a game would do here, in one line>
```

```python
def npc_reply(player_text: str, state: dict) -> str:
    # MOCKUP: always returns the same line so the example runs without an LLM.
    # Replace with your game logic or a real LLM call (see call_llm below).
    return "[MOCKUP] Halt, traveller. The bridge is closed tonight."
```

- `GAME HOOK` = a place a game is expected to plug in.
- `MOCKUP` = fake behaviour standing in for real game logic. Log mock output with a `[MOCKUP]` prefix
  so it's obvious at runtime.
- Game state is a tiny dict or object (`{"location": "bridge", "player_has_sword": False}`) with a
  `GAME HOOK` comment saying "your real game state goes here".
- The default persona is **one sentence**, e.g. `NPC_PROMPT = "You are Brom, a grumpy bridge guard in a fantasy village. Answer in one or two short sentences."`

## 3. Optional real LLM

If `LLM_API_KEY` is set, use an OpenAI-compatible chat completion (`openai` SDK with
`base_url=LLM_BASE_URL`, `model=LLM_MODEL`). Otherwise fall back to the mock. This keeps every example
runnable with only `FISH_API_KEY`.

## 4. Config and secrets

- Read env vars, loading `.env` from the example folder or any parent (Python: `python-dotenv` `find_dotenv()`;
  Node: `dotenv`). Variable names come from the root `.env.example`.
- Never put `FISH_API_KEY` in browser code. Browsers talk to a small local server.
- Write generated audio to `out/` inside the example (gitignored).

## 5. Code style

- Small and readable beats clever. Comments explain *why* (latency, protocol quirks), with a docs link
  next to each Fish API call.
- Python 3.11+, type hints, `async` where streaming needs it. TypeScript or plain modern JS for the browser.
- Print a short log of what's happening (`[stt] ...`, `[llm] ...`, `[tts] first audio after 412 ms`).
  Latency numbers help teams tune.

## 6. Git workflow

- One branch and PR per example or doc area: `feat/<example-name>` or `docs/<topic>`.
- Only touch your own folder. Root files (README, AGENTS.md, .env.example) are owned by `main`;
  propose changes in the PR description instead.
- In the PR description, say what you tested and how (real Fish key, mock only, or untested).
