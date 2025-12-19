# Data Model: RAG Chatbot Backend

## DocumentSegment
Represents a chunk of text extracted from a Docusaurus page with associated metadata.

**Fields**:
- id: str (unique identifier for the segment, generated as UUID or hash)
- content: str (the actual text content of the segment, cleaned of HTML markup)
- source_url: str (URL where the content was found, full URL including path)
- metadata: dict (additional information like page title, section, timestamp)
  - title: str (page title from the HTML)
  - section: str (section or chapter name if applicable)
  - created_at: str (timestamp when the segment was created)
- embedding: list[float] (the vector representation of the content from Cohere)

**Validation Rules**:
- content must not be empty
- source_url must be a valid URL format
- embedding must be a list of floats with consistent dimensions
- id must be unique within the collection

## PipelineConfig
Configuration parameters for the embedding pipeline.

**Fields**:
- base_url: str (the root URL to crawl, e.g., "https://physical-ai-book-rose.vercel.app/")
- sitemap_url: str (the sitemap URL to parse, default "https://physical-ai-book-rose.vercel.app/sitemap.xml")
- chunk_size: int (number of tokens per chunk, default 512)
- overlap_size: int (number of overlapping tokens between chunks, default 51)
- cohere_model: str (name of the Cohere model to use, default "embed-english-v3.0")
- batch_size: int (number of segments to process in each batch, default 10)

**Validation Rules**:
- base_url must be a valid URL format
- chunk_size must be positive integer
- overlap_size must be less than chunk_size
- cohere_model must be a valid Cohere embedding model name

## QdrantPayload
Data structure for storing additional information in Qdrant alongside embeddings.

**Fields**:
- source_url: str (URL where the content was found)
- content: str (the text content, may be truncated for storage)
- title: str (page title)
- created_at: str (timestamp)
- content_length: int (length of the original content in characters)

**Validation Rules**:
- All fields must be properly escaped for JSON storage
- content length should not exceed Qdrant payload limits