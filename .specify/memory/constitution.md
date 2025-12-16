<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles:
- Added 5 core principles based on project requirements
Added sections: Book Creation Standards, RAG Chatbot Standards, Constraints, Success Criteria
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ reviewed and aligned
- .specify/templates/spec-template.md ✅ reviewed and aligned
- .specify/templates/tasks-template.md ✅ reviewed and aligned
- .specify/templates/phr-template.prompt.md ✅ reviewed and aligned
Follow-up TODOs: None
-->

# Unified AI-Driven Book with Embedded RAG Chatbot Constitution

## Core Principles

### Spec-First, AI-Native Development
Every feature and component must be specified before implementation begins; All development follows AI-native patterns and leverages Claude Code + Spec-Kit Plus tools; Clear separation between business requirements and technical implementation.

### Technical Accuracy and Verifiability
All code and documentation must be technically accurate and verifiable against real implementations; No hallucinated APIs or undocumented behaviors allowed; All external dependencies and services must be validated and documented.

### Clear, Developer-Focused Explanations
Documentation and code must prioritize clarity and developer understanding; All examples must be complete, runnable, and well-explained; Focus on practical, implementable solutions rather than theoretical concepts.

### No Hallucinated APIs or Undocumented Behavior
Development must be based on real, existing APIs and documented behavior only; No invented interfaces, endpoints, or services without proper documentation; Strict adherence to existing technology capabilities and limitations.

### Free-Tier Compatible Services
All selected technologies and services must be compatible with free-tier offerings; No services that require paid plans for basic functionality; Cost-conscious decisions that maintain functionality while minimizing expenses.

### Modularity and Independence
Components must be modular and independently deployable where possible; Backend services should be deployable independently of frontend; Clear separation of concerns between book creation and RAG chatbot functionality.

## Book Creation Standards

Book Creation:
- Written using Claude Code + Spec-Kit Plus
- Built with Docusaurus
- Deployed to GitHub Pages
- Modular, chapter-based structure with code examples

## RAG Chatbot Standards

RAG Chatbot:
- Embedded in the book UI
- Uses OpenAI Agents / ChatKit SDKs
- Backend: FastAPI
- Storage: Neon Serverless Postgres
- Vector DB: Qdrant Cloud (Free Tier)
- Must answer book-wide questions
- Must answer questions based only on user-selected text
- No response without retrieval
- No hallucinated answers

## Constraints

- Free-tier compatible services only
- No hard-coded secrets
- Backend deployable independently
- Specs must precede implementation

## Success Criteria

- Book builds and deploys successfully
- RAG chatbot works in production
- Context-restricted answering

## Governance

All development must follow the Spec-First methodology with proper documentation before implementation. Changes to this constitution require explicit approval and must be documented in an Architectural Decision Record (ADR). All code reviews must verify compliance with these principles. Development workflow must follow the sequence: spec → plan → tasks → implementation.

**Version**: 1.1.0 | **Ratified**: 2025-12-16 | **Last Amended**: 2025-12-16