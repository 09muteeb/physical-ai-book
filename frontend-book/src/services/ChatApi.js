/**
 * API service for communicating with the RAG backend
 */
class ChatApi {
  constructor(backendUrl = 'http://localhost:8000') {
    this.backendUrl = backendUrl;
  }

  /**
   * Send a query to the RAG backend
   * @param {string} query - The user's query
   * @param {Object} options - Additional options for the query
   * @param {number} options.max_results - Maximum number of results to retrieve (default: 5)
   * @param {number} options.similarity_threshold - Minimum similarity threshold (default: 0.5)
   * @param {Object} options.context - Context information for the query
   * @returns {Promise<Object>} The response from the backend
   */
  async query(query, options = {}) {
    const {
      max_results = 5,
      similarity_threshold = 0.5,
      context = null
    } = options;

    const requestBody = {
      query,
      max_results,
      similarity_threshold
    };

    // Add context if provided
    if (context) {
      requestBody.context = context;
    }

    try {
      const response = await fetch(`${this.backendUrl}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status} - ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error communicating with backend:', error);
      throw error;
    }
  }

  /**
   * Check if the backend service is healthy
   * @returns {Promise<boolean>} True if the service is healthy
   */
  async healthCheck() {
    try {
      const response = await fetch(`${this.backendUrl}/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}

export default ChatApi;