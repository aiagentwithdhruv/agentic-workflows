# Agentic Workflows Engine

A code-first framework for building AI-powered automations. Tell the agent what you want, it builds the tools and runs them.

**The pattern:** AI reasons. Code executes. Accuracy stays high.

## Quick Start

```bash
git clone https://github.com/aiagentwithdhruv/agentic-workflows.git
cd agentic-workflows
cp .env.example .env       # Add your API keys
```

Open in [Claude Code](https://claude.ai/claude-code) or [Cursor](https://cursor.com) and prompt:

```
"Build me an automation that researches a topic and emails me a summary"
```

The agent reads `CLAUDE.md`, creates the tools, creates the workflow, runs it, and self-fixes if anything breaks.

## How It Works

```
You say what you want
        ↓
Agent reads CLAUDE.md (how to operate)
        ↓
Checks workflows/ (does a workflow exist for this?)
        ↓
Picks tools from tools/ (or creates new ones)
        ↓
Executes → Observes → Self-fixes if needed
        ↓
Delivers output + logs the run
```

**Why this works:** When AI handles every step directly, accuracy drops — 90% per step = 59% after 5 steps. By offloading execution to deterministic Python scripts, accuracy stays at 90%. The agent thinks. Scripts execute.

## Folder Structure

```
agentic-workflows/
├── CLAUDE.md              # Agent instructions — the brain
├── .env.example           # API keys template
├── config/
│   ├── models.yaml        # LLM routing (Euri, OpenRouter, OpenAI, Anthropic)
│   ├── settings.yaml      # Retries, cost limits, timeouts
│   └── credentials.yaml   # Tool → env var mapping
├── workflows/
│   └── _template.md       # Template for new workflows
├── tools/
│   ├── _template.py       # Template for new tools
│   └── registry.yaml      # Tool schemas (inputs/outputs/cost)
├── shared/
│   ├── logger.py          # Structured JSON logging
│   ├── retry.py           # Exponential backoff
│   ├── cost_tracker.py    # API cost tracking + budget limits
│   └── env_loader.py      # .env loading + validation
├── runs/                  # Auto-generated run logs
└── .tmp/                  # Temporary files (disposable)
```

## LLM Providers

Three options, all OpenAI-compatible — same SDK, just swap the base URL:

| Priority | Provider | What You Get | Cost |
|----------|----------|-------------|------|
| 1 | **[Euri](https://euron.one)** | 24 models (GPT-4o, Claude, Gemini, Llama) | **Free** — 200K tokens/day |
| 2 | **[OpenRouter](https://openrouter.ai)** | 300+ models, every provider | Pay-per-use, free credits on signup |
| 3 | OpenAI / Anthropic direct | Direct API access | Pay-per-use |

```python
from openai import OpenAI

# Euri (free — start here)
client = OpenAI(base_url="https://api.euron.one/api/v1/euri", api_key="your-euri-key")

# OpenRouter (300+ models)
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key="your-openrouter-key")
```

## What You Can Build

Anything. The framework doesn't care what the automation does:

- Research competitors → generate report → email it
- Scrape leads → classify them → send outreach emails
- Monitor YouTube channels → find viral ideas → draft scripts
- Parse invoices → update spreadsheet → send summary
- Whatever you need — just prompt the agent

Every automation you build adds tools that the next automation can reuse. The system compounds.

## The Self-Improvement Loop

```
Error occurs → Agent reads the error → Fixes the tool → Verifies the fix
→ Updates the workflow → Logs it → System is now stronger
```

Every failure makes the system more robust. The more you use it, the fewer things break.

## Credits

Architecture inspired by the [WAT pattern](https://x.com) (Workflows, Agents, Tools) — a standard industry approach to separating AI reasoning from deterministic code execution, used across LangChain, CrewAI, Anthropic's agent patterns, and more.

## License

MIT
