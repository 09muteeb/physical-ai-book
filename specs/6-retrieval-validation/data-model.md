# Data Model: Retrieval Pipeline and Data Validation

## QueryResult
Represents the output of a similarity search operation

**Fields:**
- id: str (unique identifier from Qdrant)
- content: str (the retrieved text content)
- source_url: str (URL where the content was originally found)
- metadata: dict (additional information like page title, section)
- similarity_score: float (the similarity score from the search, range 0.0-1.0)

**Validation Rules:**
- id must be a valid string identifier
- content must be non-empty
- source_url must be a valid URL format
- metadata must contain required fields: 'title', 'created_at'
- similarity_score must be between 0.0 and 1.0

## ValidationReport
Contains the results of validation checks performed on retrieved data

**Fields:**
- query: str (the original test query that was executed)
- timestamp: str (ISO format timestamp of when validation was performed)
- results_count: int (number of results returned from the search)
- validation_passed: bool (whether validation passed overall)
- accuracy_score: float (percentage of valid results, 0.0-1.0)
- details: dict (specific validation details and errors)
- performance_metrics: dict (response time and other performance data)

**Validation Rules:**
- query must be non-empty
- timestamp must be in ISO format
- results_count must be non-negative
- validation_passed must be a boolean
- accuracy_score must be between 0.0 and 1.0
- details must contain 'passed_count' and 'failed_count' keys

## TestQuery
A predefined query used to validate the retrieval pipeline

**Fields:**
- id: str (unique identifier for the test query)
- text: str (the actual query text to be used)
- expected_content_keywords: list[str] (keywords expected to appear in relevant results)
- category: str (category of query, e.g., 'concept', 'procedure', 'reference')
- priority: str (priority level: 'high', 'medium', 'low')

**Validation Rules:**
- id must be unique across all test queries
- text must be non-empty
- expected_content_keywords must be a list of non-empty strings
- category must be one of the allowed values
- priority must be one of the allowed values

## ValidationRule
Defines criteria for validating retrieved results

**Fields:**
- rule_id: str (unique identifier for the validation rule)
- rule_type: str (type of validation: 'content_accuracy', 'metadata_completeness', 'similarity_threshold')
- description: str (description of what the rule validates)
- threshold: float (threshold value for validation, if applicable)
- enabled: bool (whether this rule is currently active)

**Validation Rules:**
- rule_id must be unique
- rule_type must be one of the allowed values
- description must be non-empty
- threshold must be between 0.0 and 1.0 if applicable
- enabled must be a boolean