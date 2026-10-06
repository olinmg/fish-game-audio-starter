// Tiny token-minting server. Browser code never sees FISH_API_KEY: it asks
// this server for a session, and this server asks Fish Audio on its behalf.
// Docs: https://docs.fish.audio/agents/deploy/authentication.md
import express from "express";
import dotenv from "dotenv";
import { existsSync } from "node:fs";
import { resolve, dirname } from "node:path";
import { fileURLToPath } from "node:url";

// Load .env from this example folder or any parent (matches CONVENTIONS.md).
const here = dirname(fileURLToPath(import.meta.url));
for (const dir of [here, resolve(here, ".."), resolve(here, "../.."), resolve(here, "../../..")]) {
  const envPath = resolve(dir, ".env");
  if (existsSync(envPath)) {
    dotenv.config({ path: envPath });
    break;
  }
}

const { FISH_API_KEY, FISH_AGENT_ID } = process.env;
const PORT = process.env.PORT || 8787;

const app = express();
app.use(express.json());

// One route: mint a short-lived session token for the browser to connect with.
// https://docs.fish.audio/agents/deploy/authentication.md
app.post("/api/session", async (req, res) => {
  if (!FISH_API_KEY) {
    return res.status(500).json({ error: "FISH_API_KEY is not set. Copy .env.example to .env and fill it in." });
  }
  if (!FISH_AGENT_ID) {
    return res.status(500).json({ error: "FISH_AGENT_ID is not set. Run `npm run create-agent` first, or paste an id from the console." });
  }

  try {
    const upstream = await fetch("https://api.fish.audio/v1/agent/sessions", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${FISH_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        agent_id: FISH_AGENT_ID,
        // GAME HOOK: pass real player facts here instead of the mockup values,
        // e.g. end_user_id / dynamic_variables derived from a logged-in user.
        dynamic_variables: req.body?.dynamicVariables ?? {},
      }),
    });

    if (!upstream.ok) {
      const detail = await upstream.text();
      console.error("[server] session creation failed:", upstream.status, detail);
      return res.status(502).json({ error: "session_unavailable", status: upstream.status });
    }

    res.json(await upstream.json());
  } catch (err) {
    console.error("[server] session creation error:", err);
    res.status(502).json({ error: "session_unavailable" });
  }
});

app.listen(PORT, () => console.log(`[server] token server on http://localhost:${PORT}`));
