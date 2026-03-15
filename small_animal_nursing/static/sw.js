// Basic Service Worker to pass PWA install requirements
self.addEventListener('install', (event) => {
    console.log('Service Worker: Installed');
});

self.addEventListener('fetch', (event) => {
    // For now, we just let the browser handle all network requests normally
});