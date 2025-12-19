# RAG Agent with OpenAI Integration

The RAG (Retrieval-Augmented Generation) agent provides an intelligent question-answering system that combines OpenAI's language models with Qdrant vector database to provide accurate answers based on retrieved context from the Physical AI book.

## Features

- FastAPI endpoints for querying the RAG system
- Integration with OpenAI's GPT models for answer generation
- Qdrant vector database integration for semantic search
- Context-aware answer generation based strictly on retrieved information
- Health check and monitoring endpoints

## Requirements

- Python 3.8+
- OpenAI API key
- Qdrant database connection (with existing embeddings)
- Cohere API key (for embedding generation, if needed)

## Installation

Additional dependencies for the RAG agent:
```bash
pip install fastapi uvicorn[standard] openai==0.28.1 pydantic
```

## Usage

Run the RAG agent API server:
```bash
uvicorn rag_agent:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

- `GET /` - Root endpoint (health check)
- `GET /health` - Detailed health check
- `POST /query` - Query the RAG agent with questions

## Query Example

```json
{
  "query": "What is Physical AI?",
  "max_results": 5,
  "similarity_threshold": 0.5
}
```

## Environment Variables

Additional environment variables needed:
- `OPENAI_API_KEY`: API key for OpenAI access