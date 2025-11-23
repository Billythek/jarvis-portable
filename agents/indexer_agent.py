"""
Memory Indexer Agent - Indexation Projets
==========================================

Author: JARVIS System V3
Date: 2025-11-23
"""

import asyncio
import os
from pathlib import Path
from typing import Dict, List


class MemoryIndexerAgent:
    """Agent d'indexation automatique de projets"""

    def __init__(self, name: str, brain=None):
        self.name = name
        self.id = name
        self.brain = brain
        self.files_indexed = 0

    async def start(self):
        print(f"[{self.name}] Started")

    async def stop(self):
        print(f"[{self.name}] Stopped")

    async def execute_task(self, task: Dict) -> Dict:
        """Indexe un projet"""

        project_path = task.get('metadata', {}).get('project_path', '.')

        print(f"[{self.name}] Indexing {project_path}...")

        # Scan fichiers
        files = await self._scan_project(project_path)

        # Stocke dans mémoire
        if self.brain:
            for file in files[:10]:  # Limite pour demo
                await asyncio.to_thread(
                    self.brain.remember,
                    content=f"Indexed file: {file}",
                    importance='normal',
                    metadata={'type': 'indexed_file', 'path': file}
                )

        self.files_indexed += len(files)

        return {
            'success': True,
            'files_indexed': len(files),
            'project': project_path
        }

    async def _scan_project(self, path: str) -> List[str]:
        """Scan fichiers du projet"""

        files = []
        try:
            for root, dirs, filenames in os.walk(path):
                # Ignore dirs
                dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'node_modules']

                for filename in filenames:
                    if not filename.startswith('.'):
                        files.append(os.path.join(root, filename))

                if len(files) > 100:  # Limite
                    break

        except Exception as e:
            print(f"[{self.name} ERROR] {e}")

        return files
