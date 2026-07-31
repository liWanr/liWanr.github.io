/**
 * Vercel Speed Insights Integration for MkDocs
 * This script injects the Vercel Speed Insights tracking code into the page
 */

(function() {
  'use strict';
  
  // Only run on production (when deployed to Vercel)
  // Speed Insights will not work in development mode anyway
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('[Speed Insights] Skipping in development mode');
    return;
  }

  // Initialize the Speed Insights queue
  window.si = window.si || function () { 
    (window.siq = window.siq || []).push(arguments); 
  };

  // Get script configuration from environment variables injected by Vercel
  var config = {};
  try {
    // Vercel injects VERCEL_OBSERVABILITY_CLIENT_CONFIG during build
    if (window.VERCEL_OBSERVABILITY_CLIENT_CONFIG) {
      config = JSON.parse(window.VERCEL_OBSERVABILITY_CLIENT_CONFIG);
    }
  } catch (e) {
    console.warn('[Speed Insights] Failed to parse config:', e);
  }

  // Default script source - will be updated by Vercel automatically
  var scriptSrc = config.scriptSrc || '/_vercel/speed-insights/script.js';
  
  // Load the Speed Insights script
  var script = document.createElement('script');
  script.src = scriptSrc;
  script.defer = true;
  script.onerror = function() {
    console.warn('[Speed Insights] Failed to load script from:', scriptSrc);
  };
  
  // Insert the script
  if (document.head) {
    document.head.appendChild(script);
  } else {
    document.addEventListener('DOMContentLoaded', function() {
      document.head.appendChild(script);
    });
  }

  console.log('[Speed Insights] Initialized');
})();
