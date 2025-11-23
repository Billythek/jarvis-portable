"""
JARVIS Router - Central Agent Consultation System
==================================================

Router central pour consulter les agents experts JARVIS.
Gere le lazy loading, enrichissement contexte, et persistence.

Usage depuis Claude Code:
    from jarvis_router import consult_agent
    response = consult_agent("dataengineer", "How to optimize dbt pipeline?")

Author: JARVIS Portable System
Date: 2025-11-23
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "core"))
sys.path.insert(0, str(Path(__file__).parent / "agents"))

from core.brain import JARVISBrainV3SDK
from core.persistent_memory import PersistentMemory
from core.task_tracker import TaskTracker

# Agents
from agents.backend_expert_agent import BackendExpertAgent
from agents.data_engineer_agent import DataEngineerAgent
from agents.devops_sre_agent import DevOpsSREAgent
from agents.ai_engineer_agent import AIEngineerAgent


class JARVISRouter:
    """
    Router central pour consultation agents JARVIS

    Features:
    - Lazy loading agents (demarre seulement quand necessaire)
    - Enrichissement auto contexte via task_tracker
    - Persistence automatique dans SQLite
    - Interface simple pour Claude Code
    """

    _instance = None  # Singleton

    def __init__(self):
        """Initialise le router (lazy, agents pas encore charges)"""
        self.brain = None
        self.agents = {}
        self.initialized = False

        print("[JARVISRouter] Router created (agents not loaded yet)")

    def _ensure_initialized(self):
        """Initialise brain et memory si pas deja fait (lazy init)"""
        if self.initialized:
            return

        print("[JARVISRouter] Initializing brain and memory...")

        # Init brain
        self.brain = JARVISBrainV3SDK()

        # Init persistent memory
        self.brain.persistent_memory = PersistentMemory()

        # Init task tracker
        self.brain.task_tracker = TaskTracker(self.brain.persistent_memory)

        self.initialized = True
        print("[JARVISRouter] Initialization complete")

    def _load_agent(self, agent_name: str):
        """
        Charge un agent expert (lazy loading)

        Args:
            agent_name: dataengineer, backend, devops, ai

        Returns:
            Agent instance
        """
        # Normalize name
        agent_name = agent_name.lower().strip()

        # Check if already loaded
        if agent_name in self.agents:
            return self.agents[agent_name]

        self._ensure_initialized()

        print(f"[JARVISRouter] Loading agent: {agent_name}...")

        # Load agent based on name
        if agent_name in ["dataengineer", "data", "data_engineer"]:
            agent = DataEngineerAgent("DataEngineer", brain=self.brain)
        elif agent_name in ["backend", "backendexpert", "backend_expert"]:
            agent = BackendExpertAgent("BackendExpert", brain=self.brain)
        elif agent_name in ["devops", "sre", "devops_sre"]:
            agent = DevOpsSREAgent("DevOpsSRE", brain=self.brain)
        elif agent_name in ["ai", "aiengineer", "ai_engineer", "llm"]:
            agent = AIEngineerAgent("AIEngineer", brain=self.brain)
        else:
            raise ValueError(
                f"Unknown agent: {agent_name}. "
                f"Available: dataengineer, backend, devops, ai"
            )

        # Start agent
        asyncio.run(agent.start())

        # Cache
        self.agents[agent_name] = agent

        print(f"[JARVISRouter] Agent {agent_name} loaded and started")

        return agent

    async def consult_async(self, agent_name: str, query: str,
                          task_type: Optional[str] = None) -> str:
        """
        Consulte un agent expert (async)

        Args:
            agent_name: dataengineer, backend, devops, ai
            query: Question a poser
            task_type: Type de tache (audit, optimization, design, etc)

        Returns:
            Reponse de l'agent avec contexte enrichi
        """
        # Load agent
        agent = self._load_agent(agent_name)

        print(f"\n[JARVISRouter] Consulting {agent_name}...")
        print(f"[Query] {query}")

        # Get context automatique
        context = self.brain.task_tracker.get_context(agent.name, query)

        if context and "[Pas de contexte" not in context:
            print(f"\n[Context Retrieved]")
            print(context[:300] + "..." if len(context) > 300 else context)

        # Enrich query with context
        enriched_query = f"""
{context}

==================
NOUVELLE REQUETE:
{query}
==================

Reponds en tenant compte du contexte ci-dessus si pertinent.
"""

        # Consult agent
        response = await agent.consult(enriched_query)

        # Log task
        if task_type is None:
            # Auto-detect task type from query
            task_type = self._detect_task_type(query)

        self.brain.task_tracker.log_task(
            agent_name=agent.name,
            task_type=task_type,
            description=query[:200],
            result=response[:500],
            status="completed"
        )

        print(f"\n[JARVISRouter] Consultation saved to database")

        return response

    def consult(self, agent_name: str, query: str,
               task_type: Optional[str] = None) -> str:
        """
        Consulte un agent expert (synchrone - wrapper pour Claude Code)

        Args:
            agent_name: dataengineer, backend, devops, ai
            query: Question a poser
            task_type: Type de tache (optionnel)

        Returns:
            Reponse de l'agent
        """
        # Run async in sync context
        return asyncio.run(self.consult_async(agent_name, query, task_type))

    def _detect_task_type(self, query: str) -> str:
        """Auto-detect task type from query keywords"""
        query_lower = query.lower()

        if any(word in query_lower for word in ["audit", "check", "review", "analyze"]):
            return "audit"
        elif any(word in query_lower for word in ["optimize", "improve", "faster", "performance"]):
            return "optimization"
        elif any(word in query_lower for word in ["design", "architecture", "create", "build"]):
            return "design"
        elif any(word in query_lower for word in ["debug", "fix", "error", "issue", "problem"]):
            return "debugging"
        elif any(word in query_lower for word in ["how to", "explain", "what is"]):
            return "consultation"
        else:
            return "general"

    def get_history(self, agent_name: Optional[str] = None, days: int = 7) -> list:
        """
        Recupere historique consultations

        Args:
            agent_name: Filtrer par agent (None = tous)
            days: Derniers X jours

        Returns:
            Liste de consultations
        """
        self._ensure_initialized()

        if agent_name:
            # Normalize and get real agent name
            agent = self._load_agent(agent_name)
            agent_name = agent.name

        return self.brain.persistent_memory.recall_consultations(
            agent_name=agent_name,
            days=days,
            limit=20
        )

    def get_stats(self) -> dict:
        """Retourne stats memoire"""
        self._ensure_initialized()
        return self.brain.persistent_memory.get_stats()

    @classmethod
    def get_instance(cls):
        """Get singleton instance"""
        if cls._instance is None:
            cls._instance = JARVISRouter()
        return cls._instance


# Global singleton instance
_router = None


def consult_agent(agent_name: str, query: str, task_type: Optional[str] = None) -> str:
    """
    Fonction helper pour consulter un agent JARVIS

    Args:
        agent_name: dataengineer, backend, devops, ai
        query: Question a poser
        task_type: Type de tache (optionnel)

    Returns:
        Reponse de l'agent

    Example:
        >>> response = consult_agent("dataengineer", "How to optimize dbt pipeline?")
        >>> print(response)
    """
    global _router

    if _router is None:
        _router = JARVISRouter.get_instance()

    return _router.consult(agent_name, query, task_type)


def get_agent_history(agent_name: Optional[str] = None, days: int = 7) -> list:
    """
    Recupere historique consultations

    Args:
        agent_name: Agent specifique (ou None pour tous)
        days: Derniers X jours

    Returns:
        Liste consultations

    Example:
        >>> history = get_agent_history("dataengineer", days=14)
        >>> for h in history:
        >>>     print(f"{h['timestamp']}: {h['query']}")
    """
    global _router

    if _router is None:
        _router = JARVISRouter.get_instance()

    return _router.get_history(agent_name, days)


def get_memory_stats() -> dict:
    """
    Retourne statistiques memoire JARVIS

    Returns:
        {consultations_count, tasks_count, agents, last_activity}

    Example:
        >>> stats = get_memory_stats()
        >>> print(f"Total memories: {stats['total_memories']}")
    """
    global _router

    if _router is None:
        _router = JARVISRouter.get_instance()

    return _router.get_stats()


# CLI pour tests
if __name__ == "__main__":
    print("=" * 70)
    print("JARVIS ROUTER - TEST CLI")
    print("=" * 70)
    print()

    print("[TEST 1] Consulting DataEngineer...")
    response1 = consult_agent(
        "dataengineer",
        "How should I structure my dbt project for optimal performance?"
    )
    print(f"\n[Response Preview]:\n{response1[:300]}...\n")

    print("=" * 70)

    print("[TEST 2] Consulting BackendExpert...")
    response2 = consult_agent(
        "backend",
        "What's the best way to optimize FastAPI for 50K requests per second?"
    )
    print(f"\n[Response Preview]:\n{response2[:300]}...\n")

    print("=" * 70)

    print("[TEST 3] Getting consultation history...")
    history = get_agent_history(days=1)
    print(f"\nFound {len(history)} consultations:")
    for h in history:
        print(f"  - {h['agent']}: {h['query'][:60]}...")

    print("\n" + "=" * 70)

    print("[TEST 4] Memory stats...")
    stats = get_memory_stats()
    print(f"  Total memories: {stats['total_memories']}")
    print(f"  Consultations: {stats['consultations_count']}")
    print(f"  Agents: {', '.join(stats['agents'])}")

    print("\n" + "=" * 70)
    print("ALL TESTS COMPLETE")
    print("=" * 70)
