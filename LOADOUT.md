# Agentic Workflows Engine

## What This Is
A code-first agent workflow engine using the WAT pattern (Workflows, Agents, Tools). Separates AI reasoning from deterministic execution for reliable, self-improving automation pipelines.

Copy this into any project. Add your workflows. Add your tools. The agent handles the rest.

## Architecture
```
Agent (LLM) ←→ Workflows (markdown SOPs) ←→ Tools (Python scripts)
```

- **Agent** reads workflow, picks tools, executes, observes, self-corrects
- **Workflows** define what to do (markdown with typed inputs/outputs/steps)
- **Tools** execute deterministically (Python scripts with schemas)
- **Shared utilities** provide logging, retry, cost tracking, env loading

## Key Files
| File | Purpose |
|------|---------|
| `CLAUDE.md` | Agent instructions (how to operate) |
| `config/models.yaml` | LLM routing (which model for which task) |
| `config/settings.yaml` | Global settings (retries, cost limits) |
| `config/credentials.yaml` | Tool → env var mapping |
| `workflows/_template.md` | Template for new workflows |
| `tools/_template.py` | Template for new tools |
| `tools/registry.yaml` | Tool registry with schemas |
| `shared/` | Logger, retry, cost tracker, env loader |

## How to Use
1. Copy this folder into your project (or use as standalone)
2. Copy `.env.example` → `.env`, fill in API keys
3. Open in Claude Code / Cursor / any AI-powered editor
4. Ask the agent: "Run workflow X" or "Build me a workflow for Y"
5. Agent reads CLAUDE.md → checks workflows/ → picks tools/ → executes → logs run

## Per-Project Usage
```bash
# Copy into a new project
cp -r agentic-workflows/ my-project/agentic-workflows/

# Or use as the project root
cp -r agentic-workflows/ my-new-automation/
```

Then add project-specific workflows and tools. The framework stays the same.

## Refresh Cadence
- **Config:** Update when adding new LLM providers or changing cost limits
- **Registry:** Auto-updated when agent creates new tools
- **Workflows:** Updated by agent when it learns from failures
