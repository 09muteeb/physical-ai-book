# Quickstart: RAG Chatbot Backend

## Prerequisites

- Python 3.9 or higher
- UV package manager installed
- Cohere API key
- Qdrant Cloud account (or local Qdrant instance)

## Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

3. **Install dependencies using UV**
   ```bash
   # Install uv if you don't have it
   pip install uv

   # Install project dependencies
   uv pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env to add your API keys
   nano .env
   ```

   Add your keys:
   ```
   COHERE_API_KEY=your_cohere_api_key_here
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   ```

## Usage

1. **Run the embedding pipeline**
   ```bash
   python main.py
   ```

2. **The pipeline will:**
   - Parse the sitemap at https://physical-ai-book-rose.vercel.app/sitemap.xml to get all page URLs
   - Extract text content from all pages
   - Chunk the text appropriately
   - Generate embeddings using Cohere
   - Store the embeddings in Qdrant

## Configuration

The pipeline can be configured by modifying constants in the main.py file:
- `BASE_URL`: The root URL to crawl
- `CHUNK_SIZE`: Number of tokens per text chunk
- `OVERLAP_SIZE`: Number of overlapping tokens between chunks
- `COHERE_MODEL`: The Cohere model to use for embeddings

## Verification

After running the pipeline, you can verify:
- Check Qdrant dashboard to see the created collection and stored vectors
- Look at the logs to confirm successful processing of all pages
- Verify the collection name is "rag_embedding"