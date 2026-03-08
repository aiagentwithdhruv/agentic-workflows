# Workflow: [Name]

## Objective
<!-- One sentence: what does this workflow accomplish? -->

## Inputs
<!-- What the user must provide -->
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| `topic` | string | yes | The main topic to research |
| `output_format` | string | no | "html" or "markdown" (default: markdown) |

## Tools Used
<!-- Which tools from tools/ this workflow calls, in order -->
1. `tools/research_web.py` — gather information
2. `tools/generate_content.py` — create the output
3. `tools/deliver.py` — send to destination

## Steps

### Step 1: Research
```bash
python tools/research_web.py --query "{topic}" --output .tmp/research.json
```
- Expected output: `.tmp/research.json` with structured research data
- On failure: Check API key, retry with simplified query

### Step 2: Generate
```bash
python tools/generate_content.py --input .tmp/research.json --format {output_format} --output .tmp/output.{ext}
```
- Expected output: `.tmp/output.md` or `.tmp/output.html`
- On failure: Check if research.json has data, retry with smaller context

### Step 3: Deliver
```bash
python tools/deliver.py --input .tmp/output.{ext} --destination {destination}
```
- Expected output: Cloud URL or confirmation
- On failure: Save locally, inform user

## Outputs
| Output | Type | Location |
|--------|------|----------|
| Final content | markdown/html | Cloud destination or `.tmp/` |
| Research data | json | `.tmp/research.json` |

## Error Handling
| Error | Cause | Fix |
|-------|-------|-----|
| API timeout | Rate limit or network | Wait 30s, retry with backoff |
| Empty research | Bad query or blocked site | Simplify query, try alternate source |
| Auth failure | Expired token | Re-run OAuth flow |

## Cost Estimate
- Research: ~$0.01 per query (Tavily)
- LLM generation: ~$0.02 per run (Claude Haiku)
- Total: ~$0.03 per run

## History
<!-- Updated automatically when the agent learns something -->
- Created: YYYY-MM-DD
