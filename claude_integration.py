"""
JARVIS Claude Code Integration - Helper for Claude Code Sessions
=================================================================

Interface simple pour consulter les agents JARVIS depuis Claude Code.

Usage from Claude Code:
    from claude_integration import jarvis

    # Consult an expert
    response = jarvis("dataengineer", "How to optimize my dbt pipeline?")

    # Or more explicit
    response = jarvis.consult("backend", "FastAPI performance tips")

    # Get history
    history = jarvis.history("dataengineer", days=14)

Author: JARVIS Portable System
Date: 2025-11-23
"""

from jarvis_router import consult_agent, get_agent_history, get_memory_stats


class JARVISClaudeHelper:
    """
    Helper class pour consultations JARVIS depuis Claude Code

    Interface ultra-simple pour que Claude puisse appeler les agents.
    """

    def __call__(self, agent_name: str, query: str) -> str:
        """
        Appel direct: jarvis("agent", "query")

        Args:
            agent_name: dataengineer, backend, devops, ai
            query: Question

        Returns:
            Reponse agent
        """
        return consult_agent(agent_name, query)

    def consult(self, agent_name: str, query: str, task_type: str = None) -> str:
        """
        Methode explicite: jarvis.consult("agent", "query")

        Args:
            agent_name: dataengineer, backend, devops, ai
            query: Question
            task_type: Type de tache (optionnel)

        Returns:
            Reponse agent
        """
        return consult_agent(agent_name, query, task_type)

    def history(self, agent_name: str = None, days: int = 7) -> list:
        """
        Historique consultations: jarvis.history("agent", days=14)

        Args:
            agent_name: Agent specifique (None = tous)
            days: Derniers X jours

        Returns:
            Liste consultations
        """
        return get_agent_history(agent_name, days)

    def stats(self) -> dict:
        """
        Stats memoire: jarvis.stats()

        Returns:
            {total_memories, consultations_count, tasks_count, agents}
        """
        return get_memory_stats()

    def help(self):
        """Affiche guide d'utilisation"""
        print("""
==========================================================================
JARVIS CLAUDE CODE INTEGRATION - GUIDE D'UTILISATION
==========================================================================

4 AGENTS EXPERTS DISPONIBLES:

1. DataEngineer (dataengineer, data)
   - Modern Data Stack: dbt, Airbyte, Airflow/Dagster
   - Data warehouses: Snowflake, BigQuery, ClickHouse
   - Streaming: Kafka, Flink
   - Open Table Formats: Iceberg, Delta Lake

2. BackendExpert (backend, backendexpert)
   - FastAPI 0.121+ (50K+ req/sec)
   - PostgreSQL 17, Neo4j 2025.09
   - AsyncIO optimizations
   - API performance tuning

3. DevOpsSRE (devops, sre)
   - Kubernetes 1.30-1.32
   - GitOps: ArgoCD, FluxCD
   - SRE methodology: SLI/SLO/SLA
   - Observability: Prometheus, Grafana

4. AIEngineer (ai, aiengineer, llm)
   - LLMs: Llama 4, Mistral Medium 3, Qwen 3
   - RAG systems: SELF-RAG, SPLICE, HyDE
   - Agents: LangGraph, AutoGen, CrewAI
   - Vector DBs: Qdrant, Pinecone

--------------------------------------------------------------------------
EXEMPLES D'UTILISATION:
--------------------------------------------------------------------------

# Methode 1: Appel direct (le plus simple)
from claude_integration import jarvis

response = jarvis("dataengineer", "How to optimize my dbt project?")
print(response)

# Methode 2: Appel explicite
response = jarvis.consult(
    "backend",
    "What's the best way to scale FastAPI to 100K req/sec?"
)

# Methode 3: Avec type de tache
response = jarvis.consult(
    "devops",
    "Design a production-ready Kubernetes setup",
    task_type="architecture_design"
)

--------------------------------------------------------------------------
HISTORIQUE & STATS:
--------------------------------------------------------------------------

# Voir historique d'un agent
history = jarvis.history("dataengineer", days=14)
for h in history:
    print(f"{h['timestamp']}: {h['query']}")

# Stats memoire
stats = jarvis.stats()
print(f"Total consultations: {stats['consultations_count']}")
print(f"Agents utilises: {', '.join(stats['agents'])}")

--------------------------------------------------------------------------
CONTEXTE AUTOMATIQUE:
--------------------------------------------------------------------------

JARVIS se souvient AUTOMATIQUEMENT de toutes les consultations passees!

Exemple:
1. Tu demandes: "Audit ma base PostgreSQL"
2. 2 semaines plus tard: "Optimise ma base PostgreSQL"
3. JARVIS rappelle automatiquement l'audit precedent et dit:
   "Lors de ton audit il y a 14 jours, on a trouve 3 slow queries..."

--------------------------------------------------------------------------
MEMOIRE PERSISTANTE:
--------------------------------------------------------------------------

Toutes les consultations sont sauvegardees dans SQLite:
- Localisation: data/jarvis_memory.db
- Tables: consultations, tasks
- Recherche: temporelle, par agent, full-text
- Persistance: Survit aux redemarrages

--------------------------------------------------------------------------
COMMANDES CLI (si lance directement):
--------------------------------------------------------------------------

# Depuis terminal
cd Documents/jarvis-laptop-system
python claude_integration.py "dataengineer" "your question here"

==========================================================================
        """)


# Instance globale
jarvis = JARVISClaudeHelper()


# CLI interface
if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1 or sys.argv[1] in ["help", "--help", "-h"]:
        jarvis.help()
    elif len(sys.argv) == 2 and sys.argv[1] == "stats":
        stats = jarvis.stats()
        print("\n[JARVIS MEMORY STATS]")
        print(f"  Total memories: {stats['total_memories']}")
        print(f"  Consultations: {stats['consultations_count']}")
        print(f"  Tasks: {stats['tasks_count']}")
        print(f"  Agents: {', '.join(stats['agents'])}")
        print(f"  Last activity: {stats['last_activity']}")
    elif len(sys.argv) == 2 and sys.argv[1] == "history":
        history = jarvis.history(days=7)
        print(f"\n[JARVIS CONSULTATION HISTORY - Last 7 days]")
        print(f"Found {len(history)} consultations:\n")
        for h in history:
            print(f"[{h['timestamp']}] {h['agent']}")
            print(f"  Q: {h['query'][:80]}...")
            print(f"  A: {h['response'][:100]}...")
            print()
    elif len(sys.argv) >= 3:
        agent_name = sys.argv[1]
        query = " ".join(sys.argv[2:])

        print(f"\n[JARVIS] Consulting {agent_name}...")
        print(f"[Query] {query}\n")

        response = jarvis(agent_name, query)

        print("[Response]")
        print("=" * 70)
        print(response)
        print("=" * 70)
    else:
        print("Usage:")
        print("  python claude_integration.py help")
        print("  python claude_integration.py stats")
        print("  python claude_integration.py history")
        print("  python claude_integration.py <agent> <query>")
        print("\nExamples:")
        print("  python claude_integration.py dataengineer \"How to optimize dbt?\"")
        print("  python claude_integration.py backend \"FastAPI best practices\"")
