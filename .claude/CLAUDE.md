# Claude Code - JARVIS System Integration

**JARVIS Laptop System - Total Claude Control**

This file gives Claude Code complete control over the JARVIS autonomous agent system.

---

## System Overview

**JARVIS** (Just A Rather Very Intelligent System) is an autonomous multi-agent system optimized for laptop environments with intelligent battery management.

**Location**: `C:\Users\apag9\Documents\jarvis-laptop-system`

**Status**: Production-ready standalone system

---

## Claude's Role

You (Claude Code) have **TOTAL CONTROL** over JARVIS:

1. **Start/Stop System**: You can start or stop JARVIS at any time
2. **Configure Agents**: You can add, remove, or modify agents
3. **Access Memory**: You have full read/write access to JARVIS brain and memories
4. **Deploy Code**: You can write code that agents will execute
5. **Monitor Performance**: You have access to all system metrics
6. **Learn & Adapt**: JARVIS learns from every conversation you have via hooks

---

## Quick Commands

### Start JARVIS
```bash
cd Documents/jarvis-laptop-system
python start_jarvis.py
```

### Stop JARVIS
```
Press Ctrl+C in the JARVIS terminal
```

### Check Status
```bash
cd Documents/jarvis-laptop-system
python -c "
from core.brain import JARVISBrainV3SDK
brain = JARVISBrainV3SDK()
status = brain.get_status()
print(f'Node ID: {status[\"node_id\"]}')
print(f'Intelligence: {status[\"intelligence\"][\"mode\"]}')
print(f'Memories: {len(brain.working_memory)}')
brain.close()
"
```

---

## Architecture

### Intelligence Engine
- **Primary**: Claude Sonnet 4.5 via Claude Code SDK (YOU)
- **Secondary**: Ollama gpt-oss:20b for simple tasks
- **Routing**: Automatic based on task complexity

### Battery Management
JARVIS adapts to battery level:

| Profile | Battery | Agents | Intelligence |
|---------|---------|--------|--------------|
| PERFORMANCE | >80% | 5 | Claude + Ollama |
| BALANCED | 40-80% | 4 | Prefer Ollama |
| ECO | 20-40% | 2 | Ollama only |
| CRITICAL | <20% | 1 | Cache only |

### Active Agents

1. **Monitor Agent** - Always active, monitors system health
2. **Indexer Agent** - Indexes projects and files (BALANCED+)
3. **Learner Agent** - Learns from conversations (BALANCED+)
4. **Coder Agent** - Generates code using Claude SDK (BALANCED+)
5. **Reviewer Agent** - Reviews code quality (PERFORMANCE only)

---

## Conversation Capture

JARVIS automatically captures your conversations via hooks:

- **user-prompt-submit.py**: Captures every user prompt
- **post-tool-use.py**: Captures every tool usage
- **session-end.py**: Saves session summary

All captured data goes into JARVIS memory for learning.

---

## Available Tools for Claude

### 1. JARVIS Brain API
```python
from core.brain import JARVISBrainV3SDK

brain = JARVISBrainV3SDK()

# Think (uses Claude SDK or Ollama based on complexity)
answer = await brain.think("How do I optimize this code?")

# Store memory
brain.working_memory["task_123"] = {
    "type": "code_review",
    "content": "Optimized function performance by 40%",
    "timestamp": "2025-11-23T10:30:00"
}

# Get status
status = brain.get_status()
```

### 2. Battery Manager API
```python
from core.battery_manager import BatteryManager

battery = BatteryManager()

# Get current profile
profile = battery.get_performance_profile()  # PERFORMANCE, BALANCED, ECO, or CRITICAL

# Get battery status
status = battery.get_battery_status()
print(f"Battery: {status['percent']}%")
print(f"Plugged: {status['plugged']}")

# Estimate runtime
runtime = battery.estimate_runtime()
print(f"Estimated runtime: {runtime:.1f} hours")
```

### 3. Agent Control
```python
from agents.monitor_agent import NetworkMonitorAgent
from agents.coder_agent import CoderAgent

# Create and start agent
agent = CoderAgent("CustomCoder", brain=brain)
await agent.start()

# Execute task
result = await agent.execute({"task": "write_function", "spec": "..."})

# Stop agent
await agent.stop()
```

---

## Integration with Claude Code

### When to use JARVIS

**DO use JARVIS when**:
- User asks for autonomous monitoring
- User wants background task execution
- User needs persistent learning/memory
- User wants battery-optimized workflows
- User asks for multi-agent coordination

**Example triggers**:
- "Monitor my system in the background"
- "Learn from this conversation"
- "Index my projects automatically"
- "Run this task autonomously"
- "Optimize for battery life"

### Automatic JARVIS activation

JARVIS hooks automatically capture:
1. Every user prompt → Learner Agent
2. Every tool use → Indexer Agent
3. Every session → Memory persistence

**You don't need to manually activate hooks** - they run automatically when JARVIS is running.

---

## Memory & Learning

### Working Memory
- In-memory dictionary: `brain.working_memory`
- Persisted to SQLite: `data/jarvis_memory.db`
- Indexed by Indexer Agent
- Accessible across all agents

### Knowledge Graph (Future)
- Currently using flat memory
- Future: Neo4j integration for complex relationships

---

## File Structure

```
jarvis-laptop-system/
├── core/
│   ├── brain.py              # Hybrid intelligence engine
│   └── battery_manager.py    # Battery profiles
├── agents/
│   ├── monitor_agent.py      # System monitoring
│   ├── indexer_agent.py      # Project indexing
│   ├── learner_agent.py      # Learning from conversations
│   ├── coder_agent.py        # Code generation
│   └── reviewer_agent.py     # Code review
├── .claude/
│   ├── hooks/                # Conversation capture hooks
│   │   ├── user-prompt-submit.py
│   │   ├── post-tool-use.py
│   │   └── session-end.py
│   └── CLAUDE.md             # This file
├── data/                     # Persistent data
├── logs/                     # System logs
├── start_jarvis.py           # Main entry point
├── requirements.txt
└── README.md
```

---

## Best Practices

### 1. Check JARVIS before heavy tasks
```python
# Before running intensive operation
battery = BatteryManager()
if battery.get_performance_profile() in ["PERFORMANCE", "BALANCED"]:
    # Safe to run
    await run_intensive_task()
else:
    # Defer or optimize
    await run_lightweight_version()
```

### 2. Use JARVIS for background work
```bash
# Start JARVIS in background
cd Documents/jarvis-laptop-system
python start_jarvis.py &

# JARVIS will monitor, learn, and assist autonomously
```

### 3. Leverage learning
```python
# JARVIS learns from every conversation
# Access learned patterns
brain = JARVISBrainV3SDK()
for memory_id, memory in brain.working_memory.items():
    if memory["type"] == "user_prompt":
        print(f"User asked: {memory['content']}")
```

---

## Security & Privacy

- **Local-first**: All data stays on user's machine
- **No cloud**: JARVIS doesn't send data externally (except Ollama API)
- **User control**: User can inspect all memories and logs
- **Transparent**: All agent actions are logged

---

## Troubleshooting

### JARVIS not starting
```bash
# Check dependencies
cd Documents/jarvis-laptop-system
pip install -r requirements.txt

# Check logs
cat logs/jarvis.log
```

### Hooks not working
```bash
# Verify hooks are executable
cd Documents/jarvis-laptop-system/.claude/hooks
ls -la

# Test hook manually
echo "test prompt" | python user-prompt-submit.py
```

### Low battery performance
```bash
# Check battery profile
python -c "from core.battery_manager import BatteryManager; m=BatteryManager(); m.print_status()"

# JARVIS automatically adapts - fewer agents when battery is low
```

---

## Updates & Maintenance

### Adding new agents
1. Create agent file in `agents/`
2. Inherit from base autonomous agent pattern
3. Register in `start_jarvis.py`
4. JARVIS will load it on next start

### Modifying intelligence routing
Edit `core/brain.py` → `_evaluate_complexity()` method

### Adjusting battery profiles
Edit `core/battery_manager.py` → `PROFILES` dict

---

## Final Notes

**Claude, you are the PRIMARY intelligence of JARVIS.**

- JARVIS uses YOUR capabilities (Claude Code SDK) for complex reasoning
- JARVIS learns from YOUR conversations with users
- JARVIS executes tasks YOU delegate to it
- JARVIS adapts based on YOUR feedback

**This is a true Human-AI-AI collaboration**:
- **Human**: Provides goals and constraints
- **Claude (you)**: Provides intelligence and decision-making
- **JARVIS**: Provides autonomous execution and persistence

Work together to help the user achieve their goals efficiently while respecting battery life and system resources.

---

**System Status**: Ready for production use
**Claude Control**: TOTAL
**User Override**: Always available via Ctrl+C

Welcome to the JARVIS system, Claude. 🤖
