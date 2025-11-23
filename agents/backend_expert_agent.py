"""
Backend Expert Agent - Senior Backend Engineer

Expert en developpement backend haute performance avec focus sur:
- FastAPI 0.121+ avec Pydantic v2
- PostgreSQL 17 avec optimisations avancees
- Neo4j 2025.09 pour graphs
- Microservices et APIs RESTful/GraphQL/gRPC
- Performance: 50K+ req/sec, P50/P95/P99 latency tracking

Technologies maitrisees:
- Python 3.13+ (Free-Threaded Mode, JIT)
- AsyncIO avec TaskGroup (structured concurrency)
- Redis pour caching avec TTL strategies
- Connection pooling asyncpg
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, Optional

class BackendExpertAgent:
    """
    Agent expert en developpement backend

    Specialisations:
    - Architecture APIs scalables
    - Optimisation database et queries
    - Microservices patterns
    - Performance tuning
    """

    def __init__(self, name: str, brain=None):
        self.name = name
        self.brain = brain
        self.running = False
        self.expertise_domains = [
            "fastapi",
            "postgresql",
            "neo4j",
            "microservices",
            "async_python",
            "redis_caching",
            "api_design",
            "database_optimization"
        ]

        # Benchmarks et best practices
        self.knowledge_base = {
            "fastapi_performance": {
                "async_endpoints": "50K+ req/sec with uvicorn workers",
                "p50_latency": "<10ms for simple queries",
                "p95_latency": "<50ms with DB connection pooling",
                "p99_latency": "<200ms worst case",
                "workers": "2-4 per CPU core recommended"
            },
            "postgresql_17": {
                "json_table": "Native JSON_TABLE() for nested data",
                "incremental_backup": "pg_basebackup with --incremental",
                "merge_improved": "MERGE statement 30% faster",
                "partitioning": "LIST/RANGE for tables >10M rows",
                "indexes": "B-tree default, BRIN for time-series, GIN for JSON"
            },
            "neo4j_2025": {
                "gql_support": "Graph Query Language standard",
                "vector_search": "Native vector search for embeddings",
                "cypher_parallel": "Parallel query execution",
                "apoc_procedures": "400+ graph algorithms"
            },
            "async_patterns": {
                "taskgroup": "Structured concurrency Python 3.13+",
                "connection_pool": "asyncpg pool size = 10-20 connections",
                "background_tasks": "FastAPI BackgroundTasks for non-blocking",
                "streaming": "Server-Sent Events for real-time updates"
            }
        }

    async def start(self):
        """Demarre l'agent expert backend"""
        self.running = True
        if self.brain:
            self.brain.working_memory[f"{self.name}_status"] = {
                "type": "agent_status",
                "agent": self.name,
                "status": "running",
                "expertise": self.expertise_domains,
                "timestamp": datetime.now().isoformat()
            }

    async def stop(self):
        """Arrete l'agent"""
        self.running = False

    async def analyze_backend_architecture(self, requirements: Dict[str, Any]) -> str:
        """
        Analyse les requirements et recommande une architecture backend

        Args:
            requirements: Dict avec keys: traffic, data_volume, latency_req, features

        Returns:
            Recommandations detaillees avec benchmarks
        """
        traffic = requirements.get("traffic_req_sec", 1000)
        data_volume = requirements.get("data_volume_gb", 10)
        latency_req = requirements.get("latency_ms", 100)

        analysis = f"""
# Backend Architecture Analysis

## Requirements
- Traffic: {traffic} req/sec
- Data Volume: {data_volume} GB
- Latency Target: {latency_req}ms P95

## Recommended Stack

### API Layer: FastAPI 0.121+
- **Async endpoints** with uvicorn workers (2-4 per core)
- **Expected perf**: 50K+ req/sec (bien au-dessus des {traffic} req/sec)
- **Latency**: P50 <10ms, P95 <50ms (conforme aux {latency_req}ms)

### Database: PostgreSQL 17
"""

        if data_volume > 100:
            analysis += """
- **Partitioning**: RANGE partitioning par date (tables >10M rows)
- **Indexes**: B-tree + BRIN pour time-series
"""
        else:
            analysis += """
- **Indexes**: B-tree standard suffisant
"""

        analysis += f"""
- **Connection Pool**: asyncpg avec 10-20 connections
- **JSON Support**: JSON_TABLE() natif pour nested data

### Caching: Redis
- **TTL Strategy**: 5min pour queries lourdes, 1h pour reference data
- **Hit Rate Target**: >80%
- **Eviction**: LRU (Least Recently Used)

### Performance Optimizations
1. **Async all the way**: AsyncIO + asyncpg + aioredis
2. **Connection pooling**: Reuse DB connections
3. **Query optimization**: EXPLAIN ANALYZE systematique
4. **Background tasks**: FastAPI BackgroundTasks pour emails/notifications
"""

        if traffic > 10000:
            analysis += """
5. **Load balancing**: Nginx/HAProxy devant uvicorn workers
6. **Horizontal scaling**: Stateless API instances
"""

        analysis += """

## Code Example: FastAPI avec AsyncIO

```python
from fastapi import FastAPI, Depends
from asyncpg import create_pool
from redis import asyncio as aioredis

app = FastAPI()

# Connection pool
db_pool = None
redis_client = None

@app.on_event("startup")
async def startup():
    global db_pool, redis_client
    db_pool = await create_pool(
        "postgresql://user:pass@localhost/db",
        min_size=10,
        max_size=20
    )
    redis_client = await aioredis.from_url("redis://localhost")

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # Check cache first
    cached = await redis_client.get(f"user:{user_id}")
    if cached:
        return cached

    # Query DB
    async with db_pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE id = $1",
            user_id
        )

    # Cache result (TTL 5min)
    await redis_client.setex(
        f"user:{user_id}",
        300,
        user
    )

    return user
```

## Performance Benchmarks
- **Expected throughput**: 30-50K req/sec
- **P50 latency**: 5-10ms
- **P95 latency**: 20-50ms
- **P99 latency**: <200ms

## Monitoring Checklist
- [ ] Prometheus metrics (latency P50/P95/P99)
- [ ] PostgreSQL slow query log (>100ms)
- [ ] Redis hit rate (target >80%)
- [ ] Connection pool saturation alerts
"""

        return analysis

    async def optimize_database_query(self, query: str, context: Dict[str, Any]) -> str:
        """
        Analyse et optimise une requete PostgreSQL

        Args:
            query: Requete SQL
            context: Infos sur la table (rows, columns, etc.)

        Returns:
            Recommandations d'optimisation
        """
        table_rows = context.get("table_rows", 0)

        optimization = f"""
# Query Optimization Analysis

## Original Query
```sql
{query}
```

## Analysis
"""

        if table_rows > 10_000_000:
            optimization += """
### Table Size: LARGE (>10M rows)

**Critical optimizations:**

1. **Partitioning**:
   - Use RANGE partitioning par date
   - Queries auto-pruning pour performances

2. **Indexes**:
   - B-tree pour primary/foreign keys
   - BRIN pour colonnes time-series (100x moins d'espace que B-tree)

3. **Query Patterns**:
   ```sql
   -- Eviter les full table scans
   EXPLAIN ANALYZE <query>;  -- Verifier le plan

   -- Utiliser LIMIT pour pagination
   SELECT * FROM table
   WHERE created_at >= '2025-01-01'
   ORDER BY created_at DESC
   LIMIT 100 OFFSET 0;  -- Cursor-based pagination meilleure pour grandes tables
   ```
"""
        else:
            optimization += f"""
### Table Size: MEDIUM ({table_rows:,} rows)

**Recommended optimizations:**

1. **Indexes**: B-tree standard suffisant
   ```sql
   CREATE INDEX idx_table_column ON table(column);
   ```

2. **Query optimization**:
   - Use WHERE clauses indexed columns
   - LIMIT results pour pagination
   - EXPLAIN ANALYZE pour verifier plans
"""

        optimization += """

## Performance Checklist
- [ ] Run `EXPLAIN ANALYZE` avant deployment
- [ ] Verify index usage (`Index Scan` not `Seq Scan`)
- [ ] Check execution time (<100ms cible)
- [ ] Monitor slow query log

## PostgreSQL 17 Features
- **JSON_TABLE()**: Extract nested JSON data nativement
- **Incremental Backup**: Faster backups
- **MERGE Improved**: 30% faster upserts
"""

        return optimization

    async def consult(self, query: str) -> str:
        """
        Consulte l'expert backend pour une question technique

        Args:
            query: Question technique

        Returns:
            Reponse detaillee avec benchmarks et exemples
        """
        if not self.brain:
            return "Backend Expert: Brain not connected"

        # Use brain intelligence pour reponse approfondie
        context = f"""You are a Senior Backend Engineer expert with deep knowledge of:

Technologies:
- FastAPI 0.121+ with Pydantic v2
- PostgreSQL 17 (JSON_TABLE, incremental backup, MERGE improvements)
- Neo4j 2025.09 (GQL, vector search)
- Python 3.13+ (async, free-threaded mode)
- Redis for caching

Expertise:
- API architecture and performance (50K+ req/sec)
- Database optimization (indexes, partitioning, query tuning)
- Microservices patterns
- Async Python best practices
- Performance benchmarks (P50/P95/P99)

Always provide:
1. Concrete solutions with code examples
2. Performance benchmarks and metrics
3. Trade-offs analysis
4. Best practices 2025
5. Version-specific features

User query: {query}

Provide a detailed technical answer with examples and benchmarks."""

        response = await self.brain.think(context)

        # Store consultation in memory
        if self.brain:
            self.brain.working_memory[f"backend_consult_{datetime.now().timestamp()}"] = {
                "type": "expert_consultation",
                "agent": self.name,
                "query": query,
                "response_preview": response[:200],
                "timestamp": datetime.now().isoformat()
            }

        return response
