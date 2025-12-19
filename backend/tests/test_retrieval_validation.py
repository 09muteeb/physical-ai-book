"""
Tests for the retrieval validation system.
"""
import unittest
from retrieval_validation import (
    QueryResult,
    ValidationReport,
    TestQuery,
    ValidationRule,
    validate_text_accuracy,
    validate_metadata,
    validate_retrieved_data,
    generate_validation_report
)


class TestRetrievalValidation(unittest.TestCase):
    """Test cases for the retrieval validation system."""

    def test_query_result_validation(self):
        """Test QueryResult data class validation."""
        # Valid QueryResult
        result = QueryResult(
            id="test_id",
            content="This is test content",
            source_url="https://example.com",
            metadata={"title": "Test Title", "created_at": "2023-01-01"},
            similarity_score=0.8
        )
        self.assertEqual(result.id, "test_id")
        self.assertEqual(result.content, "This is test content")
        self.assertEqual(result.source_url, "https://example.com")
        self.assertEqual(result.metadata["title"], "Test Title")
        self.assertEqual(result.similarity_score, 0.8)

    def test_validation_report_validation(self):
        """Test ValidationReport data class validation."""
        report = ValidationReport(
            query="Test query",
            timestamp="2023-01-01T00:00:00",
            results_count=5,
            validation_passed=True,
            accuracy_score=0.9,
            details={"passed_count": 5, "failed_count": 0},
            performance_metrics={}
        )
        self.assertEqual(report.query, "Test query")
        self.assertTrue(report.validation_passed)

    def test_test_query_validation(self):
        """Test TestQuery data class validation."""
        query = TestQuery(
            id="test_query_1",
            text="What is test?",
            expected_content_keywords=["test", "example"],
            category="concept",
            priority="high"
        )
        self.assertEqual(query.id, "test_query_1")
        self.assertIn("test", query.expected_content_keywords)

    def test_validation_rule_validation(self):
        """Test ValidationRule data class validation."""
        rule = ValidationRule(
            rule_id="rule_1",
            rule_type="content_accuracy",
            description="Check content accuracy",
            threshold=0.7,
            enabled=True
        )
        self.assertEqual(rule.rule_type, "content_accuracy")
        self.assertTrue(rule.enabled)

    def test_validate_text_accuracy(self):
        """Test text accuracy validation."""
        content = "This document is about robotics and AI."
        expected_keywords = ["robotics", "AI"]

        result = validate_text_accuracy(content, expected_keywords)
        self.assertTrue(result)

        # Test with missing keywords
        expected_keywords_missing = ["robotics", "quantum"]
        result = validate_text_accuracy(content, expected_keywords_missing)
        # Should return True since we only require half the keywords
        self.assertTrue(result)

    def test_validate_metadata(self):
        """Test metadata validation."""
        # Valid metadata
        valid_metadata = {"title": "Test Title", "created_at": "2023-01-01"}
        result = validate_metadata(valid_metadata)
        self.assertTrue(result)

        # Invalid metadata - missing required field
        invalid_metadata = {"title": "Test Title"}  # missing created_at
        result = validate_metadata(invalid_metadata)
        self.assertFalse(result)

        # Invalid metadata - empty field
        invalid_metadata = {"title": "", "created_at": "2023-01-01"}
        result = validate_metadata(invalid_metadata)
        self.assertFalse(result)

    def test_validate_retrieved_data(self):
        """Test validation of retrieved data."""
        # Create test QueryResults
        results = [
            QueryResult(
                id="result_1",
                content="This is valid content",
                source_url="https://example.com/1",
                metadata={"title": "Title 1", "created_at": "2023-01-01"},
                similarity_score=0.8
            )
        ]

        validation_status, validation_details = validate_retrieved_data(results)
        self.assertTrue(validation_status)
        self.assertEqual(len(validation_details), 1)

    def test_generate_validation_report(self):
        """Test validation report generation."""
        results = [
            QueryResult(
                id="result_1",
                content="Test content",
                source_url="https://example.com",
                metadata={"title": "Title", "created_at": "2023-01-01"},
                similarity_score=0.8
            )
        ]

        validation_details = [{
            'id': 'result_1',
            'content_valid': True,
            'metadata_valid': True,
            'errors': []
        }]

        report = generate_validation_report("Test query", results, validation_details)
        self.assertEqual(report.query, "Test query")
        self.assertTrue(report.validation_passed)
        self.assertEqual(report.results_count, 1)


if __name__ == '__main__':
    unittest.main()