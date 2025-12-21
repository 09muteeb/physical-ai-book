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
      // Determine if we need to handle relative URLs for production
      let fullUrl = `${this.backendUrl}/query`;

      // If backendUrl is a relative path (starts with /), combine with current origin
      if (this.backendUrl.startsWith('/')) {
        fullUrl = `${window.location.origin}${this.backendUrl}/query`;
      }

      const response = await fetch(fullUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify(requestBody),
        // Add timeout and other options for better mobile compatibility
        mode: 'cors',
        credentials: 'omit' // Use 'include' if you need to send cookies
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status} - ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error communicating with backend:', error);
      // Provide more detailed error information
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        console.error('Network error - likely a CORS or connectivity issue');
      }
      throw error;
    }
  }

  /**
   * Check if the backend service is healthy
   * @returns {Promise<boolean>} True if the service is healthy
   */
  async healthCheck() {
    try {
      // Handle relative URLs for production
      let fullUrl = `${this.backendUrl}/health`;
      if (this.backendUrl.startsWith('/')) {
        fullUrl = `${window.location.origin}${this.backendUrl}/health`;
      }

      const response = await fetch(fullUrl);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}

export default ChatApi;