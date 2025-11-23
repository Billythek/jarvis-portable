#!/usr/bin/env python3
"""
JARVIS PORTABLE - Version Optimisée Laptop
===========================================

Version allégée de JARVIS optimisée pour ordinateur portable avec:
- Gestion intelligente de la batterie (4 profils adaptatifs)
- 9 agents essentiels + experts (vs 10+ master)
- Intelligence hybride (Claude Sonnet 4.5 + Ollama gpt-oss:20b)
- Consommation RAM réduite (1.2GB vs 6.5GB master)
- Autonomie batterie 2.6x meilleure

Agents disponibles:
- Monitor, Indexer, Learner, Coder, Reviewer (essentiels)
- Backend Expert, Data Engineer, DevOps SRE, AI Engineer (experts)

Author: JARVIS Portable System
Date: 2025-11-23
"""

import sys
import os
import asyncio
import psutil
from pathlib import Path
from datetime import datetime

# Add paths
sys.path.insert(0, str(Path(__file__).parent / "core"))
sys.path.insert(0, str(Path(__file__).parent / "agents_v3"))
sys.path.insert(0, str(Path(__file__).parent / "laptop"))

# Load environment
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

from core.brain import JARVISBrainV3SDK
from core.battery_manager import BatteryManager

# Agents essentiels
from agents.monitor_agent import NetworkMonitorAgent
from agents.coder_agent import CoderAgent
from agents.reviewer_agent import CodeReviewerAgent
from agents.indexer_agent import MemoryIndexerAgent
from agents.learner_agent import LearningAgent

# Agents experts (nouveaux!)
from agents.backend_expert_agent import BackendExpertAgent
from agents.data_engineer_agent import DataEngineerAgent
from agents.devops_sre_agent import DevOpsSREAgent
from agents.ai_engineer_agent import AIEngineerAgent


class JARVISPortable:
    """
    JARVIS Portable - Système optimisé pour laptop

    Fonctionnalités:
    - Gestion batterie intelligente (4 profils)
    - Agents essentiels adaptatifs
    - Intelligence hybride Claude + Ollama
    - RAM optimisée (~1.2GB)
    """

    def __init__(self):
        self.brain = None
        self.battery = BatteryManager()
        self.agents = {}
        self.running = False
        self.start_time = datetime.now()

        # Stats
        self.heartbeat_count = 0

    async def initialize(self):
        """Initialise JARVIS Portable"""

        print("\n" + "=" * 70)
        print("  JARVIS PORTABLE - INITIALISATION SYSTEME")
        print("=" * 70 + "\n")

        # 1. Battery Status
        print("[1/4] Analyse de la batterie...")
        self.battery.print_status()

        profile = self.battery.get_performance_profile()
        config = self.battery.get_profile_config(profile)

        print(f"  Profil actif: {profile}")
        print(f"  Agents a demarrer: {config['agents_actifs']}")
        print(f"  Intelligence: {config['intelligence']}")

        # 2. JARVIS Brain
        print("\n[2/4] Initialisation JARVIS Brain V3 SDK...")
        self.brain = JARVISBrainV3SDK()

        status = self.brain.get_status()
        print(f"  Node ID: {status['node_id']}")
        print(f"  Mode: {status['intelligence']['mode'].upper()}")
        print(f"  Claude SDK: {'OK' if status['intelligence']['claude_code_sdk'] else 'Non'}")
        print(f"  Ollama: {'OK' if status['intelligence']['ollama_gpt_oss_20b'] else 'Non'}")

        # 3. Agents essentiels selon profil batterie
        print("\n[3/4] Initialisation des agents...")
        await self._init_agents(profile, config)

        # 4. System Check
        print("\n[4/4] Verification systeme...")
        ram_mb = psutil.Process().memory_info().rss / 1024 / 1024
        cpu_percent = psutil.cpu_percent(interval=1)

        print(f"  RAM utilisee: {ram_mb:.0f}MB")
        print(f"  CPU: {cpu_percent:.1f}%")
        print(f"  Agents actifs: {len(self.agents)}")

        print("\n" + "=" * 70)
        print("  JARVIS PORTABLE - INITIALISATION TERMINEE")
        print("=" * 70 + "\n")

    async def _init_agents(self, profile: str, config: dict):
        """Initialise les agents selon le profil batterie"""

        agents_count = config['agents_actifs']

        # Agent 1: Network Monitor (TOUJOURS actif)
        monitor = NetworkMonitorAgent("Monitor_Portable", brain=self.brain)
        monitor.monitoring_interval = config['monitoring_interval']
        self.agents['monitor'] = monitor
        print(f"  [OK] Monitor ({config['monitoring_interval']}s interval)")

        if agents_count >= 2:
            # Agent 2: Memory Indexer
            indexer = MemoryIndexerAgent("Indexer_Portable", brain=self.brain)
            self.agents['indexer'] = indexer
            print("  [OK] Indexer")

        if agents_count >= 3:
            # Agent 3: Learning Agent
            learner = LearningAgent("Learner_Portable", brain=self.brain)
            self.agents['learner'] = learner
            print("  [OK] Learner")

        if agents_count >= 4:
            # Agent 4: Coder Agent
            coder = CoderAgent("Coder_Portable", brain=self.brain)
            self.agents['coder'] = coder
            print("  [OK] Coder")

        if agents_count >= 5:
            # Agent 5: Code Reviewer
            reviewer = CodeReviewerAgent("Reviewer_Portable", brain=self.brain)
            self.agents['reviewer'] = reviewer
            print("  [OK] Reviewer")

        # Agents Experts (6-9): Disponibles en PERFORMANCE ou sur demande
        if agents_count >= 6:
            # Agent 6: Backend Expert
            backend_expert = BackendExpertAgent("BackendExpert", brain=self.brain)
            self.agents['backend_expert'] = backend_expert
            print("  [OK] Backend Expert (FastAPI/PostgreSQL/Neo4j)")

        if agents_count >= 7:
            # Agent 7: Data Engineer
            data_engineer = DataEngineerAgent("DataEngineer", brain=self.brain)
            self.agents['data_engineer'] = data_engineer
            print("  [OK] Data Engineer (dbt/Modern Data Stack)")

        if agents_count >= 8:
            # Agent 8: DevOps SRE
            devops_sre = DevOpsSREAgent("DevOpsSRE", brain=self.brain)
            self.agents['devops_sre'] = devops_sre
            print("  [OK] DevOps SRE (Kubernetes/GitOps)")

        if agents_count >= 9:
            # Agent 9: AI Engineer
            ai_engineer = AIEngineerAgent("AIEngineer", brain=self.brain)
            self.agents['ai_engineer'] = ai_engineer
            print("  [OK] AI Engineer (LLM/RAG/Agents)")

    async def start_production(self):
        """Lance le système en mode production"""

        print("=" * 70)
        print("  DEMARRAGE MODE PRODUCTION PORTABLE")
        print("=" * 70)
        print()

        self.running = True

        # Démarre tous les agents
        print("[START] Lancement des agents...")
        for name, agent in self.agents.items():
            await agent.start()
            print(f"  [OK] {name} started")

        battery_status = self.battery.get_battery_status()

        print()
        print("=" * 70)
        print("  JARVIS PORTABLE - MODE PRODUCTION ACTIF")
        print("=" * 70)
        print()
        print(f"  Heure demarrage: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  Agents actifs: {len(self.agents)}")
        print(f"  Profil batterie: {self.battery.current_profile}")

        if battery_status['present']:
            print(f"  Batterie: {battery_status['percent']}%")
            print(f"  Autonomie estimee: {self.battery.estimate_runtime():.1f}h")
        else:
            print(f"  Mode: Desktop (pas de batterie)")

        print()
        print("  Systeme surveille et apprend en continu...")
        print("  Appuie sur Ctrl+C pour arreter proprement")
        print()
        print("=" * 70)
        print()

    async def run_forever(self):
        """Boucle principale de production"""

        try:
            while self.running:
                # Heartbeat toutes les 5 minutes
                await asyncio.sleep(300)

                self.heartbeat_count += 1

                # Check et adapte selon batterie
                profile_changed = await self.battery.check_and_adapt()

                if profile_changed:
                    # Adapte les agents au nouveau profil
                    await self._adapt_to_profile()

                # Stats
                uptime = (datetime.now() - self.start_time).total_seconds()
                ram_mb = psutil.Process().memory_info().rss / 1024 / 1024
                battery_status = self.battery.get_battery_status()

                print(f"\n[HEARTBEAT #{self.heartbeat_count}]")
                print(f"  Uptime: {uptime/3600:.1f}h")
                print(f"  RAM: {ram_mb:.0f}MB")
                print(f"  Agents: {len(self.agents)}")
                print(f"  Memoire: {len(self.brain.working_memory)} items")

                if battery_status['present']:
                    print(f"  Batterie: {battery_status['percent']}% ({self.battery.current_profile})")
                    print(f"  Autonomie: {self.battery.estimate_runtime():.1f}h")

                # Stats agents
                if hasattr(self.agents.get('monitor'), 'metrics_collected'):
                    print(f"  Monitor: {self.agents['monitor'].metrics_collected} metriques")

        except KeyboardInterrupt:
            print("\n\n[SHUTDOWN] Signal arret recu...")
            await self.shutdown()

    async def _adapt_to_profile(self):
        """Adapte le système au nouveau profil batterie"""

        config = self.battery.get_profile_config()

        print(f"\n[ADAPT] Adaptation au profil {self.battery.current_profile}...")

        # Adapte l'intervalle de monitoring
        if 'monitor' in self.agents:
            old_interval = self.agents['monitor'].monitoring_interval
            new_interval = config['monitoring_interval']

            if old_interval != new_interval:
                self.agents['monitor'].monitoring_interval = new_interval
                print(f"  Monitor interval: {old_interval}s -> {new_interval}s")

        # Adapte l'utilisation de Claude SDK
        if config['use_claude_sdk']:
            print("  Intelligence: Claude SDK active")
        else:
            print("  Intelligence: Ollama only (economie batterie)")

        # Si profil CRITICAL, arrête agents non-essentiels
        if self.battery.current_profile == "CRITICAL":
            print("  [WARNING] Mode CRITICAL - Arret agents non-essentiels")

            for name in list(self.agents.keys()):
                if name != 'monitor':
                    agent = self.agents.pop(name)
                    await agent.stop()
                    print(f"    [STOP] {name}")

        print()

    async def shutdown(self):
        """Arrêt gracieux du système"""

        print("\n" + "=" * 70)
        print("  JARVIS PORTABLE - ARRET GRACIEUX")
        print("=" * 70)
        print()

        self.running = False

        # Stop tous les agents
        print("[SHUTDOWN] Arret des agents...")
        for name, agent in self.agents.items():
            try:
                await agent.stop()
                print(f"  [OK] {name} stopped")
            except:
                print(f"  [WARN] {name} failed to stop gracefully")

        # Close brain
        if self.brain:
            self.brain.close()
            print("  [OK] JARVIS Brain closed")

        uptime = (datetime.now() - self.start_time).total_seconds()
        ram_mb = psutil.Process().memory_info().rss / 1024 / 1024

        print()
        print("=" * 70)
        print("  JARVIS PORTABLE - ARRET TERMINE")
        print("=" * 70)
        print()
        print(f"  Duree totale: {uptime/3600:.2f} heures")
        print(f"  RAM finale: {ram_mb:.0f}MB")
        print(f"  Memoires stockees: {len(self.brain.working_memory) if self.brain else 0}")
        print(f"  Heartbeats: {self.heartbeat_count}")
        print()
        print("  Systeme arrete proprement.")
        print()
        print("=" * 70)
        print()

    def get_ram_usage(self) -> float:
        """Retourne l'utilisation RAM en MB"""
        return psutil.Process().memory_info().rss / 1024 / 1024


async def main():
    """Point d'entrée principal"""

    # Create system
    jarvis = JARVISPortable()

    # Initialize
    await jarvis.initialize()

    # Start production
    await jarvis.start_production()

    # Run forever
    await jarvis.run_forever()


if __name__ == "__main__":
    try:
        print("\n" + "=" * 70)
        print("  JARVIS PORTABLE v1.0")
        print("  Version optimisee pour ordinateur portable")
        print("=" * 70)

        asyncio.run(main())

    except KeyboardInterrupt:
        print("\n[EXIT] JARVIS Portable arrete par utilisateur")
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
