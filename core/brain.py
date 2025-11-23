#!/usr/bin/env python3
"""
JARVIS BRAIN V3 SDK - Intelligence Hybride avec Claude Code SDK
================================================================

Version optimisée utilisant:
- Claude Code SDK (abonnement Max) au lieu d'API Anthropic
- Ollama gpt-oss:20b pour validation et tâches simples

Author: JARVIS System V3 SDK
Date: 2025-11-23
Version: 3.1.0 - SDK DIRECT
"""

import os
import sys
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import uuid
import json
import warnings

warnings.filterwarnings('ignore')

# Claude Code SDK (direct - utilise ton abonnement Max)
try:
    from claude_code_sdk import query, ClaudeCodeOptions
    CLAUDE_SDK_AVAILABLE = True
except ImportError:
    print("[WARN] Claude Code SDK not available. Run: pip install -e ../claude-code-sdk-python")
    CLAUDE_SDK_AVAILABLE = False

# Import mémoire et personnalité
sys.path.insert(0, str(Path(__file__).parent / "langchain_integration"))
try:
    from jarvis_unified_memory_v2 import JARVISUnifiedMemory
    MEMORY_AVAILABLE = True
except:
    MEMORY_AVAILABLE = False

try:
    from JARVIS_PERSONALITY import PERSONALITY_CONFIG, get_address_form
    from response_formatter import JarvisResponseFormatter
    PERSONALITY_AVAILABLE = True
except:
    PERSONALITY_AVAILABLE = False


class JARVISBrainV3SDK:
    """
    JARVIS Brain V3 avec Claude Code SDK Direct

    Utilise ton abonnement Claude Max via SDK
    + Ollama pour critique et tâches simples
    """

    def __init__(self):
        self.name = "JARVIS"
        self.version = "3.1.0-SDK"
        self.initialized_at = datetime.now()
        self.node_id = str(uuid.uuid4())[:8]

        print("\n" + "="*70)
        print(f"  {self.name} BRAIN v{self.version} - SDK DIRECT")
        print("="*70 + "\n")

        # === INTELLIGENCE ===
        print("[1/3] Intelligence: Claude Code SDK...")
        if CLAUDE_SDK_AVAILABLE:
            self.claude_sdk_available = True
            print("  [OK] Claude Code SDK Ready (using your Max subscription)")
        else:
            self.claude_sdk_available = False
            print("  [WARN] Claude Code SDK not available")

        # === OLLAMA ===
        print("\n[2/3] Intelligence: Ollama Cloud...")
        self.ollama_url = os.getenv("OLLAMA_URL", "https://ollama.com/api")
        self.ollama_key = os.getenv("OLLAMA_API_KEY")

        if self.ollama_key:
            self.ollama_available = True
            print(f"  [OK] Ollama Ready: {self.ollama_url}")
        else:
            self.ollama_available = False
            print("  [WARN] Ollama API key not configured")

        # === MÉMOIRE ===
        print("\n[3/3] Memory System...")
        if MEMORY_AVAILABLE:
            try:
                self.memory = JARVISUnifiedMemory()
                print("  [OK] Unified Memory: Operational")
            except:
                self.memory = None
                print("  [WARN] Memory: Using fallback (RAM only)")
        else:
            self.memory = None
            print("  [WARN] Memory: Using fallback (RAM only)")

        # Fallback memory
        self.working_memory = {}

        # === PERSONNALITÉ ===
        if PERSONALITY_AVAILABLE:
            try:
                self.formatter = JarvisResponseFormatter()
                print("  [OK] Personality: JARVIS Iron Man style")
            except:
                self.formatter = None
        else:
            self.formatter = None

        print("\n" + "="*70)
        print(f"  {self.name} V3 SDK - OPERATIONAL (Node: {self.node_id})")
        mode = "HYBRID" if (self.claude_sdk_available and self.ollama_available) else "LIMITED"
        print(f"  Intelligence: {mode}")
        print("="*70 + "\n")

    async def think(self, prompt: str, context: Optional[List[Dict]] = None) -> str:
        """
        Raisonnement hybride SDK

        Flow:
        1. Évalue complexité
        2. Route vers Claude SDK (complexe) OU Ollama (simple)
        3. Retourne réponse
        """

        print(f"\n[THINK SDK] {prompt[:60]}...")

        # Évaluation complexité
        complexity = self._evaluate_complexity(prompt)
        print(f"  [COMPLEXITY] Score: {complexity}/10")

        # Routage
        if complexity >= 7 and self.claude_sdk_available:
            print(f"  [ROUTE] Claude Code SDK (complex task)")
            response = await self._think_with_claude_sdk(prompt, context)
        elif self.ollama_available:
            print(f"  [ROUTE] Ollama gpt-oss:20b (simple task)")
            response = await self._think_with_ollama(prompt, context)
        else:
            print(f"  [ROUTE] Local mode (no API)")
            response = self._think_local(prompt, context)

        return response

    def _evaluate_complexity(self, prompt: str) -> int:
        """Évalue complexité 0-10"""
        score = 5
        prompt_lower = prompt.lower()

        # Longueur
        if len(prompt) > 200: score += 1
        if len(prompt) > 500: score += 1

        # Mots-clés complexes
        complex_kw = ['pourquoi', 'why', 'comment', 'how', 'analyse', 'architecture', 'implement', 'explain']
        score += min(sum(1 for kw in complex_kw if kw in prompt_lower), 3)

        # Questions simples (diminue score)
        simple_kw = ['bonjour', 'hello', 'what is', 'qui est']
        if any(kw in prompt_lower for kw in simple_kw):
            score -= 2

        return max(0, min(10, score))

    async def _think_with_claude_sdk(self, prompt: str, context: Optional[List[Dict]]) -> str:
        """
        Utilise Claude Code SDK (ton abonnement Max)
        """

        # Build context
        context_text = ""
        if context:
            context_text = "\n**Context:**\n" + "\n".join([
                f"- {c.get('content', '')[:150]}" for c in context[:3]
            ])

        full_prompt = f"""{context_text}

**Question:** {prompt}

Respond as JARVIS (Iron Man's AI): professional, concise, actionable."""

        try:
            # Utilise SDK directement (ton abonnement Max)
            messages = []

            async for msg in query(
                prompt=full_prompt,
                options=ClaudeCodeOptions(
                    max_thinking_tokens=5000
                )
            ):
                if hasattr(msg, 'content'):
                    messages.append(str(msg.content))

            return '\n'.join(messages) if messages else "No response from Claude SDK"

        except Exception as e:
            print(f"  [ERROR] Claude SDK: {e}")
            # Fallback Ollama
            if self.ollama_available:
                return await self._think_with_ollama(prompt, context)
            return self._think_local(prompt, context)

    async def _think_with_ollama(self, prompt: str, context: Optional[List[Dict]]) -> str:
        """Utilise Ollama gpt-oss:20b"""

        context_text = ""
        if context:
            items = [c.get('content', '')[:100] for c in context[:3]]
            context_text = " | ".join(items)

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.ollama_url}/chat",
                    headers={"Authorization": f"Bearer {self.ollama_key}"},
                    json={
                        "model": "gpt-oss:20b",
                        "messages": [
                            {"role": "system", "content": "You are JARVIS, Iron Man's AI. Be professional and concise."},
                            {"role": "user", "content": f"Context: {context_text}\n\nQuestion: {prompt}"}
                        ],
                        "stream": False
                    },
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    data = await resp.json()
                    return data['message']['content']

        except Exception as e:
            print(f"  [ERROR] Ollama: {e}")
            return self._think_local(prompt, context)

    def _think_local(self, prompt: str, context: Optional[List[Dict]]) -> str:
        """Fallback local"""
        return f"**Question:** {prompt}\n\n**Status:** Limited mode (no API available)\n**Suggestion:** Configure Claude Code SDK or Ollama API"

    def ask(self, question: str) -> str:
        """API synchrone"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        answer = loop.run_until_complete(self.think(question))

        # Applique personnalité si dispo
        if self.formatter:
            try:
                answer = self.formatter.format_response(answer, situation_type='normal')
            except:
                pass

        return answer

    def remember(self, content: str, importance: str = "normal", metadata: Optional[Dict] = None) -> str:
        """Stocke une mémoire"""
        memory_id = str(uuid.uuid4())

        if self.memory:
            try:
                return self.memory.remember(content, importance, metadata or {})
            except:
                pass

        # Fallback RAM
        self.working_memory[memory_id] = {
            "content": content,
            "importance": importance,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }

        return memory_id

    def recall(self, query: str, limit: int = 5) -> List[Dict]:
        """Récupère mémoires"""
        if self.memory:
            try:
                return self.memory.recall(query, limit)
            except:
                pass

        # Fallback RAM
        results = []
        for mem_id, mem in self.working_memory.items():
            if query.lower() in mem['content'].lower():
                results.append({**mem, "id": mem_id, "score": 1.0})

        return results[:limit]

    def get_status(self) -> Dict:
        """Status système"""
        return {
            "name": self.name,
            "version": self.version,
            "node_id": self.node_id,
            "initialized_at": self.initialized_at.isoformat(),
            "uptime_seconds": (datetime.now() - self.initialized_at).total_seconds(),
            "intelligence": {
                "claude_code_sdk": self.claude_sdk_available,
                "ollama_gpt_oss_20b": self.ollama_available,
                "mode": "hybrid" if (self.claude_sdk_available and self.ollama_available) else "limited"
            },
            "memory": {
                "unified": self.memory is not None,
                "working_memory_size": len(self.working_memory)
            }
        }

    def close(self):
        """Cleanup"""
        print(f"\n[SHUTDOWN] {self.name} V3 SDK closed")


# ============================================================================
# DEMO
# ============================================================================

async def demo():
    """Demo JARVIS Brain V3 SDK"""

    print("\n" + "="*70)
    print("  JARVIS BRAIN V3 SDK - DEMO")
    print("="*70 + "\n")

    brain = JARVISBrainV3SDK()

    # Test 1: Simple
    print("\n[TEST 1] Simple Question")
    answer1 = await brain.think("What is 2 + 2?")
    print(f"Answer: {answer1[:200]}\n")

    # Test 2: Complex
    print("[TEST 2] Complex Question")
    answer2 = await brain.think("Explain quantum computing")
    print(f"Answer: {answer2[:300]}\n")

    # Status
    print("[STATUS]")
    status = brain.get_status()
    print(f"Node: {status['node_id']}")
    print(f"Intelligence: {status['intelligence']['mode']}")
    print(f"Claude SDK: {status['intelligence']['claude_code_sdk']}")
    print(f"Ollama: {status['intelligence']['ollama_gpt_oss_20b']}")

    brain.close()


if __name__ == "__main__":
    asyncio.run(demo())
