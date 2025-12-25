.import os
import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from dataclasses import dataclass
from typing import List, Dict, Optional
import cohere
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import xml.etree.ElementTree as ET
import time
import re


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# Configuration constants
BASE_URL = "https://physical-ai-book-rose.vercel.app/"
SITEMAP_URL = "https://physical-ai-book-rose.vercel.app/sitemap.xml"
CHUNK_SIZE = 512  # tokens
OVERLAP_SIZE = 51  # 10% of CHUNK_SIZE
COHERE_MODEL = "embed-english-v3.0"


@dataclass
class DocumentSegment:
    """Represents a chunk of text extracted from a Docusaurus page with associated metadata."""
    id: str
    content: str
    source_url: str
    metadata: Dict
    embedding: Optional[List[float]] = None


@dataclass
class PipelineConfig:
    """Configuration parameters for the embedding pipeline."""
    base_url: str = BASE_URL
    sitemap_url: str = SITEMAP_URL
    chunk_size: int = CHUNK_SIZE
    overlap_size: int = OVERLAP_SIZE
    cohere_model: str = COHERE_MODEL
    batch_size: int = 10


def get_all_urls(sitemap_url: str) -> List[str]:
    """
    Parse the sitemap.xml to extract all valid URLs from the Docusaurus site.

    Args:
        sitemap_url: URL of the sitemap.xml file

    Returns:
        List of URLs extracted from the sitemap
    """
    logger.info(f"Fetching sitemap from {sitemap_url}")

    try:
        response = requests.get(sitemap_url)
        response.raise_for_status()

        # Parse the XML sitemap
        root = ET.fromstring(response.content)

        # Find all URL elements in the sitemap
        urls = []
        for url_element in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc_element = url_element.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
            if loc_element is not None:
                url = loc_element.text.strip()
                # Only include URLs that are part of our target site
                if url.startswith(BASE_URL):
                    urls.append(url)

        logger.info(f"Found {len(urls)} URLs in sitemap")
        return urls

    except requests.RequestException as e:
        logger.error(f"Failed to fetch sitemap: {e}")
        return []
    except ET.ParseError as e:
        logger.error(f"Failed to parse sitemap XML: {e}")
        return []


def extract_text_from_url(url: str) -> Optional[str]:
    """
    Extract clean text content from a single URL.

    Args:
        url: URL to extract text from

    Returns:
        Clean text content or None if extraction fails
    """
    logger.info(f"Extracting text from {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Try to find the main content area in a Docusaurus site
        # Docusaurus typically uses main content in divs with specific classes
        main_content = (
            soup.find('main') or
            soup.find('article') or
            soup.find('div', class_='container') or
            soup.find('div', class_='main-wrapper') or
            soup.find('div', {'role': 'main'}) or
            soup
        )

        # Get text and clean it up
        text = main_content.get_text()

        # Clean up the text
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        logger.info(f"Extracted {len(text)} characters from {url}")
        return text

    except requests.RequestException as e:
        logger.error(f"Failed to fetch URL {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Failed to extract text from {url}: {e}")
        return None


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, overlap_size: int = OVERLAP_SIZE) -> List[str]:
    """
    Split text into appropriately sized chunks with overlap.

    Args:
        text: Text to chunk
        chunk_size: Size of each chunk in tokens
        overlap_size: Size of overlap between chunks

    Returns:
        List of text chunks
    """
    # For simplicity, we'll use character-based chunking
    # In a real implementation, we'd use a proper tokenization method
    # This is a simplified approach that approximates token-based chunking

    # Convert to tokens approximately (1 token ~ 4 characters for English text)
    approx_chunk_size_chars = chunk_size * 4
    approx_overlap_size_chars = overlap_size * 4

    if len(text) <= approx_chunk_size_chars:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + approx_chunk_size_chars

        # If this is the last chunk, include the remainder
        if end >= len(text):
            chunks.append(text[start:])
            break

        # Add the chunk
        chunk = text[start:end]
        chunks.append(chunk)

        # Move start position by chunk size minus overlap
        start = end - approx_overlap_size_chars

    logger.info(f"Text chunked into {len(chunks)} segments")
    return chunks


def embed(texts: List[str], model: str = COHERE_MODEL) -> List[List[float]]:
    """
    Generate embeddings using Cohere API.

    Args:
        texts: List of text segments to embed
        model: Cohere model to use

    Returns:
        List of embedding vectors
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        logger.error("COHERE_API_KEY environment variable not set")
        return []

    try:
        co = cohere.Client(api_key)

        # Cohere has rate limits, so we need to be careful with batch sizes
        # Process in smaller batches if needed
        embeddings = []
        batch_size = 96  # Cohere's max batch size is 96

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = co.embed(
                texts=batch,
                model=model,
                input_type="search_document"
            )

            embeddings.extend(response.embeddings)
            logger.info(f"Embedded batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")

            # Add a small delay to avoid rate limiting
            time.sleep(0.1)

        logger.info(f"Generated embeddings for {len(texts)} text segments")
        return embeddings

    except Exception as e:
        logger.error(f"Failed to generate embeddings: {e}")
        return []


def create_collection(client: QdrantClient, collection_name: str = "rag_embedding"):
    """
    Set up Qdrant collection named 'rag_embedding'.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection to create
    """
    try:
        # Check if collection already exists
        collections = client.get_collections()
        collection_exists = any(col.name == collection_name for col in collections.collections)

        if collection_exists:
            logger.info(f"Collection '{collection_name}' already exists")
            return

        # Create the collection
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=1024,  # Cohere's embed-english-v3.0 returns 1024-dim vectors
                distance=models.Distance.COSINE
            )
        )

        logger.info(f"Created collection '{collection_name}' successfully")

    except Exception as e:
        logger.error(f"Failed to create collection '{collection_name}': {e}")


def save_chunk_to_qdrant(
    client: QdrantClient,
    segment: DocumentSegment,
    collection_name: str = "rag_embedding"
):
    """
    Save embeddings to Qdrant with metadata.

    Args:
        client: Qdrant client instance
        segment: Document segment with embedding to save
        collection_name: Name of the collection to save to
    """
    try:
        # Prepare the point to insert
        point = models.PointStruct(
            id=segment.id,
            vector=segment.embedding,
            payload={
                "content": segment.content[:10000],  # Limit payload size
                "source_url": segment.source_url,
                "title": segment.metadata.get("title", ""),
                "created_at": segment.metadata.get("created_at", ""),
                "content_length": len(segment.content)
            }
        )

        # Upsert the point into the collection
        client.upsert(
            collection_name=collection_name,
            points=[point]
        )

        logger.info(f"Saved segment {segment.id} to Qdrant")

    except Exception as e:
        logger.error(f"Failed to save segment {segment.id} to Qdrant: {e}")


def main():
    """
    Main execution function to orchestrate the entire pipeline.
    """
    logger.info("Starting RAG embedding pipeline")

    # Initialize Qdrant client
    qdrant_url = os.getenv("QDRANT_URL")
    qdrant_api_key = os.getenv("QDRANT_API_KEY")

    if not qdrant_url:
        logger.error("QDRANT_URL environment variable not set")
        return

    try:
        qdrant_client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_api_key,
            timeout=10
        )

        # Create the collection if it doesn't exist
        create_collection(qdrant_client, "rag_embedding")

    except Exception as e:
        logger.error(f"Failed to initialize Qdrant client: {e}")
        return

    # Get all URLs from the sitemap
    urls = get_all_urls(SITEMAP_URL)
    if not urls:
        logger.error("No URLs found in sitemap")
        return

    # Process each URL
    for i, url in enumerate(urls):
        logger.info(f"Processing URL {i+1}/{len(urls)}: {url}")

        # Extract text from the URL
        text = extract_text_from_url(url)
        if not text:
            logger.warning(f"Failed to extract text from {url}")
            continue

        # Chunk the text
        chunks = chunk_text(text)

        # Process each chunk
        for j, chunk in enumerate(chunks):
            # Create a DocumentSegment
            import uuid
            from datetime import datetime

            segment_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{url}_{j}"))
            segment = DocumentSegment(
                id=segment_id,
                content=chunk,
                source_url=url,
                metadata={
                    "title": "",  # We could extract this from the page
                    "created_at": datetime.now().isoformat()
                }
            )

            # Generate embedding
            embeddings = embed([chunk])
            if embeddings and len(embeddings) > 0:
                segment.embedding = embeddings[0]

                # Save to Qdrant
                save_chunk_to_qdrant(qdrant_client, segment)
            else:
                logger.warning(f"Failed to generate embedding for chunk {j} of {url}")

    logger.info("RAG embedding pipeline completed")


if __name__ == "__main__":
    main()