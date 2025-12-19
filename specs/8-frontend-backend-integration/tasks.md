# Implementation Tasks: Frontend and Backend Integration

## Feature Overview
Connect the Docusaurus frontend to the FastAPI backend and enable user interactions with the RAG chatbot, supporting both general queries and context-specific queries based on user-selected text.

**Target**: Developers integrating the RAG backend with the published Docusaurus book frontend

## Implementation Strategy
Implement the frontend-backend integration in phases following the priority order of user stories. Start with foundational components, then implement each user story as a complete, independently testable increment. The MVP will include the basic chat widget that connects to the backend and displays responses.

## Dependencies
- User Story 1 (P1) must be completed before User Stories 2, 3, and 4
- Foundational phase tasks must be completed before any user story phases
- Backend API must be running for frontend integration testing

## Parallel Execution Opportunities
- [P] Tasks within each phase that operate on different files/components can be executed in parallel
- UI component development can run parallel to API service implementation
- Testing tasks can run in parallel with implementation tasks for the same components

---

## Phase 1: Setup

Setup foundational project structure and dependencies for the frontend-backend integration.

- [x] T001 Create src/components/ChatWidget directory structure for the chat component
- [x] T002 Verify FastAPI backend is running and accessible at http://localhost:8000
- [x] T003 Check CORS configuration on the backend to allow frontend communication
- [x] T004 Install any necessary Docusaurus development dependencies if needed

---

## Phase 2: Foundational Components

Implement foundational components that are needed across all user stories.

- [x] T005 Create API service module for backend communication in src/services/ChatApi.js
- [x] T006 [P] Define TypeScript interfaces/types for QueryRequest and QueryResponse based on data-model.md
- [x] T007 [P] Create ChatMessage and ChatState data models in src/types/chat.d.ts
- [x] T008 [P] Implement text selection detection utility in src/utils/textSelection.js
- [x] T009 Set up basic CSS styling for the chat widget component

---

## Phase 3: [US1] Connect Docusaurus Frontend to RAG Backend

As a developer integrating the RAG backend with the published Docusaurus book frontend, I want to establish a connection between the Docusaurus frontend and FastAPI backend so that users can interact with the RAG chatbot from within the book.

**Goal**: Establish communication between the frontend and backend services to allow data exchange.

**Independent Test**: The frontend can successfully send a query to the backend and receive a response.

**Tests**:
- Query is successfully sent from frontend to backend
- Response is received from backend and processed by frontend
- Error handling works when backend is unavailable

- [x] T010 [US1] Create basic ChatWidget React component skeleton in src/components/ChatWidget/ChatWidget.js
- [x] T011 [US1] Implement API call to backend /query endpoint from the chat component
- [x] T012 [US1] Handle successful response from backend and display in UI
- [x] T013 [US1] Implement basic error handling for API failures
- [x] T014 [US1] Add loading state during API calls
- [ ] T015 [US1] Test basic communication with backend API using sample queries

---

## Phase 4: [US2] Send User Queries to Backend API

As a developer, I want to implement functionality to send user queries from the frontend to the backend API so that users can ask questions about the book content.

**Goal**: Enable users to input queries in the frontend interface and send them to the backend API with proper formatting.

**Independent Test**: User can enter a query in the frontend and it is successfully transmitted to the backend API.

**Tests**:
- User query is sent to backend API with proper formatting
- Selected text context is included when available

- [x] T016 [US2] Create input field and submit button in the chat widget UI
- [x] T017 [US2] Implement form submission handling with validation
- [x] T018 [US2] Format QueryRequest with user input and default parameters
- [x] T019 [US2] Integrate text selection detection with query submission
- [x] T020 [US2] Add query validation before sending to backend
- [ ] T021 [US2] Test query transmission with various inputs and selected text scenarios

---

## Phase 5: [US3] Display Agent Responses in Book UI

As a developer, I want to display agent responses in the book UI so that users can see answers to their questions within the context of the book.

**Goal**: Present the backend's responses in an accessible format within the book interface with proper formatting.

**Independent Test**: Backend responses are properly displayed in the frontend UI with appropriate formatting.

**Tests**:
- Agent response is displayed in the book UI with proper formatting
- Source information is shown when included in the response

- [x] T022 [US3] Implement message display area in the chat widget UI
- [x] T023 [US3] Format agent responses with proper styling and layout
- [x] T024 [US3] Display source information from the QueryResponse
- [x] T025 [US3] Implement message history with user and agent differentiation
- [x] T026 [US3] Add auto-scroll to latest message functionality
- [ ] T027 [US3] Test response display with various content types and source attribution

---

## Phase 6: [US4] Support Full Book Context or User-Selected Text Queries

As a developer, I want to support queries based on either full book context or user-selected text so that users can ask questions about specific content or general book topics.

**Goal**: Provide flexibility in how users can interact with the RAG system by supporting both broad and specific queries.

**Independent Test**: Queries with and without selected text are processed appropriately with different context.

**Tests**:
- Query with selected text uses that text as context
- General query without selected text uses full book context

- [x] T028 [US4] Enhance QueryRequest formatting to include context information
- [x] T029 [US4] Implement context detection for selected text vs general queries
- [x] T030 [US4] Add current page information to query context
- [x] T031 [US4] Update API service to handle context-rich queries
- [ ] T032 [US4] Test context-specific queries with selected text
- [ ] T033 [US4] Test general queries without selected text

---

## Phase 7: Integration and Testing

Integrate all components and test the complete frontend-backend workflow.

- [x] T034 Implement comprehensive error handling with user feedback
- [x] T035 Add configuration options for backend URL and UI positioning
- [ ] T036 Create message history management and storage
- [ ] T037 Test complete end-to-end workflow from query to response
- [ ] T038 Implement responsive design for mobile compatibility
- [ ] T039 Test error scenarios and ensure proper user feedback

---

## Phase 8: Polish & Cross-Cutting Concerns

Final polish and cross-cutting concerns for the frontend-backend integration.

- [ ] T040 Add comprehensive loading indicators and UX enhancements
- [x] T041 Integrate the chat widget into the Docusaurus layout/theme
- [ ] T042 Add accessibility features and keyboard navigation
- [ ] T043 Create documentation for the chat widget integration
- [ ] T044 Perform final integration testing of all components
- [ ] T045 Optimize performance and implement caching if needed