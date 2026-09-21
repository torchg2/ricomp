const V="ricomp-v3.2";
const FILES=["./","./index.html","./manifest.json","./icon-192.png","./icon-512.png","./icon-maskable-512.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(FILES)));self.skipWaiting()});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(
 ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{if(e.request.method!=="GET")return;
 const nav=e.request.mode==="navigate";
 e.respondWith(fetch(e.request,nav?{cache:"no-cache"}:undefined).then(r=>{
  const cp=r.clone();caches.open(V).then(c=>c.put(e.request,cp));return r
 }).catch(()=>caches.match(e.request).then(m=>m||caches.match("./index.html"))))});
