# JARVIS PORTABLE - Guide d'Utilisation

**Version optimisée pour ordinateur portable**

---

## Vue d'Ensemble

JARVIS Portable est une version allégée et optimisée de JARVIS spécialement conçue pour fonctionner efficacement sur laptop avec:

- **Gestion intelligente de la batterie** (4 profils adaptatifs)
- **Consommation RAM réduite** (1.2GB vs 6.5GB version master)
- **Autonomie 2.6x meilleure** (2.5h → 6.5h selon profil)
- **6 agents essentiels** au lieu de 10+ dans la version master
- **Intelligence hybride** Claude Sonnet 4.5 + Ollama gpt-oss:20b

---

## Démarrage Rapide

### Lancer JARVIS Portable

```bash
cd Documents/jarvis-system
python START_JARVIS_PORTABLE.py
```

### Arrêter JARVIS Portable

Appuie sur `Ctrl+C` pour arrêter proprement le système.

---

## Profils de Batterie

JARVIS Portable s'adapte automatiquement selon le niveau de batterie :

### 1. PERFORMANCE (>80% ou secteur branché)
- **Tous les agents actifs** (6 agents)
- **Intelligence**: Hybride (Claude + Ollama)
- **RAM cible**: 2.5GB
- **Intervalle monitoring**: 60s
- **Utilisation**: Performance maximale

### 2. BALANCED (40-80% batterie)
- **4 agents actifs** (Monitor, Indexer, Coder, Learner)
- **Intelligence**: Hybride préférence Ollama
- **RAM cible**: 1.2GB
- **Intervalle monitoring**: 120s (2 minutes)
- **Autonomie**: ~6.6h

### 3. ECO (20-40% batterie)
- **2 agents actifs** (Monitor + essentiel)
- **Intelligence**: Ollama uniquement
- **RAM cible**: 800MB
- **Intervalle monitoring**: 300s (5 minutes)
- **Autonomie**: ~12.5h

### 4. CRITICAL (<20% batterie)
- **1 agent actif** (Monitor seulement)
- **Intelligence**: Cache uniquement (pas de LLM)
- **RAM cible**: 500MB
- **Intervalle monitoring**: 600s (10 minutes)
- **Action**: Sauvegarde automatique puis arrêt gracieux

---

## Agents Disponibles

### Agents Essentiels (Toujours Actifs)

1. **Network Monitor Agent**
   - Surveille CPU, RAM, disque, réseau
   - S'adapte selon profil batterie
   - Alertes automatiques si anomalie

2. **Memory Indexer Agent** (si profil ≥ BALANCED)
   - Indexe tes projets automatiquement
   - Stocke dans le graphe de connaissances
   - Cherche patterns et relations

3. **Learning Agent** (si profil ≥ BALANCED)
   - Apprend depuis tes conversations
   - Améliore les réponses au fil du temps
   - DPO-inspired (préférences utilisateur)

4. **Coder Agent** (si profil ≥ BALANCED)
   - Génère du code avec Claude SDK
   - Utilise outils (Read, Write, Edit, Bash)
   - Stocke exemples pour apprentissage

5. **Code Reviewer Agent** (si profil = PERFORMANCE)
   - Critique qualité du code avec Ollama
   - Détecte bugs et problèmes
   - Propose améliorations

---

## Intelligence Hybride

JARVIS Portable utilise **2 modèles IA** selon la complexité :

### Claude Sonnet 4.5 (via Claude Code SDK)
- **Quand**: Tâches complexes (complexité ≥ 7/10)
- **Utilisation**: Coding, analyse profonde, raisonnement
- **Coût**: Utilise ton abonnement Claude Max
- **Désactivé**: En mode ECO et CRITICAL (économie batterie)

### Ollama gpt-oss:20b (via API Cloud)
- **Quand**: Tâches simples (complexité < 7/10)
- **Utilisation**: Critique code, questions rapides
- **Coût**: Gratuit (Ollama Cloud)
- **Toujours actif**: Sauf en mode CRITICAL

---

## Consommation et Performance

### Comparaison Master vs Portable

| Métrique | Master | Portable | Amélioration |
|----------|--------|----------|--------------|
| **Fichiers** | 728 | ~80 | 9x moins |
| **RAM** | 6.5GB | 1.2GB | 5.4x moins |
| **Agents** | 10+ | 6 | Optimisé |
| **Autonomie** | 2.5h | 6.5h | 2.6x mieux |
| **Démarrage** | ~45s | ~5s | 9x plus rapide |

### Utilisation Ressources Typique

**Mode BALANCED** (recommandé sur batterie):
- RAM: ~1.2GB
- CPU: 10-15% (idle), 30-40% (actif)
- Batterie: ~15% par heure → 6.6h autonomie

**Mode PERFORMANCE** (sur secteur):
- RAM: ~2.5GB
- CPU: 15-25% (idle), 50-60% (actif)
- Batterie: ~40% par heure → 2.5h autonomie

---

## Heartbeats et Monitoring

JARVIS Portable affiche un **heartbeat toutes les 5 minutes** avec:

```
[HEARTBEAT #12]
  Uptime: 1.0h
  RAM: 1150MB
  Agents: 4
  Memoire: 23 items
  Batterie: 67% (BALANCED)
  Autonomie: 5.2h
  Monitor: 12 metriques
```

### Informations du Heartbeat

- **Uptime**: Temps depuis le démarrage
- **RAM**: Mémoire utilisée actuellement
- **Agents**: Nombre d'agents actifs
- **Memoire**: Items dans la mémoire de travail
- **Batterie**: Niveau et profil actuel
- **Autonomie**: Estimation temps restant
- **Monitor**: Métriques système collectées

---

## Fichiers Importants

### Configuration
- `.env` - Variables d'environnement (clés API)
- `core/JARVIS_BRAIN_V3_SDK.py` - Cerveau principal
- `laptop/JARVIS_BATTERY_MANAGER.py` - Gestion batterie

### Scripts
- `START_JARVIS_PORTABLE.py` - **Script principal** à lancer
- `START_JARVIS_PRODUCTION.py` - Version master (complète)

### Agents
- `agents_v3/network/monitor_agent.py` - Surveillance système
- `agents_v3/development/coder_agent.py` - Génération code
- `agents_v3/development/code_reviewer_agent.py` - Critique code
- `agents_v3/memory/indexer_agent.py` - Indexation projets
- `agents_v3/memory/learner_agent.py` - Apprentissage continu

### Résultats Tests
- `TESTS_REELS_RESULTS.md` - Résultats des 5 tests réels
- Tous les tests sont PASS (100% success)

---

## FAQ

### Q: Quelle est la différence avec JARVIS Master ?

JARVIS Portable est une version allégée sans:
- Infrastructure de trading (9 fichiers)
- Bases de données lourdes (PostgreSQL, Qdrant, Neo4j)
- Agents non-essentiels
- Living Cognition complète (3 agents vs 7)

### Q: Est-ce que je perds des fonctionnalités importantes ?

Non ! JARVIS Portable garde:
- Intelligence hybride (Claude + Ollama)
- Génération et critique de code
- Apprentissage continu
- Mémoire 4-tiers (HOT/WARM/COLD/ARCHIVE)
- Monitoring système
- Indexation projets

### Q: Comment forcer un profil spécifique ?

Pour l'instant, le profil s'adapte automatiquement selon la batterie. Pour forcer:
1. Branche ton laptop sur secteur → PERFORMANCE
2. Débranche et garde >40% batterie → BALANCED

### Q: Ollama est nécessaire ?

Non ! Ollama fonctionne via l'API Cloud (clé dans .env). Pas besoin d'installer Ollama localement.

### Q: Claude SDK est nécessaire ?

Oui, pour utiliser Claude Sonnet 4.5. Si non installé, JARVIS utilise seulement Ollama (fonctionne quand même).

---

## Dépannage

### JARVIS ne démarre pas

1. Vérifie que tu es dans le bon dossier:
   ```bash
   cd Documents/jarvis-system
   ```

2. Vérifie les dépendances:
   ```bash
   pip install psutil python-dotenv asyncio aiofiles
   ```

3. Vérifie le fichier `.env` existe avec:
   ```
   OLLAMA_API_KEY=0bb4f9c171ca4f8c8a26fc4aba2972a5.dCtSDesjfRw_kH8h8pe3cURc
   OLLAMA_URL=https://ollama.com/api
   ```

### RAM trop élevée

Le système devrait automatiquement réduire la RAM en mode ECO. Si problème:
1. Ferme les applications gourmandes
2. Débranche le secteur → Force profil ECO

### Batterie se vide trop vite

1. Vérifie que le profil s'adapte (regarde les prints)
2. En mode BALANCED, autonomie ~6.6h attendue
3. Si moins, passe en mode ECO (<40% batterie)

---

## Prochaines Améliorations

**Court Terme** (1-2 semaines):
- [ ] ResearchAgent (recherche web Brave)
- [ ] Dashboard web temps réel
- [ ] Export mémoire en JSON

**Moyen Terme** (1-2 mois):
- [ ] Mode offline complet (cache + Ollama local)
- [ ] Smart Sync cloud
- [ ] Mobile app (Termux)

**Long Terme** (3-6 mois):
- [ ] Multi-LLM support (GPT-4, Gemini)
- [ ] Voice interface (ElevenLabs)
- [ ] Fine-tuning Ollama sur tes conversations

---

## Support

**Questions / Problèmes**:
1. Lis ce README complet
2. Vérifie `TESTS_REELS_RESULTS.md`
3. Regarde les logs dans le terminal

**Contributions**:
- Fork le projet
- Crée une branche (`feature/ma-fonctionnalite`)
- Commit et push
- Ouvre une Pull Request

---

## Licence

MIT License

---

**Créé avec Claude Code pour l'autonomie et la performance sur laptop** 🚀

*Version 1.0 - 2025-11-23*
