# RAG Agent with OpenAI and Qdrant

This module implements a Retrieval-Augmented Generation (RAG) agent that combines OpenAI's language models with Qdrant vector database to provide accurate answers based on retrieved context from the Physical AI book.

## Features

- FastAPI endpoints for querying the RAG system
- Integration with OpenAI's GPT models for answer generation
- Qdrant vector database integration for semantic search
- Context-aware answer generation based strictly on retrieved information
- Health check and monitoring endpoints

## Requirements

- Python 3.8+
- OpenAI API key
- Qdrant database connection
- Cohere API key (for embedding generation, if needed)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```env
OPENAI_API_KEY=your_openai_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
COHERE_API_KEY=your_cohere_api_key
```

## Usage

### Running the API Server

```bash
cd backend
uvicorn rag_agent:app --host 0.0.0.0 --port 8000 --reload
```

### API Endpoints

- `GET /` - Root endpoint (health check)
- `GET /health` - Detailed health check
- `POST /query` - Query the RAG agent

### Query Example

```json
{
  "query": "What is Physical AI?",
  "max_results": 5,
  "similarity_threshold": 0.5
}
```

Response:
```json
{
  "query": "What is Physical AI?",
  "answer": "Physical AI is a field that combines artificial intelligence with physical systems...",
  "retrieved_chunks": [
    {
      "id": "chunk-id",
      "content": "Physical AI represents the integration of AI algorithms...",
      "source_url": "https://physical-ai-book-rose.vercel.app/...",
      "similarity_score": 0.85,
      "metadata": {
        "title": "Introduction to Physical AI",
        "created_at": "2025-12-19T10:30:00"
      }
    }
  ],
  "timestamp": "2025-12-19T15:30:00.123456",
  "sources": [
    "https://physical-ai-book-rose.vercel.app/introduction"
  ]
}
```

## Architecture

The RAG agent follows this workflow:

1. **Query Processing**: User query is received via FastAPI endpoint
2. **Context Retrieval**: Similarity search performed in Qdrant database
3. **Answer Generation**: OpenAI model generates answer based on retrieved context
4. **Response Formation**: Structured response with answer and metadata is returned

## Testing

Run the test suite:
```bash
python test_rag_agent.py
```

Test the API endpoints:
```bash
python api_client.py
```

## Environment Variables

- `OPENAI_API_KEY`: Required for OpenAI API access
- `QDRANT_URL`: URL for Qdrant database connection
- `QDRANT_API_KEY`: API key for Qdrant authentication
- `COHERE_API_KEY`: API key for Cohere (used in retrieval functions)