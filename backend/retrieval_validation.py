"""
Retrieval Pipeline and Data Validation System

This module provides functionality to:
- Connect to Qdrant and query stored embeddings
- Perform similarity searches with test queries
- Validate returned chunks and metadata
- Generate validation reports
"""

import os
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import time

# Import qdrant client
from qdrant_client import QdrantClient
from qdrant_client.http import models
from qdrant_client.models import PointStruct, ScoredPoint
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration constants
COLLECTION_NAME = "rag_embedding"
SIMILARITY_THRESHOLD = 0.5
MAX_RESULTS = 5
CHUNK_SIZE_LIMIT = 10000  # Max payload size for Qdrant


@dataclass
class QueryResult:
    """Represents the output of a similarity search operation."""
    id: str
    content: str
    source_url: str
    metadata: Dict
    similarity_score: float  # range 0.0-1.0

    def __post_init__(self):
        """Validate QueryResult fields according to data model."""
        if not isinstance(self.id, str):
            raise ValueError("id must be a valid string identifier")
        if not self.content.strip():
            raise ValueError("content must be non-empty")
        if not isinstance(self.source_url, str) or not self.source_url.startswith(('http://', 'https://')):
            raise ValueError("source_url must be a valid URL format")
        if not isinstance(self.metadata, dict):
            raise ValueError("metadata must be a dictionary")
        if 'title' not in self.metadata or 'created_at' not in self.metadata:
            raise ValueError("metadata must contain required fields: 'title', 'created_at'")
        if not (0.0 <= self.similarity_score <= 1.0):
            raise ValueError("similarity_score must be between 0.0 and 1.0")


@dataclass
class ValidationReport:
    """Contains the results of validation checks performed on retrieved data."""
    query: str
    timestamp: str
    results_count: int
    validation_passed: bool
    accuracy_score: float  # percentage of valid results, 0.0-1.0
    details: Dict  # specific validation details and errors
    performance_metrics: Dict  # response time and other performance data

    def __post_init__(self):
        """Validate ValidationReport fields according to data model."""
        if not self.query.strip():
            raise ValueError("query must be non-empty")
        if not isinstance(self.timestamp, str):
            raise ValueError("timestamp must be in ISO format")
        if self.results_count < 0:
            raise ValueError("results_count must be non-negative")
        if not isinstance(self.validation_passed, bool):
            raise ValueError("validation_passed must be a boolean")
        if not (0.0 <= self.accuracy_score <= 1.0):
            raise ValueError("accuracy_score must be between 0.0 and 1.0")
        if not isinstance(self.details, dict) or 'passed_count' not in self.details or 'failed_count' not in self.details:
            raise ValueError("details must contain 'passed_count' and 'failed_count' keys")


@dataclass
class TestQuery:
    """A predefined query used to validate the retrieval pipeline."""
    id: str
    text: str
    expected_content_keywords: List[str]
    category: str  # 'concept', 'procedure', 'reference'
    priority: str  # 'high', 'medium', 'low'

    def __post_init__(self):
        """Validate TestQuery fields according to data model."""
        if not self.id.strip():
            raise ValueError("id must be non-empty")
        if not self.text.strip():
            raise ValueError("text must be non-empty")
        if not isinstance(self.expected_content_keywords, list) or not all(isinstance(kw, str) and kw.strip() for kw in self.expected_content_keywords):
            raise ValueError("expected_content_keywords must be a list of non-empty strings")
        if self.category not in ['concept', 'procedure', 'reference']:
            raise ValueError("category must be one of: 'concept', 'procedure', 'reference'")
        if self.priority not in ['high', 'medium', 'low']:
            raise ValueError("priority must be one of: 'high', 'medium', 'low'")


@dataclass
class ValidationRule:
    """Defines criteria for validating retrieved results."""
    rule_id: str
    rule_type: str  # 'content_accuracy', 'metadata_completeness', 'similarity_threshold'
    description: str
    threshold: float  # threshold value for validation, if applicable
    enabled: bool  # whether this rule is currently active

    def __post_init__(self):
        """Validate ValidationRule fields according to data model."""
        if not self.rule_id.strip():
            raise ValueError("rule_id must be non-empty")
        if self.rule_type not in ['content_accuracy', 'metadata_completeness', 'similarity_threshold']:
            raise ValueError("rule_type must be one of: 'content_accuracy', 'metadata_completeness', 'similarity_threshold'")
        if not self.description.strip():
            raise ValueError("description must be non-empty")
        if self.threshold is not None and not (0.0 <= self.threshold <= 1.0):
            raise ValueError("threshold must be between 0.0 and 1.0 if applicable")
        if not isinstance(self.enabled, bool):
            raise ValueError("enabled must be a boolean")


# Constants for configuration
QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

# Additional constants
SIMILARITY_SEARCH_TIMEOUT = 30  # seconds
CONNECTION_RETRY_ATTEMPTS = 3
CONNECTION_RETRY_DELAY = 1  # seconds

# Configuration from environment with defaults
CONFIG = {
    'collection_name': os.getenv('QDRANT_COLLECTION_NAME', 'rag_embedding'),
    'similarity_threshold': float(os.getenv('SIMILARITY_THRESHOLD', '0.5')),
    'max_results': int(os.getenv('MAX_RESULTS', '5')),
    'chunk_size_limit': int(os.getenv('CHUNK_SIZE_LIMIT', '10000')),
    'similarity_search_timeout': int(os.getenv('SIMILARITY_SEARCH_TIMEOUT', '30')),
    'connection_retry_attempts': int(os.getenv('CONNECTION_RETRY_ATTEMPTS', '3')),
    'connection_retry_delay': int(os.getenv('CONNECTION_RETRY_DELAY', '1')),
    'consistency_runs': int(os.getenv('CONSISTENCY_RUNS', '3')),
    'min_content_chars': int(os.getenv('MIN_CONTENT_CHARS', '10')),
    'validation_batch_size': int(os.getenv('VALIDATION_BATCH_SIZE', '10'))
}

# Update global constants with config values
COLLECTION_NAME = CONFIG['collection_name']
SIMILARITY_THRESHOLD = CONFIG['similarity_threshold']
MAX_RESULTS = CONFIG['max_results']
CHUNK_SIZE_LIMIT = CONFIG['chunk_size_limit']
SIMILARITY_SEARCH_TIMEOUT = CONFIG['similarity_search_timeout']
CONNECTION_RETRY_ATTEMPTS = CONFIG['connection_retry_attempts']
CONNECTION_RETRY_DELAY = CONFIG['connection_retry_delay']


def connect_to_qdrant() -> QdrantClient:
    """
    Establish connection to Qdrant instance with error handling.

    Returns:
        QdrantClient: Connected client instance

    Raises:
        ConnectionError: If unable to connect to Qdrant after retries
        ValueError: If required environment variables are missing
    """
    if not QDRANT_URL:
        raise ValueError("QDRANT_URL environment variable not set")

    # Try to connect with retry logic
    for attempt in range(CONNECTION_RETRY_ATTEMPTS):
        try:
            logger.info(f"Connecting to Qdrant at {QDRANT_URL} (attempt {attempt + 1})")

            client = QdrantClient(
                url=QDRANT_URL,
                api_key=QDRANT_API_KEY,
                timeout=SIMILARITY_SEARCH_TIMEOUT
            )

            # Test the connection by getting collection list
            client.get_collections()
            logger.info("Successfully connected to Qdrant")
            return client

        except Exception as e:
            logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt == CONNECTION_RETRY_ATTEMPTS - 1:
                # Last attempt failed
                raise ConnectionError(f"Failed to connect to Qdrant after {CONNECTION_RETRY_ATTEMPTS} attempts: {e}")

            # Wait before retry
            time.sleep(CONNECTION_RETRY_DELAY)

    raise ConnectionError(f"Failed to connect to Qdrant after {CONNECTION_RETRY_ATTEMPTS} attempts")


def retrieve_embeddings(client: QdrantClient, limit: int = 10) -> List[QueryResult]:
    """
    Fetch stored embeddings from Qdrant with associated metadata.

    Args:
        client: Connected QdrantClient instance
        limit: Maximum number of embeddings to retrieve (default 10)

    Returns:
        List[QueryResult]: List of retrieved embeddings with metadata

    Raises:
        ValueError: If the collection doesn't exist
        Exception: If retrieval fails
    """
    try:
        logger.info(f"Retrieving up to {limit} embeddings from collection '{COLLECTION_NAME}'")

        # Check if collection exists
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]
        if COLLECTION_NAME not in collection_names:
            raise ValueError(f"Collection '{COLLECTION_NAME}' does not exist")

        # Retrieve points from the collection
        points = client.scroll(
            collection_name=COLLECTION_NAME,
            limit=limit,
            with_payload=True,
            with_vectors=False  # We don't need the actual vectors for validation
        )

        results = []
        for point in points[0]:  # points[0] contains the actual points
            # Extract content and metadata from the payload
            payload = point.payload
            content = payload.get("content", "")
            source_url = payload.get("source_url", "")
            title = payload.get("title", "")
            created_at = payload.get("created_at", "")

            # Handle edge case: empty or malformed content
            if not content or len(content.strip()) < CONFIG['min_content_chars']:
                logger.warning(f"Skipping point {point.id} due to insufficient content")
                continue

            # Create QueryResult object, handling potential validation errors
            try:
                query_result = QueryResult(
                    id=str(point.id),
                    content=content,
                    source_url=source_url,
                    metadata={
                        "title": title,
                        "created_at": created_at
                    },
                    similarity_score=1.0  # For retrieval, we use 1.0 as placeholder
                )
                results.append(query_result)
            except ValueError as ve:
                logger.warning(f"Skipping point {point.id} due to validation error: {ve}")
                continue

        logger.info(f"Successfully retrieved {len(results)} embeddings from Qdrant")
        return results

    except Exception as e:
        logger.error(f"Failed to retrieve embeddings from Qdrant: {e}")
        raise


def count_embeddings(client: QdrantClient) -> int:
    """
    Get total count of stored embeddings in the Qdrant collection.

    Args:
        client: Connected QdrantClient instance

    Returns:
        int: Total number of stored embeddings

    Raises:
        ValueError: If the collection doesn't exist
        Exception: If counting fails
    """
    try:
        logger.info(f"Counting embeddings in collection '{COLLECTION_NAME}'")

        # Check if collection exists
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]
        if COLLECTION_NAME not in collection_names:
            raise ValueError(f"Collection '{COLLECTION_NAME}' does not exist")

        # Get the collection info which includes the count
        collection_info = client.get_collection(COLLECTION_NAME)
        count = collection_info.points_count

        logger.info(f"Total embeddings in collection '{COLLECTION_NAME}': {count}")
        return count

    except Exception as e:
        logger.error(f"Failed to count embeddings in Qdrant: {e}")
        raise


def run_similarity_search(client: QdrantClient, query_text: str, limit: int = MAX_RESULTS) -> List[QueryResult]:
    """
    Execute similarity search with test query against stored embeddings.

    Args:
        client: Connected QdrantClient instance
        query_text: The search query text
        limit: Maximum number of results to return (default MAX_RESULTS)

    Returns:
        List[QueryResult]: List of similar text chunks with similarity scores

    Raises:
        ValueError: If the collection doesn't exist or query is empty
        Exception: If search fails
    """
    if not query_text.strip():
        raise ValueError("Query text cannot be empty")

    # Handle edge case: extremely long queries
    if len(query_text) > 1000:  # Arbitrary limit, can be configured
        logger.warning(f"Query is very long ({len(query_text)} chars), truncating to 1000 chars")
        query_text = query_text[:1000]

    try:
        logger.info(f"Performing similarity search for query: '{query_text[:50]}...'")

        # Check if collection exists
        collections = client.get_collections()
        collection_names = [col.name for col in collections.collections]
        if COLLECTION_NAME not in collection_names:
            raise ValueError(f"Collection '{COLLECTION_NAME}' does not exist")

        # To perform semantic search, we need to embed the query text using the same model
        # that was used for the stored embeddings (Cohere embed-english-v3.0)
        # We need to import cohere for this
        import cohere
        cohere_api_key = os.getenv("COHERE_API_KEY")
        if not cohere_api_key:
            raise ValueError("COHERE_API_KEY environment variable not set for query embedding")

        co = cohere.Client(cohere_api_key)

        # Embed the query text
        try:
            response = co.embed(
                texts=[query_text],
                model="embed-english-v3.0",
                input_type="search_query"
            )
            query_embedding = response.embeddings[0]
        except Exception as embed_error:
            logger.error(f"Failed to embed query text: {embed_error}")
            raise ValueError(f"Failed to embed query text: {embed_error}")

        # Search for points similar to the query embedding in the collection
        search_results = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_embedding,  # Using the embedded query vector
            limit=limit,
            with_payload=True
        )

        results = []
        # Handle the result structure from query_points method
        for point in search_results.points:
            payload = point.payload
            content = payload.get("content", "")
            source_url = payload.get("source_url", "")
            title = payload.get("title", "")
            created_at = payload.get("created_at", "")

            # Handle edge case: empty or malformed content
            if not content or len(content.strip()) < CONFIG['min_content_chars']:
                logger.warning(f"Skipping result {point.id} due to insufficient content")
                continue

            # Create QueryResult object, handling potential validation errors
            try:
                query_result = QueryResult(
                    id=str(point.id),
                    content=content,
                    source_url=source_url,
                    metadata={
                        "title": title,
                        "created_at": created_at
                    },
                    similarity_score=point.score  # Use the actual similarity score from Qdrant
                )
                results.append(query_result)
            except ValueError as ve:
                logger.warning(f"Skipping result {point.id} due to validation error: {ve}")
                continue

        logger.info(f"Similarity search returned {len(results)} results")
        return results

    except Exception as e:
        logger.error(f"Failed to perform similarity search: {e}")
        raise


# Predefined test queries for validation
TEST_QUERIES = [
    TestQuery(
        id="tq001",
        text="What is ROS 2 and how does it work with Physical AI?",
        expected_content_keywords=["ROS 2", "Physical AI", "robotics"],
        category="concept",
        priority="high"
    ),
    TestQuery(
        id="tq002",
        text="How to implement a basic robot controller?",
        expected_content_keywords=["robot", "controller", "implementation"],
        category="procedure",
        priority="high"
    ),
    TestQuery(
        id="tq003",
        text="Explain the architecture of the nervous system for robots",
        expected_content_keywords=["architecture", "nervous system", "robot"],
        category="concept",
        priority="medium"
    ),
    TestQuery(
        id="tq004",
        text="What are the key components of Physical AI?",
        expected_content_keywords=["components", "Physical AI", "key"],
        category="reference",
        priority="medium"
    ),
    TestQuery(
        id="tq005",
        text="How does the RAG system work?",
        expected_content_keywords=["RAG", "system", "retrieval"],
        category="concept",
        priority="low"
    )
]


def load_test_queries(category: Optional[str] = None) -> List[TestQuery]:
    """
    Load predefined test queries for validation.

    Args:
        category: Optional category filter ('concept', 'procedure', 'reference')

    Returns:
        List[TestQuery]: List of test queries, optionally filtered by category
    """
    if category:
        return [q for q in TEST_QUERIES if q.category == category]
    return TEST_QUERIES.copy()


def add_similarity_threshold_to_search(client: QdrantClient, query_text: str, limit: int = MAX_RESULTS, threshold: float = SIMILARITY_THRESHOLD) -> List[QueryResult]:
    """
    Execute similarity search with configurable threshold filtering.

    Args:
        client: Connected QdrantClient instance
        query_text: The search query text
        limit: Maximum number of results to return
        threshold: Minimum similarity score threshold

    Returns:
        List[QueryResult]: List of similar text chunks with similarity scores above threshold
    """
    all_results = run_similarity_search(client, query_text, limit)
    # Filter results based on similarity threshold
    filtered_results = [result for result in all_results if result.similarity_score >= threshold]
    logger.info(f"Filtered {len(all_results)} results to {len(filtered_results)} based on threshold {threshold}")
    return filtered_results


def validate_text_accuracy(content: str, expected_keywords: List[str]) -> bool:
    """
    Check if retrieved content contains expected keywords.

    Args:
        content: The content to validate
        expected_keywords: List of keywords that should appear in the content

    Returns:
        bool: True if content contains expected keywords, False otherwise
    """
    if not content or not expected_keywords:
        return len(expected_keywords) == 0  # If no expected keywords, consider valid

    content_lower = content.lower()
    found_keywords = []

    for keyword in expected_keywords:
        if keyword.lower() in content_lower:
            found_keywords.append(keyword)

    # Consider valid if we find at least half of the expected keywords
    required_matches = max(1, len(expected_keywords) // 2)  # At least 1 or half, whichever is higher
    return len(found_keywords) >= required_matches


def validate_metadata(metadata: dict) -> bool:
    """
    Verify metadata completeness and format.

    Args:
        metadata: The metadata dictionary to validate

    Returns:
        bool: True if metadata is valid, False otherwise
    """
    if not isinstance(metadata, dict):
        return False

    # Check for required fields
    required_fields = ['title', 'created_at']

    for field in required_fields:
        if field not in metadata:
            logger.warning(f"Missing required metadata field: {field}")
            return False

        # Check if the field value is not empty
        if not metadata[field]:
            logger.warning(f"Required metadata field '{field}' is empty")
            return False

    return True


def validate_retrieved_data(results: List[QueryResult]) -> Tuple[bool, List[Dict]]:
    """
    Validate QueryResult objects for content and metadata accuracy.

    Args:
        results: List of QueryResult objects to validate

    Returns:
        Tuple[bool, List[Dict]]: Overall validation status and details for each result
    """
    if not results:
        return True, []  # Empty results are considered valid

    validation_details = []
    all_valid = True

    for result in results:
        result_detail = {
            'id': result.id,
            'content_valid': True,
            'metadata_valid': True,
            'errors': []
        }

        # Validate metadata
        metadata_valid = validate_metadata(result.metadata)
        result_detail['metadata_valid'] = metadata_valid
        if not metadata_valid:
            result_detail['errors'].append("Metadata validation failed")
            all_valid = False

        # For content validation, we can't validate against expected keywords without knowing the context
        # So we'll just ensure content is not empty
        if not result.content.strip():
            result_detail['content_valid'] = False
            result_detail['errors'].append("Content is empty")
            all_valid = False

        validation_details.append(result_detail)

    return all_valid, validation_details


def generate_validation_report(query: str, results: List[QueryResult], validation_results: List[Dict],
                              start_time: Optional[datetime] = None,
                              end_time: Optional[datetime] = None) -> ValidationReport:
    """
    Create structured validation output with performance metrics.

    Args:
        query: The original test query
        results: The search results
        validation_results: The validation details from validate_retrieved_data
        start_time: Optional start time for performance tracking
        end_time: Optional end time for performance tracking

    Returns:
        ValidationReport: Structured validation report with performance metrics
    """
    timestamp = datetime.now().isoformat()

    # Calculate accuracy score
    total_results = len(results) if results else 1  # Avoid division by zero
    valid_results = sum(1 for detail in validation_results if detail.get('content_valid', True) and detail.get('metadata_valid', True))
    accuracy_score = valid_results / total_results if total_results > 0 else 1.0

    # Determine overall validation status
    validation_passed = all(
        detail.get('content_valid', True) and detail.get('metadata_valid', True)
        for detail in validation_results
    )

    # Calculate performance metrics
    duration_ms = None
    if start_time and end_time:
        duration_ms = (end_time - start_time).total_seconds() * 1000
    elif start_time:
        duration_ms = (datetime.now() - start_time).total_seconds() * 1000

    # Create performance metrics
    performance_metrics = {
        'start_time': start_time.isoformat() if start_time else timestamp,
        'end_time': end_time.isoformat() if end_time else datetime.now().isoformat(),
        'duration_ms': duration_ms,
        'results_per_second': len(results) / (duration_ms / 1000) if duration_ms and duration_ms > 0 else 0,
        'average_similarity_score': sum(r.similarity_score for r in results) / len(results) if results else 0.0
    }

    # Create details dict
    details = {
        'passed_count': sum(1 for detail in validation_results if detail.get('content_valid', True) and detail.get('metadata_valid', True)),
        'failed_count': sum(1 for detail in validation_results if not (detail.get('content_valid', True) and detail.get('metadata_valid', True))),
        'validation_details': validation_results,
        'accuracy_breakdown': {
            'content_accuracy': sum(1 for detail in validation_results if detail.get('content_valid', True)) / len(validation_results) if validation_results else 1.0,
            'metadata_accuracy': sum(1 for detail in validation_results if detail.get('metadata_valid', True)) / len(validation_results) if validation_results else 1.0
        }
    }

    return ValidationReport(
        query=query,
        timestamp=timestamp,
        results_count=len(results),
        validation_passed=validation_passed,
        accuracy_score=accuracy_score,
        details=details,
        performance_metrics=performance_metrics
    )


def validate_retrieval_consistency(client: QdrantClient, query_text: str, num_runs: int = 3) -> Dict:
    """
    Validate consistency of results across multiple identical queries.

    Args:
        client: Connected QdrantClient instance
        query_text: The query to test for consistency
        num_runs: Number of times to run the query (default 3)

    Returns:
        Dict: Consistency validation results
    """
    results_list = []
    similarity_scores = []

    logger.info(f"Testing consistency for query '{query_text}' over {num_runs} runs")

    for i in range(num_runs):
        try:
            run_start = datetime.now()
            results = run_similarity_search(client, query_text, limit=MAX_RESULTS)
            run_end = datetime.now()

            results_list.append(results)
            similarity_scores.extend([r.similarity_score for r in results])

            duration = (run_end - run_start).total_seconds() * 1000
            logger.info(f"Run {i+1}: {len(results)} results in {duration:.2f}ms")

        except Exception as e:
            logger.error(f"Run {i+1} failed: {e}")
            # Return partial results if any runs succeeded
            continue

    # Analyze consistency
    if not results_list:
        return {
            'consistent': False,
            'message': 'All runs failed',
            'num_successful_runs': 0,
            'avg_results_per_run': 0,
            'similarity_std_dev': 0
        }

    # Calculate consistency metrics
    num_results_per_run = [len(results) for results in results_list]
    avg_results = sum(num_results_per_run) / len(num_results_per_run)

    # Calculate similarity score standard deviation (lower is more consistent)
    import statistics
    similarity_std_dev = statistics.stdev(similarity_scores) if len(similarity_scores) > 1 else 0

    # Check if result counts are consistent
    result_count_consistent = all(count == num_results_per_run[0] for count in num_results_per_run)

    # For content consistency, we'd need to check if the same IDs are returned
    # This is a basic check - in practice, semantic similarity might return slightly different results
    consistency_percentage = 0
    if len(results_list) > 1:
        first_run_ids = {r.id for r in results_list[0]}
        consistent_ids = 0
        for results in results_list[1:]:
            current_ids = {r.id for r in results}
            consistent_ids += len(first_run_ids.intersection(current_ids))

        # Calculate average consistency across runs
        consistency_percentage = consistent_ids / (len(results_list) - 1) if len(results_list) > 1 else 100

    return {
        'consistent': result_count_consistent and similarity_std_dev < 0.1,  # Threshold for consistency
        'message': f'Consistency check completed across {len(results_list)} successful runs',
        'num_successful_runs': len(results_list),
        'avg_results_per_run': avg_results,
        'similarity_std_dev': similarity_std_dev,
        'result_count_consistent': result_count_consistent,
        'consistency_percentage': consistency_percentage,
        'individual_run_results': num_results_per_run
    }


def run_complete_validation_pipeline(test_query: Optional[str] = None, category: Optional[str] = None) -> List[ValidationReport]:
    """
    Run the complete validation pipeline with test queries.

    Args:
        test_query: Optional specific query to test (if provided, ignores category)
        category: Optional category to filter test queries

    Returns:
        List[ValidationReport]: List of validation reports for each tested query
    """
    start_time = datetime.now()
    logger.info("Starting complete retrieval validation pipeline")

    try:
        # Connect to Qdrant
        client = connect_to_qdrant()

        # Determine which queries to run
        if test_query:
            queries_to_test = [TestQuery(
                id="custom_query",
                text=test_query,
                expected_content_keywords=[],
                category="custom",
                priority="high"
            )]
        elif category:
            queries_to_test = load_test_queries(category=category)
        else:
            queries_to_test = load_test_queries()  # All queries

        validation_reports = []

        for test_query in queries_to_test:
            logger.info(f"Validating query: '{test_query.text}' (ID: {test_query.id})")

            query_start = datetime.now()

            try:
                # Run similarity search
                search_results = run_similarity_search(client, test_query.text)

                # Validate the results
                validation_status, validation_details = validate_retrieved_data(search_results)

                # Generate validation report
                query_end = datetime.now()
                report = generate_validation_report(
                    query=test_query.text,
                    results=search_results,
                    validation_results=validation_details,
                    start_time=query_start,
                    end_time=query_end
                )
                validation_reports.append(report)

                logger.info(f"Query '{test_query.text[:30]}...' validation: {'PASSED' if report.validation_passed else 'FAILED'} "
                           f"({report.results_count} results, {report.accuracy_score:.2%} accuracy)")

            except Exception as e:
                logger.error(f"Validation failed for query '{test_query.text}': {e}")
                # Create a failure report
                failure_report = ValidationReport(
                    query=test_query.text,
                    timestamp=datetime.now().isoformat(),
                    results_count=0,
                    validation_passed=False,
                    accuracy_score=0.0,
                    details={'errors': [str(e)]},
                    performance_metrics={'duration_ms': (datetime.now() - query_start).total_seconds() * 1000}
                )
                validation_reports.append(failure_report)

        total_duration = (datetime.now() - start_time).total_seconds() * 1000
        logger.info(f"Validation pipeline completed in {total_duration:.2f}ms with {len(validation_reports)} test queries")

        # Print summary
        successful_validations = sum(1 for report in validation_reports if report.validation_passed)
        logger.info(f"Summary: {successful_validations}/{len(validation_reports)} queries passed validation")

        return validation_reports

    except Exception as e:
        logger.error(f"Validation pipeline failed: {e}")
        raise


def main():
    """
    Command-line interface for the retrieval validation system.
    """
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="RAG Retrieval Pipeline and Data Validation")
    parser.add_argument("--query", type=str, help="Run validation with a specific query")
    parser.add_argument("--category", type=str, choices=['concept', 'procedure', 'reference'],
                        help="Run validation with queries from a specific category")
    parser.add_argument("--consistency-test", action="store_true",
                        help="Run consistency test on a query instead of full validation")
    parser.add_argument("--test-query", type=str, help="Test a specific query for consistency")

    args = parser.parse_args()

    try:
        if args.consistency_test or args.test_query:
            # Run consistency test
            client = connect_to_qdrant()
            test_query = args.test_query or "What is Physical AI?"
            consistency_result = validate_retrieval_consistency(client, test_query)
            logger.info(f"Consistency test result: {consistency_result}")
        else:
            # Run full validation pipeline
            run_complete_validation_pipeline(test_query=args.query, category=args.category)

    except KeyboardInterrupt:
        logger.info("Validation interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error during validation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()