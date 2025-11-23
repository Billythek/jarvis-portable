"""
JARVIS System Audit - Consultation de tous les agents experts
==============================================================

Lance les 4 agents experts en parallele pour audit complet du systeme.

Author: JARVIS Portable System
Date: 2025-11-23
"""

import asyncio
from jarvis_router import JARVISRouter

async def audit_complet():
    """Lance les 4 consultations en parallele"""

    print("=" * 70)
    print("JARVIS SYSTEM AUDIT - CONSULTATION DES 4 AGENTS EXPERTS")
    print("=" * 70)
    print()

    # Create router instance
    router = JARVISRouter.get_instance()

    # Questions pour chaque agent
    questions = {
        "devops": """Audit complet infrastructure JARVIS laptop system:

1. Analyse architecture actuelle (4 agents + router + brain)
2. Containerisation: Dockerfile manquant, comment structurer?
3. CI/CD: Quelle pipeline GitHub Actions pour tests auto + deploy?
4. Observability: Quels metrics tracker pour chaque agent?
5. Deployment strategy: Local laptop vs cloud-ready

Donne recommandations concretes avec priorites (HIGH/MEDIUM/LOW).""",

        "backend": """Audit architecture backend JARVIS:

1. Performance actuelle: Async/await optimise?
2. SQLite persistent_memory: Limits? Migration PostgreSQL necessaire?
3. Connection pooling: Configuration actuelle OK?
4. Error handling: Retry logic avec backoff?
5. API design: Router pattern bien implemente?
6. Caching strategy: Faut-il ajouter Redis?

Analyse code et donne top 5 optimizations.""",

        "dataengineer": """Audit data pipeline JARVIS:

1. SQLite schema: Tables consultations + tasks optimisees?
2. Indexes: Performance queries actuelles?
3. Backup strategy: Comment sauvegarder data/ ?
4. Data retention: Politique de cleanup?
5. Analytics: Export vers Parquet pour analyse?
6. Scalability: SQLite suffit ou migration warehouse necessaire?

Recommandations data engineering.""",

        "ai": """Audit intelligence JARVIS:

1. Hybrid intelligence: Claude SDK + Ollama architecture OK?
2. Local Expert Mode: Knowledge bases suffisantes?
3. Context enrichment: Task tracker bien integre?
4. RAG system: Faut-il ajouter vector DB (Qdrant)?
5. Agent orchestration: Router + lazy loading optimise?
6. Memory system: Unified memory vs persistent memory?

Recommandations AI/ML pour ameliorer intelligence."""
    }

    # Resultats
    results = {}

    # Consultation 1: DevOpsSRE
    print("\n[1/4] Consulting DevOpsSRE Agent...")
    print("-" * 70)
    results["devops"] = await router.consult_async("devops", questions["devops"], task_type="audit")
    print("[OK] DevOpsSRE audit complete\n")

    # Consultation 2: BackendExpert
    print("[2/4] Consulting BackendExpert Agent...")
    print("-" * 70)
    results["backend"] = await router.consult_async("backend", questions["backend"], task_type="audit")
    print("[OK] BackendExpert audit complete\n")

    # Consultation 3: DataEngineer
    print("[3/4] Consulting DataEngineer Agent...")
    print("-" * 70)
    results["dataengineer"] = await router.consult_async("dataengineer", questions["dataengineer"], task_type="audit")
    print("[OK] DataEngineer audit complete\n")

    # Consultation 4: AIEngineer
    print("[4/4] Consulting AIEngineer Agent...")
    print("-" * 70)
    results["ai"] = await router.consult_async("ai", questions["ai"], task_type="audit")
    print("[OK] AIEngineer audit complete\n")

    # Summary
    print("\n" + "=" * 70)
    print("AUDIT COMPLETE - SUMMARY")
    print("=" * 70)
    print()

    for agent, response in results.items():
        print(f"\n### {agent.upper()} RECOMMENDATIONS ###")
        print("-" * 70)
        print(response[:500] + "...\n")

    # Save full report
    with open("audit_report.md", "w", encoding="utf-8") as f:
        f.write("# JARVIS SYSTEM AUDIT REPORT\n\n")
        f.write(f"Date: 2025-11-23\n\n")
        f.write("=" * 70 + "\n\n")

        for agent, response in results.items():
            f.write(f"## {agent.upper()} AUDIT\n\n")
            f.write(response)
            f.write("\n\n" + "=" * 70 + "\n\n")

    print("\n[SAVED] Full audit report: audit_report.md")
    print()

    return results


if __name__ == "__main__":
    asyncio.run(audit_complet())
