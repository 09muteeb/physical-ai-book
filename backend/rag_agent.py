"""
RAG Agent with OpenAI Agents SDK + FastAPI

This module implements a RAG (Retrieval-Augmented Generation) agent that:
- Uses OpenAI Agents SDK to create intelligent agents
- Integrates with FastAPI for web endpoints
- Retrieves information from Qdrant vector database
- Generates answers based strictly on retrieved context
"""

import os
import logging
from typing import List, Dict, Optional
from datetime import datetime
import asyncio

from openai import OpenAI
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import Qdrant client and retrieval functions from existing code
from retrieval_validation import connect_to_qdrant, run_similarity_search, QueryResult

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

# Initialize OpenAI client
# Check if this is an OpenRouter key and configure accordingly
if OPENAI_API_KEY.startswith("sk-or-"):
    # This appears to be an OpenRouter API key
    # Configure OpenAI client to use OpenRouter's API endpoint
    client = OpenAI(
        api_key=OPENAI_API_KEY,
        base_url="https://openrouter.ai/api/v1"
    )
else:
    # Use standard OpenAI endpoint
    client = OpenAI(api_key=OPENAI_API_KEY)

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    max_results: int = 5
    similarity_threshold: float = 0.5

class QueryResponse(BaseModel):
    query: str
    answer: str
    retrieved_chunks: List[Dict]
    timestamp: str
    sources: List[str]

# Initialize FastAPI app
app = FastAPI(
    title="RAG Agent API",
    description="Retrieval-Augmented Generation Agent with OpenAI and Qdrant integration",
    version="1.0.0"
)

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Qdrant client
qdrant_client = None

@app.on_event("startup")
async def startup_event():
    """Initialize Qdrant client on startup"""
    global qdrant_client
    try:
        qdrant_client = connect_to_qdrant()
        logger.info("Successfully connected to Qdrant on startup")
    except Exception as e:
        logger.error(f"Failed to connect to Qdrant: {e}")
        raise

def retrieve_context(query: str, max_results: int = 5, threshold: float = 0.5) -> List[QueryResult]:
    """
    Retrieve relevant context from Qdrant based on the query.

    Args:
        query: The user's query
        max_results: Maximum number of results to retrieve
        threshold: Minimum similarity threshold

    Returns:
        List of QueryResult objects containing relevant context
    """
    if not qdrant_client:
        raise Exception("Qdrant client not initialized")

    try:
        # Perform similarity search
        results = run_similarity_search(qdrant_client, query, limit=max_results)

        # Filter results based on similarity threshold
        filtered_results = [result for result in results if result.similarity_score >= threshold]

        logger.info(f"Retrieved {len(filtered_results)} relevant chunks for query: '{query[:50]}...'")
        return filtered_results

    except Exception as e:
        logger.error(f"Error retrieving context: {e}")
        raise

def generate_answer(query: str, context_chunks: List[QueryResult]) -> str:
    """
    Generate an answer based on the query and retrieved context using OpenAI.
    This function creates a temporary assistant for the query using the Assistants API.

    Args:
        query: The user's query
        context_chunks: List of retrieved context chunks

    Returns:
        Generated answer based on the context
    """
    try:
        # Format context for the LLM
        context_text = "\n\n".join([
            f"Source: {chunk.source_url}\nContent: {chunk.content}"
            for chunk in context_chunks
        ])

        # Create an assistant for this specific query
        assistant = client.beta.assistants.create(
            name="Physical AI Book Assistant",
            instructions="You are a helpful assistant that answers questions based strictly on the provided context. Only use information from the context to answer the user's query. If the context doesn't contain sufficient information to answer the query, state that clearly.",
            model="gpt-3.5-turbo",  # Can be configured to use gpt-4 if needed
            temperature=0.3
        )

        # Create a thread for this conversation
        thread = client.beta.threads.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Context:\n{context_text}\n\nQuestion: {query}\n\nPlease provide a comprehensive answer based only on the context provided above."
                }
            ]
        )

        # Run the assistant on the thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Wait for the run to complete
        import time
        while run.status in ['queued', 'in_progress', 'requires_action']:
            time.sleep(0.5)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            # Handle any required actions if they come up
            if run.status == 'requires_action':
                logger.warning(f"Assistant requires action: {run.required_action}")

        # Get the messages from the thread
        messages = client.beta.threads.messages.list(
            thread_id=thread.id,
            order="desc"  # Get messages in descending order (newest first)
        )

        # Extract the assistant's response (first assistant message, which will be the newest)
        answer = ""
        for message in messages.data:
            if message.role == "assistant":
                for content_block in message.content:
                    if content_block.type == "text":
                        answer = content_block.text.value
                        break
                if answer:
                    break

        # Clean up: Delete the assistant (optional in production)
        try:
            client.beta.assistants.delete(assistant.id)
        except:
            pass  # Ignore cleanup errors

        logger.info(f"Generated answer for query: '{query[:50]}...'")

        return answer

    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        raise


def generate_answer_with_chat_model(query: str, context_chunks: List[QueryResult]) -> str:
    """
    Generate an answer based on the query and retrieved context using OpenAI's Chat Completions API.

    Args:
        query: The user's query
        context_chunks: List of retrieved context chunks

    Returns:
        Generated answer based on the context
    """
    try:
        # Format context for the LLM
        context_text = "\n\n".join([
            f"Source: {chunk.source_url}\nContent: {chunk.content}"
            for chunk in context_chunks
        ])

        # Create the message for the chat model
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that answers questions based strictly on the provided context. Only use information from the context to answer the user's query. If the context doesn't contain sufficient information to answer the query, state that clearly."
            },
            {
                "role": "user",
                "content": f"Context:\n{context_text}\n\nQuestion: {query}\n\nPlease provide a comprehensive answer based only on the context provided above."
            }
        ]

        # Call the chat completions API
        # Use a model that's available on OpenRouter
        model_name = "openai/gpt-3.5-turbo"  # OpenRouter format for GPT-3.5
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=0.3,
            max_tokens=1000  # Limit response length
        )

        # Extract the answer from the response
        answer = response.choices[0].message.content

        logger.info(f"Generated answer for query: '{query[:50]}...'")

        return answer

    except Exception as e:
        logger.error(f"Error generating answer: {e}")
        raise

class RAGAgent:
    """
    RAG Agent class that orchestrates the retrieval and generation process.
    """

    def __init__(self):
        self.qdrant_client = qdrant_client
        # No need to create an assistant since we're using chat completions API

    def generate_general_answer(self, query: str) -> str:
        """
        Generate a general answer using the LLM's knowledge when no specific context is found.

        Args:
            query: The user's query

        Returns:
            Generated answer based on the LLM's general knowledge
        """
        try:
            # Create the message for the chat model
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant knowledgeable about robotics, AI, and related topics. Answer the user's question based on your general knowledge. If the question is about a specific concept, provide a comprehensive explanation."
                },
                {
                    "role": "user",
                    "content": query
                }
            ]

            # Call the chat completions API
            # Use a model that's available on OpenRouter
            model_name = "openai/gpt-3.5-turbo"  # OpenRouter format for GPT-3.5
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.3,
                max_tokens=1000  # Limit response length
            )

            # Extract the answer from the response
            answer = response.choices[0].message.content

            logger.info(f"Generated general knowledge answer for query: '{query[:50]}...'")

            return answer

        except Exception as e:
            logger.error(f"Error generating general answer: {e}")
            return "I'm sorry, but I couldn't generate an answer for your question."

    async def process_query(self, query: str, max_results: int = 5, threshold: float = 0.5) -> QueryResponse:
        """
        Process a user query through the RAG pipeline.

        Args:
            query: The user's query
            max_results: Maximum number of results to retrieve
            threshold: Minimum similarity threshold

        Returns:
            QueryResponse with answer and metadata
        """
        logger.info(f"Processing query: '{query}'")

        # Step 1: Retrieve relevant context from Qdrant
        context_chunks = retrieve_context(query, max_results, threshold)

        if not context_chunks:
            logger.warning(f"No relevant context found for query: '{query}'")
            # Instead of just returning an error, generate a general answer using the LLM's knowledge
            # but inform the user that this is general knowledge, not from the book
            general_answer = self.generate_general_answer(query)
            answer = f"{general_answer}\n\n(Disclaimer: This answer is based on general knowledge as I couldn't find specific information about this topic in the Physical AI book.)"
        else:
            # Step 2: Generate answer based on retrieved context using chat model
            answer = generate_answer_with_chat_model(query, context_chunks)

        # Prepare response
        response = QueryResponse(
            query=query,
            answer=answer,
            retrieved_chunks=[
                {
                    "id": chunk.id,
                    "content": chunk.content[:500] + "..." if len(chunk.content) > 500 else chunk.content,  # Truncate long content
                    "source_url": chunk.source_url,
                    "similarity_score": chunk.similarity_score,
                    "metadata": chunk.metadata
                }
                for chunk in context_chunks
            ],
            timestamp=datetime.now().isoformat(),
            sources=list(set([chunk.source_url for chunk in context_chunks]))  # Unique sources
        )

        logger.info(f"Query processed successfully: '{query[:30]}...'")
        return response

# Create RAG agent instance (will be initialized when needed)
rag_agent = None

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "RAG Agent API is running", "status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Endpoint to process user queries through the RAG agent.

    Args:
        request: QueryRequest containing the query and parameters

    Returns:
        QueryResponse with the answer and retrieved context
    """
    global rag_agent
    try:
        # Initialize RAG agent if not already created
        if rag_agent is None:
            rag_agent = RAGAgent()

        response = await rag_agent.process_query(
            query=request.query,
            max_results=request.max_results,
            threshold=request.similarity_threshold
        )
        return response
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "operational",
            "qdrant": "connected" if qdrant_client else "disconnected"
        }
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8000))  # Use PORT from environment, default to 8000
    uvicorn.run(
        "rag_agent:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )