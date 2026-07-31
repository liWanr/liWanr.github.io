/**
 * Vercel Speed Insights initialization for static MkDocs site
 * 
 * This script initializes Vercel Speed Insights to track web vitals
 * and performance metrics for the site.
 * 
 * Documentation: https://vercel.com/docs/speed-insights
 */

// Initialize Speed Insights queue before the main script loads
(function() {
  'use strict';
  
  // Check if we're in a browser environment
  if (typeof window === 'undefined') return;
  
  // Initialize the Speed Insights queue
  if (!window.si) {
    window.si = function() {
      window.siq = window.siq || [];
      window.siq.push(arguments);
    };
  }
  
  // Function to inject the Speed Insights script
  function injectSpeedInsights() {
    // Check if script is already loaded
    var scriptSrc = '/_vercel/speed-insights/script.js';
    if (document.head.querySelector('script[src*="' + scriptSrc + '"]')) {
      return;
    }
    
    // Create and configure the script element
    var script = document.createElement('script');
    script.src = scriptSrc;
    script.defer = true;
    
    // Set data attributes for configuration
    script.dataset.sdkn = '@vercel/speed-insights';
    script.dataset.sdkv = '2.0.0';
    
    // Error handling
    script.onerror = function() {
      console.log(
        '[Vercel Speed Insights] Failed to load script from ' + scriptSrc + '. ' +
        'Please check if any content blockers are enabled and try again.'
      );
    };
    
    // Inject the script into the page
    document.head.appendChild(script);
  }
  
  // Initialize when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', injectSpeedInsights);
  } else {
    injectSpeedInsights();
  }
})();
