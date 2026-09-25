# 🚀 Enterprise Agentic RAG

> **Production-grade, scalable Agentic RAG system for enterprise document intelligence**, built with **LangGraph, Portkey, Gemini Embeddings, Qdrant, FlashRank, NeMo Guardrails, RAGAS, LangSmith, and Pydantic Logfire**.

Enterprise Agentic RAG is designed to retrieve reliable information from large document collections while reducing the impact of irrelevant, noisy, malicious, or off-topic data.

The system combines **agentic planning, semantic retrieval, local reranking, safety guardrails, LLM gateway routing, conversation memory, observability, and automated evaluation** into a production-oriented RAG pipeline.

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Agentic Intelligence Flow](#-agentic-intelligence-flow)
- [End-to-End Pipeline](#-end-to-end-pipeline)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Data Ingestion Pipeline](#-data-ingestion-pipeline)
- [Retrieval Pipeline](#-retrieval-pipeline)
- [Agent Architecture](#-agent-architecture)
- [Guardrails](#-guardrails)
- [LLM Gateway](#-llm-gateway)
- [Observability](#-observability)
- [Evaluation](#-evaluation)
- [Installation](#-installation)
- [Environment Variables](#-environment-variables)
- [Running the Project](#-running-the-project)
- [API](#-api)
- [Documentation](#-documentation)
- [Enterprise Design Considerations](#-enterprise-design-considerations)
- [Future Improvements](#-future-improvements)

---

# 🎯 Overview

Traditional RAG systems generally follow:

```text
User Query
    ↓
Embedding
    ↓
Vector Search
    ↓
LLM
    ↓
Answer
```

This project extends that architecture into an **Agentic RAG pipeline**:

```text
                         ┌──────────────────┐
                         │    User Query    │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │   NeMo Guardrails│
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ LangGraph Planner│
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │     Retrieval    │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ Qdrant Vector DB │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ FlashRank Rerank │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ LangGraph Agent  │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │  Response LLM    │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ Output Guardrail │
                         └────────┬─────────┘
                                  ↓
                         ┌──────────────────┐
                         │ Final Response   │
                         └──────────────────┘
```

The system is specifically designed to distinguish between:

- ✅ **Relevant / True Data**
- ❌ **Irrelevant / Noisy Data**
- 🛡️ **Malicious or Prompt-Injection Data**
- 🚫 **Off-topic Queries**

---

# ✨ Key Features

## 🤖 Agentic Intelligence

Built using **LangGraph** to support:

- Multi-step reasoning
- Query planning
- Cyclic workflows
- Conditional routing
- Retrieval decisions
- Conversation-aware planning
- Memory-aware responses
- Planner → Retriever → Responder architecture

---

## 🛡️ NeMo Guardrails

Safety checks are applied **before retrieval** and during response generation.

The guardrail layer helps detect:

- Off-topic questions
- Prompt injection
- Jailbreak attempts
- Unsafe inputs
- Retrieval manipulation
- Unsafe model outputs

```text
User
 ↓
Input Guardrail
 ↓
Allowed?
 ├── No  → Block
 └── Yes
       ↓
   RAG Pipeline
       ↓
Output Guardrail
       ↓
Response
```

---

## 🔎 Enterprise Retrieval

The retrieval pipeline combines:

### Vector Search

**Qdrant Cloud** provides scalable vector similarity search.

### Semantic Reranking

**FlashRank** performs local reranking after vector retrieval.

```text
Query
 ↓
Gemini Embedding
 ↓
Qdrant Top-K
 ↓
Candidate Documents
 ↓
FlashRank
 ↓
Top Relevant Context
```

This helps reduce irrelevant results returned by pure vector similarity search.

---

## 🧠 Gemini Embeddings

The system uses:

```text
gemini-embedding-2-preview
```

with **3072-dimensional embeddings** through `langchain-google-genai`.

The same embedding strategy is used during document indexing and query retrieval.

---

## 🌐 Portkey LLM Gateway

LLM requests are routed through **Portkey**.

The gateway provides:

- Centralized LLM access
- Request routing
- Fallback handling
- Provider abstraction
- Observability
- Production-oriented model management

Example:

```text
Application
     ↓
Portkey Gateway
     ↓
Primary Groq Key
     │
     └── Failure / Rate Limit
              ↓
       Backup Groq Key
```

---

## 📊 Observability

The system integrates:

### Pydantic Logfire

Used for application-level tracing and nested execution visibility.

### LangSmith

Used for:

- LangChain tracing
- LangGraph execution
- Agent node inspection
- Prompt/response tracing
- Debugging
- RAG workflow analysis

Example trace:

```text
Request
 ├── Guardrail
 ├── Planner
 │    └── LLM Call
 ├── Retriever
 │    ├── Embedding
 │    ├── Qdrant Search
 │    └── FlashRank
 ├── Responder
 │    └── LLM Call
 └── Output Guardrail
```

---

# 🧠 Agentic Intelligence Flow

The LangGraph workflow follows a planner-driven architecture:

```text
                    ┌───────────────┐
                    │  User Query   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ Input Guardrail│
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │    Planner    │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │   Retriever   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ Qdrant Search │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │   FlashRank   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │   Responder   │
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │Output Guardrail│
                    └───────┬───────┘
                            ↓
                    ┌───────────────┐
                    │ Final Answer  │
                    └───────────────┘
```

Because the workflow is implemented with LangGraph, nodes can be extended with conditional routing and cyclic execution when required.

---

# 🔄 End-to-End Pipeline

## 1. Document Ingestion

Documents are loaded locally from:

```text
DATA/
```

Supported formats:

- PDF
- HTML
- TXT
- DOCX
- PPTX

No external OCR service is required for the supported parsing pipeline.

---

## 2. Document Parsing

Documents are converted into normalized text.

Example:

```text
PDF
 ↓
pypdf / pdfplumber
 ↓
Raw Text
```

---

## 3. Chunking

The parsed documents are split into manageable chunks.

Current configuration:

```text
Maximum chunk size: ~1500 characters
```

The ingestion pipeline stores processed information in:

```text
processed_data/
```

---

## 4. Embedding

Each chunk is converted into a vector using:

```text
Gemini Embedding
        ↓
3072-dimensional vector
```

---

## 5. Vector Indexing

Vectors and metadata are stored in:

```text
Qdrant Cloud
```

---

## 6. Query Processing

A user query enters the application through FastAPI.

```text
User Query
    ↓
NeMo Guardrails
    ↓
Planner
    ↓
Query Embedding
    ↓
Qdrant Search
```

---

## 7. Semantic Reranking

Retrieved candidates are passed to FlashRank:

```text
Qdrant Top-K
     ↓
FlashRank
     ↓
Semantic Relevance
     ↓
Top Documents
```

---

## 8. Response Generation

The selected context is passed to the responder agent.

```text
Context + Query
       ↓
Portkey
       ↓
Groq / Llama
       ↓
Generated Response
```

---

## 9. Output Validation

The generated response passes through the output safety layer before being returned to the user.

---

# 🧰 Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| API | FastAPI |
| Agent Orchestration | LangGraph |
| LLM Framework | LangChain |
| LLM Gateway | Portkey |
| Primary LLM | Groq / Llama 3.3 70B |
| Embeddings | Gemini `gemini-embedding-2-preview` |
| Vector Database | Qdrant Cloud |
| Reranking | FlashRank |
| Guardrails | NeMo Guardrails |
| PDF Parsing | pypdf / pdfplumber |
| HTML Parsing | Local HTML parser |
| DOCX Parsing | python-docx |
| PPTX Parsing | python-pptx |
| Observability | Pydantic Logfire |
| LLM Tracing | LangSmith |
| Evaluation | RAGAS |
| Evaluation UI | Streamlit |
| Frontend / Demo | Streamlit |
| Configuration | Python `.env` |

---

# 📁 Project Structure

```text
enterprise-agentic-rag/
│
├── app/
│   │
│   ├── agents/
│   │   └── nodes/
│   │       ├── planner.py
│   │       ├── retriever.py
│   │       └── responder.py
│   │
│   ├── gateway/
│   │   └── portkey.py
│   │
│   ├── guardrails/
│   │   ├── config/
│   │   ├── rails/
│   │   └── ...
│   │
│   ├── ingestion/
│   │   ├── chunking/
│   │   │   └── ...
│   │   │
│   │   ├── loaders/
│   │   │   ├── pdf_loader.py
│   │   │   ├── html_loader.py
│   │   │   ├── txt_loader.py
│   │   │   ├── docx_loader.py
│   │   │   └── pptx_loader.py
│   │   │
│   │   └── processor.py
│   │
│   ├── services/
│   │   └── retrieval/
│   │       ├── embeddings.py
│   │       ├── qdrant.py
│   │       └── reranker.py
│   │
│   ├── config.py
│   └── main.py
│
├── evals/
│   ├── ...
│   └── app.py
│
├── ui/
│   └── app.py
│
├── DATA/
│   ├── true_data/
│   └── noisy_data/
│
├── processed_data/
│   └── ...
│
├── docs/
│   ├── 01-system-overview.md
│   ├── 02-ingestion-engine.md
│   ├── 03-node-intelligence.md
│   ├── 04-observability.md
│   ├── 05-environment-variables.md
│   ├── 06-known-gotchas.md
│   ├── 07-flashrank-reranking.md
│   ├── 08-guardrails.md
│   ├── 09-llm-gateway.md
│   ├── 10-evals.md
│   └── 11-evals-pipeline.md
│
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 📥 Data Ingestion Pipeline

Run:

```bash
python -m app.ingestion.processor DATA --wipe
```

### `--wipe`

Drops and recreates the Qdrant collection before indexing.

Use this when performing a fresh indexing operation.

```bash
python -m app.ingestion.processor DATA --wipe
```

### Without `--wipe`

Existing vectors are preserved and new documents are appended.

```bash
python -m app.ingestion.processor DATA
```

Pipeline:

```text
DATA/
 ↓
Document Loader
 ↓
Text Extraction
 ↓
Cleaning
 ↓
Chunking
 ↓
Metadata Generation
 ↓
Gemini Embeddings
 ↓
Qdrant
```

---

# 🔍 Retrieval Pipeline

The retrieval system uses a two-stage architecture.

### Stage 1 — Vector Retrieval

```text
Query
 ↓
Gemini Embedding
 ↓
Qdrant Similarity Search
 ↓
Top-K Candidates
```

### Stage 2 — Semantic Reranking

```text
Top-K Candidates
       ↓
    FlashRank
       ↓
Relevance Ranking
       ↓
Final Context
```

This approach separates **fast candidate retrieval** from **deeper semantic relevance ranking**.

---

# 🤖 Agent Architecture

The core agent workflow contains three major nodes.

## Planner

Responsible for:

- Understanding the user's request
- Using conversation history
- Determining retrieval requirements
- Creating the retrieval plan
- Routing the workflow

```text
User Query
    ↓
Planner
    ↓
Retrieval Plan
```

---

## Retriever

Responsible for:

- Query embedding
- Vector search
- Metadata filtering
- Candidate selection
- Semantic reranking

```text
Query
 ↓
Embedding
 ↓
Qdrant
 ↓
FlashRank
 ↓
Relevant Context
```

---

## Responder

Responsible for:

- Combining query and retrieved context
- Generating the final answer
- Following response constraints
- Producing grounded responses

```text
Query + Context
      ↓
   Responder
      ↓
   Answer
```

---

# 🛡️ Guardrails

NeMo Guardrails is positioned at the boundary of the RAG system.

## Input Protection

Before retrieval:

```text
User Input
    ↓
NeMo Guardrails
    ↓
┌───────────────┐
│ Safe Request? │
└───────┬───────┘
        │
   ┌────┴────┐
   ↓         ↓
  YES        NO
   ↓         ↓
  RAG       BLOCK
```

The guardrail layer is intended to detect:

- Prompt injection
- Jailbreak attempts
- Off-topic requests
- Unsafe instructions
- Retrieval manipulation

## Output Protection

Generated responses can also be inspected before being returned to the client.

---

# 🌐 Portkey LLM Gateway

Portkey acts as the centralized LLM gateway.

```text
                   ┌───────────────┐
                   │ FastAPI / UI  │
                   └───────┬───────┘
                           ↓
                    ┌─────────────┐
                    │   Portkey   │
                    └──────┬──────┘
                           ↓
                 ┌──────────────────┐
                 │ Primary Groq Key │
                 └────────┬─────────┘
                          │
                    Failure / Limit
                          ↓
                 ┌──────────────────┐
                 │ Backup Groq Key  │
                 └──────────────────┘
```

This provides an abstraction layer between the application and the underlying LLM provider.

---

# 📊 Observability

## Pydantic Logfire

Used for application tracing and execution visibility.

Useful for identifying:

- Slow operations
- Failed nodes
- Retrieval latency
- LLM latency
- Exceptions
- Nested execution

## LangSmith

Used for LangChain/LangGraph observability.

The project tracks:

```text
Request
 ├── Planner
 ├── Retriever
 │    ├── Embedding
 │    ├── Vector Search
 │    └── Reranking
 └── Responder
```

This makes it easier to debug agent behavior and RAG quality.

---

# 🧪 Evaluation

The project includes a dedicated evaluation pipeline using **RAGAS**.

The evaluation suite contains multiple RAG quality metrics along with a custom tool-correctness evaluation.

Example evaluation flow:

```text
Evaluation Dataset
        ↓
FastAPI RAG Pipeline
        ↓
Generated Answers
        ↓
RAGAS Evaluation
        ↓
Metrics
        ↓
Streamlit Dashboard
```

The evaluation application can be launched with:

```bash
streamlit run evals/app.py
```

> The FastAPI backend should be running before starting the evaluation application.

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>

cd enterprise-agentic-rag
```

---

## 2. Create Virtual Environment

### Windows

```powershell
python -m venv tenvv
.\tenvv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv tenvv
source tenvv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

```env
# ==========================================
# GROQ
# ==========================================

GROQ_API_KEY=""
GROQ_FALLBACK_API_KEY=""


# ==========================================
# PORTKEY
# ==========================================

PORTKEY_API_KEY=""


# ==========================================
# QDRANT
# ==========================================

QDRANT_API_KEY=""
QDRANT_CLUSTER_ENDPOINT=""


# ==========================================
# PYDANTIC LOGFIRE
# ==========================================

LOGFIRE_TOKEN=""


# ==========================================
# LANGSMITH
# ==========================================

LANGSMITH_TRACING=true
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY=""
LANGSMITH_PROJECT=""


# ==========================================
# STREAMLIT → FASTAPI
# ==========================================

BACKEND_URL="http://localhost:8000"


# ==========================================
# EVALUATION
# ==========================================

JUDGE_GROQ=""


# ==========================================
# GEMINI EMBEDDINGS
# ==========================================

GEMINI_API_KEY=""
```

### ⚠️ Security

Never commit `.env` to GitHub.

Add it to `.gitignore`:

```gitignore
.env
.env.*
!.env.example
__pycache__/
*.pyc
.venv/
tenvv/
.streamlit/secrets.toml
processed_data/
```

---

# 🚀 Running the Project

## Step 1 — Index Documents

```bash
python -m app.ingestion.processor DATA --wipe
```

---

## Step 2 — Start FastAPI

Open Terminal 1:

```bash
uvicorn app.main:app --reload --port 8000
```

API will be available at:

```text
http://localhost:8000
```

FastAPI Swagger documentation:

```text
http://localhost:8000/docs
```

---

## Step 3 — Start Streamlit UI

Open Terminal 2:

```bash
streamlit run ui/app.py
```

---

## Step 4 — Start Evaluation UI

Optional:

```bash
streamlit run evals/app.py
```

Make sure FastAPI is running before starting the evaluation pipeline.

---

# 🔌 API

The main application exposes a query endpoint:

```text
POST /query
```

Conceptual request:

```json
{
  "query": "Explain the authentication architecture."
}
```

Conceptual response:

```json
{
  "answer": "The authentication system uses...",
  "sources": [
    {
      "document": "authentication.pdf",
      "score": 0.91
    }
  ]
}
```

> Request and response schemas should be updated here if the API contract changes.

---

# 📚 Documentation

Detailed architecture and operational documentation is available under:

```text
docs/
```

| # | Document | Description |
|---|---|---|
| 01 | System Overview | High-level architecture and end-to-end flow |
| 02 | Ingestion Engine | Document parsing and indexing pipeline |
| 03 | Node Intelligence | Planner, Retriever and Responder internals |
| 04 | Observability | Logfire and LangSmith tracing |
| 05 | Environment Variables | Configuration reference |
| 06 | Known Gotchas | Architectural decisions and non-obvious issues |
| 07 | FlashRank Reranking | Semantic reranking architecture |
| 08 | Guardrails | NeMo Guardrails implementation |
| 09 | LLM Gateway | Portkey routing and fallback |
| 10 | Evals | RAGAS metrics and evaluation theory |
| 11 | Evals Pipeline | Live evaluation pipeline and Streamlit demo |

---

# 🏢 Enterprise Design Considerations

This project demonstrates several patterns commonly required in production RAG systems.

### Scalability

```text
FastAPI
   ↓
Agent Layer
   ↓
Qdrant
   ↓
LLM Gateway
```

Components are separated so individual services can be scaled independently.

### Reliability

LLM fallback routing helps reduce dependency on a single API key/provider configuration.

### Security

Guardrails provide an additional boundary around user inputs and generated responses.

### Retrieval Quality

Combining:

```text
Vector Search
+
Semantic Reranking
```

provides a stronger retrieval pipeline than relying solely on vector similarity.

### Observability

Tracing across agent nodes makes the system easier to debug and operate.

### Evaluation

RAGAS and custom evaluation metrics provide a repeatable way to measure RAG quality rather than relying only on manual testing.

---

# 🔮 Future Improvements

Potential extensions include:

- [ ] Hybrid search — dense + sparse retrieval
- [ ] BM25 retrieval
- [ ] Advanced metadata filtering
- [ ] Query rewriting
- [ ] Multi-query retrieval
- [ ] Parent-document retrieval
- [ ] Context compression
- [ ] Adaptive Top-K
- [ ] Cross-encoder reranking
- [ ] Distributed ingestion workers
- [ ] Background ingestion with Celery / RabbitMQ
- [ ] Redis caching
- [ ] Authentication and RBAC
- [ ] Multi-tenant Qdrant collections
- [ ] Document versioning
- [ ] Incremental indexing
- [ ] CI/CD pipeline
- [ ] Docker deployment
- [ ] Kubernetes deployment
- [ ] Production rate limiting
- [ ] Advanced evaluation datasets
- [ ] Human feedback loop

---

# 🎯 Why This Project?

This project demonstrates a production-oriented approach to **Enterprise RAG and Agentic AI**, combining:

```text
                 Enterprise Agentic RAG
                         │
       ┌─────────────────┼─────────────────┐
       ↓                 ↓                 ↓
   Agentic AI        Retrieval          Safety
       │                 │                 │
   LangGraph         Qdrant            Guardrails
   Planning          FlashRank         NeMo
   Memory            Gemini
       │                 │
       └─────────┬───────┘
                 ↓
            LLM Gateway
              Portkey
                 ↓
             Groq LLM
                 ↓
          Observability
        Logfire + LangSmith
                 ↓
             Evaluation
                RAGAS
```

The architecture is intended as a foundation for building scalable enterprise document intelligence applications.

---

# ⭐ Highlights

- 🤖 **Agentic RAG with LangGraph**
- 🔍 **Qdrant vector search**
- 🧠 **Gemini 3072-dimensional embeddings**
- ⚡ **Local FlashRank reranking**
- 🛡️ **NeMo Guardrails**
- 🌐 **Portkey LLM Gateway**
- 🔄 **Groq fallback routing**
- 📊 **LangSmith + Pydantic Logfire**
- 🧪 **RAGAS evaluation**
- 📄 **Local document parsing**
- 🚀 **FastAPI backend**
- 🎨 **Streamlit interfaces**
- 🏢 **Enterprise-oriented architecture**

---

## 📄 License

Add your preferred license here, for example:

```text
MIT License
```

---

## 👨‍💻 Author

**Gyanesh Shukla**

Full Stack Developer | AI / GenAI Engineer

- MERN Stack
- FastAPI
- LangChain
- LangGraph
- RAG
- Agentic AI
- Vector Databases
- LLM Applications

---

> **Built for High-Scale Enterprise Document Intelligence.**