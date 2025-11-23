#!/usr/bin/env python3
"""
JARVIS Hook: Post Tool Use
==========================

Captures Claude Code tool usage for JARVIS learning.
Tracks what tools are used, parameters, and results.

This hook triggers after Claude Code executes any tool.
"""

import sys
import os
import json
from datetime import datetime
from pathlib import Path

# Add JARVIS to path
JARVIS_PATH = Path(__file__).parent.parent.parent
sys.path.insert(0, str(JARVIS_PATH / "core"))

try:
    from brain import JARVISBrainV3SDK
    JARVIS_AVAILABLE = True
except ImportError:
    JARVIS_AVAILABLE = False


def capture_tool_use(tool_data: dict) -> None:
    """Capture tool usage and send to JARVIS for learning"""

    if not JARVIS_AVAILABLE:
        return

    try:
        # Initialize JARVIS Brain
        brain = JARVISBrainV3SDK()

        # Extract tool info
        tool_name = tool_data.get("tool_name", "unknown")
        tool_params = tool_data.get("parameters", {})
        tool_result = tool_data.get("result", {})
        success = tool_data.get("success", False)

        # Store tool usage in working memory
        memory_entry = {
            "type": "tool_usage",
            "tool_name": tool_name,
            "parameters": tool_params,
            "success": success,
            "timestamp": datetime.now().isoformat(),
            "source": "claude_code_hook",
            "session_id": os.environ.get("CLAUDE_SESSION_ID", "unknown")
        }

        # Add result summary if available
        if tool_result:
            result_str = str(tool_result)
            memory_entry["result_summary"] = result_str[:500]  # First 500 chars

        # Add to JARVIS memory
        memory_id = f"tool_use_{tool_name}_{datetime.now().timestamp()}"
        brain.working_memory[memory_id] = memory_entry

        # Log capture
        log_file = JARVIS_PATH / "logs" / "hooks.log"
        log_file.parent.mkdir(exist_ok=True)

        with open(log_file, "a", encoding="utf-8") as f:
            status = "SUCCESS" if success else "FAILED"
            f.write(f"[{datetime.now().isoformat()}] TOOL_USE [{status}]: {tool_name}\n")

        brain.close()

    except Exception as e:
        # Silent fail - don't interrupt Claude Code
        pass


def main():
    """Hook entry point"""

    # Read tool data from stdin (Claude Code hook protocol)
    if not sys.stdin.isatty():
        try:
            tool_json = sys.stdin.read().strip()
            if tool_json:
                tool_data = json.loads(tool_json)
                capture_tool_use(tool_data)
        except json.JSONDecodeError:
            pass

    # No output required for post-tool-use hook


if __name__ == "__main__":
    main()
