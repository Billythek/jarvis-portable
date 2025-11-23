"""
AI Engineer Agent - LLM & RAG Expert

Expert en intelligence artificielle et systemes LLM:
- LLMs: Llama 4 Scout/Omni, Mistral Medium 3, Qwen 3, DeepSeek-V3
- Frameworks: LangGraph v1.0, AutoGen v0.4, CrewAI v1.0
- RAG Advanced: SELF-RAG, SPLICE, HyDE, reranking (Cohere/BGE)
- Optimization: vLLM 0.8+ (24x faster), quantization W4A4/QuaRot/AWQ
- Fine-tuning: LoRA/QLoRA, DPO, IPO
- Vector DBs: Qdrant 1.12, Pinecone, Weaviate 1.28
- Observability: LangSmith, Arize Phoenix, Helicone

Focus: Production-ready LLM systems, RAG optimization, agent orchestration
"""

import asyncio
from datetime import datetime
from typing import Dict, Any

class AIEngineerAgent:
    """Agent expert en AI/ML et systemes LLM"""

    def __init__(self, name: str, brain=None):
        self.name = name
        self.brain = brain
        self.running = False
        self.expertise_domains = [
            "llm_engineering",
            "rag_systems",
            "autonomous_agents",
            "vector_databases",
            "llm_optimization",
            "fine_tuning",
            "prompt_engineering"
        ]

        self.knowledge_base = {
            "llm_models_2025": {
                "llama4_scout": "70B params, 128K context, fastest reasoning (1.2s/prompt)",
                "llama4_omni": "405B params, multimodal, 2M context window",
                "mistral_medium3": "Mixture of Experts, 8x better than GPT-4T",
                "qwen3": "Open-source champion, 236B params, coding excellence",
                "deepseek_v3": "671B params MoE, only 37B active, $1/M tokens"
            },
            "rag_architectures": {
                "self_rag": "Self-reflection + retrieval, 15% accuracy gain",
                "splice": "Semantic chunking, 40% better context relevance",
                "hyde": "Hypothetical document embeddings, no real docs needed",
                "reranking": "Cohere Rerank v3, BGE-reranker-v2, 2x precision",
                "multi_hop": "Iterative retrieval for complex questions"
            },
            "agent_frameworks": {
                "langgraph": "v1.0 stateful graphs, human-in-loop, checkpoints",
                "autogen": "v0.4 multi-agent conversations, group chat, code execution",
                "crewai": "v1.0 role-based agents, hierarchical tasks, tools",
                "swarm": "OpenAI experimental, lightweight agent orchestration"
            },
            "optimization": {
                "vllm": "0.8+ PagedAttention, 24x faster than HuggingFace",
                "quantization": "W4A4 (weights+activations 4-bit), QuaRot, AWQ",
                "batching": "Continuous batching for 10x throughput",
                "kv_cache": "Multi-query attention, grouped-query attention"
            },
            "vector_databases": {
                "qdrant": "1.12 fast filtering, 100M vectors <1s, Rust-based",
                "pinecone": "Serverless, auto-scaling, 2B vectors easy",
                "weaviate": "1.28 hybrid search (vector + BM25), generative search",
                "chroma": "Embedded DB, good for prototyping"
            }
        }

    async def start(self):
        """Demarre l'agent AI engineer"""
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

    async def design_rag_system(self, requirements: Dict[str, Any]) -> str:
        """Concoit un systeme RAG production-ready"""

        doc_volume = requirements.get("doc_count", 1000)
        query_complexity = requirements.get("complexity", "simple")  # simple, complex, multi_hop
        latency_req = requirements.get("latency_ms", 500)

        design = f"""
# Production RAG System Design

## Requirements Analysis
- Document Volume: {doc_volume:,} documents
- Query Complexity: {query_complexity}
- Latency Target: {latency_req}ms

## Recommended Architecture

### 1. Document Processing Pipeline

**Chunking Strategy**:
"""

        if doc_volume > 100000:
            design += """
**SPLICE Semantic Chunking** (for large corpus)
- Context-aware splitting (not fixed 512 tokens)
- Overlap: 10-15% for continuity
- Metadata: doc_id, section, page_num
- Processing: 1M docs in ~2 hours with parallel workers

```python
from langchain.text_splitter import SemanticChunker

chunker = SemanticChunker(
    embeddings=embeddings,
    breakpoint_threshold_type="percentile",  # Dynamic threshold
    breakpoint_threshold_amount=85
)
chunks = chunker.split_documents(documents)
```
"""
        else:
            design += """
**RecursiveCharacterTextSplitter** (standard approach)
- Chunk size: 512 tokens with 50 token overlap
- Separators: paragraphs -> sentences -> words
- Fast processing: ~1K docs/minute

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=50,
    separators=["\\n\\n", "\\n", ". ", " ", ""]
)
```
"""

        design += f"""

### 2. Embedding Model Selection
"""

        if latency_req < 200:
            design += """
**BGE-M3 (Fast + Multilingual)**
- 1024 dimensions
- 8192 context window
- Latency: ~50ms per query (batch 32)
- Support: 100+ languages
"""
        else:
            design += """
**OpenAI text-embedding-3-large**
- 3072 dimensions
- Best retrieval accuracy
- Latency: ~100-200ms
- Cost: $0.13/1M tokens
"""

        design += f"""

### 3. Vector Database
"""

        if doc_volume > 10_000_000:
            design += f"""
**Pinecone Serverless** (for >10M docs)
- Auto-scaling
- Handles {doc_volume:,} vectors easily
- P95 latency: <100ms
- Cost: $0.096/1M queries
- Metadata filtering: Fast hybrid search
"""
        elif doc_volume > 100_000:
            design += f"""
**Qdrant 1.12** (self-hosted, cost-efficient)
- Rust-based, ultra-fast
- {doc_volume:,} vectors: ~50ms P95 latency
- Advanced filtering (metadata + vector)
- Hardware: 16GB RAM sufficient
- Cost: $50-100/month server vs $500+ managed
"""
        else:
            design += """
**Weaviate 1.28** (best for <100K docs)
- Hybrid search (vector + BM25 keyword)
- Generative search (RAG built-in)
- Docker deployment: Easy setup
- Good for prototyping and medium scale
"""

        design += """

### 4. Retrieval Strategy
"""

        if query_complexity == "multi_hop":
            design += """
**Multi-Hop Retrieval** (complex questions)
1. Initial retrieval (top-20 chunks)
2. LLM extracts sub-questions
3. Iterative retrieval per sub-question
4. Combine results + rerank

```python
from langchain.chains import MultiRetrievalQAChain

# Example: "What's the revenue difference between Q1 2024 and Q1 2023?"
# Sub-Q1: "What was Q1 2024 revenue?"
# Sub-Q2: "What was Q1 2023 revenue?"
# Combine: Calculate difference
```
"""
        elif query_complexity == "complex":
            design += """
**SELF-RAG** (self-reflective retrieval)
- Retrieve top-10 chunks
- LLM judges relevance (reflection)
- Re-retrieve if needed
- 15% accuracy improvement

```python
# Pseudo-code
chunks = vector_db.search(query, k=10)
relevance_scores = llm.judge_relevance(query, chunks)
if avg(relevance_scores) < 0.7:
    # Reformulate query and retry
    new_query = llm.reformulate(query)
    chunks = vector_db.search(new_query, k=10)
```
"""
        else:
            design += """
**Standard Retrieval + Reranking**
- Retrieve top-20 chunks (recall-focused)
- Rerank with Cohere Rerank v3 (precision-focused)
- Return top-5 to LLM
- 2x better precision than vector search alone

```python
from cohere import Client

cohere_client = Client(api_key="...")

# Initial retrieval
chunks = vector_db.search(query, k=20)

# Rerank
reranked = cohere_client.rerank(
    query=query,
    documents=[c.text for c in chunks],
    top_n=5,
    model="rerank-v3"
)
```
"""

        design += """

### 5. LLM Selection for Generation
"""

        if latency_req < 1000:
            design += """
**Llama 4 Scout 70B** (fast inference)
- vLLM 0.8+ deployment
- Latency: ~800ms for 500 token response
- Throughput: 50 queries/sec with 1x A100
- Cost: $0.60/1M tokens (self-hosted) vs $2-5 API

```bash
# vLLM deployment
docker run --gpus all \\
  -v ~/.cache/huggingface:/root/.cache/huggingface \\
  -p 8000:8000 \\
  vllm/vllm-openai:latest \\
  --model meta-llama/Llama-4-Scout-70B \\
  --tensor-parallel-size 1
```
"""
        else:
            design += """
**Mistral Medium 3** (best quality)
- API-based (no infra management)
- Latency: ~2-3s for complex answers
- Cost: $2.70/1M tokens
- Best for accuracy-critical applications
"""

        design += f"""

## Complete RAG Pipeline Code

```python
from langchain_community.vectorstores import Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import VLLM

# 1. Initialize components
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

vector_db = Qdrant(
    collection_name="docs",
    embeddings=embeddings,
    url="http://localhost:6333"
)

llm = VLLM(
    model="meta-llama/Llama-4-Scout-70B",
    trust_remote_code=True,
    max_tokens=512,
    temperature=0.7
)

# 2. Create RAG chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",  # Or "map_reduce" for long contexts
    retriever=vector_db.as_retriever(
        search_kwargs={{"k": 5}}
    ),
    return_source_documents=True
)

# 3. Query
result = qa_chain({{"query": "Your question here"}})
print(result["result"])
print(f"Sources: {{len(result['source_documents'])}}")
```

## Performance Benchmarks
- Embedding: {50 if latency_req < 200 else 150}ms per query
- Vector search: {50 if doc_volume < 1000000 else 100}ms (P95)
- Reranking: 100ms (Cohere API)
- LLM generation: {800 if latency_req < 1000 else 2000}ms (500 tokens)
- **Total E2E latency**: {1100 if latency_req < 1000 else 2400}ms

## Cost Optimization
- Self-host embeddings: BGE-M3 (free vs $0.13/1M OpenAI)
- Self-host LLM: vLLM ($0.60/1M vs $2-5/1M API)
- Vector DB: Qdrant self-hosted ($50/mo vs $500+ Pinecone)
- **Total cost**: ~$100/month for 1M queries (vs $1000+ managed)

## Observability Stack
- **LangSmith**: Trace every LLM call, debug chains
- **Arize Phoenix**: RAG quality metrics (retrieval precision, context relevance)
- **Helicone**: Cost tracking, latency P50/P95/P99

```python
# LangSmith integration
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "rag-production"
```
"""

        return design

    async def design_agent_system(self, requirements: Dict[str, Any]) -> str:
        """Concoit un systeme d'agents autonomes"""

        agent_count = requirements.get("agent_count", 3)
        task_type = requirements.get("task_type", "research")  # research, coding, analysis

        design = f"""
# Autonomous Agent System Design

## Requirements
- Agent Count: {agent_count} specialized agents
- Task Type: {task_type}

## Framework Selection: LangGraph v1.0
"""

        design += """
**Why LangGraph**:
- Stateful graphs (persist agent state)
- Human-in-the-loop (approval gates)
- Checkpoints (resume from failures)
- Built-in memory (short + long term)

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver

# Define agent state
class AgentState(TypedDict):
    messages: List[Message]
    current_agent: str
    task_result: Optional[str]
    iterations: int

# Create graph
workflow = StateGraph(AgentState)

# Add agents as nodes
workflow.add_node("researcher", research_agent)
workflow.add_node("coder", coding_agent)
workflow.add_node("reviewer", review_agent)

# Define edges (agent transitions)
workflow.add_edge("researcher", "coder")
workflow.add_edge("coder", "reviewer")
workflow.add_conditional_edges(
    "reviewer",
    should_continue,  # Function that decides next step
    {
        "continue": "coder",  # Revision needed
        "end": END
    }
)

# Add checkpoints (persistence)
memory = SqliteSaver.from_conn_string(":memory:")
app = workflow.compile(checkpointer=memory)

# Run with human approval
config = {"configurable": {"thread_id": "1"}}
for output in app.stream(initial_state, config):
    print(output)
    # Human can inspect and approve before next step
```

## Agent Orchestration Patterns
"""

        if agent_count <= 3:
            design += """
**Sequential Pipeline** (3 agents)
- Agent 1 (Researcher) -> Agent 2 (Coder) -> Agent 3 (Reviewer)
- Clear handoffs, easy debugging
- Total time: Sum of agent times (~5-10 min)

```
[Research] -> [Code] -> [Review] -> [Done]
   2min        5min      3min      10min total
```
"""
        else:
            design += """
**Hierarchical Multi-Agent** (5+ agents)
- Manager agent coordinates specialists
- Parallel execution when possible
- Dynamic task allocation

```
                [Manager]
                    |
        +-----------+-----------+
        |           |           |
    [Research]  [Code]      [Test]
        |           |           |
        +-----[Synthesizer]-----+
```
"""

        design += """

## Agent Tools & Capabilities

### Research Agent Tools
```python
from langchain.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.tools import ArxivQueryRun

tools = [
    DuckDuckGoSearchRun(),
    WikipediaQueryRun(),
    ArxivQueryRun(),
    # Custom tools
    PythonREPLTool(),  # Execute code
    FileReadTool(),    # Read local files
]

research_agent = create_react_agent(
    llm=ChatOpenAI(model="gpt-4"),
    tools=tools,
    prompt=research_prompt
)
```

### Code Generation Agent
```python
from langchain.tools import PythonREPLTool

code_agent = create_react_agent(
    llm=ChatOpenAI(model="gpt-4"),
    tools=[
        PythonREPLTool(),
        ShellTool(),  # Run bash commands
        GitTool(),    # Git operations
    ],
    prompt=coding_prompt
)
```

## Memory Management

**Short-term Memory** (conversation buffer):
```python
from langchain.memory import ConversationBufferWindowMemory

memory = ConversationBufferWindowMemory(
    k=10,  # Last 10 messages
    return_messages=True
)
```

**Long-term Memory** (vector store):
```python
from langchain.memory import VectorStoreRetrieverMemory

long_term_memory = VectorStoreRetrieverMemory(
    retriever=vector_db.as_retriever(search_kwargs={"k": 5}),
)

# Agent can recall past experiences
similar_tasks = long_term_memory.load_memory_variables(
    {"query": "How did we solve similar problem before?"}
)
```

## Error Handling & Retries

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
async def agent_step(state):
    try:
        result = await agent.ainvoke(state)
        return result
    except Exception as e:
        print(f"Agent error: {e}")
        # Retry with exponential backoff
        raise
```

## Performance & Cost

**LLM Selection by Task**:
- Complex reasoning: GPT-4 ($30/1M tokens)
- Simple tasks: Llama 4 Scout ($0.60/1M tokens self-hosted)
- Code generation: Qwen 3 Coder (free, self-hosted)

**Expected Performance**:
- Research task: 2-5 min (3-5 LLM calls)
- Code generation: 3-8 min (5-10 LLM calls + execution)
- Total cost per task: $0.05-0.20 (with smart LLM routing)

## Observability

```python
from langsmith import Client

client = Client()

# Trace every agent action
with trace("agent_system", project_name="autonomous-agents"):
    result = await agent_system.run(task)

# View in LangSmith UI:
# - Agent decisions
# - Tool calls
# - Latency per step
# - Cost per agent
```

## Production Checklist
- [ ] Checkpointing enabled (resume from failures)
- [ ] Human-in-loop for critical decisions
- [ ] Rate limiting (avoid API throttling)
- [ ] Cost monitoring (alert if >$X per task)
- [ ] Error budget (max retries per agent)
- [ ] Logging (LangSmith or custom)
"""

        return design

    async def consult(self, query: str) -> str:
        """Consultation AI engineering experte"""
        if not self.brain:
            return "AI Engineer: Brain not connected"

        context = f"""You are an Expert AI Engineer with deep knowledge of:

LLM Models 2025:
- Llama 4 Scout/Omni (70B/405B, 128K-2M context)
- Mistral Medium 3 (8x better than GPT-4T)
- Qwen 3 (236B, coding excellence)
- DeepSeek-V3 (671B MoE, $1/M tokens)

RAG Systems:
- Advanced: SELF-RAG (self-reflection), SPLICE (semantic chunking)
- HyDE (hypothetical docs), Multi-hop retrieval
- Reranking: Cohere Rerank v3, BGE-reranker-v2
- Vector DBs: Qdrant 1.12, Pinecone serverless, Weaviate 1.28

Agent Frameworks:
- LangGraph v1.0 (stateful graphs, checkpoints, human-in-loop)
- AutoGen v0.4 (multi-agent conversations)
- CrewAI v1.0 (role-based, hierarchical)

Optimization:
- vLLM 0.8+ (24x faster inference, PagedAttention)
- Quantization: W4A4, QuaRot, AWQ
- Continuous batching (10x throughput)

Fine-tuning:
- LoRA/QLoRA (parameter-efficient)
- DPO/IPO (direct preference optimization)
- Supervised fine-tuning (SFT)

Observability:
- LangSmith (trace LLM calls)
- Arize Phoenix (RAG quality metrics)
- Helicone (cost tracking)

Always provide:
1. Production-ready architectures
2. Performance benchmarks (latency, cost)
3. Code examples with latest libraries
4. Trade-offs analysis (managed vs self-hosted)
5. Observability setup

User query: {query}

Provide detailed technical guidance with concrete examples and benchmarks."""

        response = await self.brain.think(context)

        if self.brain:
            self.brain.working_memory[f"ai_consult_{datetime.now().timestamp()}"] = {
                "type": "expert_consultation",
                "agent": self.name,
                "query": query,
                "response_preview": response[:200],
                "timestamp": datetime.now().isoformat()
            }

        return response
