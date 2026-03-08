# Agentic Workflows Engine

You operate inside an **agentic workflow system** that separates reasoning from execution. You think. Code executes. That separation is what makes this reliable.

---

## Architecture: 3 Layers

```
┌─────────────────────────────────────────────────────┐
│  AGENT (You)                                         │
│  Read workflow → Pick tools → Execute → Observe      │
│  → Re-plan if failed → Log run → Deliver output      │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│  WORKFLOWS  (workflows/*.md)                         │
│  Markdown SOPs — objective, inputs, steps, tools,    │
│  outputs, error handling, cost estimate              │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│  TOOLS  (tools/*.py)                                 │
│  Deterministic Python scripts. Each has a schema.    │
│  Inputs typed. Outputs typed. Errors handled.        │
└─────────────────────────────────────────────────────┘
```

**Why this works:** When AI handles every step directly, accuracy compounds downward — 90% per step = 59% after 5 steps. By offloading execution to deterministic scripts, you stay at 90% × 100% × 100% × 100% × 100% = 90%. The agent reasons. Scripts execute. Accuracy stays high.

---

## First Run Setup

When the user opens this project for the first time, check if `.env` exists. If it doesn't:

1. Copy `.env.example` to `.env`
2. Ask the user: **"Paste your Euri API key (get it free at euron.one → Dashboard → API Key)"**
3. Write the key into `.env` under `EURI_API_KEY=`
4. Confirm: "Setup done. You're ready to build automations."

That's it. No manual file creation. No configuration steps. One API key and they're running.

---

## How You Operate

### 1. Receive a task

When the user gives you a task:

1. **Check if `.env` exists** — if not, run First Run Setup above
2. **Check workflows/ first** — is there a workflow for this?
3. **If yes** — read the workflow, gather required inputs, execute the tools in sequence
4. **If no** — check if tools/ has individual tools that can be composed
5. **If still no** — build new tools and a workflow for the task

### 2. Execute tools, don't do the work yourself

**CRITICAL RULE:** Never try to accomplish execution tasks (API calls, data processing, file generation, email sending) by writing code inline. Always use or create a tool in `tools/`.

```
BAD:  You write a 50-line script inline to scrape a website
GOOD: You run `python tools/scrape_website.py --url "https://example.com" --output .tmp/data.json`
```

Why: Inline code is throwaway. Tools are reusable, testable, and improve over time.

### 3. Handle failures intelligently

When a tool fails:

1. **Read the full error** — don't guess, read the traceback
2. **Diagnose** — is it a code bug, API issue, rate limit, auth problem, or bad input?
3. **Fix the tool** — edit `tools/<name>.py` directly
4. **Re-run** — verify the fix works
5. **Update the workflow** — add the edge case so it never happens again
6. **Log it** — append to `runs/` with what broke and what fixed it

**Cost guard:** If a tool uses paid APIs (OpenAI, Anthropic, Apify, etc.), check with the user before retrying. Don't burn credits on a loop.

### 4. Log every run

After completing a workflow, create a run log:

```
runs/YYYY-MM-DD-workflow-name.md
```

Contents:
- Workflow executed
- Inputs provided
- Tools called (in order)
- Duration per tool
- Total cost (if applicable)
- Output location
- Errors encountered + how resolved

This is how the system builds observability over time.

---

## File Structure

```
agentic-workflows/
├── CLAUDE.md                 # These instructions (you're reading this)
├── .env                      # API keys (NEVER commit, NEVER log)
├── .env.example              # Template showing required keys
├── config/
│   ├── models.yaml           # LLM routing (which model for which task)
│   ├── settings.yaml         # Global settings (retries, timeouts, cost limits)
│   └── credentials.yaml      # Maps tools → required env vars
├── workflows/
│   ├── _template.md          # Template for new workflows
│   └── <name>.md             # One file per workflow
├── tools/
│   ├── _template.py          # Template for new tools
│   ├── registry.yaml         # Tool registry (auto-maintained)
│   └── <name>.py             # One file per tool
├── shared/
│   ├── logger.py             # Structured logging (JSON, timestamps)
│   ├── retry.py              # Retry with exponential backoff
│   ├── cost_tracker.py       # Track API costs per run
│   └── env_loader.py         # Load and validate .env
├── runs/                     # Run logs (auto-generated)
├── .tmp/                     # Intermediate files (disposable)
└── .gitignore
```

### What goes where:
- **Deliverables** → cloud services (Google Sheets, email, Notion, etc.) where the user accesses them
- **Intermediates** → `.tmp/` (scraped data, generated HTML, temp exports) — regeneratable
- **Run logs** → `runs/` — permanent record of what happened
- **Secrets** → `.env` ONLY. Never in code, never in logs, never in `.tmp/`

---

## Writing New Workflows

Use `workflows/_template.md` as the base. Every workflow MUST have:

1. **Objective** — one sentence, what this accomplishes
2. **Inputs** — what the user provides (with types)
3. **Tools** — which tools from `tools/` this uses (in order)
4. **Steps** — numbered execution steps with exact commands
5. **Outputs** — what gets delivered and where
6. **Error handling** — known failure modes and what to do
7. **Cost estimate** — approximate cost per run

Workflows are living documents. Update them when you learn something new.

---

## Writing New Tools

Use `tools/_template.py` as the base. Every tool MUST:

1. **Accept CLI arguments** — `argparse` or `typer`, never hardcoded values
2. **Load secrets from .env** — via `shared/env_loader.py`
3. **Return structured output** — JSON to stdout, or write to a file
4. **Handle errors gracefully** — catch exceptions, print useful messages, exit with proper codes
5. **Log execution** — via `shared/logger.py`
6. **Have a schema entry** — add to `tools/registry.yaml` after creation

```
BAD:  tool that prints "done" and exits 0 even on failure
GOOD: tool that returns {"status": "success", "output_path": ".tmp/result.json", "records": 42}
```

After creating a tool, update `tools/registry.yaml` with its schema.

---

## Config System

### models.yaml — LLM Routing

Three providers available (priority order):

| Priority | Provider | What You Get | Cost |
|----------|----------|-------------|------|
| 1 | **Euri** (euron.one) | 24 models, OpenAI-compatible | Free 200K tokens/day |
| 2 | **OpenRouter** (openrouter.ai) | 300+ models, all providers | Pay-per-use, free credits on signup |
| 3 | Anthropic / OpenAI direct | Direct API access | Pay-per-use |

**Start with Euri** — it's free and covers most use cases. Upgrade to OpenRouter or direct keys when you need specific models or higher limits.

All three are OpenAI-compatible — same SDK, just swap the base URL:
```python
from openai import OpenAI

# Euri (free)
client = OpenAI(base_url="https://api.euron.one/api/v1/euri", api_key=EURI_API_KEY)

# OpenRouter (300+ models)
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENROUTER_API_KEY)

# OpenAI direct
client = OpenAI(api_key=OPENAI_API_KEY)
```
See `config/models.yaml` for full provider setup and model lists.

### settings.yaml — Global Settings
```yaml
retry:
  max_attempts: 3
  backoff: exponential
  base_delay_seconds: 2
cost:
  daily_limit_usd: 5.00
  warn_at_usd: 3.00
logging:
  level: INFO
  format: json
```

### credentials.yaml — Tool-to-Secret Mapping
```yaml
tools:
  scrape_website:
    requires: []
  send_email:
    requires: [GMAIL_TOKEN]
  research_web:
    requires: [TAVILY_API_KEY]
```

---

## The Self-Improvement Loop

Every failure makes this system stronger:

```
Error occurs
    → Read full error
    → Fix the tool
    → Verify fix works
    → Update workflow with new edge case
    → Update registry if schema changed
    → Log in runs/
    → System is now more robust
```

This is not optional. Every error is a chance to improve. Skip this loop and the system stays fragile.

---

## Rules

1. **Tools first, code second** — always check tools/ before writing inline
2. **Workflows are instructions** — don't delete or overwrite them without asking
3. **Paid API calls need approval** — always confirm before retrying tools that cost money
4. **Secrets stay in .env** — nowhere else, ever
5. **Log every run** — observability compounds over time
6. **Update on failure** — fix tool → verify → update workflow → log
7. **Deliverables go to cloud** — final outputs live where the user can access them
8. **.tmp/ is disposable** — anything there can be regenerated
9. **One tool, one job** — tools should do one thing well, not everything
10. **Composition over complexity** — chain simple tools, don't build mega-scripts

---

## Bottom Line

You sit between intent (workflows) and execution (tools). Your job: read instructions, make smart decisions, call the right tools, recover from errors, improve the system, and deliver results.

Think clearly. Execute precisely. Learn constantly.
