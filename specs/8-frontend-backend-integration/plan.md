# Implementation Plan: Frontend and Backend Integration

## Technical Context

### Current State
- Docusaurus frontend exists for the Physical AI book
- FastAPI RAG backend is implemented and running
- Need to connect the two systems for user interaction
- Backend has /query endpoint that accepts QueryRequest and returns QueryResponse

### Target State
- Docusaurus frontend with integrated chatbot UI
- User can submit queries to backend from within the book
- Responses displayed in the book UI with proper formatting
- Support for both full-book and selected-text queries

### Architecture Components
- Frontend: Docusaurus React components for chat interface
- Communication: HTTP/HTTPS API calls to backend
- Backend: FastAPI service with RAG agent
- Data flow: QueryRequest → FastAPI → RAG processing → QueryResponse

### Unknowns
- [NEEDS CLARIFICATION: What is the current structure of the Docusaurus frontend? Are there existing components we should extend or should we create new ones?]
- [NEEDS CLARIFICATION: What is the expected UI placement for the chatbot? Should it be a sidebar, bottom widget, or page-integrated component?]

## Constitution Check

Based on the project constitution principles:
- ✅ Spec-First, AI-Native Development: Following the specification created in spec.md
- ✅ Technical Accuracy and Verifiability: Using actual existing backend API
- ✅ Clear, Developer-Focused Explanations: Plan includes clear implementation steps
- ✅ No Hallucinated APIs: Using the real backend API that was already implemented
- ✅ Free-Tier Compatible Services: Docusaurus and FastAPI are free-tier compatible
- ✅ Modularity and Independence: Frontend integration will be modular

## Phase 0: Research

### Research Tasks Completed

**Decision**: Use React-based chat component for Docusaurus integration
**Rationale**: Docusaurus is React-based, so React components integrate naturally
**Alternatives considered**: Plain JavaScript, Vue, Angular - React chosen for compatibility

**Decision**: Implement as a floating chat widget positioned at the bottom right
**Rationale**: Common pattern for chatbots, doesn't interfere with main content, always accessible
**Alternatives considered**: Sidebar integration, top-bar widget - floating widget provides best UX

**Decision**: Use standard fetch API for HTTP communication with backend
**Rationale**: Native browser API, no additional dependencies, well-supported
**Alternatives considered**: Axios, other HTTP libraries - fetch is sufficient for this use case

### Assumptions Resolved
- Docusaurus is configured with standard setup allowing custom components
- Backend API is available at a configurable endpoint (default: http://localhost:8000)
- CORS is configured to allow frontend-backend communication

## Phase 1: Design

### Data Model

#### QueryRequest (from backend)
- query: string (user's question)
- max_results: number (optional, default 5)
- similarity_threshold: number (optional, default 0.5)
- context: object (optional, for selected text context)

#### QueryResponse (from backend)
- query: string (original user query)
- answer: string (generated answer)
- retrieved_chunks: array (context chunks used)
- timestamp: string (ISO format)
- sources: array (source URLs)

#### Frontend-specific entities
- ChatMessage: {id, text, sender, timestamp, sources}
- ChatState: {messages, isLoading, error, context}
- UIConfiguration: {backendUrl, position, theme, etc.}

### API Contracts

#### Backend API (already implemented)
- POST /query: Accepts QueryRequest, returns QueryResponse
- GET /health: Returns health status

#### Frontend Integration Points
- Chat component renders in Docusaurus layout
- Text selection detection and context capture
- Message history management
- Loading states and error handling

### Component Architecture

#### ChatWidget Component
- State management for messages, loading, errors
- UI for message display and input
- API communication logic
- Context capture (selected text)

#### Integration Layer
- API service module for backend communication
- Message formatting and history management
- Error handling and user feedback

#### UI Components
- Message bubbles (user vs agent)
- Input area with send button
- Loading indicators
- Error display
- Context indicators

## Implementation Approach

### Components to Implement

1. **Backend API Service**
   - HTTP client for communicating with FastAPI backend
   - Request/response formatting
   - Error handling and retry logic

2. **Chat Widget Component**
   - React component for the chat interface
   - State management for messages and UI state
   - Integration with Docusaurus layout

3. **Text Selection Integration**
   - Logic to detect user text selection
   - Context capture for selected text queries
   - Integration with query submission

4. **UI Components**
   - Message display with proper formatting
   - Input area with validation
   - Loading and error states
   - Source attribution for responses

5. **Configuration and Styling**
   - CSS styling for the chat widget
   - Configuration options for backend URL
   - Responsive design for different screen sizes

## Risk Mitigation

- **CORS Issues**: Configure backend to allow frontend domain
- **API Availability**: Implement proper error handling and user feedback
- **Performance**: Implement loading indicators and timeout handling
- **Text Selection**: Fallback to full-book context when no text selected
- **Security**: Validate user inputs before sending to backend
- **Responsive Design**: Ensure chat widget works on mobile devices