"""
API client for testing the RAG Agent FastAPI endpoints
"""
import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print("Health check: PASSED")
            print(f"Status: {data.get('status')}")
            print(f"Services: {data.get('services')}")
            return True
        else:
            print(f"Health check: FAILED - Status code {response.status_code}")
            return False
    except Exception as e:
        print(f"Health check: FAILED - {e}")
        return False

def test_query_endpoint(query: str = "What is Physical AI?", max_results: int = 3):
    """Test the query endpoint"""
    try:
        payload = {
            "query": query,
            "max_results": max_results,
            "similarity_threshold": 0.3
        }

        response = requests.post(f"{BASE_URL}/query", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"Query: {data.get('query')}")
            print(f"Answer: {data.get('answer')[:200]}...")
            print(f"Retrieved chunks: {len(data.get('retrieved_chunks'))}")
            print(f"Sources: {data.get('sources')[:3]}")  # Show first 3 sources
            return True
        else:
            print(f"Query endpoint: FAILED - Status code {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Query endpoint: FAILED - {e}")
        return False

def main():
    """Run API tests"""
    print("Testing RAG Agent API endpoints...\n")

    # Test 1: Health check
    health_ok = test_health_endpoint()
    print()

    if health_ok:
        # Test 2: Query endpoint
        query_ok = test_query_endpoint("What is Physical AI?")
        print()

        # Test 3: Another query
        query_ok2 = test_query_endpoint("Explain ROS 2 in Physical AI context", max_results=5)
        print()
    else:
        print("Skipping query tests due to health check failure")
        query_ok = False
        query_ok2 = False

    # Summary
    print("API Test Summary:")
    print(f"- Health Endpoint: {'✓' if health_ok else '✗'}")
    print(f"- Query Test 1: {'✓' if query_ok else '✗'}")
    print(f"- Query Test 2: {'✓' if query_ok2 else '✗'}")

    all_passed = health_ok and query_ok and query_ok2
    print(f"\nOverall: {'ALL TESTS PASSED' if all_passed else 'SOME TESTS FAILED'}")

if __name__ == "__main__":
    main()