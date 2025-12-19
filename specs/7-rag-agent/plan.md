# Implementation Plan: RAG Agent with OpenAI and FastAPI

## Technical Context

### Current State
- Backend service exists that extracts text from Docusaurus URLs
- Cohere embeddings are generated and stored in Qdrant
- Retrieval validation system is implemented
- Need to create a RAG agent that uses OpenAI for answer generation

### Target State
- FastAPI service for RAG backend
- OpenAI agent that retrieves context from Qdrant
- Answers generated strictly from retrieved context
- Proper handling of "not found in context" responses

### Architecture Components
- FastAPI application with endpoints
- OpenAI integration for answer generation
- Qdrant integration for context retrieval
- RAG agent orchestrating the workflow

## Constitution Check

Based on the project constitution principles:
- ✅ Minimal Viable Change: Implement only necessary components for RAG agent
- ✅ Testable Requirements: Each component will have test coverage
- ✅ Clear Boundaries: Well-defined interfaces between components
- ✅ Error Handling: Proper error responses and logging
- ✅ Security: API keys handled securely via environment variables

## Phase 0: Research

### Research Tasks Completed

**Decision**: Use FastAPI for web framework
**Rationale**: FastAPI provides automatic API documentation, type validation, and async support
**Alternatives considered**: Flask, Django - FastAPI chosen for better performance and modern features

**Decision**: Use OpenAI GPT-3.5-turbo for answer generation
**Rationale**: Good balance of quality and cost, well-documented API
**Alternatives considered**: GPT-4, other LLM providers - GPT-3.5-turbo for initial implementation

**Decision**: Reuse existing Qdrant retrieval functions
**Rationale**: Leverage existing codebase and maintain consistency
**Alternatives considered**: New retrieval implementation - reuse preferred for maintainability

## Phase 1: Design

### Data Model

#### QueryRequest
- query: str (user's question)
- max_results: int (default 5, max results to retrieve)
- similarity_threshold: float (default 0.5, minimum similarity score)

#### QueryResponse
- query: str (original user query)
- answer: str (generated answer from OpenAI)
- retrieved_chunks: List[Dict] (context chunks retrieved from Qdrant)
- timestamp: str (ISO format timestamp)
- sources: List[str] (unique source URLs)

#### QueryResult (from existing code)
- id: str (Qdrant point ID)
- content: str (retrieved text content)
- source_url: str (URL of source document)
- metadata: Dict (additional metadata)
- similarity_score: float (cosine similarity score)

### API Contracts

#### GET /health
- Description: Health check endpoint
- Response: 200 with service status information

#### POST /query
- Description: Query the RAG agent
- Request body: QueryRequest schema
- Response: 200 with QueryResponse schema
- Error responses: 400 for bad requests, 500 for internal errors

## Implementation Approach

### Components to Implement

1. **FastAPI Application Setup**
   - Initialize FastAPI app with proper configuration
   - Add health check endpoint
   - Set up dependency injection

2. **Qdrant Integration**
   - Connect to existing retrieval functions
   - Implement context retrieval with configurable parameters

3. **OpenAI Integration**
   - Set up OpenAI client with API key
   - Create prompt engineering for context-based answers
   - Implement answer generation with proper error handling

4. **RAG Agent Class**
   - Orchestrate retrieval and generation workflow
   - Handle "not found in context" responses
   - Format responses appropriately

5. **API Endpoints**
   - Create /query endpoint that accepts user queries
   - Validate input parameters
   - Return structured responses

## Risk Mitigation

- **API Key Security**: Store API keys in environment variables, never in code
- **Rate Limiting**: Implement proper error handling for API rate limits
- **Context Quality**: Validate retrieved context before sending to LLM
- **Performance**: Implement timeouts and connection pooling
- **Error Handling**: Graceful degradation when services are unavailable