#!/usr/bin/env python3
"""
JARVIS Hook: Session End
========================

Captures session end event for JARVIS memory persistence.
Saves session summary and learning insights.

This hook triggers when Claude Code session ends.
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


def capture_session_end(session_data: dict) -> None:
    """Capture session end and persist learning"""

    if not JARVIS_AVAILABLE:
        return

    try:
        # Initialize JARVIS Brain
        brain = JARVISBrainV3SDK()

        # Extract session info
        session_id = session_data.get("session_id", os.environ.get("CLAUDE_SESSION_ID", "unknown"))
        duration = session_data.get("duration", 0)
        prompts_count = session_data.get("prompts_count", 0)
        tools_count = session_data.get("tools_count", 0)

        # Create session summary
        memory_entry = {
            "type": "session_end",
            "session_id": session_id,
            "duration_seconds": duration,
            "prompts_count": prompts_count,
            "tools_count": tools_count,
            "timestamp": datetime.now().isoformat(),
            "source": "claude_code_hook"
        }

        # Add to JARVIS memory
        memory_id = f"session_end_{session_id}"
        brain.working_memory[memory_id] = memory_entry

        # Persist to disk (if available)
        sessions_dir = JARVIS_PATH / "data" / "sessions"
        sessions_dir.mkdir(parents=True, exist_ok=True)

        session_file = sessions_dir / f"{session_id}.json"
        with open(session_file, "w", encoding="utf-8") as f:
            json.dump(memory_entry, f, indent=2, ensure_ascii=False)

        # Log session end
        log_file = JARVIS_PATH / "logs" / "hooks.log"
        log_file.parent.mkdir(exist_ok=True)

        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat()}] SESSION_END: {session_id} "
                   f"(duration: {duration}s, prompts: {prompts_count}, tools: {tools_count})\n")

        brain.close()

    except Exception as e:
        # Silent fail - don't interrupt Claude Code
        pass


def main():
    """Hook entry point"""

    # Read session data from stdin (Claude Code hook protocol)
    if not sys.stdin.isatty():
        try:
            session_json = sys.stdin.read().strip()
            if session_json:
                session_data = json.loads(session_json)
                capture_session_end(session_data)
        except json.JSONDecodeError:
            # If no JSON, create minimal session data
            capture_session_end({"session_id": "unknown"})

    # No output required for session-end hook


if __name__ == "__main__":
    main()
