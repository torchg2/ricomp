var fail = 0;
var t = function(name, fn) {
  try { fn(); console.log('  ok   ' + name); }
  catch (e) { fail++; console.log('  FAIL ' + name + ' -> ' + e.message); }
};
var eq = function(a, b, m) {
  if (JSON.stringify(a) !== JSON.stringify(b))
    throw new Error((m || '') + ' atteso ' + JSON.stringify(b) + ', trovato ' + JSON.stringify(a));
};
var ok = function(c, m) { if (!c) throw new Error(m || 'falso'); };
var T = today();

console.log('\n--- dati ---');
t('più di 450 alimenti, ordinati, con la categoria sushi', () => {
  ok(DB.foods.length > 450, 'alimenti: ' + DB.foods.length);
  const n = DB.foods.map(f => f.n.toLowerCase());
  eq(n.slice().sort(), n, 'ordine alfabetico');
  ok(DB.cats.indexOf('sushi') >= 0, 'manca la categoria sushi');
  const s = DB.foods.find(f => f.n === 'Nigiri salmone'); ok(s && s.u === 'pezzo', 'nigiri a pezzo');
  ok(DB.foods.find(f => f.n === 'Broccoli bolliti'), 'verdure bollite');
  ok(DB.foods.find(f => f.n === 'Salsa tonnata'), 'salsa tonnata');
});
t('80 opzioni, 20 per pasto, tutte con etichetta e peso', () => {
  ['colazione', 'pranzo', 'spuntino', 'cena'].forEach(m => {
    eq(DB.meals[m].length, 20, m);
    DB.meals[m].forEach(o => { ok(DB.labs[o.lab], o.n + ': etichetta ' + o.lab); ok(o.peso > 50, o.n + ': peso'); });
  });
});
t('ogni opzione entro 45 kcal dal target del suo pasto', () => {
  const tg = { colazione: 550, pranzo: 620, spuntino: 330, cena: 550 };
  Object.keys(tg).forEach(m => DB.meals[m].forEach(o => ok(Math.abs(o.kcal - tg[m]) <= 45, o.n + ' ' + o.kcal)));
});
t('target rev.3: 2050 / 1900, storta 2150, proteine 135', () => {
  eq(DB.target.allen.kcal, 2050); eq(DB.target.riposo.kcal, 1900); eq(DB.target.storta.kcal, 2150);
  eq(DB.target.allen.p, 135); eq(DB.target.storta.p, 135);
});
t('sedute con recupero, riscaldamento per zona, prima/durante sui 23', () => {
  ['A', 'B', 'C', 'D'].forEach(k => DB.sedute[k].ex.forEach(e => ok(e.rest > 0, k + ' ' + e.n)));
  eq(DB.warm.alta.length, 4); eq(DB.warm.bassa.length, 4);
  eq(Object.keys(DB.ex).length, 23);
  Object.keys(DB.ex).forEach(n => { ok(DB.ex[n].prima.length > 30, n + ' prima'); ok(DB.ex[n].durante.length > 30, n + ' durante'); });
  eq(Object.keys(SVG).length, 23);
});

console.log('\n--- ricerca ---');
t('tollera un errore di battitura', () => {
  ok(score('Yogurt greco 0%', 'yougurt') >= 0, 'yougurt');
  ok(score('Broccoli bolliti', 'brocoli') >= 0, 'brocoli');
  ok(score('Petto di pollo crudo', 'polo') >= 0, 'polo');
  eq(score('Mela', 'xyz'), -1);
});
t('chi inizia con la query viene prima, la ricerca attraversa tutte le fonti', () => {
  const r = rank(allFoods(), 'pol', x => x.n).map(x => x.n);
  ok(r[0].toLowerCase().indexOf('pol') === 0, 'primo: ' + r[0]);
  pSlot = 'pranzo'; pQ = 'pollo'; pCat = null; pAdded = []; renderPick();
  const h = el('sbody').innerHTML;
  ok(h.indexOf('Dal piano') >= 0 && h.indexOf('Alimenti') >= 0 && h.indexOf('Piatti tipici') >= 0);
});
t('le opzioni del piano si trovano anche per ingrediente', () => {
  pSlot = 'cena'; pQ = 'sgombro'; pCat = null; renderPick();
  ok(el('sbody').innerHTML.indexOf('Sgombro e patate') >= 0);
});
t('nomi con apostrofo selezionabili (indice, non JSON inline)', () => {
  pSlot = 'colazione'; pQ = "burro d'ar"; pCat = null; renderPick();
  const h = el('sbody').innerHTML;
  ok(h.indexOf('qtyI(') >= 0 && h.indexOf("Burro d'arachidi") >= 0);
});

console.log('\n--- inserimento ---');
t('la scheda resta aperta dopo Aggiungi e il pulsante diventa Fatto', () => {
  cur = T; day(T).m.pranzo = []; pick('pranzo');
  qty(food('Petto di pollo crudo'), 'g', 150); qAdd();
  eq(day(T).m.pranzo.length, 1);
  eq(el('sclose').textContent, 'Fatto');
  ok(el('sbody').innerHTML.indexOf('Aggiunto: Petto di pollo crudo') >= 0);
});
t('la quantità proposta e l ultima usata', () => {
  qty(food('Petto di pollo crudo')); eq(qMode, 'g'); eq(qVal, 150);
  qty(food('Uovo intero'), 'u', 3); qAdd();
  qty(food('Uovo intero')); eq(qMode, 'u'); eq(qVal, 3);
});
t('opzione del piano aggiunta con undo di gruppo', () => {
  day(T).m.cena = []; pick('cena'); addMeal(0);
  const n = DB.meals.cena[0].items.length;
  eq(day(T).m.cena.length, n); eq(ub.type, 'add'); eq(ub.n, n);
  undo(); eq(day(T).m.cena.length, 0);
});
t('Ripeti ieri copia il pasto e si annulla', () => {
  const Y = shift(T, -1); day(Y).m.colazione = [{ n: 'Skyr', g: 200, kcal: 126, p: 21, f: 0.4, c: 8, fib: 0 }];
  day(T).m.colazione = []; cur = T; ripeti('colazione');
  eq(day(T).m.colazione.length, 1); undo(); eq(day(T).m.colazione.length, 0);
});
t('modifica valori: per sempre e solo per questa volta', () => {
  pick('spuntino'); qty(food('Skyr'), 'g', 200);
  el('o-k').value = '130'; el('o-p').value = '22'; el('o-f').value = '0.4'; el('o-c').value = '8'; el('o-fb').value = '0';
  saveOvr(1); eq(S.ovr['Skyr'].p, 22); eq(food('Skyr').p, 22);
  el('o-p').value = '30'; saveOvr(0); eq(qCur.p, 30); eq(qCur.once, 1); eq(S.ovr['Skyr'].p, 22, 'per sempre non cambia');
  qAdd(); const it = day(T).m.spuntino[day(T).m.spuntino.length - 1]; eq(it.p, 60); eq(it.mod, 1);
  qty(food('Skyr')); resetOvr(); ok(!S.ovr['Skyr']); eq(food('Skyr').p, DB.foods.find(f => f.n === 'Skyr').p);
});
t('conferma sul peso fuori da 40-150', () => {
  let asked = 0; global.confirm = () => { asked++; return false; };
  cur = T; setM('w', '7.1'); ok(!S.meas[T] || S.meas[T].w === undefined, 'salvato 7,1');
  eq(asked, 1); global.confirm = () => true;
  setM('w', '71'); eq(S.meas[T].w, 71);
});

console.log('\n--- settimana storta e target ---');
t('storta: tre pasti, target 2150, log quando si spegne', () => {
  cur = T; ok(!isStorta(T)); toggleStorta(); ok(isStorta(T)); eq(mealsFor(T).length, 3); eq(target(T).kcal, 2150);
  toggleStorta(); ok(!S.storta.on); eq(S.storta.log.length, 1); ok(isStorta(T), 'il giorno resta storto nel log');
  ok(!isStorta(shift(T, 1)), 'domani non lo e');
  ok(stortaRecente(shift(T, 3)));
  S.storta = { on: false, from: null, log: [] };
});
t('target per giorno: allenamento / riposo', () => {
  day(T).tr = true; eq(target(T).kcal, 2050); day(T).tr = false; eq(target(T).kcal, 1900);
});
t('Calcola dai dati: 71 kg da 2050 / 1900', () => {
  S.tg = null; S.prof = null; renderMisure();
  el('s-peso').value = '71'; el('s-eta').value = '35'; el('s-alt').value = '181'; calcTg();
  eq(+el('ta-kcal').value, 2050); eq(+el('tr-kcal').value, 1900); eq(+el('ta-p').value, 135);
});
t('domanda dei 21 giorni: si alza di 100', () => {
  S.days = {}; S.meas = {}; S.tg = null; S.check21 = null;
  const F = shift(T, -25); day(F).m.pranzo = [{ n: 'x', g: 100, kcal: 500, p: 30, f: 10, c: 50, fib: 2 }];
  ok(check21Card().length > 0, 'card assente');
  risp21(1); eq(TG().allen.kcal, 2150); eq(check21Card(), '');
  S.tg = null; S.check21 = null;
});

console.log('\n--- anca e migrazione ---');
t('il voto sta sul giorno corrente e si attribuisce a ieri', () => {
  const Y = shift(T, -1); day(Y).w = { done: true, sed: 'B', ex: {}, corta: false };
  cur = T; hip(2); eq(day(T).hip, 2); ok(day(Y).hip === null || day(Y).hip === undefined);
  renderAllen(); ok(el('allen-dyn').innerHTML.indexOf('dopo la seduta B') >= 0);
});
t('migrazione v2 -> v3 sposta il voto al giorno dopo', () => {
  const o = { v: 2, days: {}, meas: {}, custom: [], ovr: {}, sch: {} };
  o.days['2026-09-10'] = { m: {}, tr: true, sup: {}, water: 0, w: { done: true, sed: 'B', ex: {} }, hip: 2 };
  o.days['2026-09-11'] = { m: {}, tr: false, sup: {}, water: 0, w: { done: false, sed: null, ex: {} }, hip: 1 };
  o.days['2026-09-10'].m = { colazione: [{ n: 'Caffe', g: 30, kcal: 1, p: 0, f: 0, c: 0 }, { n: 'Skyr', g: 150, kcal: 90, p: 15, f: 0, c: 6 }] };
  S = Object.assign(blank(), o);
  ok(migraS(), 'la migrazione deve scattare su v2'); eq(S.v, 3);
  eq(day('2026-09-11').hip, 2); eq(day('2026-09-12').hip, 1); eq(day('2026-09-10').hip, null);
  eq(day('2026-09-10').m.colazione.map(i => i.n), ['Caffè', 'Skyr'], 'nomi rinominati nel diario');
  ok(!migraS(), 'non deve girare due volte');
  S = blank();
});

console.log('\n--- protocollo dei 14 giorni ---');
function seed(startDaysAgo, weights, ex) {
  S = blank(); S.seenVer = DB.ver;
  const F = shift(T, -startDaysAgo); day(F).m.pranzo = [{ n: 'x', g: 100, kcal: 500, p: 30, f: 10, c: 50, fib: 2 }];
  weights.forEach((w, i) => { const k = shift(T, -(weights.length - 1 - i)); S.meas[k] = { w: w }; });
}
t('tace prima del giorno 21', () => { seed(10, [71]); eq(proto().stato, 'presto'); });
t('chiede 14 pesate', () => { seed(30, [71, 71]); eq(proto().stato, 'pesi'); });
t('calo lento, non toccare', () => {
  seed(40, [71.4, 71.3, 71.4, 71.2, 71.3, 71.2, 71.3, 71.0, 71.0, 70.9, 71.0, 70.9, 70.9, 70.8]);
  const p = proto(); eq(p.stato, 'ok'); eq(p.delta, 0); ok(p.v.indexOf('Non toccare') === 0, p.v);
});
t('calo troppo veloce, aggiungi 150', () => {
  seed(40, [72, 72, 72, 72, 72, 72, 72, 71.2, 71.2, 71.2, 71.2, 71.2, 71.2, 71.2]);
  const p = proto(); eq(p.delta, 150);
});
t('peso e girovita in salita, togli 150', () => {
  seed(40, [70, 70, 70, 70, 70, 70, 70, 70.5, 70.5, 70.5, 70.5, 70.5, 70.5, 70.5]);
  S.meas[shift(T, -30)] = { v: 84 }; S.meas[T].v = 85.5;
  const p = proto(); eq(p.delta, -150);
});
t('forza in calo batte la bilancia', () => {
  seed(40, [71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71, 71]);
  day(shift(T, -6)).w = { done: true, sed: 'A', corta: false, ex: { 'Trazioni alla sbarra': -1 } };
  day(shift(T, -2)).w = { done: true, sed: 'A', corta: false, ex: { 'Trazioni alla sbarra': -1 } };
  const p = proto(); eq(p.delta, 150); ok(p.mot.indexOf('Trazioni') >= 0);
});
t('Applica: sposta i target e tace 14 giorni, mai sotto 1750', () => {
  seed(40, [70, 70, 70, 70, 70, 70, 70, 70.5, 70.5, 70.5, 70.5, 70.5, 70.5, 70.5]);
  S.meas[shift(T, -30)] = { v: 84 }; S.meas[T].v = 85.5;
  applyProto(-150); eq(TG().allen.kcal, 1900); eq(TG().riposo.kcal, 1750); eq(proto().stato, 'attesa');
  S.lastAdj = shift(T, -15); const p = proto(); eq(p.delta, 0, 'blocco sotto 1750'); ok(p.mot.indexOf('1750') >= 0);
});

console.log('\n--- rendering ---');
t('cinque schede si disegnano senza errori', () => {
  S = blank(); cur = T;
  ['oggi', 'piano', 'allen', 'mis', 'graf'].forEach(x => setTab(x));
  ok(el('piano-dyn').innerHTML.indexOf('Colazione') >= 0);
  ok(el('oggi-dyn').innerHTML.indexOf('Novità della v' + DB.ver) >= 0, 'card novita');
  ok(el('oggi-dyn').innerHTML.indexOf('Ripeti ieri') >= 0, 'ripeti ieri');
  ok(el('mis-dyn').innerHTML.indexOf('v' + DB.ver) >= 0, 'versione in Misure');
});
t('Piano: opzioni oltre il residuo in grigio, filtro per etichetta', () => {
  S = blank(); cur = T; day(T).tr = false;
  day(T).m.pranzo = [{ n: 'x', g: 0, kcal: 1700, p: 100, f: 60, c: 150, fib: 10 }];
  plLab = 'liquida'; plQ = ''; renderPiano();
  const h = el('piano-dyn').innerHTML;
  ok(h.indexOf('lrow dim') >= 0, 'nessuna opzione in grigio');
  ok(h.indexOf('Frullato completo') >= 0 && h.indexOf('Pasta al tonno') < 0, 'filtro etichetta');
  plLab = null;
});
t('scheda esercizio e scheda opzione', () => {
  exSheet('Stacco rumeno con i manubri');
  ok(el('s2body').innerHTML.indexOf('Prima') >= 0 && el('s2body').innerHTML.indexOf('<svg') >= 0);
  planSheet('cena', 0); ok(el('s2body').innerHTML.indexOf('Aggiungi a Cena') >= 0);
  day(T).m.cena = []; planAdd('cena', 0); eq(day(T).m.cena.length, DB.meals.cena[0].items.length);
});
t('grafici toccabili: CH registra le serie con le date', () => {
  S = blank(); for (let i = 9; i >= 0; i--) S.meas[shift(T, -i)] = { w: 70 + i / 10 };
  renderGrafici(); ok(CH.peso && CH.peso.labels.length === 10);
  chTouch({ target: { closest: () => ({ dataset: { id: 'peso' }, getBoundingClientRect: () => ({ left: 0, width: 300 }) }) }, clientX: 300 });
  ok(el('tip-peso').textContent.indexOf('70') >= 0, el('tip-peso').textContent);
});
t('timer parte e si ferma', () => { timer(60); ok(TM.end > Date.now()); timerStop(); eq(TM.iv, null); });
t('export/import con migrazione', () => {
  S = blank(); const raw = JSON.stringify({ v: 2, days: { '2026-09-10': { m: {}, w: { done: true, sed: 'A', ex: {} }, hip: 1 } }, meas: {}, custom: [], ovr: {}, sch: {} });
  global.FileReader = function () { const r = this; this.readAsText = () => { r.result = raw; r.onload(); }; };
  importJ({ files: [{}] }); eq(day('2026-09-11').hip, 1); eq(S.v, 3);
  ok(Object.keys(DB.ren).length >= 4 && DB.ren['Caffe'] === 'Caffè', 'mappa dei rinominati nel DB');
  ok(food('Caffè') && !food('Caffe'), 'il nuovo nome esiste, il vecchio no');
});

console.log('\n' + (fail ? fail + ' TEST FALLITI' : 'tutti i test passano') + '\n');
globalThis.__fail = fail;
