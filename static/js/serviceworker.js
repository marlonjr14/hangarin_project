self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('v1').then(cache => {
      return cache.addAll([
        '/',
        '/index.html',
        '/main.js',
        '/icon-192.png',
        '/manifest.json'
      ]);
    })
  );
});
 
self.addEventListener('fetch', function(e) { 
  e.respondWith( 
    caches.match(e.request).then(function(response) { 
      return response || fetch(e.request); 
    }) 
  ); 
}); 