# Fish Audio Game Audio Starter

Starting blocks for the **audio layer** of a voice-driven game, built on [Fish Audio](https://fish.audio).
The game itself is yours to build. This repo gives you working, copy-pasteable snippets for making
characters **speak**, **listen** and **hold conversations**, plus docs on the concepts behind them.

## 🤖 Building with an AI coding agent? Start here

Give your agent the official Fish Audio knowledge **before** it writes code:

```bash
npx skills add https://docs.fish.audio
```

This installs two official skills, **`fish-audio-sdk`** (Python and JS SDK signatures) and **`fish-audio-api`**
(raw REST and WebSocket protocol), for Claude Code, Cursor, Codex and others. Claude Code users already have them:
they are committed in [`.claude/skills/`](.claude/skills/). Also point your agent at:

| Resource | URL |
|---|---|
| Doc index for LLMs | https://docs.fish.audio/llms.txt |
| Full docs in one file | https://docs.fish.audio/llms-full.txt |
| Fish Audio MCP server (tools: voices, TTS, STT) | `https://api.fish.audio/mcp` |
| This repo's rules for agents | [AGENTS.md](AGENTS.md) |

> Every example runs with only a `FISH_API_KEY`. The "game brain" in each example is a clearly marked
> **MOCKUP** (a one-sentence prompt or a fake LLM that always returns the same line). Replace it with
> your game.

## Quick start

```bash
cp .env.example .env        # then paste your FISH_API_KEY (https://fish.audio/app/api-keys)
cd examples/01-tts-basics   # pick any example and follow its README
```

Python examples use [uv](https://docs.astral.sh/uv/) (`uv run ...`). Browser examples use Node 20+.

## Pick a path

| | Path | Control | Effort | Start here |
|---|---|---|---|---|
| 🔊 | **Just speech**: narrator, NPC barks, cutscenes | — | Lowest | [01-tts-basics](examples/01-tts-basics) · [03-npc-voice-factory](examples/03-npc-voice-factory) |
| ⚡ | **Streaming speech**: an LLM's text spoken as it is generated | Medium | Low | [02-streaming-tts](examples/02-streaming-tts) |
| 🗣️ | **A. Hosted Fish agent**: Fish runs STT + LLM + TTS + turn-taking; your game injects events and receives tool calls | Medium | Low | [04-agent-web](examples/04-agent-web) |
| 🧠 | **B. Hosted agent + your own LLM server**: Fish handles voice, your "game master" server owns state and replies | High | Medium | [05-agent-custom-llm](examples/05-agent-custom-llm) |
| 🔧 | **C. Own pipeline**: mic → voice detection → STT → LLM → streaming TTS, every piece swappable | Full | Highest | [06-own-pipeline](examples/06-own-pipeline) |

Not sure which one fits? Read [docs/00-choose-your-path.md](docs/00-choose-your-path.md).

## Where your game code goes

Every example keeps its game logic in **one file** (`game.py` / `game.ts` / `game.js`), separate from the
audio plumbing. Find the spots to change with:

```bash
grep -rn "GAME HOOK" examples/     # places meant for your game logic
grep -rn "MOCKUP" examples/        # placeholder behaviour you should replace
```

See [CONVENTIONS.md](CONVENTIONS.md) for details.

## Docs

- [docs/00-choose-your-path.md](docs/00-choose-your-path.md): decision tree and trade-offs
- [docs/concepts/](docs/concepts/): latency, turn-taking, context injection, emotion tags, voices, NPC prompting
- [docs/gotchas.md](docs/gotchas.md): things that will bite you (read this one)
- [docs/fish-audio-links.md](docs/fish-audio-links.md): curated links into the official Fish Audio docs
