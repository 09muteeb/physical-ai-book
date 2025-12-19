# Research Document: RAG Chatbot Backend

## Decision: Cohere Embedding Model
**Rationale**: Selected Cohere's embed-english-v3.0 model as it's the latest and most efficient for text content. This model is optimized for English text and provides high-quality embeddings suitable for semantic search.

**Alternatives considered**:
- embed-english-light-v3.0: Smaller and faster but less accurate
- multilingual models: Not needed since the content is primarily in English

## Decision: Qdrant Vector Database
**Rationale**: Qdrant Cloud free tier provides sufficient capacity for development and initial deployment. It has excellent Python client support and is specifically designed for vector similarity search.

**Alternatives considered**:
- Local Qdrant instance: Requires more setup and maintenance
- Pinecone: Commercial solution without free tier
- Weaviate: Alternative vector database but Qdrant has better Python integration

## Decision: Web Crawling Approach
**Rationale**: Using Beautiful Soup and requests for web crawling as Docusaurus generates static HTML that doesn't require JavaScript rendering. This approach is reliable and well-documented.

**Alternatives considered**:
- Selenium: For dynamic content (not needed for static Docusaurus sites)
- Scrapy: More complex for simple crawling needs

## Decision: Text Chunking Strategy
**Rationale**: Using 512-token chunks with 10% overlap (51 tokens) to balance context preservation with embedding efficiency. This allows for good semantic understanding while maintaining reasonable processing speed.

**Alternatives considered**:
- Fixed character counts: Less semantic meaning
- Sentence-based chunking: May create chunks of very different sizes

## Docusaurus Site Structure
**Finding**: The deployed site at https://physical-ai-book-rose.vercel.app/ follows standard Docusaurus URL patterns with documentation pages under /docs/ paths. The site structure is predictable and crawlable.

## Sitemap Usage
**Finding**: Docusaurus sites typically have a sitemap.xml file at the root (e.g., https://physical-ai-book-rose.vercel.app/sitemap.xml) that contains all the page URLs. This is a more reliable method than crawling to discover all pages, as it provides an authoritative list of all indexed pages.

**Decision**: Use sitemap.xml to get all URLs for the Docusaurus site
**Rationale**: Sitemaps provide a complete and up-to-date list of all pages without the risk of missing content due to navigation issues or JavaScript-rendered links
**Alternatives considered**: Manual URL discovery through crawling (less reliable, may miss pages)

## UV Package Manager
**Finding**: UV is a fast Python package installer and resolver, much faster than pip. It can be used as a drop-in replacement and works well with requirements.txt files.