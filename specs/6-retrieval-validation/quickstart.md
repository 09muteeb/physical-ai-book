# Quickstart: Retrieval Pipeline and Data Validation

## Setup

1. **Clone the repository**
   ```bash
   git clone [repository-url]
   cd [repository-name]
   ```

2. **Navigate to the backend directory**
   ```bash
   cd backend
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or using UV (recommended):
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` to add your Qdrant connection details:
   ```env
   QDRANT_URL="your-qdrant-url"
   QDRANT_API_KEY="your-qdrant-api-key"
   ```

## Usage

### Run the validation pipeline

```bash
python retrieval_validation.py
```

This will:
- Connect to your Qdrant instance
- Load existing embeddings from the 'rag_embedding' collection
- Run similarity searches with predefined test queries
- Validate retrieved text and metadata accuracy
- Log and verify retrieval results

### Run specific validation tests

```bash
python retrieval_validation.py --test-category concept
```

Available test categories: `concept`, `procedure`, `reference`

### Run validation with custom query

```bash
python retrieval_validation.py --query "your test query here"
```

## Configuration

The validation script can be configured by modifying constants in the `retrieval_validation.py` file:

- `COLLECTION_NAME`: The Qdrant collection to validate (default: "rag_embedding")
- `SIMILARITY_THRESHOLD`: Minimum similarity score for valid results (default: 0.5)
- `MAX_RESULTS`: Maximum number of results to return per query (default: 5)
- `TEST_QUERIES`: Predefined queries used for validation

## Output

The validation process generates:
- Console output with validation results
- Log file with detailed validation information
- Summary report with accuracy metrics
- Performance metrics including response times

## Troubleshooting

**Connection Issues**: Verify that QDRANT_URL and QDRANT_API_KEY are correctly set in your .env file.

**No Results**: Ensure that the 'rag_embedding' collection contains data from the embedding pipeline.

**Validation Failures**: Check that the retrieved content and metadata match expected formats.