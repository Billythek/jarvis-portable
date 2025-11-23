"""
Data Engineer Agent - Expert Modern Data Stack

Expert en pipelines de donnees et Modern Data Stack:
- dbt Core 1.8+ pour transformations SQL
- Airbyte/Fivetran pour ingestion (600+ connecteurs)
- Apache Airflow 2.8+ / Dagster 1.6+ orchestration
- Snowflake, BigQuery, ClickHouse, Databricks
- Open Table Formats: Iceberg, Delta Lake, Hudi
- Real-time streaming: Kafka 3.7+, Flink 2.0
- Data Quality: Great Expectations, Monte Carlo

Focus: ELT (Extract, Load, Transform) modern approach
"""

import asyncio
from datetime import datetime
from typing import Dict, Any

class DataEngineerAgent:
    """Agent expert en data engineering et Modern Data Stack"""

    def __init__(self, name: str, brain=None):
        self.name = name
        self.brain = brain
        self.running = False
        self.expertise_domains = [
            "dbt",
            "modern_data_stack",
            "data_warehousing",
            "streaming",
            "data_quality",
            "elt_pipelines",
            "open_table_formats"
        ]

        self.knowledge_base = {
            "dbt_performance": {
                "1m_rows": "2-5 seconds staging models",
                "10m_rows_joins": "30-60 seconds intermediate models",
                "incremental": "90% faster than full refresh",
                "materialization": "table (best perf), view (no storage), incremental (delta only)"
            },
            "modern_data_stack_2025": {
                "ingestion": "Airbyte (open-source, 600+ connectors), Fivetran (managed)",
                "transformation": "dbt Core (SQL), dbt Cloud (GUI + orchestration)",
                "orchestration": "Airflow 2.8+ (traditional), Dagster 1.6+ (modern)",
                "warehouses": "Snowflake (elastic compute), BigQuery (serverless), ClickHouse (OLAP)",
                "quality": "Great Expectations 0.18+, Monte Carlo (ML-powered)",
                "observability": "dbt Cloud, Monte Carlo, Datadog"
            },
            "open_lakehouse": {
                "iceberg": "Standard industrie v2, multi-engine (Spark/Trino/Flink/Snowflake)",
                "delta_lake": "Databricks, Rust kernel perf",
                "hudi": "CDC focused, incremental processing",
                "benefits": "No vendor lock-in, time travel, schema evolution, ACID"
            },
            "streaming": {
                "kafka": "Distributed log, <1s latency, 3.7+ (KRaft no Zookeeper)",
                "flink": "True streaming <100ms, stateful computations, SQL support",
                "spark_streaming": "Micro-batch (1-10s latency), good for batch+stream hybrid"
            }
        }

    async def start(self):
        """Demarre l'agent data engineer"""
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

    async def design_data_pipeline(self, requirements: Dict[str, Any]) -> str:
        """Conçoit un pipeline de donnees moderne"""

        data_volume = requirements.get("daily_gb", 10)
        sources = requirements.get("sources", [])
        latency_req = requirements.get("latency", "batch")  # batch, near-realtime, realtime

        design = f"""
# Modern Data Pipeline Design

## Requirements Analysis
- Data Volume: {data_volume} GB/day
- Sources: {len(sources)} sources
- Latency: {latency_req}

## Recommended Architecture

### 1. Data Ingestion Layer
"""

        if latency_req == "realtime":
            design += """
**Real-Time Streaming**: Apache Kafka 3.7+
- Kafka Connect pour sources (Debezium CDC)
- Sub-second latency
- Exactly-once semantics

**Processing**: Apache Flink 2.0
- True streaming <100ms
- Stateful aggregations
- SQL interface
"""
        else:
            design += """
**ELT Approach**: Airbyte 0.50+ / Fivetran
- 600+ connectors pre-built
- Incremental sync (CDC quand disponible)
- Schema evolution auto
- Load raw data first (schema-on-read)
"""

        design += f"""

### 2. Data Warehouse Layer
"""

        if data_volume > 1000:
            design += """
**Snowflake** (best for >1TB data)
- Elastic compute (scale up/down)
- Time travel (90 days)
- Zero-copy cloning
- $2-4/TB/month storage
"""
        elif data_volume > 100:
            design += """
**ClickHouse 24.12+** (OLAP optimized)
- 100x faster que PostgreSQL pour analytics
- Native Iceberg support
- Columnar storage
- $0.50/TB/month self-hosted
"""
        else:
            design += """
**BigQuery** (serverless, good for <100GB)
- Pay per query ($5/TB scanned)
- Auto-scaling
- ML built-in (BQML)
"""

        design += """

### 3. Transformation Layer: dbt Core 1.8+

**Project Structure**:
```
dbt_project/
├── models/
│   ├── staging/         # Raw cleanup (1-to-1 sources)
│   │   └── stg_users.sql
│   ├── intermediate/    # Business logic, joins
│   │   └── int_user_orders.sql
│   └── marts/          # Final tables pour BI
│       ├── core/       # Company-wide
│       └── marketing/  # Team-specific
├── tests/              # Data quality
└── macros/             # Reusable SQL
```

**Performance Tips**:
- Incremental models (90% faster)
- Partitioning par date
- dbt_utils for common patterns

### 4. Data Quality: Great Expectations 0.18+

```python
# Expectations
expect_column_values_to_not_be_null("user_id")
expect_column_values_to_be_between("age", 0, 120)
expect_column_values_to_be_in_set("status", ["active", "inactive"])
```

### 5. Orchestration
"""

        if len(sources) > 10:
            design += """
**Dagster 1.6+** (modern, asset-based)
- Data lineage native
- Backfills easy
- Type-safe Python
"""
        else:
            design += """
**Apache Airflow 2.8+**
- Mature ecosystem
- 1000+ operators
- Dynamic DAGs
"""

        design += """

## Cost Optimization
- Partition large tables
- Use views pour rarely accessed data
- Incremental dbt models (not full refresh)
- Warehouse auto-suspend (Snowflake)
- Query result caching

## Performance Benchmarks
- dbt staging models: 2-5s per 1M rows
- dbt incremental: 90% faster than full
- Kafka throughput: 1M+ messages/sec
- Flink latency: <100ms for streaming
"""

        return design

    async def consult(self, query: str) -> str:
        """Consultation data engineering experte"""
        if not self.brain:
            return "Data Engineer: Brain not connected"

        context = f"""You are an Expert Data Engineer with deep knowledge of:

Modern Data Stack 2025:
- dbt Core 1.8+ (transformations SQL)
- Airbyte 0.50+ / Fivetran (ELT ingestion)
- Apache Airflow 2.8+ / Dagster 1.6+ (orchestration)
- Snowflake, BigQuery, ClickHouse 24.12+, Databricks
- Open Table Formats: Iceberg v2, Delta Lake, Hudi
- Streaming: Kafka 3.7+, Flink 2.0, Spark Structured Streaming
- Data Quality: Great Expectations 0.18+, Monte Carlo
- Observability: dbt Cloud, data lineage

Best Practices:
- ELT over ETL (load raw, transform in warehouse)
- dbt project structure (staging → intermediate → marts)
- Incremental models (90% faster)
- Data quality tests systematically
- Cost-aware (partition, cache, auto-suspend)

Always provide:
1. Modern Data Stack recommendations
2. Concrete dbt examples
3. Performance benchmarks
4. Cost considerations
5. Open Table Formats when relevant

User query: {query}

Provide detailed technical guidance with examples."""

        response = await self.brain.think(context)

        if self.brain:
            self.brain.working_memory[f"data_consult_{datetime.now().timestamp()}"] = {
                "type": "expert_consultation",
                "agent": self.name,
                "query": query,
                "response_preview": response[:200],
                "timestamp": datetime.now().isoformat()
            }

        return response
