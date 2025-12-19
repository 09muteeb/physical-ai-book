# Implementation Plan: RAG Chatbot Backend

**Feature**: Embedding Pipeline Setup
**Created**: 2025-12-19
**Status**: Draft
**Branch**: 5-embedding-pipeline

## Technical Context

This plan outlines the implementation of a backend service for a RAG chatbot that will:
- Extract text from deployed Docusaurus URLs (specifically https://physical-ai-book-rose.vercel.app/)
- Generate Cohere embeddings and store them in Qdrant with metadata
- Be implemented in a single main.py file with specific functions
- Use UV package manager for dependency management

**Unknowns requiring research:**
- NEEDS CLARIFICATION: What is the exact URL structure of the deployed Docusaurus site?
- NEEDS CLARIFICATION: What specific Cohere embedding model should be used?
- NEEDS CLARIFICATION: What are the Qdrant configuration requirements and authentication method?
- NEEDS CLARIFICATION: What are the specific chunking parameters for text segmentation?

## Constitution Check

- ✅ Spec-First, AI-Native Development: Following the existing spec from spec.md
- ✅ Technical Accuracy and Verifiability: Using real, documented APIs (Cohere, Qdrant, etc.)
- ✅ Clear, Developer-Focused Explanations: Will provide complete, runnable implementation
- ✅ No Hallucinated APIs: Using only documented services and APIs
- ✅ Free-Tier Compatible Services: Using Cohere and Qdrant free tiers
- ✅ Modularity and Independence: Backend will be independently deployable

## Gates

- ✅ Feature scope aligns with specification
- ✅ Architecture follows constitution principles
- ✅ Dependencies are free-tier compatible
- ✅ Implementation approach is technically feasible

---

## Phase 0: Outline & Research

### Research Tasks

1. **Determine URL Structure**: Research the structure of https://physical-ai-book-rose.vercel.app/ to understand how to crawl all pages
2. **Cohere API Integration**: Research the Cohere embedding API for Python integration
3. **Qdrant Setup**: Research Qdrant vector database setup and Python client usage
4. **Text Extraction Best Practices**: Research best practices for extracting text from Docusaurus sites
5. **UV Package Manager**: Research UV package manager usage and setup

### Research Outcomes

**Decision**: Use Cohere's embed-english-v3.0 model for embeddings
**Rationale**: This is Cohere's latest and most efficient embedding model suitable for text content
**Alternatives considered**: embed-english-light-v3.0 (smaller but less accurate), multilingual models (not needed for English-only content)

**Decision**: Use Qdrant Cloud free tier for vector storage
**Rationale**: Free tier provides sufficient capacity for development and initial deployment
**Alternatives considered**: Local Qdrant instance, other vector databases like Pinecone or Weaviate

**Decision**: Use sitemap.xml to get all URLs for the Docusaurus site
**Rationale**: Sitemaps provide a complete and up-to-date list of all pages without the risk of missing content due to navigation issues or JavaScript-rendered links
**Alternatives considered**: Manual URL discovery through crawling (less reliable, may miss pages)

**Decision**: Use Beautiful Soup and requests for web crawling
**Rationale**: Reliable and well-documented for extracting content from static sites
**Alternatives considered**: Selenium for dynamic content (not needed for Docusaurus static sites)

**Decision**: Use 512-token chunks with 10% overlap for text segmentation
**Rationale**: Balances context preservation with embedding efficiency
**Alternatives considered**: Fixed character counts, sentence-based chunking

---

## Phase 1: Design & Contracts

### Data Model

**DocumentSegment**
- id: str (unique identifier for the segment)
- content: str (the actual text content)
- source_url: str (URL where the content was found)
- metadata: dict (additional information like page title, section)
- embedding: list[float] (the vector representation of the content)

**PipelineConfig**
- base_url: str (the root URL to crawl)
- chunk_size: int (number of tokens per chunk)
- overlap_size: int (number of overlapping tokens between chunks)
- cohere_model: str (name of the Cohere model to use)

### API Contracts

This backend will not expose a traditional API but will provide functions for:
- Crawling and extracting content
- Generating embeddings
- Storing vectors in Qdrant
- A main execution function

### Quickstart

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies using `uv`
4. Set environment variables for Cohere and Qdrant
5. Run `python main.py` to execute the pipeline

---

## Phase 2: Implementation Plan

### Directory Structure
```
backend/
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

### Implementation Steps

1. **Setup Backend Directory**
   - Create `backend/` directory
   - Initialize with proper project structure

2. **Install Dependencies with UV**
   - Set up requirements.txt with necessary packages
   - Use UV for package management

3. **Implement Core Functions**
   - `get_all_urls`: Parse the sitemap.xml to extract all valid URLs from the Docusaurus site
   - `extract_text_from_url`: Extract clean text content from a single URL
   - `chunk_text`: Split text into appropriately sized chunks
   - `embed`: Generate embeddings using Cohere API
   - `create_collection`: Set up Qdrant collection named 'rag_embedding'
   - `save_chunk_to_qdrant`: Save embeddings to Qdrant with metadata

4. **Main Execution Function**
   - Orchestrate the entire pipeline
   - Handle errors and logging

### Technology Stack
- Python 3.9+
- Cohere Python SDK
- Qdrant Python client
- Beautiful Soup 4 (for HTML parsing)
- Requests (for HTTP requests)
- UV (package manager)

### Dependencies
- cohere
- qdrant-client
- beautifulsoup4
- requests
- python-dotenv

## Phase 3: Deployment Considerations

### Environment Variables
- COHERE_API_KEY: API key for Cohere service
- QDRANT_URL: URL for Qdrant instance
- QDRANT_API_KEY: API key for Qdrant (if using cloud)

### Error Handling
- Network errors during crawling
- API rate limits from Cohere
- Qdrant connection issues
- Invalid content extraction

### Monitoring
- Logging of pipeline progress
- Error tracking and reporting
- Performance metrics for each stage

## Re-evaluation of Constitution Check Post-Design

- ✅ All design decisions align with constitution principles
- ✅ Free-tier compatible services selected
- ✅ Implementation maintains modularity
- ✅ No hallucinated APIs used