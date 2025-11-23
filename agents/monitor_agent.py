"""
Network Monitor Agent - Surveillance Système
=============================================

Author: JARVIS System V3
Date: 2025-11-23
"""

import asyncio
import psutil
from typing import Dict
from datetime import datetime


class NetworkMonitorAgent:
    """Agent de monitoring système continu"""

    def __init__(self, name: str, brain=None):
        self.name = name
        self.id = name
        self.brain = brain
        self.monitoring_interval = 60  # secondes
        self.running = False
        self.metrics_collected = 0

    async def start(self):
        """Démarre monitoring en background"""
        self.running = True
        asyncio.create_task(self._monitoring_loop())
        print(f"[{self.name}] Started (monitoring every {self.monitoring_interval}s)")

    async def stop(self):
        self.running = False
        print(f"[{self.name}] Stopped")

    async def _monitoring_loop(self):
        """Boucle infinie de collecte métriques"""
        while self.running:
            data = await self._collect_metrics()

            # Stocke dans JARVIS memory
            if self.brain:
                await asyncio.to_thread(
                    self.brain.remember,
                    content=f"System metrics: CPU={data['cpu_percent']}% RAM={data['ram_percent']}%",
                    importance='normal',
                    metadata={'type': 'system_metrics', **data}
                )

            # Alerte si anomalie
            if data['cpu_percent'] > 90 or data['ram_percent'] > 85:
                print(f"[{self.name} ALERT] High usage: CPU={data['cpu_percent']}% RAM={data['ram_percent']}%")

            self.metrics_collected += 1
            await asyncio.sleep(self.monitoring_interval)

    async def _collect_metrics(self) -> Dict:
        """Collecte métriques système"""
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'ram_percent': psutil.virtual_memory().percent,
            'disk_percent': psutil.disk_usage('/').percent,
            'network_io': psutil.net_io_counters()._asdict(),
            'timestamp': datetime.now().isoformat()
        }

    async def execute_task(self, task: Dict) -> Dict:
        """Collecte métriques à la demande"""
        data = await self._collect_metrics()
        return {'success': True, 'metrics': data}
