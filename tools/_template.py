#!/usr/bin/env python3
"""
Tool: [name]
Description: [one line — what this tool does]
Inputs: [list key inputs]
Outputs: [what it returns/writes]
"""

import argparse
import json
import sys
import os

# Add shared utilities to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from shared.env_loader import load_env
from shared.logger import get_logger

logger = get_logger(__name__)


def main(args):
    """Main execution logic."""
    logger.info(f"Starting [tool_name]", extra={"inputs": vars(args)})

    try:
        # --- YOUR LOGIC HERE ---
        result = {"status": "success", "message": "Tool executed"}
        # --- END LOGIC ---

        # Write output
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            logger.info(f"Output written to {args.output}")
        else:
            print(json.dumps(result, indent=2))

        return result

    except Exception as e:
        logger.error(f"Tool failed: {e}", exc_info=True)
        error_result = {"status": "error", "error": str(e)}
        print(json.dumps(error_result), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    load_env()

    parser = argparse.ArgumentParser(description="[Tool description]")
    parser.add_argument("--input", help="Input file path or value")
    parser.add_argument("--output", help="Output file path (default: stdout)")
    # Add tool-specific arguments here

    args = parser.parse_args()
    main(args)
