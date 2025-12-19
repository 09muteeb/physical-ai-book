"""
Mock RAG Agent with FastAPI for Testing

This module implements a mock version of the RAG agent that:
- Provides mock responses for testing purposes
- Integrates with FastAPI for web endpoints
- Simulates the behavior of the real RAG agent
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime
import asyncio
import random

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Pydantic models for request/response
class QueryRequest(BaseModel):
    query: str
    max_results: int = 5
    similarity_threshold: float = 0.5
    context: Optional[Dict] = None  # Added context field to match frontend expectations

class QueryResponse(BaseModel):
    query: str
    answer: str
    retrieved_chunks: List[Dict]
    timestamp: str
    sources: List[str]

# Initialize FastAPI app
app = FastAPI(
    title="Mock RAG Agent API",
    description="Mock Retrieval-Augmented Generation Agent for testing frontend integration",
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

def generate_mock_answer(query: str) -> str:
    """Generate a mock answer based on the query"""
    mock_answers = [
        f"I understand you're asking about '{query}'. Based on the Physical AI book content, this topic covers important concepts about connecting AI with robotic systems.",
        f"Regarding your query '{query}', the Physical AI book explains that this involves integrating AI algorithms with physical robot control systems.",
        f"That's an interesting question about '{query}'. The book discusses how to bridge the gap between AI logic and robot body control.",
        f"In the context of Physical AI, '{query}' relates to how artificial intelligence can be effectively connected to robotic hardware systems.",
        f"The Physical AI book addresses '{query}' by explaining the principles of connecting AI agents with robot bodies."
    ]

    # Add some context-aware responses
    query_lower = query.lower()
    if 'ros' in query_lower:
        return f"Regarding ROS 2 (Robot Operating System 2) in the context of '{query}', the Physical AI book covers how ROS 2 serves as the 'nervous system' connecting AI to robot bodies. This includes message passing, service calls, and action libraries that facilitate communication between AI decision-making and robot control."
    elif 'simulation' in query_lower or 'isaac' in query_lower:
        return f"Concerning simulation and NVIDIA Isaac in your query about '{query}', the Physical AI book explains how digital twins and simulation environments allow for safe testing of AI-robot interactions. Isaac Sim provides photorealistic simulation and synthetic data generation for training AI in robotics."
    elif 'ai' in query_lower or 'intelligence' in query_lower:
        return f"Regarding AI and intelligence in your query '{query}', the Physical AI book explores how artificial intelligence algorithms can be connected to physical robot bodies. This includes perception, planning, and control systems that bridge the virtual and physical worlds."

    return random.choice(mock_answers)

def generate_mock_sources() -> List[str]:
    """Generate mock source URLs"""
    return [
        "http://localhost:3000/docs/module-1-ros2-nervous-system",
        "http://localhost:3000/docs/module-2-digital-twins-simulation-hri",
        "http://localhost:3000/docs/module-3-isaac-ai-brain",
        "http://localhost:3000/docs/intro"
    ]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Mock RAG Agent API is running", "status": "healthy"}

@app.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    """
    Endpoint to process user queries with mock responses.
    """
    try:
        # Generate mock answer
        answer = generate_mock_answer(request.query)

        # Generate mock retrieved chunks
        mock_chunks = [
            {
                "id": f"mock_chunk_{i}",
                "content": f"Mock content related to {request.query}... This is sample content from the Physical AI book demonstrating how this topic is covered in the documentation.",
                "source_url": random.choice(generate_mock_sources()),
                "similarity_score": round(random.uniform(0.6, 0.95), 2),
                "metadata": {"section": f"section_{i}", "type": "documentation"}
            }
            for i in range(request.max_results)
        ]

        # Prepare response
        response = QueryResponse(
            query=request.query,
            answer=answer,
            retrieved_chunks=mock_chunks,
            timestamp=datetime.now().isoformat(),
            sources=generate_mock_sources()[:3]  # Return 3 mock sources
        )

        return response
    except Exception as e:
        print(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "api": "operational",
            "qdrant": "mocked"  # Indicating it's mocked
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "mock_rag_agent:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )