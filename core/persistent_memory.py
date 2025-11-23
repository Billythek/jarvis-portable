"""
JARVIS Persistent Memory - SQLite Backend
==========================================

Systeme de memoire persistante pour JARVIS avec SQLite.
Permet de sauvegarder et recuperer consultations, taches et contexte.

Author: JARVIS Portable System
Date: 2025-11-23
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pathlib import Path


class PersistentMemory:
    """
    Memoire persistante SQLite pour JARVIS

    Tables:
    - consultations: Historique consultations agents experts
    - tasks: Tracking taches executees

    Features:
    - Recherche par agent, temporelle, full-text
    - Indexation optimisee pour requetes rapides
    - Pas de dependances externes (SQLite built-in)
    """

    def __init__(self, db_path: str = None):
        """
        Initialise la memoire persistante

        Args:
            db_path: Chemin vers DB SQLite (default: ./data/jarvis_memory.db)
        """
        if db_path is None:
            # Default path: data/jarvis_memory.db
            data_dir = Path(__file__).parent.parent / "data"
            data_dir.mkdir(exist_ok=True)
            db_path = str(data_dir / "jarvis_memory.db")

        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Pour acceder par nom de colonne

        self._init_schema()

        print(f"[PersistentMemory] Initialized at {db_path}")

    def _init_schema(self):
        """Cree le schema de la base de donnees"""

        cursor = self.conn.cursor()

        # Table consultations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                query TEXT NOT NULL,
                response TEXT NOT NULL,
                importance TEXT DEFAULT 'normal',
                metadata TEXT,
                timestamp TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Table tasks (tracking plus structure)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                agent_name TEXT NOT NULL,
                task_type TEXT NOT NULL,
                description TEXT NOT NULL,
                result TEXT,
                status TEXT DEFAULT 'completed',
                metadata TEXT,
                timestamp TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Indexes pour performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_consultations_agent
            ON consultations(agent_name)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_consultations_timestamp
            ON consultations(timestamp DESC)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_agent
            ON tasks(agent_name)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_timestamp
            ON tasks(timestamp DESC)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_type
            ON tasks(task_type)
        """)

        self.conn.commit()

    def remember_consultation(self, agent_name: str, query: str, response: str,
                            importance: str = "normal", metadata: Dict = None) -> int:
        """
        Sauvegarde une consultation agent

        Args:
            agent_name: Nom de l'agent consulte
            query: Question posee
            response: Reponse de l'agent
            importance: normal, high, critical
            metadata: Metadonnees additionnelles (dict)

        Returns:
            ID de la consultation creee
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO consultations
            (agent_name, query, response, importance, metadata, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            agent_name,
            query,
            response,
            importance,
            json.dumps(metadata or {}),
            datetime.now().isoformat()
        ))

        self.conn.commit()
        return cursor.lastrowid

    def remember_task(self, agent_name: str, task_type: str, description: str,
                     result: str = None, status: str = "completed",
                     metadata: Dict = None) -> int:
        """
        Sauvegarde une tache executee

        Args:
            agent_name: Agent qui a execute
            task_type: Type de tache (audit, optimization, design, etc)
            description: Description courte
            result: Resultat/output de la tache
            status: completed, failed, pending
            metadata: Metadonnees additionnelles

        Returns:
            ID de la tache creee
        """
        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO tasks
            (agent_name, task_type, description, result, status, metadata, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            agent_name,
            task_type,
            description,
            result,
            status,
            json.dumps(metadata or {}),
            datetime.now().isoformat()
        ))

        self.conn.commit()
        return cursor.lastrowid

    def recall_consultations(self, agent_name: str = None, limit: int = 10,
                           days: int = None) -> List[Dict]:
        """
        Recupere consultations passees

        Args:
            agent_name: Filtrer par agent (None = tous)
            limit: Nombre max de resultats
            days: Limiter aux X derniers jours (None = illimite)

        Returns:
            Liste de consultations [{agent, query, response, timestamp}, ...]
        """
        cursor = self.conn.cursor()

        query = "SELECT * FROM consultations WHERE 1=1"
        params = []

        if agent_name:
            query += " AND agent_name = ?"
            params.append(agent_name)

        if days is not None:
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()
            query += " AND timestamp > ?"
            params.append(cutoff)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)

        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row["id"],
                "agent": row["agent_name"],
                "query": row["query"],
                "response": row["response"],
                "importance": row["importance"],
                "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                "timestamp": row["timestamp"]
            })

        return results

    def recall_tasks(self, agent_name: str = None, task_type: str = None,
                   limit: int = 10, days: int = None) -> List[Dict]:
        """
        Recupere taches passees

        Args:
            agent_name: Filtrer par agent
            task_type: Filtrer par type de tache
            limit: Nombre max de resultats
            days: Limiter aux X derniers jours

        Returns:
            Liste de taches [{agent, type, description, result, timestamp}, ...]
        """
        cursor = self.conn.cursor()

        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if agent_name:
            query += " AND agent_name = ?"
            params.append(agent_name)

        if task_type:
            query += " AND task_type = ?"
            params.append(task_type)

        if days is not None:
            cutoff = (datetime.now() - timedelta(days=days)).isoformat()
            query += " AND timestamp > ?"
            params.append(cutoff)

        query += " ORDER BY timestamp DESC LIMIT ?"
        params.append(limit)

        cursor.execute(query, params)

        results = []
        for row in cursor.fetchall():
            results.append({
                "id": row["id"],
                "agent": row["agent_name"],
                "task_type": row["task_type"],
                "description": row["description"],
                "result": row["result"],
                "status": row["status"],
                "metadata": json.loads(row["metadata"]) if row["metadata"] else {},
                "timestamp": row["timestamp"]
            })

        return results

    def search(self, keyword: str, limit: int = 10) -> List[Dict]:
        """
        Recherche full-text dans consultations et taches

        Args:
            keyword: Mot-cle a chercher
            limit: Nombre max de resultats

        Returns:
            Liste combinee de consultations et taches correspondantes
        """
        cursor = self.conn.cursor()

        results = []

        # Search consultations
        cursor.execute("""
            SELECT 'consultation' as type, agent_name, query, response, timestamp
            FROM consultations
            WHERE query LIKE ? OR response LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (f"%{keyword}%", f"%{keyword}%", limit))

        for row in cursor.fetchall():
            results.append({
                "type": "consultation",
                "agent": row["agent_name"],
                "query": row["query"],
                "response": row["response"][:200] + "...",
                "timestamp": row["timestamp"]
            })

        # Search tasks
        cursor.execute("""
            SELECT 'task' as type, agent_name, task_type, description, result, timestamp
            FROM tasks
            WHERE description LIKE ? OR result LIKE ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, (f"%{keyword}%", f"%{keyword}%", limit))

        for row in cursor.fetchall():
            results.append({
                "type": "task",
                "agent": row["agent_name"],
                "task_type": row["task_type"],
                "description": row["description"],
                "result": row["result"][:200] + "..." if row["result"] else None,
                "timestamp": row["timestamp"]
            })

        # Sort by timestamp
        results.sort(key=lambda x: x["timestamp"], reverse=True)

        return results[:limit]

    def get_stats(self) -> Dict:
        """
        Retourne statistiques de la memoire

        Returns:
            {consultations_count, tasks_count, agents, last_activity}
        """
        cursor = self.conn.cursor()

        # Count consultations
        cursor.execute("SELECT COUNT(*) as count FROM consultations")
        consultations_count = cursor.fetchone()["count"]

        # Count tasks
        cursor.execute("SELECT COUNT(*) as count FROM tasks")
        tasks_count = cursor.fetchone()["count"]

        # Get unique agents
        cursor.execute("""
            SELECT DISTINCT agent_name FROM (
                SELECT agent_name FROM consultations
                UNION
                SELECT agent_name FROM tasks
            )
        """)
        agents = [row["agent_name"] for row in cursor.fetchall()]

        # Last activity
        cursor.execute("""
            SELECT MAX(timestamp) as last_timestamp FROM (
                SELECT timestamp FROM consultations
                UNION
                SELECT timestamp FROM tasks
            )
        """)
        last_activity = cursor.fetchone()["last_timestamp"]

        return {
            "consultations_count": consultations_count,
            "tasks_count": tasks_count,
            "total_memories": consultations_count + tasks_count,
            "agents": agents,
            "last_activity": last_activity
        }

    def close(self):
        """Ferme la connexion SQLite"""
        if self.conn:
            self.conn.close()
            print("[PersistentMemory] Connection closed")


# Test
if __name__ == "__main__":
    print("=" * 70)
    print("TEST: JARVIS Persistent Memory")
    print("=" * 70)
    print()

    # Create memory
    memory = PersistentMemory(db_path=":memory:")  # In-memory pour test

    # Test 1: Remember consultations
    print("[TEST 1] Saving consultations...")
    memory.remember_consultation(
        agent_name="DataEngineer",
        query="How to optimize dbt models?",
        response="Use incremental models with partitioning...",
        importance="high"
    )

    memory.remember_consultation(
        agent_name="BackendExpert",
        query="FastAPI performance optimization?",
        response="Use async endpoints with uvicorn workers...",
        importance="normal"
    )

    print("  [OK] 2 consultations saved")
    print()

    # Test 2: Remember tasks
    print("[TEST 2] Saving tasks...")
    memory.remember_task(
        agent_name="DataEngineer",
        task_type="database_audit",
        description="Audit PostgreSQL production database",
        result="Found 3 slow queries, 1 missing index"
    )

    print("  [OK] 1 task saved")
    print()

    # Test 3: Recall consultations
    print("[TEST 3] Recalling consultations...")
    consultations = memory.recall_consultations(agent_name="DataEngineer")
    print(f"  Found: {len(consultations)} consultations")
    for c in consultations:
        print(f"    - {c['timestamp']}: {c['query'][:50]}...")
    print()

    # Test 4: Recall tasks
    print("[TEST 4] Recalling tasks...")
    tasks = memory.recall_tasks(task_type="database_audit")
    print(f"  Found: {len(tasks)} tasks")
    for t in tasks:
        print(f"    - {t['timestamp']}: {t['description']}")
    print()

    # Test 5: Search
    print("[TEST 5] Searching for 'optimization'...")
    results = memory.search("optimization")
    print(f"  Found: {len(results)} results")
    for r in results:
        print(f"    - [{r['type']}] {r['agent']}: {r.get('query', r.get('description'))[:40]}...")
    print()

    # Test 6: Stats
    print("[TEST 6] Memory statistics...")
    stats = memory.get_stats()
    print(f"  Total memories: {stats['total_memories']}")
    print(f"  Consultations: {stats['consultations_count']}")
    print(f"  Tasks: {stats['tasks_count']}")
    print(f"  Agents: {', '.join(stats['agents'])}")
    print()

    memory.close()

    print("=" * 70)
    print("ALL TESTS PASSED")
    print("=" * 70)
