# JARVIS Laptop System - Quickstart

## Installation en 4 étapes

### 1. Installer les dépendances
```bash
cd Documents/jarvis-laptop-system
pip install -r requirements.txt
```

### 2. Configurer l'environnement (optionnel)
```bash
cp .env.example .env
# Éditer .env pour ajouter ta clé Ollama si tu en as une
```

### 3. Installer les hooks Claude Code
```bash
python install_hooks.py
```

**Ce que font les hooks:**
- Capture automatique de toutes tes conversations avec Claude Code
- Logging de toutes les actions de Claude (outils utilisés, fichiers modifiés)
- Sauvegarde des sessions pour apprentissage continu
- JARVIS apprend de chaque interaction pour mieux t'assister

### 4. Démarrer JARVIS
```bash
python start_jarvis.py
```

## Ce qui démarre automatiquement

**JARVIS Brain** - Intelligence hybride Claude + Ollama
**Battery Manager** - 4 profils adaptatifs (PERFORMANCE → BALANCED → ECO → CRITICAL)
**Agents** (1 à 5 selon batterie):
- Monitor Agent (toujours actif) - Surveillance système
- Indexer Agent (≥BALANCED) - Indexation projets
- Learner Agent (≥BALANCED) - Apprentissage continu
- Coder Agent (≥BALANCED) - Génération code
- Reviewer Agent (=PERFORMANCE) - Critique code

## Profils de batterie

| Profil | Batterie | Agents | Intelligence | Autonomie |
|--------|----------|--------|--------------|-----------|
| **PERFORMANCE** | >80% ou secteur | 5 agents | Hybrid (Claude + Ollama) | ~2.5h |
| **BALANCED** | 40-80% | 4 agents | Hybrid prefer Ollama | ~6.6h |
| **ECO** | 20-40% | 2 agents | Ollama only | ~12h |
| **CRITICAL** | <20% | 1 agent | Cache only | ~20h |

## Utilisation

JARVIS tourne en continu avec heartbeats toutes les 5 minutes.

Pour arrêter: `Ctrl+C`

## Logs

Les logs sont dans `logs/` (créé automatiquement).

## Documentation complète

Voir `README.md` pour la documentation complète.
