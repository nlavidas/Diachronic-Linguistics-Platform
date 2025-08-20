// Minimal background script for Chrome extension
chrome.runtime.onInstalled.addListener(() => {
  console.log('Extension installed.');
});
// Background service worker
chrome.runtime.onInstalled.addListener(() => {
  console.log('Valency Annotator installed');
});

// Handle messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'saveAnnotation') {
    // Save to storage
    chrome.storage.local.set({
      [request.key]: request.data
    });
  }
});