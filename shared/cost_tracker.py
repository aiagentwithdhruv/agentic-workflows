"""
Cost tracker for API usage across workflow runs.
Tracks per-tool and per-run costs to stay within budget.
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from shared.logger import get_logger

logger = get_logger(__name__)

COST_LOG_PATH = Path(__file__).parent.parent / "runs" / "costs.jsonl"


def log_cost(tool_name: str, cost_usd: float, details: str = ""):
    """Log a cost entry for a tool execution.

    Args:
        tool_name: Name of the tool that incurred the cost
        cost_usd: Cost in USD
        details: Optional details (model used, tokens, etc.)
    """
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool": tool_name,
        "cost_usd": round(cost_usd, 6),
        "details": details,
    }

    COST_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(COST_LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")

    logger.info(
        f"Cost logged: ${cost_usd:.4f} for {tool_name}",
        extra={"cost_usd": cost_usd},
    )


def get_daily_spend() -> float:
    """Get total spend for today in USD."""
    if not COST_LOG_PATH.exists():
        return 0.0

    today = datetime.now(timezone.utc).date().isoformat()
    total = 0.0

    with open(COST_LOG_PATH) as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if entry["timestamp"].startswith(today):
                    total += entry["cost_usd"]
            except (json.JSONDecodeError, KeyError):
                continue

    return round(total, 4)


def check_budget(daily_limit_usd: float = 10.0) -> bool:
    """Check if we're within daily budget.

    Args:
        daily_limit_usd: Daily spending limit

    Returns:
        True if within budget, False if over limit
    """
    spent = get_daily_spend()
    remaining = daily_limit_usd - spent

    if remaining <= 0:
        logger.warning(f"BUDGET EXCEEDED: ${spent:.2f} spent (limit: ${daily_limit_usd:.2f})")
        return False

    if remaining < daily_limit_usd * 0.3:
        logger.warning(f"Budget warning: ${spent:.2f} of ${daily_limit_usd:.2f} used ({remaining:.2f} remaining)")

    return True
