---
id: 1
title: Update Constitution
stage: constitution
date: 2025-12-16
surface: agent
model: Claude Sonnet 4.5
feature: none
branch: master
user: User
command: /sp.constitution
labels: [constitution, governance, principles]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

```
/sp.constitution

Project:
Unified AI-Driven Book with Embedded RAG Chatbot

Core Principles:
- Spec-first, AI-native development
- Technical accuracy and verifiability
- Clear, developer-focused explanations
- No hallucinated APIs or undocumented behavior

Key Standards:

Book Creation:
- Written using Claude Code + Spec-Kit Plus
- Built with Docusaurus
- Deployed to GitHub Pages
- Modular, chapter-based structure with code examples

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

Constraints:
- Free-tier compatible services only
- No hard-coded secrets
- Backend deployable independently
- Specs must precede implementation

Success Criteria:
- Book builds and deploys successfully
- RAG chatbot works in production
- Context-restricted answering
```

## Response snapshot

Updated the project constitution to reflect the requirements for the Unified AI-Driven Book with Embedded RAG Chatbot project. The new constitution includes 6 core principles: Spec-First AI-Native Development, Technical Accuracy and Verifiability, Clear Developer-Focused Explanations, No Hallucinated APIs or Undocumented Behavior, Free-Tier Compatible Services, and Modularity and Independence. It also includes specific sections for Book Creation Standards, RAG Chatbot Standards, Constraints, and Success Criteria as specified in the user input.

## Outcome

- ✅ Impact: Updated project constitution with specific principles and standards
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: Continue with feature specification and planning
- 🧠 Reflection: Constitution now properly reflects the project requirements and constraints

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): Standard constitution update
- Next experiment (smallest change to try): Begin feature specification based on updated constitution