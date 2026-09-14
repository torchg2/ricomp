const V=2;
const C="ricomp-v"+V;
const F=["./","./index.html","./manifest.json","./icon-192.png","./icon-512.png","./icon-maskable-512.png"];
self.addEventListener("install",e=>{self.skipWaiting();
 e.waitUntil(caches.open(C).then(c=>c.addAll(F)).catch(()=>{}))});
self.addEventListener("activate",e=>{e.waitUntil(
 caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==C).map(k=>caches.delete(k))))
 .then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{if(e.request.method!=="GET")return;
 const nav=e.request.mode==="navigate";
 const req=nav?new Request(e.request,{cache:"no-cache"}):e.request;
 e.respondWith(fetch(req).then(r=>{const cp=r.clone();
  caches.open(C).then(c=>c.put(e.request,cp)).catch(()=>{});return r})
  .catch(()=>caches.match(e.request).then(r=>r||caches.match("./index.html"))))});
