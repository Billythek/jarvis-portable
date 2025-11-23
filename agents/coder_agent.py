"""
Coder Agent - Génération de Code avec Claude SDK
=================================================

Agent spécialisé dans l'écriture de code utilisant
Claude Code SDK + tools intégrés.

Author: JARVIS System V3
Date: 2025-11-23
"""

import asyncio
from typing import Dict, List, Optional
import json
from datetime import datetime


try:
    from claude_code_sdk import query, ClaudeCodeOptions
    SDK_AVAILABLE = True
except ImportError:
    print("[WARN] Claude Code SDK not available for CoderAgent")
    SDK_AVAILABLE = False


class CoderAgent:
    """
    Agent de génération de code

    Utilise Claude Code SDK avec outils (Read, Write, Edit, Bash, etc.)
    pour écrire du code propre et documenté.
    """

    def __init__(self, name: str, brain=None):
        """
        Initialise le coder agent

        Args:
            name: Nom de l'agent
            brain: Instance JARVISBrainV3 (accès mémoire)
        """

        self.name = name
        self.id = name
        self.brain = brain

        # Outils disponibles
        self.tools = ['Read', 'Write', 'Edit', 'Bash', 'Grep', 'Glob']

        # Stats
        self.tasks_completed = 0
        self.files_created = 0
        self.files_modified = 0

        print(f"[{self.name}] Initialized (SDK: {SDK_AVAILABLE})")

    async def start(self):
        """Démarre l'agent"""
        print(f"[{self.name}] Started")

    async def stop(self):
        """Arrête l'agent"""
        print(f"[{self.name}] Stopped")

    async def execute_task(self, task: Dict) -> Dict:
        """
        Exécute une tâche de coding

        Args:
            task: {
                'description': str,
                'metadata': {'project_path': str, 'language': str, ...}
            }

        Returns:
            {
                'success': bool,
                'code': str or List[str],
                'files': List[str],
                'error': str (si échec)
            }
        """

        description = task['description']
        metadata = task.get('metadata', {})

        print(f"[{self.name}] Executing: {description[:60]}...")

        # 1. Cherche contexte dans mémoire JARVIS
        context = None
        if self.brain and self.brain.memory:
            context_query = f"code examples similar to: {description}"
            context = await asyncio.to_thread(
                self.brain.memory.recall,
                context_query,
                limit=3
            )

        # 2. Génère code avec Claude SDK
        if SDK_AVAILABLE:
            result = await self._generate_with_claude_sdk(
                description,
                context,
                metadata
            )
        else:
            result = await self._generate_fallback(description, metadata)

        # 3. Stocke dans mémoire pour apprentissage
        if result['success'] and self.brain:
            await asyncio.to_thread(
                self.brain.remember,
                content=f"Code generated: {description}\n{result.get('code', '')[:500]}",
                importance='normal',
                metadata={
                    'agent': self.name,
                    'task_type': 'code_generation',
                    'files': result.get('files', []),
                    'timestamp': datetime.now().isoformat()
                }
            )

        # Stats
        if result['success']:
            self.tasks_completed += 1
            self.files_created += result.get('files_created', 0)
            self.files_modified += result.get('files_modified', 0)

        return result

    async def _generate_with_claude_sdk(
        self,
        description: str,
        context: Optional[List[Dict]],
        metadata: Dict
    ) -> Dict:
        """Génère code avec Claude Code SDK"""

        # Build prompt avec contexte
        context_text = ""
        if context:
            context_text = "\n**Context from JARVIS memory:**\n"
            for mem in context:
                context_text += f"- {mem.get('content', '')[:200]}...\n"

        prompt = f"""{context_text}

**Task:** {description}

**Requirements:**
- Write clean, well-documented code
- Follow best practices
- Use appropriate tools (Read, Write, Edit, Bash)
- Test the code if possible

**Metadata:** {json.dumps(metadata, indent=2)}

Execute the task completely."""

        # Options SDK
        options = ClaudeCodeOptions(
            allowed_tools=self.tools,
            permission_mode='acceptEdits',  # Auto-accept edits
            max_thinking_tokens=20000
        )

        try:
            messages = []
            files_modified = []

            async for msg in query(prompt=prompt, options=options):
                # Collecte messages
                if hasattr(msg, 'content'):
                    messages.append(str(msg.content))

                # Détecte fichiers modifiés (outil Write/Edit)
                if hasattr(msg, 'tool_use') and msg.tool_use:
                    tool_name = getattr(msg.tool_use, 'name', None)
                    if tool_name in ['Write', 'Edit']:
                        params = getattr(msg.tool_use, 'parameters', {})
                        file_path = params.get('file_path')
                        if file_path and file_path not in files_modified:
                            files_modified.append(file_path)

            code_output = '\n'.join(messages)

            return {
                'success': True,
                'code': code_output,
                'files': files_modified,
                'files_created': len([f for f in files_modified if 'created' in code_output.lower()]),
                'files_modified': len(files_modified)
            }

        except Exception as e:
            print(f"[{self.name} ERROR] {e}")
            return {
                'success': False,
                'error': str(e)
            }

    async def _generate_fallback(self, description: str, metadata: Dict) -> Dict:
        """Fallback sans SDK (génère template)"""

        template_code = f"""# Generated Code Template
# Task: {description}
# Metadata: {json.dumps(metadata, indent=2)}

def main():
    \"\"\"
    TODO: Implement {description}
    \"\"\"
    pass

if __name__ == "__main__":
    main()
"""

        return {
            'success': True,
            'code': template_code,
            'files': [],
            'note': 'Template generated (SDK not available)'
        }

    def get_stats(self) -> Dict:
        """Retourne statistiques de l'agent"""

        return {
            'name': self.name,
            'tasks_completed': self.tasks_completed,
            'files_created': self.files_created,
            'files_modified': self.files_modified
        }
