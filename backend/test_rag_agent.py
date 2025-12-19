"""
Test suite for the RAG Agent implementation
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from rag_agent import RAGAgent, QueryRequest, retrieve_context, generate_answer

def test_retrieve_context():
    """Test the context retrieval function"""
    print("Testing context retrieval...")

    try:
        # Test retrieval with a sample query
        query = "What is Physical AI?"
        results = retrieve_context(query, max_results=3)

        print(f"Retrieved {len(results)} results for query: '{query}'")
        for i, result in enumerate(results):
            print(f"Result {i+1}:")
            print(f"  Source: {result.source_url}")
            print(f"  Similarity: {result.similarity_score}")
            print(f"  Content preview: {result.content[:100]}...")
            print()

        return len(results) > 0

    except Exception as e:
        print(f"Error in context retrieval: {e}")
        return False

def test_generate_answer():
    """Test the answer generation function"""
    print("Testing answer generation...")

    try:
        # First get some context
        query = "What is ROS 2?"
        context_chunks = retrieve_context(query, max_results=2)

        if context_chunks:
            # Generate answer based on context
            answer = generate_answer(query, context_chunks)
            print(f"Query: {query}")
            print(f"Answer: {answer}")
            print()
            return True
        else:
            print("No context retrieved for answer generation test")
            return False

    except Exception as e:
        print(f"Error in answer generation: {e}")
        return False

async def test_full_agent():
    """Test the complete RAG agent workflow"""
    print("Testing full RAG agent workflow...")

    try:
        # Create agent instance
        agent = RAGAgent()

        # Test query
        query = "What are the key components of Physical AI?"
        response = await agent.process_query(query, max_results=3)

        print(f"Query: {response.query}")
        print(f"Answer: {response.answer}")
        print(f"Retrieved {len(response.retrieved_chunks)} chunks")
        print(f"Sources: {response.sources}")
        print()

        return True

    except Exception as e:
        print(f"Error in full agent test: {e}")
        return False

async def main():
    """Run all tests"""
    print("Starting RAG Agent tests...\n")

    # Test 1: Context retrieval
    retrieval_success = test_retrieve_context()
    print(f"Context retrieval test: {'PASSED' if retrieval_success else 'FAILED'}\n")

    # Test 2: Answer generation
    if retrieval_success:
        generation_success = test_generate_answer()
        print(f"Answer generation test: {'PASSED' if generation_success else 'FAILED'}\n")
    else:
        generation_success = False
        print("Skipping answer generation test due to retrieval failure\n")

    # Test 3: Full agent workflow
    if retrieval_success:
        agent_success = await test_full_agent()
        print(f"Full agent test: {'PASSED' if agent_success else 'FAILED'}\n")
    else:
        agent_success = False
        print("Skipping full agent test due to retrieval failure\n")

    # Summary
    print("Test Summary:")
    print(f"- Context Retrieval: {'✓' if retrieval_success else '✗'}")
    print(f"- Answer Generation: {'✓' if generation_success else '✗'}")
    print(f"- Full Agent Workflow: {'✓' if agent_success else '✗'}")

    all_passed = retrieval_success and generation_success and agent_success
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")

    return all_passed

if __name__ == "__main__":
    asyncio.run(main())