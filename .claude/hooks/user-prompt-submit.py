#!/usr/bin/env python3
"""
JARVIS Hook: User Prompt Submit
================================

Captures user prompts for JARVIS learning and memory indexing.
Automatically sends prompts to JARVIS Brain for context building.

This hook triggers when the user submits a prompt to Claude Code.
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


def capture_user_prompt(prompt: str) -> None:
    """Capture user prompt and send to JARVIS for learning"""

    if not JARVIS_AVAILABLE:
        return

    try:
        # Initialize JARVIS Brain
        brain = JARVISBrainV3SDK()

        # Store user prompt in working memory
        memory_entry = {
            "type": "user_prompt",
            "content": prompt,
            "timestamp": datetime.now().isoformat(),
            "source": "claude_code_hook",
            "session_id": os.environ.get("CLAUDE_SESSION_ID", "unknown")
        }

        # Add to JARVIS memory
        memory_id = f"user_prompt_{datetime.now().timestamp()}"
        brain.working_memory[memory_id] = memory_entry

        # Log capture
        log_file = JARVIS_PATH / "logs" / "hooks.log"
        log_file.parent.mkdir(exist_ok=True)

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] USER_PROMPT captured: {prompt[:100]}...\n")

        brain.close()

    except Exception as e:
        # Silent fail - don't interrupt Claude Code
        pass


def main():
    """Hook entry point"""

    # Read prompt from stdin (Claude Code hook protocol)
    if not sys.stdin.isatty():
        prompt = sys.stdin.read().strip()
        if prompt:
            capture_user_prompt(prompt)

    # Echo prompt back (required by hook protocol)
    if len(sys.argv) > 1:
        print(sys.argv[1])


if __name__ == "__main__":
    main()
