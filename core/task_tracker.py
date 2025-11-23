"""
JARVIS Task Tracker - Context-Aware Task Management
====================================================

Tracking taches avec enrichissement automatique du contexte.
Permet de savoir ce qui a deja ete fait et d'eviter la repetition.

Author: JARVIS Portable System
Date: 2025-11-23
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional

try:
    from .persistent_memory import PersistentMemory
except ImportError:
    # For standalone testing
    from persistent_memory import PersistentMemory


class TaskTracker:
    """
    Task Tracker avec context

 automatique

    Features:
    - Log taches executees
    - Detecte si tache similaire deja faite
    - Enrichit contexte avec historique pertinent
    - Suggestions basees sur patterns passees
    """

    def __init__(self, persistent_memory: PersistentMemory):
        """
        Initialise le task tracker

        Args:
            persistent_memory: Instance de PersistentMemory
        """
        self.memory = persistent_memory
        print("[TaskTracker] Initialized")

    def log_task(self, agent_name: str, task_type: str, description: str,
                result: str = None, status: str = "completed", metadata: Dict = None) -> int:
        """
        Enregistre une tache executee

        Args:
            agent_name: Agent qui a execute
            task_type: Type (audit, optimization, design, etc)
            description: Description
            result: Resultat
            status: completed, failed, pending
            metadata: Metadonnees

        Returns:
            ID de la tache
        """
        task_id = self.memory.remember_task(
            agent_name=agent_name,
            task_type=task_type,
            description=description,
            result=result,
            status=status,
            metadata=metadata
        )

        print(f"[TaskTracker] Logged: {agent_name} - {task_type}")
        return task_id

    def has_done_before(self, agent_name: str, keywords: List[str],
                       days: int = 30) -> bool:
        """
        Verifie si une tache similaire a deja ete faite

        Args:
            agent_name: Nom de l'agent
            keywords: Liste de mots-cles a chercher
            days: Chercher dans les X derniers jours

        Returns:
            True si tache similaire trouvee
        """
        # Get recent tasks for this agent
        tasks = self.memory.recall_tasks(agent_name=agent_name, days=days, limit=50)

        # Check if any keyword matches
        for task in tasks:
            text = (task['description'] + " " + (task['result'] or "")).lower()
            for keyword in keywords:
                if keyword.lower() in text:
                    return True

        return False

    def get_context(self, agent_name: str, query: str, max_items: int = 3) -> str:
        """
        Recupere contexte automatique pour enrichir une consultation

        Args:
            agent_name: Nom de l'agent consulte
            query: Query actuelle
            max_items: Nombre max d'items de contexte

        Returns:
            Contexte formate en string
        """
        context_parts = []

        # 1. Chercher consultations recentes de cet agent
        recent_consultations = self.memory.recall_consultations(
            agent_name=agent_name,
            days=14,
            limit=max_items
        )

        if recent_consultations:
            context_parts.append("=== CONSULTATIONS RECENTES ===")
            for i, c in enumerate(recent_consultations[:max_items], 1):
                age_days = (datetime.now() - datetime.fromisoformat(c['timestamp'])).days
                context_parts.append(
                    f"[{i}] Il y a {age_days} jours:\n"
                    f"    Q: {c['query']}\n"
                    f"    R: {c['response'][:150]}..."
                )

        # 2. Chercher taches recentes similaires
        # Extract keywords from query
        keywords = self._extract_keywords(query)

        if keywords:
            # Search for similar past tasks
            all_tasks = self.memory.recall_tasks(agent_name=agent_name, days=30, limit=20)
            similar_tasks = []

            for task in all_tasks:
                text = (task['description'] + " " + (task['result'] or "")).lower()
                matches = sum(1 for kw in keywords if kw.lower() in text)

                if matches > 0:
                    similar_tasks.append((matches, task))

            # Sort by relevance
            similar_tasks.sort(key=lambda x: x[0], reverse=True)

            if similar_tasks:
                context_parts.append("\n=== TACHES SIMILAIRES PASSEES ===")
                for i, (matches, task) in enumerate(similar_tasks[:max_items], 1):
                    age_days = (datetime.now() - datetime.fromisoformat(task['timestamp'])).days
                    context_parts.append(
                        f"[{i}] Il y a {age_days} jours - {task['task_type']}:\n"
                        f"    {task['description']}\n"
                        f"    Resultat: {(task['result'] or 'N/A')[:150]}..."
                    )

        # 3. Suggestions basees sur patterns
        suggestions = self._get_suggestions(agent_name, query)
        if suggestions:
            context_parts.append("\n=== SUGGESTIONS ===")
            for s in suggestions:
                context_parts.append(f"- {s}")

        if not context_parts:
            return "[Pas de contexte anterieur trouve]"

        return "\n".join(context_parts)

    def get_task_history(self, agent_name: str = None, task_type: str = None,
                        days: int = 30) -> List[Dict]:
        """
        Recupere historique des taches

        Args:
            agent_name: Filtrer par agent
            task_type: Filtrer par type
            days: Limiter aux X derniers jours

        Returns:
            Liste de taches
        """
        return self.memory.recall_tasks(
            agent_name=agent_name,
            task_type=task_type,
            days=days,
            limit=50
        )

    def get_recent_activity(self, days: int = 7) -> Dict:
        """
        Resume de l'activite recente

        Args:
            days: Derniers X jours

        Returns:
            {total_tasks, by_agent, by_type, recent_tasks}
        """
        tasks = self.memory.recall_tasks(days=days, limit=100)

        by_agent = {}
        by_type = {}

        for task in tasks:
            agent = task['agent']
            task_type = task['task_type']

            by_agent[agent] = by_agent.get(agent, 0) + 1
            by_type[task_type] = by_type.get(task_type, 0) + 1

        return {
            "total_tasks": len(tasks),
            "by_agent": by_agent,
            "by_type": by_type,
            "recent_tasks": tasks[:10]
        }

    def _extract_keywords(self, text: str, min_length: int = 4) -> List[str]:
        """
        Extrait mots-cles d'un texte

        Args:
            text: Texte source
            min_length: Longueur minimale des mots

        Returns:
            Liste de keywords
        """
        # Simple word extraction (lowercase, filter short words)
        import re

        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may',
            'mon', 'ma', 'mes', 'le', 'la', 'les', 'un', 'une', 'des', 'de', 'du',
            'et', 'ou', 'mais', 'pour', 'dans', 'sur', 'avec', 'par', 'que', 'qui',
            'comment', 'quoi'
        }

        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [
            w for w in words
            if len(w) >= min_length and w not in stop_words
        ]

        # Return unique keywords
        return list(set(keywords))

    def _get_suggestions(self, agent_name: str, query: str) -> List[str]:
        """
        Generate suggestions basees sur patterns passees

        Args:
            agent_name: Agent consulte
            query: Query actuelle

        Returns:
            Liste de suggestions
        """
        suggestions = []

        # Get task types done by this agent
        tasks = self.memory.recall_tasks(agent_name=agent_name, days=90, limit=50)

        if not tasks:
            suggestions.append("Premiere consultation avec cet agent")
            return suggestions

        # Analyze patterns
        task_types = {}
        for task in tasks:
            task_type = task['task_type']
            task_types[task_type] = task_types.get(task_type, 0) + 1

        # Most common task types
        common_types = sorted(task_types.items(), key=lambda x: x[1], reverse=True)

        if common_types:
            top_type = common_types[0][0]
            count = common_types[0][1]
            suggestions.append(
                f"Tu as deja fait {count} taches de type '{top_type}' avec cet agent"
            )

        # Check if similar query was done recently
        keywords = self._extract_keywords(query)
        if keywords and self.has_done_before(agent_name, keywords, days=14):
            suggestions.append(
                "Attention: Une tache similaire a ete faite recemment (voir contexte ci-dessus)"
            )

        return suggestions


# Test
if __name__ == "__main__":
    from persistent_memory import PersistentMemory

    print("=" * 70)
    print("TEST: JARVIS Task Tracker")
    print("=" * 70)
    print()

    # Create memory and tracker
    memory = PersistentMemory(db_path=":memory:")
    tracker = TaskTracker(memory)

    # Test 1: Log tasks
    print("[TEST 1] Logging tasks...")
    tracker.log_task(
        agent_name="DataEngineer",
        task_type="database_audit",
        description="Audit PostgreSQL production database",
        result="Found 3 slow queries, 1 missing index",
        status="completed"
    )

    tracker.log_task(
        agent_name="DataEngineer",
        task_type="optimization",
        description="Optimize dbt pipeline for faster incremental builds",
        result="Reduced build time by 40% using partitioning",
        status="completed"
    )

    tracker.log_task(
        agent_name="BackendExpert",
        task_type="performance_audit",
        description="Analyze FastAPI endpoint performance",
        result="P95 latency 45ms, recommended connection pooling",
        status="completed"
    )

    print("  [OK] 3 tasks logged")
    print()

    # Test 2: Check if done before
    print("[TEST 2] Checking if task done before...")
    done_before = tracker.has_done_before(
        agent_name="DataEngineer",
        keywords=["database", "audit"],
        days=30
    )
    print(f"  Database audit done before: {done_before}")
    print()

    # Test 3: Get context
    print("[TEST 3] Getting context for new query...")
    context = tracker.get_context(
        agent_name="DataEngineer",
        query="How to optimize PostgreSQL queries?",
        max_items=3
    )
    print("  Context retrieved:")
    print("  " + "\n  ".join(context.split("\n")[:10]))
    print("  ...")
    print()

    # Test 4: Get recent activity
    print("[TEST 4] Getting recent activity...")
    activity = tracker.get_recent_activity(days=30)
    print(f"  Total tasks (30 days): {activity['total_tasks']}")
    print(f"  By agent: {activity['by_agent']}")
    print(f"  By type: {activity['by_type']}")
    print()

    memory.close()

    print("=" * 70)
    print("ALL TESTS PASSED")
    print("=" * 70)
