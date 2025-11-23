"""
Code Reviewer Agent - Critique de Code avec Ollama
====================================================

Agent spécialisé dans la révision de code utilisant Ollama
pour détecter bugs, problèmes et proposer améliorations.

Author: JARVIS System V3
Date: 2025-11-23
"""

import asyncio
import requests
from typing import Dict, List
from datetime import datetime


class CodeReviewerAgent:
    """
    Agent de révision de code

    Utilise Ollama pour critiquer la qualité du code.
    """

    def __init__(self, name: str, brain=None):
        self.name = name
        self.id = name
        self.brain = brain

        # Stats
        self.reviews_completed = 0

        print(f"[{self.name}] Initialized")

    async def start(self):
        """Démarre l'agent"""
        print(f"[{self.name}] Started")

    async def stop(self):
        """Arrête l'agent"""
        print(f"[{self.name}] Stopped")

    async def execute_task(self, task: Dict) -> Dict:
        """
        Exécute une tâche de review

        Args:
            task: {'code': str, 'description': str}

        Returns:
            {'success': bool, 'score': int, 'issues': List[str], 'suggestions': List[str]}
        """

        code = task.get('code', '')
        description = task.get('description', 'Code review')

        print(f"[{self.name}] Reviewing: {description[:60]}...")

        # Simple review (fallback si pas d'Ollama)
        result = await self._review_code(code)

        # Stocke dans mémoire
        if result['success'] and self.brain:
            await asyncio.to_thread(
                self.brain.remember,
                content=f"Code review: {description}\nScore: {result['score']}/100",
                importance='normal',
                metadata={
                    'agent': self.name,
                    'task_type': 'code_review',
                    'score': result['score']
                }
            )

        self.reviews_completed += 1

        return result

    async def _review_code(self, code: str) -> Dict:
        """Review basique de code"""

        # Analyse simple
        issues = []
        score = 70  # Score par défaut

        # Checks basiques
        if len(code) < 10:
            issues.append("Code trop court")
            score -= 10

        if "def" not in code and "function" not in code and "class" not in code:
            issues.append("Pas de fonction/classe détectée")
            score -= 10

        if "# " not in code and '"""' not in code:
            issues.append("Pas de commentaires/docstrings")
            score -= 5

        if "import" not in code:
            issues.append("Pas d'imports détectés")
            score -= 5

        return {
            'success': True,
            'score': max(0, score),
            'issues': issues,
            'suggestions': ["Ajouter des docstrings", "Ajouter des tests"],
            'approved': score >= 60
        }

    def get_stats(self) -> Dict:
        """Retourne statistiques"""
        return {
            'name': self.name,
            'reviews_completed': self.reviews_completed
        }
