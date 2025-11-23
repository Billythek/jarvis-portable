"""
JARVIS Battery Manager - Gestion Intelligente de la Batterie
==============================================================

Adapte automatiquement les performances de JARVIS selon le niveau
de batterie pour maximiser l'autonomie sur laptop.

Author: JARVIS Portable System
Date: 2025-11-23
"""

import psutil
import asyncio
from typing import Dict, Literal
from datetime import datetime

ProfileType = Literal["PERFORMANCE", "BALANCED", "ECO", "CRITICAL"]


class BatteryManager:
    """
    Gestionnaire intelligent de batterie pour JARVIS Portable

    Profils adaptatifs:
    - PERFORMANCE (>80% ou secteur): Toutes fonctionnalités
    - BALANCED (40-80%): Ollama only, agents réduits
    - ECO (20-40%): Mode minimal, cache maximal
    - CRITICAL (<20%): Offline strict, sauvegarde
    """

    def __init__(self):
        self.current_profile: ProfileType = "PERFORMANCE"
        self.last_check = datetime.now()
        self.check_interval = 60  # secondes

        # Historique pour prédiction
        self.battery_history = []

        print(f"[BatteryManager] Initialized")

    def get_battery_status(self) -> Dict:
        """Récupère l'état complet de la batterie"""

        battery = psutil.sensors_battery()

        if battery is None:
            # Pas de batterie (desktop ou VM)
            return {
                "present": False,
                "percent": 100,
                "plugged": True,
                "time_left": None
            }

        return {
            "present": True,
            "percent": battery.percent,
            "plugged": battery.power_plugged,
            "time_left": battery.secsleft if battery.secsleft != psutil.POWER_TIME_UNLIMITED else None
        }

    def get_performance_profile(self) -> ProfileType:
        """Détermine le profil de performance optimal"""

        status = self.get_battery_status()

        # Si branché sur secteur -> PERFORMANCE
        if status["plugged"]:
            return "PERFORMANCE"

        # Si pas de batterie (desktop) -> PERFORMANCE
        if not status["present"]:
            return "PERFORMANCE"

        # Sinon, selon niveau batterie
        level = status["percent"]

        if level > 80:
            return "PERFORMANCE"
        elif level > 40:
            return "BALANCED"
        elif level > 20:
            return "ECO"
        else:
            return "CRITICAL"

    def get_level(self) -> float:
        """Retourne le pourcentage de batterie"""
        status = self.get_battery_status()
        return status["percent"]

    def estimate_runtime(self) -> float:
        """Estime l'autonomie restante en heures"""

        status = self.get_battery_status()

        # Sur secteur = illimité
        if status["plugged"]:
            return float('inf')

        # Utilise le temps système si disponible
        if status["time_left"] is not None and status["time_left"] > 0:
            return status["time_left"] / 3600.0  # secondes -> heures

        # Estimation basique selon profil
        profile = self.current_profile
        level = status["percent"]

        # Consommation estimée par profil (% par heure)
        consumption_rates = {
            "PERFORMANCE": 40,  # 40% / heure = 2.5h autonomie
            "BALANCED": 15,     # 15% / heure = 6.6h autonomie
            "ECO": 8,          # 8% / heure = 12.5h autonomie
            "CRITICAL": 5       # 5% / heure = 20h autonomie
        }

        rate = consumption_rates[profile]
        return (level / rate) if rate > 0 else 0.0

    async def check_and_adapt(self) -> bool:
        """
        Vérifie la batterie et adapte le profil si nécessaire

        Returns:
            True si le profil a changé
        """

        # Throttle checks
        now = datetime.now()
        if (now - self.last_check).total_seconds() < self.check_interval:
            return False

        self.last_check = now

        # Nouveau profil optimal
        new_profile = self.get_performance_profile()

        # Si changement de profil
        if new_profile != self.current_profile:
            old_profile = self.current_profile
            self.current_profile = new_profile

            status = self.get_battery_status()

            print(f"\n[BatteryManager] PROFIL CHANGÉ: {old_profile} → {new_profile}")
            print(f"  Batterie: {status['percent']}%")
            print(f"  Secteur: {'Oui' if status['plugged'] else 'Non'}")
            print(f"  Autonomie estimée: {self.estimate_runtime():.1f}h")
            print()

            # Store dans historique
            self.battery_history.append({
                "timestamp": now,
                "level": status["percent"],
                "profile": new_profile,
                "plugged": status["plugged"]
            })

            # Limite historique à 100 entrées
            if len(self.battery_history) > 100:
                self.battery_history = self.battery_history[-100:]

            return True

        return False

    def get_profile_config(self, profile: ProfileType = None) -> Dict:
        """
        Retourne la configuration pour un profil donné

        Args:
            profile: Profil spécifique ou None pour le profil actuel

        Returns:
            Configuration du profil
        """

        if profile is None:
            profile = self.current_profile

        configs = {
            "PERFORMANCE": {
                "agents_actifs": 9,           # TOUS les agents (5 essentiels + 4 experts)
                "intelligence": "hybrid",     # Claude + Ollama
                "use_claude_sdk": True,
                "use_ollama": True,
                "cache_ttl": 3600,            # 1h
                "monitoring_interval": 60,    # 1 minute
                "ram_target_mb": 3000,        # Augmenté pour 9 agents
                "cpu_limit_percent": 80,
                "description": "Performance maximale - Tous les agents experts actifs (secteur ou >80%)"
            },

            "BALANCED": {
                "agents_actifs": 5,           # 5 agents essentiels (Monitor, Indexer, Learner, Coder, Reviewer)
                "intelligence": "hybrid_prefer_ollama",
                "use_claude_sdk": True,       # Disponible mais non préféré
                "use_ollama": True,
                "cache_ttl": 14400,           # 4h
                "monitoring_interval": 120,   # 2 minutes
                "ram_target_mb": 1500,        # Ajusté pour 5 agents
                "cpu_limit_percent": 50,
                "description": "Équilibré - Agents essentiels seulement (40-80% batterie)"
            },

            "ECO": {
                "agents_actifs": 2,           # Monitor + Indexer minimal
                "intelligence": "ollama_only",
                "use_claude_sdk": False,      # Désactivé pour économie
                "use_ollama": True,
                "cache_ttl": 86400,           # 24h
                "monitoring_interval": 300,   # 5 minutes
                "ram_target_mb": 800,
                "cpu_limit_percent": 30,
                "description": "Économie d'énergie - Monitoring minimal (20-40% batterie)"
            },

            "CRITICAL": {
                "agents_actifs": 1,           # Monitor seulement
                "intelligence": "cache_only",
                "use_claude_sdk": False,
                "use_ollama": False,          # Même Ollama désactivé
                "cache_ttl": 604800,          # 7 jours
                "monitoring_interval": 600,   # 10 minutes
                "ram_target_mb": 500,
                "cpu_limit_percent": 15,
                "description": "Critique - Sauvegarde et arrêt automatique (<20% batterie)"
            }
        }

        return configs[profile]

    def print_status(self):
        """Affiche le statut actuel de la batterie"""

        status = self.get_battery_status()
        config = self.get_profile_config()

        print("\n" + "=" * 60)
        print("JARVIS BATTERY MANAGER - STATUS")
        print("=" * 60)

        if not status["present"]:
            print("  Batterie: Non detectee (desktop)")
            print("  Profil: PERFORMANCE")
        else:
            print(f"  Niveau: {status['percent']}%")
            print(f"  Secteur: {'Oui [POWER]' if status['plugged'] else 'Non [BATTERY]'}")
            print(f"  Profil actuel: {self.current_profile}")
            print(f"  Autonomie estimée: {self.estimate_runtime():.1f}h")

        print(f"\n  Configuration active:")
        print(f"    - Agents actifs: {config['agents_actifs']}")
        print(f"    - Intelligence: {config['intelligence']}")
        print(f"    - RAM cible: {config['ram_target_mb']}MB")
        print(f"    - CPU limite: {config['cpu_limit_percent']}%")

        print("=" * 60 + "\n")

    def is_on_power(self) -> bool:
        """Retourne True si branché sur secteur"""
        status = self.get_battery_status()
        return status["plugged"]

    async def wait_for_power(self, max_wait: int = 3600):
        """
        Attend que l'ordinateur soit branché sur secteur

        Args:
            max_wait: Temps d'attente maximum en secondes

        Returns:
            True si branché, False si timeout
        """

        elapsed = 0
        check_interval = 30  # secondes

        while elapsed < max_wait:
            if self.is_on_power():
                return True

            await asyncio.sleep(check_interval)
            elapsed += check_interval

        return False


# Factory function
def get_battery_manager() -> BatteryManager:
    """Retourne une instance singleton de BatteryManager"""

    global _battery_manager_instance

    if '_battery_manager_instance' not in globals():
        _battery_manager_instance = BatteryManager()

    return _battery_manager_instance


# Tests
if __name__ == "__main__":
    async def test_battery_manager():
        print("[BATTERY] TEST BATTERY MANAGER\n")

        manager = BatteryManager()

        # Test 1: Status
        manager.print_status()

        # Test 2: Profils
        print("[PROFILES] CONFIGURATIONS DES PROFILS:\n")
        for profile in ["PERFORMANCE", "BALANCED", "ECO", "CRITICAL"]:
            config = manager.get_profile_config(profile)
            print(f"{profile}:")
            print(f"  {config['description']}")
            print(f"  Agents: {config['agents_actifs']} | RAM: {config['ram_target_mb']}MB")
            print()

        # Test 3: Monitoring adaptatif
        print("[MONITOR] TEST MONITORING ADAPTATIF (30s)...\n")
        for i in range(6):
            changed = await manager.check_and_adapt()
            if changed:
                print("  [CHANGEMENT] Nouveau profil applique!")
            else:
                print(f"  [TICK {i+1}/6] Profil stable: {manager.current_profile}")

            await asyncio.sleep(5)

        print("\n[OK] Tests Battery Manager termines!\n")

    asyncio.run(test_battery_manager())
