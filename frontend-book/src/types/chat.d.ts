/**
 * TypeScript definitions for chat-related interfaces
 */

// Base request format for the RAG backend
export interface QueryRequest {
  query: string;
  max_results?: number;
  similarity_threshold?: number;
  context?: {
    selected_text?: string;
    current_page?: string;
    page_title?: string;
  };
}

// Response format from the RAG backend
export interface QueryResponse {
  query: string;
  answer: string;
  retrieved_chunks: Array<{
    id: string;
    content: string;
    source_url: string;
    metadata: {
      title: string;
      created_at: string;
    };
    similarity_score: number;
  }>;
  timestamp: string;
  sources: string[];
}

// Individual message in the chat
export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'agent';
  timestamp: string;
  sources?: string[];
  isLoading?: boolean;
  isError?: boolean;
}

// Current state of the chat
export interface ChatState {
  messages: ChatMessage[];
  isLoading: boolean;
  error?: string;
  context?: {
    selectedText?: string;
    currentPage?: string;
  };
}

// Configuration options for the chat UI
export interface UIConfiguration {
  backendUrl: string;
  position: 'bottom-right' | 'bottom-left' | 'top-right' | 'top-left';
  theme?: 'light' | 'dark' | 'auto';
  isOpen?: boolean;
  showOnAllPages?: boolean;
}

// Context information for queries
export interface QueryContext {
  selected_text?: string;
  current_page?: string;
  page_title?: string;
}