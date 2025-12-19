/**
 * Utility functions for text selection detection
 */

/**
 * Get the currently selected text in the browser
 * @returns {string} The selected text, or empty string if no text is selected
 */
export function getSelectedText() {
  const selection = window.getSelection();
  return selection ? selection.toString().trim() : '';
}

/**
 * Get detailed information about the current text selection
 * @returns {Object|null} Selection info or null if no selection
 */
export function getSelectedTextInfo() {
  const selection = window.getSelection();

  if (!selection || selection.toString().trim() === '') {
    return null;
  }

  const range = selection.rangeCount > 0 ? selection.getRangeAt(0) : null;

  if (!range) {
    return null;
  }

  return {
    text: selection.toString().trim(),
    startContainer: range.startContainer,
    startOffset: range.startOffset,
    endContainer: range.endContainer,
    endOffset: range.endOffset,
    rect: range.getBoundingClientRect ? range.getBoundingClientRect() : null
  };
}

/**
 * Check if text is currently selected on the page
 * @returns {boolean} True if text is selected
 */
export function isTextSelected() {
  return getSelectedText().length > 0;
}

/**
 * Get context information about the current page
 * @returns {Object} Page context information
 */
export function getPageContext() {
  return {
    current_page: window.location.pathname,
    page_title: document.title,
    url: window.location.href
  };
}

/**
 * Get selected text with additional context information
 * @returns {Object|null} Selected text with context or null if no selection
 */
export function getSelectedTextWithContext() {
  const selectedText = getSelectedText();

  if (!selectedText) {
    return null;
  }

  return {
    selected_text: selectedText,
    ...getPageContext()
  };
}

/**
 * Add event listener for text selection changes
 * @param {Function} callback - Function to call when selection changes
 * @returns {Function} Function to remove the event listener
 */
export function addSelectionListener(callback) {
  const handleSelectionChange = () => {
    callback(getSelectedTextWithContext());
  };

  document.addEventListener('selectionchange', handleSelectionChange);

  // Return cleanup function
  return () => {
    document.removeEventListener('selectionchange', handleSelectionChange);
  };
}