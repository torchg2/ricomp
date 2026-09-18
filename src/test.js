// Esegue il JS generato con un DOM finto e prova i percorsi principali.
//   node test.js
const fs = require('fs');

const store = {};
const els = {};
function el(id) {
  if (!els[id]) els[id] = {
    id, innerHTML: '', textContent: '', value: '', style: {}, dataset: {}, files: [],
    classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
    click() {}, remove() {}, appendChild() {}, addEventListener() {},
    setAttribute() {}, closest() { return null; },
    getBoundingClientRect() { return { left: 0, width: 300 }; },
  };
  return els[id];
}
global.localStorage = {
  getItem: k => (k in store ? store[k] : null),
  setItem: (k, v) => { store[k] = v; },
};
global.document = {
  getElementById: el,
  createElement: () => el('_tmp'),
  body: { appendChild() {} },
  addEventListener() {},
};
global.window = { scrollTo() {}, addEventListener() {} };
global.navigator = { vibrate() {} };
global.alert = m => { throw new Error('alert: ' + m); };
global.confirm = () => true;
global.URL = { createObjectURL: () => 'blob:' };
global.Blob = function () {};
global.File = function () {};
global.setInterval = () => 1; global.clearInterval = () => {};
global.setTimeout = () => 1; global.clearTimeout = () => {};

const html = fs.readFileSync(__dirname + '/../index.html', 'utf8');
const js = html.match(/<script>\n([\s\S]*)\n<\/script>/)[1];
const tests = fs.readFileSync(__dirname + '/tests_body.js', 'utf8');
eval(js + '\n' + tests);
process.exit(globalThis.__fail ? 1 : 0);
