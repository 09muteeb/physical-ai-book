# RAG Chatbot Backend

This backend service extracts text from deployed Docusaurus URLs, generates embeddings using Cohere, and stores them in Qdrant for RAG-based retrieval. It also includes validation tools to verify the retrieval pipeline functionality.

## Setup

1. Clone the repository
2. Navigate to the backend directory
3. Install dependencies using `uv`:
   ```bash
   uv pip install -r requirements.txt
   ```
   Or using pip:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` to add your API keys

## Usage

### Embedding Pipeline
Run the embedding pipeline to extract and store content:
```bash
python main.py
```

The pipeline will:
- Parse the sitemap at https://physical-ai-book-rose.vercel.app/sitemap.xml to get all page URLs
- Extract text content from all pages
- Chunk the text appropriately
- Generate embeddings using Cohere
- Store the embeddings in Qdrant

### Retrieval Validation
Validate the retrieval pipeline functionality:
```bash
python retrieval_validation.py
```

Run validation with a specific query:
```bash
python retrieval_validation.py --query "What is Physical AI?"
```

Run validation with queries from a specific category:
```bash
python retrieval_validation.py --category concept
```

Run consistency test on a query:
```bash
python retrieval_validation.py --consistency-test --test-query "What is ROS 2?"
```

## Configuration

The system can be configured using environment variables:

### General Configuration:
- `QDRANT_URL`: URL for Qdrant instance
- `QDRANT_API_KEY`: API key for Qdrant
- `COHERE_API_KEY`: API key for Cohere

### Validation Configuration:
- `QDRANT_COLLECTION_NAME`: Collection name (default: 'rag_embedding')
- `SIMILARITY_THRESHOLD`: Minimum similarity score (default: 0.5)
- `MAX_RESULTS`: Maximum results to return (default: 5)
- `CHUNK_SIZE_LIMIT`: Maximum payload size (default: 10000)
- `SIMILARITY_SEARCH_TIMEOUT`: Search timeout in seconds (default: 30)
- `CONNECTION_RETRY_ATTEMPTS`: Connection retry attempts (default: 3)
- `CONSISTENCY_RUNS`: Number of runs for consistency tests (default: 3)
- `MIN_CONTENT_CHARS`: Minimum content characters (default: 10)

## Validation Features

The retrieval validation system provides:
- Connection validation to Qdrant
- Similarity search functionality testing
- Content and metadata validation
- Consistency testing across multiple runs
- Performance metrics reporting
- Comprehensive validation reports

## Troubleshooting

- **Connection Issues**: Verify that QDRANT_URL and QDRANT_API_KEY are correctly set in your .env file.
- **No Results**: Ensure that the 'rag_embedding' collection contains data from the embedding pipeline.
- **Validation Failures**: Check that the retrieved content and metadata match expected formats.