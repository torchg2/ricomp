# -*- coding: utf-8 -*-
"""Assembla index.html, sw.js e manifest.json.

    python3 build_app.py

Scrive nella cartella superiore (la root del repo). Non tocca i dati sul
telefono: quelli stanno in localStorage e sopravvivono agli aggiornamenti.
"""

import json
import os
import sys

from foods import FOODS, CATEGORIE, RINOMINATI
from meals import MEALS, ETICHETTE, REGOLE
from app_data import (VERSIONE, DATA_BUILD, NOME, NOME_LUNGO, NOVITA, PROFILO,
                      TARGET, FATTORE_ATTIVITA, DEFICIT, DELTA_RIPOSO, KCAL_MINIME,
                      GIORNI_CREATINA, PASSO_MAX, PIATTI, RISCALDAMENTO,
                      NOTA_MATTINO, SEDUTE)
from esercizi import ESERCIZI

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, ".."))

MEAL_KEYS = ["colazione", "pranzo", "spuntino", "cena"]
MEAL_LAB = {"colazione": "Colazione", "pranzo": "Pranzo",
            "spuntino": "Spuntino", "cena": "Cena"}
# quota di calorie per pasto: 550 / 620 / 330 / 550 su 2.050
MEAL_SHARE = {"colazione": 0.268, "pranzo": 0.302, "spuntino": 0.161, "cena": 0.268}
# settimana storta: tre pasti
MEAL_SHARE_STORTA = {"colazione": 0.30, "pranzo": 0.37, "cena": 0.33}

BYNAME = {f["n"]: f for f in FOODS}


def err(msg):
    print("ERRORE: " + msg)
    sys.exit(1)


def calcola_pasto(items):
    t = {"kcal": 0.0, "p": 0.0, "f": 0.0, "c": 0.0, "fib": 0.0}
    peso = 0
    for nome, g in items:
        f = BYNAME.get(nome)
        if not f:
            err("l'opzione pasto usa '%s', che non esiste in foods.py" % nome)
        k = g / 100.0
        for key in t:
            t[key] += f[key] * k
        peso += g
    out = {key: round(v) for key, v in t.items()}
    out["peso"] = peso
    return out


def build_meals():
    out = {}
    for slot in MEAL_KEYS:
        lst = []
        seen = set()
        for o in MEALS[slot]:
            if o["n"] in seen:
                err("opzione duplicata in %s: %s" % (slot, o["n"]))
            seen.add(o["n"])
            if o["lab"] not in ETICHETTE:
                err("etichetta sconosciuta '%s' in %s" % (o["lab"], o["n"]))
            m = calcola_pasto(o["items"])
            m.update({"n": o["n"], "nota": o["nota"], "lab": o["lab"],
                      "items": [{"n": n, "g": g} for n, g in o["items"]]})
            lst.append(m)
        out[slot] = lst
    return out


def build_sedute():
    out = {}
    nomi_ex = {e["n"] for e in ESERCIZI}
    for k, s in SEDUTE.items():
        for n, _pr, _r in s["ex"]:
            if n not in nomi_ex:
                err("la seduta %s usa '%s', che non è nell'appendice" % (k, n))
        for n in s["corta"]:
            if n not in [x[0] for x in s["ex"]]:
                err("la versione corta di %s cita '%s', che non è nella seduta" % (k, n))
        out[k] = {"nome": s["nome"], "zona": s["zona"], "nota": s.get("nota", ""),
                  "ex": [{"n": n, "pr": pr, "rest": r} for n, pr, r in s["ex"]],
                  "corta": s["corta"]}
    return out


def build_db():
    for old, new in RINOMINATI.items():
        if new not in BYNAME:
            err("RINOMINATI: '%s' non esiste tra gli alimenti" % new)
        if old in BYNAME:
            err("RINOMINATI: '%s' esiste ancora, va rinominato" % old)
    return {
        "foods": sorted(FOODS, key=lambda f: f["n"].lower()),
        "cats": CATEGORIE,
        "piatti": [{"n": n, "kcal": k, "p": p, "f": f, "c": c, "fib": fib}
                   for n, k, p, f, c, fib in PIATTI],
        "meals": build_meals(),
        "labs": ETICHETTE,
        "regole": REGOLE,
        "sedute": build_sedute(),
        "warm": RISCALDAMENTO,
        "notaMattino": NOTA_MATTINO,
        "ex": {e["n"]: {"desc": e["desc"], "prima": e.get("prima", ""),
                        "durante": e.get("durante", ""), "att": e["att"],
                        "sedute": e["sedute"]} for e in ESERCIZI},
        "target": TARGET,
        "prof": PROFILO,
        "att": FATTORE_ATTIVITA,
        "deficit": DEFICIT,
        "dRip": DELTA_RIPOSO,
        "kmin": KCAL_MINIME,
        "gCre": GIORNI_CREATINA,
        "passo": PASSO_MAX,
        "share": MEAL_SHARE,
        "shareStorta": MEAL_SHARE_STORTA,
        "novita": NOVITA,
        "ren": RINOMINATI,
        "ver": VERSIONE,
        "data": DATA_BUILD,
    }


# ------------------------------------------------------------------ CSS

CSS = """
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{--bg:#faf9f7;--card:#fff;--soft:#f1efe8;--line:#e4e1d8;--tx:#2c2c2a;--tx2:#6b6a64;--tx3:#9a9891;
--acc:#534ab7;--accbg:#eeedfe;--ok:#0f6e56;--okbg:#e1f5ee;--warn:#854f0b;--warnbg:#faeeda;
--cor:#993c1d;--corbg:#faece7;--blu:#1f5f9e;--blubg:#e3eefa;
--fig:#2c2c2a;--fig2:#5f5e5a;--fig3:#9a9891;--figline:#c4c2ba;--figar:#c2703a;--figband:#7f77dd}
@media(prefers-color-scheme:dark){:root{--bg:#17171a;--card:#1f1f23;--soft:#26262b;--line:#33333a;
--tx:#ececea;--tx2:#a3a29c;--tx3:#75746f;--acc:#afa9ec;--accbg:#2b2857;--ok:#5dcaa5;--okbg:#0f3b31;
--warn:#fac775;--warnbg:#40290a;--cor:#f0997b;--corbg:#431c0f;--blu:#8fc0f0;--blubg:#12304d;
--fig:#dcdbd6;--fig2:#a8a69f;--fig3:#6f6e69;--figline:#4a4952;--figar:#e2a074;--figband:#9a92e8}}
html,body{margin:0;padding:0;background:var(--bg);color:var(--tx);
font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
font-size:15px;line-height:1.5;-webkit-text-size-adjust:100%;overscroll-behavior-y:contain;
font-variant-numeric:tabular-nums;font-feature-settings:"tnum" 1}
#app{max-width:520px;margin:0 auto;padding:0 12px 96px}
h2{font-size:17px;font-weight:600;margin:18px 0 8px}
h3{font-size:15px;font-weight:600;margin:18px 0 6px}
summary{cursor:pointer;list-style:none}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";float:right;color:var(--tx3);font-size:18px;line-height:1}
details[open]>summary::after{content:"\\2013"}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;margin:10px 0}
.card.r1{border-left:3px solid var(--acc)}
.card.r2{border-left:3px solid var(--ok)}
.card.r3{border-left:3px solid var(--warn)}
.card.dim{opacity:.6}
.pad{padding:12px 14px}
.slab{font-size:11px;text-transform:uppercase;letter-spacing:.8px;color:var(--tx3);
font-weight:600;margin:16px 2px 4px}
.row{display:flex;align-items:center;justify-content:space-between;gap:10px}
.mut{color:var(--tx2);font-size:13px}.mut3{color:var(--tx3);font-size:12px}
.big{font-size:28px;font-weight:600;line-height:1.1}
.bar{height:8px;background:var(--soft);border-radius:4px;overflow:hidden}
.bar>i{display:block;height:100%;background:var(--acc);border-radius:4px}
.bar.s{height:5px}.bar.s>i{background:var(--tx3)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px}
.seg{display:flex;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.seg>button{flex:1;border:0;background:transparent;color:var(--tx2);font-size:13px;padding:8px 10px;font-family:inherit;min-height:40px}
.seg>button.on{background:var(--acc);color:#fff}
button{font-family:inherit;cursor:pointer}
.btn{background:transparent;border:1px solid var(--line);border-radius:8px;padding:9px 12px;color:var(--tx);font-size:14px;min-height:40px}
.btn:active{transform:scale(.98)}
.btn.acc{background:var(--acc);color:#fff;border-color:var(--acc)}
.btn.ok{background:var(--ok);color:#fff;border-color:var(--ok)}
.btn.w{width:100%}
.btn.sm{padding:6px 10px;font-size:13px;min-height:36px}
.mhead{display:flex;align-items:flex-start;justify-content:space-between;gap:10px}
.mname{font-weight:600;font-size:16px}
.frow{display:flex;align-items:center;gap:6px;padding:6px 0;border-bottom:1px solid var(--line)}
.frow:last-of-type{border-bottom:0}
.fn{flex:1;min-width:0;font-size:14px;line-height:1.35;padding:4px 0}
.fg{color:var(--tx2)}
.fk{font-size:12px;color:var(--tx2);white-space:nowrap;text-align:right}
.fx{border:0;background:transparent;color:var(--tx3);font-size:22px;line-height:1;
width:44px;height:44px;margin-right:-10px;display:flex;align-items:center;justify-content:center}
.pill{display:inline-block;font-size:12px;padding:6px 11px;border-radius:8px;border:1px solid var(--line);
color:var(--tx3);background:transparent;margin:0 6px 6px 0;min-height:34px}
.pill.on{background:var(--okbg);color:var(--ok);border-color:var(--okbg)}
.lab{display:inline-block;font-size:10px;text-transform:uppercase;letter-spacing:.5px;font-weight:600;
padding:2px 7px;border-radius:5px;margin-left:6px;vertical-align:2px}
.lab.densa{background:var(--warnbg);color:var(--warn)}
.lab.media{background:var(--accbg);color:var(--acc)}
.lab.voluminosa{background:var(--okbg);color:var(--ok)}
.lab.liquida{background:var(--blubg);color:var(--blu)}
nav{position:fixed;left:0;right:0;bottom:0;background:var(--card);border-top:1px solid var(--line);
display:grid;grid-template-columns:repeat(5,1fr);z-index:40;padding-bottom:env(safe-area-inset-bottom)}
nav button{border:0;background:transparent;color:var(--tx3);font-size:10.5px;padding:7px 0 8px;letter-spacing:.2px}
nav button.on{color:var(--acc)}
nav svg{width:22px;height:22px;display:block;margin:0 auto 2px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.sheet{position:fixed;inset:0;background:var(--bg);z-index:60;display:none;flex-direction:column}
.sheet.on{display:flex}
.sheeth{padding:10px 12px;border-bottom:1px solid var(--line);background:var(--card);display:flex;gap:10px;align-items:center}
.sheetb{flex:1;overflow:auto;padding:0 12px 24px;max-width:520px;margin:0 auto;width:100%}
.added{background:var(--okbg);color:var(--ok);border-radius:8px;padding:8px 12px;font-size:13px;margin:10px 0 4px;display:flex;justify-content:space-between;gap:8px}
input,select,textarea{font-family:inherit;font-size:15px;background:var(--card);color:var(--tx);
border:1px solid var(--line);border-radius:8px;padding:9px 10px;width:100%;min-height:42px}
.lrow{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:11px 2px;border-bottom:1px solid var(--line);min-height:52px}
.lrow:active{background:var(--soft)}
.lrow.dim{opacity:.45}
.bdg{display:inline-block;font-size:10px;text-transform:uppercase;letter-spacing:.5px;
color:var(--tx3);border:1px solid var(--line);border-radius:4px;padding:1px 5px;margin-left:6px;
vertical-align:1px;font-weight:600}
.bdg.p{color:var(--acc);border-color:var(--acc)}
.chips{display:flex;gap:6px;overflow-x:auto;padding:8px 0 4px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.chips button{white-space:nowrap;border:1px solid var(--line);background:transparent;color:var(--tx2);
border-radius:16px;padding:7px 13px;font-size:13px;min-height:36px}
.chips button.on{background:var(--tx);color:var(--bg);border-color:var(--tx)}
.qb{width:44px;height:44px;border-radius:10px;border:1px solid var(--line);background:transparent;
color:var(--tx2);font-size:20px;display:flex;align-items:center;justify-content:center}
.qb.up{background:var(--okbg);color:var(--ok);border-color:var(--okbg)}
.qb.dn{background:var(--warnbg);color:var(--warn);border-color:var(--warnbg)}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.g4 button{padding:10px 0;border-radius:8px;border:1px solid var(--line);background:transparent;color:var(--tx2);font-size:15px;min-height:44px}
.g4 button.on{background:var(--ok);color:#fff;border-color:var(--ok)}
.note{background:var(--accbg);color:var(--acc);border-radius:8px;padding:10px 12px;font-size:13px;line-height:1.5;margin:10px 0}
.note.w{background:var(--warnbg);color:var(--warn)}
.note.g{background:var(--okbg);color:var(--ok)}
.prow{padding:10px 0;border-bottom:1px solid var(--line)}
.pn{font-weight:600;font-size:14px}
.pq{font-size:13px;color:var(--tx2);margin-top:3px;line-height:1.5}
.pnote{font-size:12px;color:var(--tx3);margin-top:2px;line-height:1.45}
.pm{font-size:12px;color:var(--acc);margin-top:4px}
.srow{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid var(--line);font-size:14px}
.exc{padding:14px 0;border-bottom:1px solid var(--line)}
.dgw{margin:8px 0}
.dgw svg{width:100%;height:auto;max-width:340px}
.attl{font-size:11px;text-transform:uppercase;letter-spacing:.7px;color:var(--cor);font-weight:600;margin:10px 0 2px}
.attl.k{color:var(--tx3)}
ul.att{margin:0;font-size:13px;color:var(--tx2);background:var(--corbg);border-radius:8px;padding:8px 10px 8px 26px}
ul.att li{margin-bottom:3px}
.exrow{padding:10px 0;border-bottom:1px solid var(--line)}
.exrow:last-child{border-bottom:0}
.exn{font-size:14px;font-weight:600;flex:1;min-width:0;padding:6px 0}
.exn i{font-style:normal;color:var(--tx3);font-weight:400}
.expr{font-size:17px;font-weight:600;color:var(--tx)}
.tbtn{border:1px solid var(--line);background:transparent;color:var(--tx2);border-radius:8px;padding:6px 10px;font-size:13px;min-height:36px}
.pm2{display:flex;gap:6px}
.undo{position:fixed;left:12px;right:12px;bottom:74px;background:var(--tx);color:var(--bg);border-radius:10px;
padding:11px 14px;display:none;z-index:50;font-size:14px;align-items:center;justify-content:space-between;
max-width:496px;margin:0 auto;gap:10px}
.undo.on{display:flex}
.undo button{background:transparent;border:0;color:var(--bg);font-weight:600;font-size:14px;text-decoration:underline;min-height:32px}
.tbar{position:fixed;left:12px;right:12px;bottom:74px;background:var(--acc);color:#fff;border-radius:10px;
padding:10px 14px;display:none;z-index:55;align-items:center;justify-content:space-between;max-width:496px;margin:0 auto;gap:10px}
.tbar.on{display:flex}
.tbar.done{background:var(--ok)}
.tbar b{font-size:22px;font-variant-numeric:tabular-nums}
.tbar button{background:rgba(255,255,255,.18);border:0;color:#fff;border-radius:8px;padding:7px 11px;font-size:13px;min-height:36px}
svg.ch{width:100%;height:auto;display:block}
.chw{touch-action:pan-y}
.chtip{font-size:12px;color:var(--tx2);min-height:18px;margin-top:4px}
.lg{display:flex;gap:14px;font-size:12px;color:var(--tx2);margin:4px 0 8px;flex-wrap:wrap}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px}
.dl{font-size:12px;color:var(--tx3);text-align:center;padding:14px 0 4px}
.ring{width:84px;height:84px;flex:0 0 84px}
.wk{display:flex;justify-content:space-between;margin:2px 0 12px}
.wk button{border:0;background:transparent;padding:0;width:34px;display:flex;flex-direction:column;align-items:center;gap:3px;color:var(--tx3);font-size:10px}
.wk i{display:block;width:12px;height:12px;border-radius:50%;border:1.5px solid var(--line);background:transparent}
.wk i.f{background:var(--acc);border-color:var(--acc)}
.wk i.t{box-shadow:0 0 0 2px var(--bg),0 0 0 3.5px var(--ok)}
.wk button.on{color:var(--tx)}
.wk button.on i{border-color:var(--tx)}
.dn2{text-align:center;flex:1}
.dn2 b{font-size:15px;display:block}
.stg{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:8px 0 0}
.sw{width:44px;height:26px;border-radius:13px;background:var(--line);position:relative;border:0;padding:0;flex:0 0 44px}
.sw::after{content:"";position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:#fff;transition:left .15s}
.sw.on{background:var(--warn)}.sw.on::after{left:21px}
.ing{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--line);font-size:14px}
.ing:last-child{border-bottom:0}
"""


# ------------------------------------------------- HTML statico (schede)

def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def html_regole():
    h = []
    for tit, testo in REGOLE:
        h.append('<div class="prow"><div class="pn">%s</div><div class="pq">%s</div></div>'
                 % (esc(tit), esc(testo)))
    h.append('<div class="pnote" style="margin-top:8px">Materiale informativo, non prescrizione '
             'dietetica. Per i prodotti confezionati fa fede l\'etichetta.</div>')
    return "\n".join(h)


def html_sedute(dbsed):
    h = []
    for k in ["A", "B", "C", "D"]:
        s = dbsed[k]
        h.append('<h3>Seduta %s &mdash; %s</h3>' % (k, esc(s["nome"])))
        if s["nota"]:
            h.append('<div class="pnote">%s</div>' % esc(s["nota"]))
        for e in s["ex"]:
            h.append('<div class="srow"><span>%s</span><b>%s &middot; %d s</b></div>'
                     % (esc(e["n"]), esc(e["pr"]), e["rest"]))
        h.append('<div class="pnote" style="margin-top:6px">Versione da 15 minuti: %s.</div>'
                 % esc(", ".join(s["corta"])))
    h.append("""
   <h3>Come progredire</h3>
   <div class="pq">Con due manubri da 3 kg non puoi aumentare il peso, quindi la progressione va in
   quest'ordine, una leva alla volta: numero di serie, poi ripetizioni, poi elastico più duro, poi
   tempo (3 secondi in discesa). Quando raggiungi il massimo di ripetizioni in tutte le serie, la
   volta dopo aumenti la difficoltà.</div>
   <h3>Dolore: come leggerlo</h3>
   <div class="pq">Indolenzimento normale: nella pancia del muscolo, sordo, compare dopo 24-48 ore,
   migliora muovendosi. Segnale da fermarsi: nell'inguine o davanti all'anca, acuto, pizzica o
   aggancia, peggiora con il movimento. In quel caso dimezzi l'ampiezza; se dopo una settimana resta,
   togli l'esercizio; se c'è anche senza allenarti o ti sveglia la notte, chiami l'ortopedico.</div>
   <h3>Cosa non fare mai</h3>
   <div class="pq">Squat profondo, affondi profondi, step-up su rialzi alti, sit-up e sollevamento
   gambe, rotazione dell'anca sotto carico, cyclette con sella bassa, stretching a piccione e
   allungamento aggressivo dei flessori dell'anca, corsa e salti ripetuti nei primi mesi.</div>
   <div class="pnote" style="margin-top:10px">La parte bassa va validata da un fisioterapista o da un
   medico dello sport. Interrompi e consulta un medico in caso di dolore acuto o blocco articolare.</div>""")
    return "\n".join(h)


def blocco_esercizio(e):
    att = "".join("<li>%s</li>" % a for a in e["att"])
    return ('<div class="pq">%s</div>'
            '<div class="attl k">Prima</div><div class="pq">%s</div>'
            '<div class="attl k">Durante</div><div class="pq">%s</div>'
            '<div class="attl">Attenzione</div><ul class="att">%s</ul>'
            % (e["desc"], e.get("prima", ""), e.get("durante", ""), att))


def html_appendice():
    h = []
    for e in ESERCIZI:
        h.append('<div class="exc"><div class="pn">%s</div>'
                 '<div class="pnote">Sedute: %s</div>'
                 '<div class="dgw">%s</div>%s</div>'
                 % (e["n"], e["sedute"], e["svg"], blocco_esercizio(e)))
    return "".join(h)


def svg_map():
    """Diagrammi per nome, usati dalla scheda esercizio al tocco."""
    return {e["n"]: e["svg"] for e in ESERCIZI}


# ------------------------------------------------------------------- JS
# Parte 1: stato, aiuti, scheda Oggi

JS1 = r"""
const MEALS=["colazione","pranzo","spuntino","cena"];
const MLAB={colazione:"Colazione",pranzo:"Pranzo",spuntino:"Spuntino",cena:"Cena"};
const LABN={densa:"Densa",media:"Media",voluminosa:"Voluminosa",liquida:"Liquida"};
const SUP=[["cre","Creatina"],["om","Omega-3"],["vd","Vitamina D"]];
const KEY="ricomp_v1";
const $=i=>document.getElementById(i);
const R=(n,d)=>{const m=Math.pow(10,d||0);return Math.round(n*m)/m};
const esc=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;");
const cap=s=>s.charAt(0).toUpperCase()+s.slice(1);
const PLUR={uovo:"uova",mezzo:"mezzi",media:"medie",medio:"medi",cono:"coni",bowl:"bowl",falafel:"falafel"};
function plur(u,n){if(n===1)return u;if(PLUR[u])return PLUR[u];
 const l=u.slice(-1);if(l==="a")return u.slice(0,-1)+"e";
 if(l==="o"||l==="e")return u.slice(0,-1)+"i";return u}
function nfmt(n){return String(n).replace(".",",")}
function haptic(ms){try{if(navigator.vibrate)navigator.vibrate(ms||12)}catch(e){}}

function blank(){return{v:3,days:{},meas:{},custom:[],ovr:{},sch:{1:"A",2:"B",4:"C",6:"D"},
 lastBackup:null,tg:null,prof:null,lastQty:{},seenVer:null,lastAdj:null,check21:null,
 storta:{on:false,from:null,log:[]},persist:null}}
let S=blank();
try{const raw=localStorage.getItem(KEY);if(raw)S=Object.assign(blank(),JSON.parse(raw))}catch(e){}
if(!S.storta)S.storta={on:false,from:null,log:[]};
if(!S.lastQty)S.lastQty={};
let warned=false;
function save(){try{localStorage.setItem(KEY,JSON.stringify(S))}catch(e){if(!warned){warned=true;
 alert("Memoria del telefono piena: esporta il backup.")}}}

function iso(d){return d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0")}
function parseIso(k){const p=k.split("-");return new Date(+p[0],+p[1]-1,+p[2])}
function shift(k,n){const d=parseIso(k);d.setDate(d.getDate()+n);return iso(d)}
function diffDays(a,b){return Math.round((parseIso(b)-parseIso(a))/864e5)}
const GG=["domenica","lunedì","martedì","mercoledì","giovedì","venerdì","sabato"];
const GGS=["D","L","M","M","G","V","S"];
const MM=["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"];
function human(k){const d=parseIso(k);return GG[d.getDay()]+" "+d.getDate()+" "+MM[d.getMonth()]}
function corto(k){const d=parseIso(k);return d.getDate()+"/"+(d.getMonth()+1)}
const today=()=>iso(new Date());
let cur=today(),tab="oggi";

/* --- migrazione: nella v2 il voto anca stava sul giorno della seduta,
   dato la mattina dopo. Dalla v3 sta sul giorno in cui lo dai. --- */
function migraS(){if((S.v||1)>=3)return false;
 const mv=[];Object.keys(S.days).forEach(k=>{const d=S.days[k];if(!d)return;
  if(d.hip!==null&&d.hip!==undefined){mv.push([shift(k,1),d.hip]);d.hip=null}
  Object.keys(d.m||{}).forEach(m=>(d.m[m]||[]).forEach(i=>{if(DB.ren[i.n])i.n=DB.ren[i.n]}))});
 mv.forEach(([k,v])=>{day(k).hip=v});S.v=3;return true}
if(migraS())save();

function day(k){if(!S.days[k]){const wd=parseIso(k).getDay();const sed=S.sch[wd]||null;
 S.days[k]={m:{},tr:!!sed,sup:{},water:0,w:{done:false,sed:sed,ex:{},corta:false,presto:false},hip:null}}
 const d=S.days[k];if(!d.m)d.m={};MEALS.forEach(m=>{if(!d.m[m])d.m[m]=[]});
 if(!d.sup)d.sup={};if(!d.w)d.w={done:false,sed:null,ex:{},corta:false,presto:false};
 if(!d.w.ex)d.w.ex={};if(d.water===undefined)d.water=0;if(d.hip===undefined)d.hip=null;return d}

/* --- target e settimana storta --- */
function TG(){const t=S.tg||DB.target;if(!t.storta)t.storta=DB.target.storta;return t}
function PR(){return S.prof||DB.prof}
function isStorta(k){const s=S.storta;if(!s)return false;
 if(s.on&&s.from&&k>=s.from)return true;
 return (s.log||[]).some(p=>k>=p.from&&k<=p.to)}
function stortaRecente(k){const s=S.storta;if(!s)return false;
 if(s.on)return true;
 return (s.log||[]).some(p=>diffDays(p.to,k)<=7&&diffDays(p.to,k)>=0)}
function mealsFor(k){return isStorta(k)?["colazione","pranzo","cena"]:MEALS}
function target(k){const d=day(k);if(isStorta(k))return TG().storta;return d.tr?TG().allen:TG().riposo}
function shareFor(k){return isStorta(k)?DB.shareStorta:DB.share}
function toggleStorta(){const s=S.storta,t=today();
 if(s.on){(s.log=s.log||[]).push({from:s.from,to:t});s.on=false;s.from=null}
 else{s.on=true;s.from=t}
 save();haptic();render()}

/* --- alimenti --- */
const BYN={};
DB.foods.forEach(f=>{BYN[f.n]=f});
(S.custom||[]).forEach(f=>{BYN[f.n]=f});
function food(n){const b=BYN[n];if(!b)return null;
 return S.ovr[n]?Object.assign({},b,S.ovr[n]):b}
function allFoods(){return DB.foods.concat(S.custom).map(f=>S.ovr[f.n]?Object.assign({},f,S.ovr[f.n]):f)}
function tot(d){const t={kcal:0,p:0,f:0,c:0,fib:0};
 MEALS.forEach(m=>(d.m[m]||[]).forEach(i=>{t.kcal+=i.kcal;t.p+=i.p;t.f+=i.f;t.c+=i.c;t.fib+=i.fib||0}));return t}
function firstDay(){let f=null;
 Object.keys(S.days).forEach(k=>{if(tot(day(k)).kcal>0&&(!f||k<f))f=k});
 Object.keys(S.meas).forEach(k=>{if(S.meas[k].w&&(!f||k<f))f=k});return f}

function bar(v,max,s){const w=Math.max(0,Math.min(100,v/max*100));
 return '<div class="bar'+(s?' s':'')+'"><i style="width:'+w.toFixed(0)+'%"></i></div>'}
function cell(l,v,max,cv){return '<div><div class="row" style="font-size:12px;color:var(--tx2)">'
 +'<span>'+l+'</span><span style="color:var(--tx)">'+v+'</span></div>'+bar(cv,max,1)+'</div>'}
function ring(v,max){const r=34,c=2*Math.PI*r,f=Math.max(0,Math.min(1,v/max));
 return '<svg class="ring" viewBox="0 0 80 80"><circle cx="40" cy="40" r="'+r+'" fill="none" stroke="var(--soft)" stroke-width="7"/>'
 +'<circle cx="40" cy="40" r="'+r+'" fill="none" stroke="var(--acc)" stroke-width="7" stroke-linecap="round" stroke-dasharray="'+c.toFixed(1)+'" stroke-dashoffset="'+(c*(1-f)).toFixed(1)+'" transform="rotate(-90 40 40)"/>'
 +'<text x="40" y="47" text-anchor="middle" font-size="22" font-weight="600" fill="var(--tx)">'+R(v)+'</text></svg>'}
function datenav(){const t=today();
 return '<div class="row" style="margin-bottom:6px">'
 +'<button class="btn" onclick="go(-1)">&lsaquo;</button>'
 +'<div class="dn2" onclick="goToday()"><b>'+human(cur)+'</b>'
 +'<div class="mut3">'+(cur===t?"oggi":(cur>t?"futuro":"tocca per tornare a oggi"))+'</div></div>'
 +'<button class="btn" onclick="go(1)">&rsaquo;</button></div>'}
function weekStrip(){let h='<div class="wk">';
 for(let i=6;i>=0;i--){const k=shift(cur,-i),d=S.days[k];const f=d&&tot(day(k)).kcal>0,t=d&&d.w&&d.w.done;
  h+='<button class="'+(i===0?"on":"")+'" onclick="goDay(\''+k+'\')"><i class="'+(f?"f":"")+(t?" t":"")+'"></i>'+GGS[parseIso(k).getDay()]+'</button>'}
 return h+'</div>'}

function qLab(i){
 if(i.u)return nfmt(i.q)+" "+plur(i.u,i.q)+" &middot; "+nfmt(i.g)+" g";
 if(i.pz)return nfmt(i.pz)+" "+(i.pz===1?"porzione":"porzioni");
 if(i.st)return "stima";
 if(i.g)return nfmt(i.g)+" g";
 return ""}

function renderOggi(){const d=day(cur),t=tot(d),g=target(cur),k=cur;
 const manca=Math.max(0,g.p-t.p),rest=g.kcal-t.kcal,st=isStorta(k);
 let h="";
 if(S.seenVer!==DB.ver)h+='<div class="card r1 pad"><div class="row"><b>Novità della v'+DB.ver+'</b><span class="mut3">'+DB.data+'</span></div>'
  +'<ul style="margin:8px 0 6px;padding-left:18px;font-size:13px;color:var(--tx2)">'+DB.novita.map(x=>'<li>'+esc(x)+'</li>').join("")+'</ul>'
  +'<button class="btn sm w" onclick="S.seenVer=DB.ver;save();renderOggi()">Ok, visto</button></div>';
 h+='<div class="card r1 pad">'+datenav()+weekStrip()
  +'<div class="stg"><div><b style="font-size:14px">Settimana storta</b><div class="mut3">'+(st?"Tre pasti, mantenimento, sedute A e B corte":"Influenza, notti in bianco, viaggi")+'</div></div>'
  +'<button class="sw '+(st?"on":"")+'" onclick="toggleStorta()" aria-label="settimana storta"></button></div>'
  +(st?'':'<div class="seg" style="margin:12px 0"><button class="'+(d.tr?"on":"")+'" onclick="setTr(1)">Allenamento</button>'
   +'<button class="'+(d.tr?"":"on")+'" onclick="setTr(0)">Riposo</button></div>')
  +'<div style="display:flex;align-items:center;gap:14px;margin-top:'+(st?'12px':'0')+'">'+ring(t.p,g.p)
  +'<div style="flex:1"><div style="font-size:15px"><b>'+R(t.p)+'</b> <span class="mut">/ '+g.p+' g proteine</span></div>'
  +'<div class="mut">'+(manca>0?"mancano "+R(manca)+" g":"raggiunte")+'</div>'
  +'<div class="mut" style="margin-top:4px">'+(rest>=0?"restano <b style=\"color:var(--tx)\">"+R(rest)+"</b> kcal":"<b style=\"color:var(--tx)\">"+R(-rest)+"</b> kcal oltre il target")+'</div></div></div>'
  +'<div class="grid2" style="margin-top:12px">'
  +cell("Calorie",R(t.kcal)+" / "+g.kcal,g.kcal,t.kcal)+cell("Grassi",R(t.f)+" g",g.f,t.f)
  +cell("Carboidrati",R(t.c)+" g",g.c,t.c)+cell("Fibra",R(t.fib)+" g",g.fib,t.fib)+'</div></div>';
 h+=check21Card();
 h+='<div class="slab">I pasti</div>';
 const ms=mealsFor(k),sh=shareFor(k);
 ms.forEach(m=>{const it=d.m[m];
  const s=it.reduce((a,i)=>{a.k+=i.kcal;a.p+=i.p;return a},{k:0,p:0});
  const q=Math.round(g.kcal*sh[m]/5)*5;
  const y=S.days[shift(k,-1)],hasY=y&&y.m&&y.m[m]&&y.m[m].length;
  h+='<div class="card r2 pad"><div class="mhead">'
   +'<div><div class="mname">'+MLAB[m]+'</div>'
   +'<div class="mut3">obiettivo ~'+q+' kcal</div></div>'
   +(it.length?'<div style="text-align:right"><div class="mut">'+R(s.k)+' kcal</div>'
     +'<div class="mut3">'+R(s.p)+' g P</div></div>':'')
   +'</div>';
  if(it.length){h+='<div style="margin-top:6px">'+it.map((i,ix)=>
    '<div class="frow"><div class="fn" onclick="editItem(\''+m+'\','+ix+')">'+esc(i.n)+' <span class="fg">'+qLab(i)+'</span></div>'
    +'<div class="fk" onclick="editItem(\''+m+'\','+ix+')">'+R(i.kcal)+' kcal<br>'+R(i.p,1)+' g P</div>'
    +'<button class="fx" onclick="rm(\''+m+'\','+ix+')" aria-label="elimina">&times;</button></div>'
   ).join("")+'</div>'
   +'<button class="btn w sm" style="margin-top:10px" onclick="pick(\''+m+'\')">+ Aggiungi</button>'}
  else{h+='<div class="grid2" style="margin-top:10px">'
   +'<button class="btn sm" '+(hasY?'onclick="ripeti(\''+m+'\')"':'disabled style="opacity:.4"')+'>Ripeti ieri</button>'
   +'<button class="btn sm" onclick="pick(\''+m+'\',\'__piano\')">Dal piano</button></div>'
   +'<button class="btn w sm" style="margin-top:8px" onclick="pick(\''+m+'\')">+ Cerca un alimento</button>'}
  h+='</div>'});
 if(st&&d.m.spuntino.length){h+='<div class="card r2 pad"><div class="mname">Spuntino</div><div class="mut3">registrato prima della settimana storta</div>'
  +d.m.spuntino.map(i=>'<div class="frow"><div class="fn">'+esc(i.n)+' <span class="fg">'+qLab(i)+'</span></div><div class="fk">'+R(i.kcal)+' kcal</div></div>').join("")+'</div>'}
 h+='<div class="slab">Integratori e acqua</div><div class="card r3 pad">';
 SUP.forEach(s=>{h+='<button class="pill '+(d.sup[s[0]]?"on":"")+'" onclick="sup(\''+s[0]+'\')">'
  +(d.sup[s[0]]?"&#10003; ":"")+s[1]+'</button>'});
 h+='<div class="row" style="margin-top:10px"><span class="mut">Acqua &middot; '+d.water+' bicchieri ('
  +R(d.water*0.25,2)+' L)</span><span><button class="btn" onclick="water(-1)">&minus;</button> '
  +'<button class="btn" onclick="water(1)">+</button></span></div></div>';
 if(t.f>0&&t.f<55&&t.kcal>1200)h+='<div class="note w">Grassi sotto i 55 g. Aggiungi 15 g di mandorle o frutta secca.</div>';
 if(t.fib>0&&t.fib<18&&t.kcal>1200)h+='<div class="note w">Fibra sotto i 18 g. Un frutto o 10 g di semi di chia sistemano la giornata.</div>';
 $("oggi-dyn").innerHTML=h}

function check21Card(){const f=firstDay();if(!f||isStorta(cur))return "";
 const ds=diffDays(f,today());if(ds<21)return "";
 const c=S.check21;
 if(c&&c.ok)return "";
 if(c&&!c.ok&&diffDays(c.at,today())<14)return "";
 return '<div class="card r1 pad"><b>Giorno '+ds+'. Finisci i pasti senza sforzo?</b>'
  +'<div class="mut" style="margin:4px 0 10px">Il target di partenza è provvisorio: se ci arrivi senza fatica, si risale di 100. Se no, te lo richiedo fra 14 giorni.</div>'
  +'<div class="grid2"><button class="btn ok" onclick="risp21(1)">Sì, senza sforzo</button><button class="btn" onclick="risp21(0)">No, non ancora</button></div></div>'}
function risp21(ok){S.check21={at:today(),ok:!!ok};
 if(ok){const t=JSON.parse(JSON.stringify(TG()));t.allen.kcal+=100;t.riposo.kcal+=100;t.allen.c+=25;t.riposo.c+=25;S.tg=t}
 save();haptic();renderOggi()}

function go(n){cur=shift(cur,n);render()}
function goToday(){cur=today();render()}
function goDay(k){cur=k;render()}
function setTr(v){day(cur).tr=!!v;save();renderOggi()}
function sup(k){const d=day(cur);d.sup[k]=!d.sup[k];save();haptic();renderOggi()}
function water(n){const d=day(cur);d.water=Math.max(0,d.water+n);save();haptic();renderOggi()}
let ub=null,ut=null;
function showUndo(txt){$("utxt").textContent=txt;$("undo").classList.add("on");clearTimeout(ut);
 ut=setTimeout(()=>{$("undo").classList.remove("on");ub=null},6000)}
function rm(m,ix){const d=day(cur);ub={type:"del",m:m,ix:ix,it:d.m[m][ix]};d.m[m].splice(ix,1);save();haptic();render();
 showUndo("Voce eliminata")}
function undo(){if(ub){const d=day(cur);
 if(ub.type==="del")d.m[ub.m].splice(ub.ix,0,ub.it);
 else if(ub.type==="add")d.m[ub.m].splice(-ub.n,ub.n);
 ub=null;save();render()}
 $("undo").classList.remove("on")}
function ripeti(m){const y=S.days[shift(cur,-1)];if(!y||!y.m||!y.m[m]||!y.m[m].length)return;
 const arr=y.m[m].map(i=>Object.assign({},i));day(cur).m[m].push(...arr);ub={type:"add",m:m,n:arr.length};
 save();haptic();renderOggi();showUndo("Copiate "+arr.length+" voci da ieri")}
"""


# Parte 2: inserimento cibo, quantità, ricerca

JS2 = r"""
let pSlot=null,pQ="",pCat=null,qEdit=null,pAdded=[];
function pick(m,cat){pSlot=m;pQ="";pCat=cat||null;qEdit=null;pAdded=[];
 $("sheet").classList.add("on");$("sq").value="";renderPick()}
function closePick(){$("sheet").classList.remove("on");qEdit=null;pAdded=[];render()}
function norm(s){return s.toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"")}
function pSearch(v){pQ=v;pCat=null;renderPick()}
function pSetCat(c){pCat=(pCat===c)?null:c;renderPick()}

function recents(){const r=[],seen={};const ks=Object.keys(S.days).sort().reverse();
 for(const k of ks){for(const m of MEALS){for(const i of (S.days[k].m[m]||[])){
  if(!seen[i.n]){seen[i.n]=1;r.push(i)}if(r.length>=25)return r}}}return r}

function ed(a,b){const m=a.length,n=b.length;if(!m)return n;if(!n)return m;
 let prev=[];for(let j=0;j<=n;j++)prev[j]=j;
 for(let i=1;i<=m;i++){const c=[i];for(let j=1;j<=n;j++){
  c[j]=Math.min(prev[j]+1,c[j-1]+1,prev[j-1]+(a[i-1]===b[j-1]?0:1))}prev=c}
 return prev[n]}
function score(name,q){const n=norm(name);
 if(n.indexOf(q)===0)return 0;
 const w=n.split(/[\s('",]+/);
 for(const x of w)if(x.indexOf(q)===0)return 1;
 if(n.indexOf(q)>=0)return 2;
 if(q.length>=4){for(const x of w){for(const L of [q.length-1,q.length,q.length+1]){
  if(L>0&&L<=x.length&&x[0]===q[0]&&ed(q,x.slice(0,L))<=1)return 3}}}
 return -1}
function rank(list,q,key){const o=[];
 list.forEach(x=>{const s=score(key(x),q);if(s>=0)o.push({s:s,l:key(x).length,x:x})});
 o.sort((a,b)=>a.s-b.s||a.l-b.l);return o.map(z=>z.x)}

let PB=[];
function pb(x){PB.push(x);return PB.length-1}
function labChip(l){return l?'<span class="lab '+l+'">'+LABN[l]+'</span>':''}
function rowFood(f){const b=f.cat?'<span class="bdg">'+esc(f.cat)+'</span>':'';
 const mod=S.ovr[f.n]?'<span class="bdg">modificato</span>':'';
 const sub=f.u?nfmt(f.ug)+" g a "+f.u:"per 100 g";
 return '<div class="lrow" onclick="qtyI('+pb(f)+')">'
 +'<span>'+esc(f.n)+b+mod+'<div class="mut3">'+sub+'</div></span>'
 +'<span class="mut" style="white-space:nowrap;text-align:right">'+R(f.kcal)+' kcal<br>'+R(f.p,1)+' g P</span></div>'}
function rowPiatto(f){return '<div class="lrow" onclick="qtyI('+pb(f)+',\'porz\')">'
 +'<span>'+esc(f.n)+'<span class="bdg">piatto</span><div class="mut3">stima a porzione</div></span>'
 +'<span class="mut" style="white-space:nowrap;text-align:right">'+f.kcal+' kcal<br>'+f.p+' g P</span></div>'}
function rowRecent(i){return '<div class="lrow" onclick="addRawI('+pb(i)+')">'
 +'<span>'+esc(i.n)+'<span class="bdg">recente</span><div class="mut3">'+qLab(i)+'</div></span>'
 +'<span class="mut" style="white-space:nowrap;text-align:right">'+R(i.kcal)+' kcal<br>'+R(i.p,1)+' g P</span></div>'}
function rowMeal(o,ix){return '<div class="lrow" onclick="addMeal('+ix+')">'
 +'<span><b>'+esc(o.n)+'</b>'+labChip(o.lab)+'<div class="mut3">'+o.peso+' g nel piatto &middot; '+esc(o.nota)+'</div></span>'
 +'<span class="mut" style="white-space:nowrap;text-align:right">'+o.kcal+' kcal<br>'+o.p+' g P</span></div>'}

function renderPick(){
 $("stitle").textContent=qEdit?"Modifica":MLAB[pSlot];
 $("sclose").textContent=pAdded.length?"Fatto":"Chiudi";
 PB=[];
 const q=norm(pQ.trim());
 let h="";
 if(pAdded.length){const d=day(cur),it=d.m[pSlot];const s=it.reduce((a,i)=>{a.k+=i.kcal;a.p+=i.p;return a},{k:0,p:0});
  const l=pAdded[pAdded.length-1];
  h+='<div class="added"><span>Aggiunto: '+esc(l.n)+' '+qLab(l)+'</span><span>'+MLAB[pSlot]+' '+R(s.k)+' kcal &middot; '+R(s.p)+' g P</span></div>'}
 if(!q){
  const cats=(S.custom.length?["nuovi"]:[]).concat(DB.cats);
  h+='<div class="chips"><button class="'+(pCat===null?"on":"")+'" onclick="pSetCat(null)">Suggeriti</button>'
   +'<button class="'+(pCat==="__rec"?"on":"")+'" onclick="pSetCat(\'__rec\')">Recenti</button>'
   +'<button class="'+(pCat==="__piano"?"on":"")+'" onclick="pSetCat(\'__piano\')">Dal piano</button>'
   +cats.map(c=>'<button class="'+(pCat===c?"on":"")+'" onclick="pSetCat(\''+c+'\')">'+cap(c)+'</button>').join("")
   +'</div>'}
 const pl=(DB.meals[pSlot]||[]).map((o,ix)=>({o:o,ix:ix}));
 if(q){
  const rc=rank(recents(),q,x=>x.n);
  const pm=rank(pl,q,x=>x.o.n+" "+x.o.items.map(i=>i.n).join(" "));
  const al=rank(allFoods(),q,x=>x.n);
  const pt=rank(DB.piatti,q,x=>x.n);
  if(rc.length)h+='<div class="slab">Recenti</div>'+rc.slice(0,5).map(rowRecent).join("");
  if(pm.length)h+='<div class="slab">Dal piano</div>'+pm.map(x=>rowMeal(x.o,x.ix)).join("");
  if(al.length)h+='<div class="slab">Alimenti</div>'+al.slice(0,60).map(rowFood).join("");
  if(pt.length)h+='<div class="slab">Piatti tipici</div>'+pt.map(rowPiatto).join("");
  if(!rc.length&&!pm.length&&!al.length&&!pt.length)
   h+='<div class="note">Nessun risultato per "'+esc(pQ)+'". Aggiungilo dall\'etichetta qui sotto: resta salvato e la prossima volta lo trovi.</div>'}
 else if(pCat===null){
  const rc=recents();
  if(rc.length)h+='<div class="slab">Recenti</div>'+rc.slice(0,8).map(rowRecent).join("");
  h+='<div class="slab">Dal piano</div>'+pl.map(x=>rowMeal(x.o,x.ix)).join("")}
 else if(pCat==="__rec"){const rc=recents();
  h+=rc.length?rc.map(rowRecent).join(""):'<div class="mut3" style="padding:12px 0">Ancora niente.</div>'}
 else if(pCat==="__piano"){h+=pl.map(x=>rowMeal(x.o,x.ix)).join("")}
 else{const l=allFoods().filter(f=>(f.cat||"nuovi")===pCat).sort((a,b)=>a.n.localeCompare(b.n));
  h+=l.map(rowFood).join("")}
 h+='<div class="grid2" style="margin:20px 0 8px">'
  +'<button class="btn" onclick="openNuovo()">Nuovo alimento</button>'
  +'<button class="btn" onclick="openStima()">Stima rapida</button></div>';
 $("sbody").innerHTML=h;$("sbody").scrollTop=0}

/* ---------------- quantità ---------------- */
let qCur=null,qMode="g",qVal=100;
function qtyI(i,mode,val){qty(PB[i],mode,val)}
function addRawI(i){putItem(Object.assign({},PB[i]))}
function qty(obj,mode,val){qCur=Object.assign({},obj);
 const last=S.lastQty[qCur.n];
 if(mode){qMode=mode}
 else if(last&&(last.m!=="u"||qCur.u))qMode=last.m;
 else qMode=qCur.u?"u":"g";
 if(val!==undefined&&val!==null)qVal=val;
 else if(!mode&&last&&last.m===qMode)qVal=last.v;
 else qVal=(qMode==="g"?100:1);
 renderQty()}
function qSwitch(m){const f=qCur;
 if(m===qMode)return;
 if(m==="g")qVal=R(qVal*f.ug,0); else qVal=Math.max(0.5,R(qVal/f.ug*2,0)/2);
 qMode=m;renderQty()}
function renderQty(){const f=qCur;
 const pr=qMode==="u"?[1,2,3,4]:qMode==="porz"?[0.5,1,1.5,2]:[50,100,150,200];
 const u=qMode==="u"?plur(f.u,qVal):qMode==="porz"?(qVal===1?"porzione":"porzioni"):"g";
 let h='<h3>'+esc(f.n)+(S.ovr[f.n]?'<span class="bdg">modificato</span>':'')+(f.once?'<span class="bdg">solo oggi</span>':'')+'</h3>';
 if(f.u&&qMode!=="porz")h+='<div class="seg" style="margin:10px 0">'
  +'<button class="'+(qMode==="u"?"on":"")+'" onclick="qSwitch(\'u\')">'+cap(plur(f.u,2))+'</button>'
  +'<button class="'+(qMode==="g"?"on":"")+'" onclick="qSwitch(\'g\')">Grammi</button></div>';
 h+='<div class="row" style="margin:14px 0"><button class="btn" style="min-width:52px" onclick="qAdj(-1)">&minus;</button>'
 +'<div style="text-align:center"><div class="big">'+nfmt(qVal)+'</div><div class="mut3">'+u+'</div></div>'
 +'<button class="btn" style="min-width:52px" onclick="qAdj(1)">+</button></div>'
 +'<div class="g4">'+pr.map(p=>'<button class="'+(p===qVal?"on":"")+'" onclick="qSet('+p+')">'+nfmt(p)+'</button>').join("")+'</div>'
 +'<div class="mut" id="qm" style="margin:14px 0"></div>'
 +'<button class="btn acc w" onclick="qAdd()">'+(qEdit?"Salva":"Aggiungi a "+MLAB[pSlot])+'</button>'
 +'<button class="btn w" style="margin-top:8px" onclick="renderPick()">Annulla</button>'
 +'<div style="margin-top:20px"><button class="btn w" onclick="editFood()">Modifica i valori nutrizionali</button></div>';
 $("sbody").innerHTML=h;$("sbody").scrollTop=0;qmShow()}
function qK(){const f=qCur;
 if(qMode==="porz")return qVal;
 if(qMode==="u")return qVal*f.ug/100;
 return qVal/100}
function qmShow(){const f=qCur,k=qK();
 let s=R(f.kcal*k)+' kcal &middot; '+R(f.p*k,1)+' g P &middot; '+R(f.f*k,1)+' g G &middot; '+R(f.c*k,1)+' g C';
 if(qMode==="u")s+='<div class="mut3">'+nfmt(R(qVal*f.ug,1))+' g</div>';
 $("qm").innerHTML=s}
function qAdj(s){const st=qMode==="g"?10:0.5;qVal=Math.max(st,R(qVal+s*st,1));renderQty()}
function qSet(v){qVal=v;renderQty()}
function qAdd(){const fd=qCur,k=qK();
 const it={n:fd.n,g:0,kcal:R(fd.kcal*k),p:R(fd.p*k,1),f:R(fd.f*k,1),c:R(fd.c*k,1),fib:R((fd.fib||0)*k,1)};
 if(qMode==="porz")it.pz=qVal;
 else if(qMode==="u"){it.g=R(qVal*fd.ug,1);it.u=fd.u;it.q=qVal}
 else it.g=qVal;
 if(fd.once)it.mod=1;
 S.lastQty[fd.n]={m:qMode,v:qVal};
 putItem(it)}
function putItem(it){haptic();
 if(qEdit){day(cur).m[qEdit.m][qEdit.ix]=it;qEdit=null;save();closePick();return}
 day(cur).m[pSlot].push(it);pAdded.push(it);save();pQ="";$("sq").value="";pCat=null;renderPick()}
function addMeal(ix){const o=DB.meals[pSlot][ix];const arr=[];
 o.items.forEach(i=>{const f=food(i.n);if(!f)return;const k=i.g/100;
  arr.push({n:i.n,g:i.g,kcal:R(f.kcal*k),p:R(f.p*k,1),f:R(f.f*k,1),c:R(f.c*k,1),fib:R((f.fib||0)*k,1)})});
 haptic();
 if(qEdit){day(cur).m[qEdit.m].splice(qEdit.ix,1,...arr);qEdit=null;save();closePick();return}
 day(cur).m[pSlot].push(...arr);pAdded.push(...arr);ub={type:"add",m:pSlot,n:arr.length};save();
 pQ="";$("sq").value="";pCat=null;renderPick()}

function editItem(m,ix){const i=day(cur).m[m][ix];
 pSlot=m;qEdit={m:m,ix:ix};pQ="";pCat=null;pAdded=[];
 $("sheet").classList.add("on");$("sq").value="";
 if(i.st){openStima(i);return}
 const k=i.pz?i.pz:(i.g?i.g/100:0);
 if(!k){openStima(i);return}
 const base={n:i.n,kcal:R(i.kcal/k),p:R(i.p/k,1),f:R(i.f/k,1),c:R(i.c/k,1),fib:R((i.fib||0)/k,1)};
 const src=food(i.n);if(src&&src.cat)base.cat=src.cat;
 if(i.u){base.u=i.u;base.ug=R(i.g/i.q,1)}
 else if(src&&src.u&&!i.pz){base.u=src.u;base.ug=src.ug}
 qty(base,i.pz?"porz":(i.u?"u":"g"),i.pz||i.q||i.g)}

/* ---------------- stima rapida, nuovo alimento, modifica valori ---------------- */
function openStima(pre){pre=pre||{};
 $("sbody").innerHTML='<h3>Stima rapida</h3><div class="mut" style="margin-bottom:8px">'
 +'Per quello che non puoi pesare. Meglio un numero approssimativo che una giornata vuota.</div>'
 +'<label class="mut3">Descrizione</label><input id="e-n" placeholder="Pizza con crudo e rucola" value="'+esc(pre.n||pQ.trim())+'">'
 +'<div class="grid2" style="margin-top:10px">'
 +'<div><label class="mut3">kcal</label><input id="e-k" type="number" inputmode="numeric" value="'+(pre.kcal||"")+'"></div>'
 +'<div><label class="mut3">Proteine (g)</label><input id="e-p" type="number" inputmode="numeric" value="'+(pre.p||"")+'"></div>'
 +'<div><label class="mut3">Grassi (g)</label><input id="e-f" type="number" inputmode="numeric" value="'+(pre.f||"")+'"></div>'
 +'<div><label class="mut3">Carboidrati (g)</label><input id="e-c" type="number" inputmode="numeric" value="'+(pre.c||"")+'"></div></div>'
 +'<button class="btn acc w" style="margin-top:12px" onclick="addStima()">'+(qEdit?"Salva":"Aggiungi")+'</button>'
 +'<button class="btn w" style="margin-top:8px" onclick="renderPick()">Annulla</button>'}
function addStima(){putItem({n:($("e-n").value.trim()||"Stima rapida"),g:0,st:1,
 kcal:+$("e-k").value||0,p:+$("e-p").value||0,f:+$("e-f").value||0,c:+$("e-c").value||0,fib:0})}
function openNuovo(){
 $("sbody").innerHTML='<h3>Nuovo alimento</h3><div class="mut" style="margin-bottom:8px">'
 +'Valori per 100 g, dall\'etichetta. Resta salvato e lo ritrovi nella categoria Nuovi.</div>'
 +'<label class="mut3">Nome</label><input id="n-n" value="'+esc(pQ.trim())+'">'
 +'<div class="grid2" style="margin-top:10px">'
 +'<div><label class="mut3">kcal</label><input id="n-k" type="number" inputmode="decimal"></div>'
 +'<div><label class="mut3">Proteine</label><input id="n-p" type="number" inputmode="decimal"></div>'
 +'<div><label class="mut3">Grassi</label><input id="n-f" type="number" inputmode="decimal"></div>'
 +'<div><label class="mut3">Carboidrati</label><input id="n-c" type="number" inputmode="decimal"></div>'
 +'<div><label class="mut3">Fibra</label><input id="n-fb" type="number" inputmode="decimal"></div></div>'
 +'<div class="slab">Se si conta a pezzi</div>'
 +'<div class="grid2">'
 +'<div><label class="mut3">Unita (fetta, vasetto)</label><input id="n-u" placeholder="facoltativo"></div>'
 +'<div><label class="mut3">Grammi per unità</label><input id="n-ug" type="number" inputmode="decimal"></div></div>'
 +'<button class="btn acc w" style="margin-top:12px" onclick="addNuovo()">Salva e aggiungi</button>'
 +'<button class="btn w" style="margin-top:8px" onclick="renderPick()">Annulla</button>'}
function addNuovo(){const n=$("n-n").value.trim();if(!n){alert("Serve un nome");return}
 const f={n:n,kcal:+$("n-k").value||0,p:+$("n-p").value||0,f:+$("n-f").value||0,
  c:+$("n-c").value||0,fib:+$("n-fb").value||0,cat:"nuovi"};
 const u=$("n-u").value.trim(),ug=+$("n-ug").value||0;
 if(u&&ug>0){f.u=u;f.ug=ug}
 S.custom=S.custom.filter(x=>x.n!==n);S.custom.push(f);BYN[n]=f;save();qty(f)}
function editFood(){const f=qCur,orig=BYN[f.n];
 $("sbody").innerHTML='<h3>'+esc(f.n)+'</h3><div class="mut" style="margin-bottom:8px">Valori per 100 g.'
 +(S.ovr[f.n]?' Questo alimento è già stato modificato.':'')+'</div>'
 +'<div class="grid2"><div><label class="mut3">kcal</label><input id="o-k" type="number" inputmode="decimal" value="'+f.kcal+'"></div>'
 +'<div><label class="mut3">Proteine</label><input id="o-p" type="number" inputmode="decimal" value="'+f.p+'"></div>'
 +'<div><label class="mut3">Grassi</label><input id="o-f" type="number" inputmode="decimal" value="'+f.f+'"></div>'
 +'<div><label class="mut3">Carboidrati</label><input id="o-c" type="number" inputmode="decimal" value="'+f.c+'"></div>'
 +'<div><label class="mut3">Fibra</label><input id="o-fb" type="number" inputmode="decimal" value="'+(f.fib||0)+'"></div></div>'
 +'<div class="grid2" style="margin-top:12px"><button class="btn acc" onclick="saveOvr(1)">Salva per sempre</button>'
 +'<button class="btn" onclick="saveOvr(0)">Solo per questa volta</button></div>'
 +'<div class="mut3" style="margin-top:8px">Per sempre: vale da ora in poi ogni volta che lo usi, le voci già registrate non cambiano. Solo per questa volta: vale per la voce che stai aggiungendo adesso.</div>'
 +(S.ovr[f.n]&&orig?'<button class="btn w" style="margin-top:12px" onclick="resetOvr()">Ripristina il valore originale ('+orig.kcal+' kcal, '+orig.p+' g P)</button>':'')
 +'<button class="btn w" style="margin-top:8px" onclick="renderQty()">Annulla</button>'}
function ovrVals(){return {kcal:+$("o-k").value||0,p:+$("o-p").value||0,f:+$("o-f").value||0,c:+$("o-c").value||0,fib:+$("o-fb").value||0}}
function saveOvr(forever){const n=qCur.n,v=ovrVals();
 if(forever){S.ovr[n]=v;save();qCur=Object.assign({},qCur,v);delete qCur.once}
 else{qCur=Object.assign({},qCur,v,{once:1})}
 renderQty()}
function resetOvr(){const n=qCur.n;delete S.ovr[n];save();qCur=Object.assign({},BYN[n]);renderQty()}
"""


# Parte 3: scheda Piano e scheda a schermo intero (opzione / esercizio)

JS3 = r"""
let plLab=null,plQ="";
function plSetLab(l){plLab=(plLab===l)?null:l;renderPiano()}
function plSearch(v){plQ=v;renderPiano()}
function renderPiano(){const k=cur,d=day(k),g=target(k),t=tot(d),rest=g.kcal-t.kcal;
 const q=norm(plQ.trim());
 let h='<div class="card r1 pad">'+datenav()
  +'<div class="row" style="align-items:baseline"><div><span class="big">'+R(Math.abs(rest))+'</span>'
  +'<span class="mut"> kcal '+(rest>=0?"ancora disponibili":"oltre il target")+'</span></div>'
  +'<span class="mut3">'+(g.p-t.p>0?"mancano "+R(g.p-t.p)+" g P":"proteine fatte")+'</span></div>'
  +'<div class="mut3" style="margin-top:4px">Le opzioni che non ci stanno sono in grigio. Tocca un\'opzione per vedere ingredienti e registrarla.</div>'
  +'<input placeholder="Cerca per nome o ingrediente" value="'+esc(plQ)+'" oninput="plSearch(this.value)" style="margin-top:10px">'
  +'<div class="chips">'+[["densa","Densa"],["media","Media"],["voluminosa","Voluminosa"],["liquida","Liquida"]].map(([l,n])=>
   '<button class="'+(plLab===l?"on":"")+'" onclick="plSetLab(\''+l+'\')">'+n+'</button>').join("")+'</div>'
  +(plLab?'<div class="mut3">'+esc(DB.labs[plLab])+'</div>':'')+'</div>';
 const ms=mealsFor(k),sh=shareFor(k);let tot0=0;
 ms.forEach(m=>{const qm=Math.round(g.kcal*sh[m]/5)*5;
  let lst=DB.meals[m].map((o,ix)=>({o:o,ix:ix}));
  if(plLab)lst=lst.filter(x=>x.o.lab===plLab);
  if(q)lst=rank(lst,q,x=>x.o.n+" "+x.o.items.map(i=>i.n).join(" "));
  if(!lst.length)return;tot0+=lst.length;
  h+='<div class="slab">'+MLAB[m]+' &middot; ~'+qm+' kcal &middot; '+lst.length+' opzioni</div><div class="card r2" style="padding:0 14px">';
  lst.forEach(x=>{const o=x.o;const dim=o.kcal>rest+60;
   h+='<div class="lrow'+(dim?" dim":"")+'" onclick="planSheet(\''+m+'\','+x.ix+')">'
   +'<span><b>'+esc(o.n)+'</b>'+labChip(o.lab)+'<div class="mut3">'+o.peso+' g nel piatto</div></span>'
   +'<span class="mut" style="white-space:nowrap;text-align:right">'+o.kcal+' kcal<br>'+o.p+' g P</span></div>'});
  h+='</div>'});
 if(!tot0)h+='<div class="note">Nessuna opzione con questi filtri.</div>';
 h+='<details class="card pad" style="margin-top:16px"><summary style="font-weight:600">Regole del piano</summary><div id="regole-st"></div></details>';
 $("piano-dyn").innerHTML=h;$("regole-st").innerHTML=$("regole-src").innerHTML}

function sheet2(title,body){$("s2title").textContent=title;$("s2body").innerHTML=body;$("sheet2").classList.add("on");$("s2body").scrollTop=0}
function closeSheet2(){$("sheet2").classList.remove("on")}
function planSheet(m,ix){const o=DB.meals[m][ix],g=target(cur),t=tot(day(cur)),rest=g.kcal-t.kcal;
 let h='<div style="margin:12px 0 4px">'+labChip(o.lab)+' <span class="mut3">'+esc(DB.labs[o.lab])+'</span></div>'
  +'<div class="row" style="align-items:baseline;margin:8px 0"><span class="big">'+o.kcal+'<span class="mut" style="font-size:14px"> kcal</span></span>'
  +'<span class="mut">'+o.p+' g P &middot; '+o.f+' g G &middot; '+o.c+' g C &middot; '+o.fib+' g fibra</span></div>'
  +'<div class="mut3">'+o.peso+' g nel piatto'+(o.kcal>rest+60?' &middot; supera di '+R(o.kcal-rest)+' kcal quello che resta oggi':'')+'</div>'
  +'<div class="slab">Ingredienti</div>';
 o.items.forEach(i=>{const f=food(i.n)||{kcal:0,p:0};const kk=i.g/100;
  h+='<div class="ing"><span>'+esc(i.n)+'</span><span class="mut">'+i.g+' g &middot; '+R(f.kcal*kk)+' kcal &middot; '+R(f.p*kk)+' g P</span></div>'});
 h+='<div class="pq" style="margin-top:12px">'+esc(o.nota)+'</div>'
  +'<button class="btn acc w" style="margin-top:16px" onclick="planAdd(\''+m+'\','+ix+')">Aggiungi a '+MLAB[m]+' di '+(cur===today()?"oggi":corto(cur))+'</button>'
  +'<button class="btn w" style="margin-top:8px" onclick="closeSheet2()">Chiudi</button>';
 sheet2(o.n,h)}
function planAdd(m,ix){const o=DB.meals[m][ix];const arr=[];
 o.items.forEach(i=>{const f=food(i.n);if(!f)return;const k=i.g/100;
  arr.push({n:i.n,g:i.g,kcal:R(f.kcal*k),p:R(f.p*k,1),f:R(f.f*k,1),c:R(f.c*k,1),fib:R((f.fib||0)*k,1)})});
 day(cur).m[m].push(...arr);ub={type:"add",m:m,n:arr.length};save();haptic();closeSheet2();render();
 showUndo(o.n+" aggiunto a "+MLAB[m].toLowerCase())}

function exSheet(n){const e=DB.ex[n];if(!e)return;
 let ex=null,sed=null;Object.keys(DB.sedute).forEach(k=>DB.sedute[k].ex.forEach(x=>{if(x.n===n&&!ex){ex=x;sed=k}}));
 const d=day(cur);if(d.w.sed&&DB.sedute[d.w.sed].ex.some(x=>x.n===n)){ex=DB.sedute[d.w.sed].ex.find(x=>x.n===n);sed=d.w.sed}
 let h='<div class="pnote">Sedute: '+esc(e.sedute)+'</div><div class="dgw">'+(SVG[n]||"")+'</div>';
 if(ex)h+='<div class="row" style="margin:6px 0 10px"><span class="expr">'+esc(ex.pr)+'</span>'
  +'<button class="tbtn" onclick="timer('+ex.rest+')">&#9201; recupero '+ex.rest+' s</button></div>';
 h+='<div class="pq">'+e.desc+'</div>'
  +'<div class="attl k">Prima</div><div class="pq">'+e.prima+'</div>'
  +'<div class="attl k">Durante</div><div class="pq">'+e.durante+'</div>'
  +'<div class="attl">Attenzione</div><ul class="att">'+e.att.map(a=>'<li>'+a+'</li>').join("")+'</ul>'
  +'<button class="btn w" style="margin-top:16px" onclick="closeSheet2()">Chiudi</button>';
 sheet2(n,h)}
"""


# Parte 4: allenamento (riscaldamento, timer, anche ogni giorno)

JS4 = r"""
function sedEx(sed,corta){const s=DB.sedute[sed];
 return corta?s.ex.filter(e=>s.corta.indexOf(e.n)>=0):s.ex}
function corteWeek(){let n=0;for(let i=0;i<7;i++){const dd=S.days[shift(cur,-i)];
 if(dd&&dd.w&&dd.w.done&&dd.w.corta)n++}return n}

/* --- timer di recupero --- */
const TM={end:0,iv:null};
function fmtT(s){return Math.floor(s/60)+":"+String(s%60).padStart(2,"0")}
function timer(sec){TM.end=Date.now()+sec*1000;clearInterval(TM.iv);$("tbar").classList.remove("done");
 $("tbar").classList.add("on");TM.iv=setInterval(tick,250);tick();haptic(20)}
function timerPlus(){if(!TM.iv)return;TM.end+=30000;tick()}
function tick(){const r=Math.max(0,Math.ceil((TM.end-Date.now())/1000));$("tval").textContent=fmtT(r);
 if(r<=0){clearInterval(TM.iv);TM.iv=null;haptic([150,80,150,80,300]);$("tbar").classList.add("done");
  $("tval").textContent="via";setTimeout(()=>{$("tbar").classList.remove("on","done")},2500)}}
function timerStop(){clearInterval(TM.iv);TM.iv=null;$("tbar").classList.remove("on","done")}

function renderAllen(){const d=day(cur),pk=shift(cur,-1),pd=S.days[pk],st=isStorta(cur);
 const sed=d.w.sed;
 let h='<div class="card r1 pad">'+datenav()
  +'<div class="row"><div><div style="font-weight:600">'+(sed?"Seduta "+sed:"Nessuna seduta prevista")+'</div>'
  +'<div class="mut3">'+(sed?esc(DB.sedute[sed].nome):"Giorno di riposo")+'</div></div>'
  +'<div class="seg" style="width:130px"><button class="'+(d.w.done?"on":"")+'" onclick="wdone(1)">Fatta</button>'
  +'<button class="'+(d.w.done?"":"on")+'" onclick="wdone(0)">No</button></div></div>'
  +'<div style="margin-top:10px"><span class="mut3">Seduta: </span>'
  +["A","B","C","D"].map(s=>'<button class="pill '+(sed===s?"on":"")+'" onclick="wsed(\''+s+'\')">'+s+'</button>').join("")
  +'</div>'
  +'<div class="seg" style="margin-top:8px"><button class="'+(!d.w.corta?"on":"")+'" onclick="wcorta(0)">30 minuti</button>'
  +'<button class="'+(d.w.corta?"on":"")+'" onclick="wcorta(1)">15 minuti</button></div>'
  +(st?'<div class="note w" style="margin-bottom:0">Settimana storta: due sedute, A e B, in versione corta. L\'obiettivo è non perdere terreno, non progredire.</div>':'')
  +'</div>';
 if(sed){const z=DB.sedute[sed].zona,w=DB.warm[z];
  h+='<details class="card r3 pad"><summary style="font-weight:600">Riscaldamento &middot; '+(d.w.presto?8:5)+' min<span class="mut3" style="font-weight:400"> &middot; parte '+z+'</span></summary>'
   +'<ul style="margin:8px 0;padding-left:18px;font-size:13px;color:var(--tx2)">'+w.map(x=>'<li>'+esc(x)+'</li>').join("")+'</ul>'
   +'<div class="seg"><button class="'+(!d.w.presto?"on":"")+'" onclick="wpresto(0)">Orario normale</button>'
   +'<button class="'+(d.w.presto?"on":"")+'" onclick="wpresto(1)">Entro un\'ora dal risveglio</button></div>'
   +(d.w.presto?'<div class="note w" style="margin-bottom:0">'+esc(DB.notaMattino)+'</div>':'')
   +(z==="bassa"?'<div class="mut3" style="margin-top:8px">Niente stretching dei flessori e niente piccione prima di allenarti.</div>':'')
   +'</details>'}
 if(sed){const lst=sedEx(sed,d.w.corta),s=DB.sedute[sed];
  h+='<div class="slab">'+(d.w.corta?"Versione da 15 minuti":"Esercizi")+(d.w.done?" &middot; tocca solo se è andata diversamente":"")+'</div>'
   +'<div class="card r2 pad">'+(s.nota?'<div class="mut3" style="margin-bottom:6px">'+esc(s.nota)+'</div>':'');
  lst.forEach(e=>{const v=d.w.ex[e.n]||0;const en=e.n.replace(/'/g,"\\'");
   h+='<div class="exrow"><div class="row"><div class="exn" onclick="exSheet(\''+en+'\')">'+esc(e.n)+' <i>&rsaquo;</i></div>'
   +(d.w.done?'<div class="pm2"><button class="qb '+(v===-1?"dn":"")+'" onclick="wex(\''+en+'\',-1)">&minus;</button>'
   +'<button class="qb '+(v===1?"up":"")+'" onclick="wex(\''+en+'\',1)">+</button></div>':'')+'</div>'
   +'<div class="row" style="margin-top:2px"><div class="expr">'+esc(e.pr)+(v===1?' <span class="mut3" style="font-weight:400">più del previsto</span>':v===-1?' <span class="mut3" style="font-weight:400">meno del previsto</span>':'')+'</div>'
   +'<button class="tbtn" onclick="timer('+e.rest+')">&#9201; '+e.rest+' s</button></div></div>'});
  h+='</div>'}
 h+='<div class="slab">Anche oggi</div><div class="card r3 pad">'
  +'<div class="mut">Come stanno le anche oggi?</div>'
  +'<div class="mut3" style="margin-bottom:9px">'+(pd&&pd.w&&pd.w.done?"Ieri: seduta "+pd.w.sed+(pd.w.corta?" corta":""):"Ieri: nessuna seduta, vale come linea di base")+'</div><div class="g4">'
  +[0,1,2,3].map(v=>'<button class="'+(d.hip===v?"on":"")+'" onclick="hip('+v+')">'+v+'</button>').join("")
  +'</div><div class="mut3" style="margin-top:7px">0 niente &middot; 1 lo sento ma passa &middot; 2 fastidio tutto il giorno &middot; 3 dolore</div>'
  +(d.hip>=2&&pd&&pd.w&&pd.w.done?'<div class="note w" style="margin-bottom:0">Voto '+d.hip+' dopo la seduta '+pd.w.sed+'. Al 2 dimezzi il range dell\'esercizio sospetto, al 3 lo togli. Se c\'e anche senza allenarti o ti sveglia la notte, chiami l\'ortopedico.</div>':'')
  +(d.hip>=2&&!(pd&&pd.w&&pd.w.done)?'<div class="note w" style="margin-bottom:0">Voto '+d.hip+' senza seduta il giorno prima. Se si ripete, è un segnale da portare all\'ortopedico, non da allenare.</div>':'')
  +'</div>';
 const cw=corteWeek();
 if(cw>2&&!st)h+='<div class="note w">'+cw+' sedute corte in questi sette giorni. La settimana prossima non aumentare niente: resta sui numeri di prima.</div>';
 const tp=progTips();if(tp.length)h+=tp.map(t=>'<div class="note">'+esc(t)+'</div>').join("");
 $("allen-dyn").innerHTML=h}
function wdone(v){const d=day(cur);d.w.done=!!v;if(v&&!d.w.sed)d.w.sed="A";save();haptic();renderAllen()}
function wsed(s){day(cur).w.sed=s;save();renderAllen()}
function wcorta(v){day(cur).w.corta=!!v;save();renderAllen()}
function wpresto(v){day(cur).w.presto=!!v;save();renderAllen()}
function wex(n,v){const d=day(cur);d.w.ex[n]=(d.w.ex[n]===v)?0:v;save();haptic();renderAllen()}
function hip(v){const d=day(cur);d.hip=(d.hip===v)?null:v;save();haptic();renderAllen()}
function exScore(){const sc={};Object.keys(S.days).sort().forEach(k=>{const w=S.days[k].w;
 if(w&&w.done&&!w.corta)Object.keys(w.ex||{}).forEach(n=>{if(!sc[n])sc[n]={s:0,run:0,last:0};
  const v=w.ex[n];sc[n].s+=v;
  if(v!==0&&v===sc[n].last)sc[n].run++;else if(v!==0)sc[n].run=1;else sc[n].run=0;
  sc[n].last=v})});return sc}
function progTips(){const sc=exScore(),o=[];
 Object.keys(sc).forEach(n=>{if(sc[n].run>=2&&sc[n].last===1)
  o.push(n+": seconda volta sopra il previsto. La prossima aumenta, elastico più duro o tempo più lento.");
  if(sc[n].run>=2&&sc[n].last===-1)
  o.push(n+": due volte sotto il previsto. Non aumentare niente, e guarda il protocollo in Misure.")});
 return o.slice(0,3)}
/* forza in calo negli ultimi 21 giorni: stesso esercizio sotto il previsto in due sedute consecutive */
function forzaCalo(){const t=today(),last={},hit=[];
 Object.keys(S.days).sort().forEach(k=>{if(diffDays(k,t)>21||diffDays(k,t)<0)return;const w=S.days[k].w;
  if(!w||!w.done||w.corta)return;Object.keys(w.ex||{}).forEach(n=>{const v=w.ex[n];
   if(v===-1&&last[n]===-1&&hit.indexOf(n)<0)hit.push(n);last[n]=v})});return hit}
"""


# Parte 5: misure, protocollo dei 14 giorni, impostazioni, backup

JS5 = r"""
function serie(f){const ks=Object.keys(S.meas).filter(k=>S.meas[k][f]!==undefined&&S.meas[k][f]!=="").sort();
 return {ks:ks,v:ks.map(k=>S.meas[k][f])}}
function media(a){return a.length?a.reduce((x,y)=>x+y,0)/a.length:null}
function bloccoDelta(){const s=serie("w");
 if(s.v.length<14)return null;
 const a=s.v.slice(-7),b=s.v.slice(-14,-7);
 return {d:media(a)-media(b),a:media(a),b:media(b)}}
function girovitaTrend(){const s=serie("v");if(s.v.length<2)return null;
 const lk=s.ks[s.ks.length-1],lv=s.v[s.v.length-1];
 let ri=0;for(let i=s.ks.length-2;i>=0;i--){if(diffDays(s.ks[i],lk)>=26){ri=i;break}}
 const span=diffDays(s.ks[ri],lk);
 return {d:lv-s.v[ri],span:span,fermo4:Math.abs(lv-s.v[ri])<1.0&&span>=26}}
function segno(d,u){const s=d>0?"+":"";return s+nfmt(R(d,1))+" "+u}

function proto(){const f=firstDay(),t=today();
 if(!f)return {stato:"vuoto",txt:"Parte quando ci sono dati."};
 const ds=diffDays(f,t);
 if(ds<DB.gCre)return {stato:"presto",txt:"Tace fino al giorno "+DB.gCre+": nelle prime tre settimane la creatina trattiene 1-1,5 kg d'acqua e ogni numero sarebbe falso. Oggi è il giorno "+ds+"."};
 if(stortaRecente(t))return {stato:"storta",txt:"Settimana storta in corso o appena finita: si aspettano 7 giorni prima di guardare la media, il sonno mancato e il sale gonfiano il numero."};
 if(S.lastAdj&&diffDays(S.lastAdj,t)<14)return {stato:"attesa",txt:"Modifica applicata il "+human(S.lastAdj)+". Si rivaluta il "+human(shift(S.lastAdj,14))+": mai prima."};
 const bd=bloccoDelta();
 if(!bd)return {stato:"pesi",txt:"Servono 14 pesate consecutive. Ne hai "+serie("w").v.length+"."};
 const rate=bd.d,gv=girovitaTrend(),fc=forzaCalo();
 let v,delta,mot;
 if(fc.length){v="Aggiungi 150 kcal";delta=150;mot="Ripetizioni in calo per due sedute di seguito su "+fc.join(", ")+". La forza è il primo indicatore a muoversi: stai mangiando troppo poco. Si aggiunge, non si toglie."}
 else if(rate<-0.5){v="Aggiungi 150 kcal";delta=150;mot="Stai perdendo "+nfmt(R(-rate,1))+" kg a settimana, oltre il mezzo chilo: una parte è muscolo."}
 else if(rate>0.3&&gv&&gv.d>0){v="Togli 150 kcal dai carboidrati";delta=-150;mot="Peso in salita di "+nfmt(R(rate,1))+" kg a settimana e girovita in salita di "+nfmt(R(gv.d,1))+" cm."}
 else if(Math.abs(rate)<=0.3&&gv&&gv.fermo4){v="Togli 100 kcal dai carboidrati";delta=-100;mot="Peso stabile e girovita fermo da "+gv.span+" giorni. Il minimo, mai 400."}
 else if(Math.abs(rate)<=0.3&&gv&&gv.d<0){v="Non toccare niente";delta=0;mot="Peso stabile, girovita in calo di "+nfmt(R(-gv.d,1))+" cm: è la ricomposizione che funziona esattamente come deve."}
 else if(rate<-0.2){v="Non toccare niente";delta=0;mot="Cali di "+nfmt(R(-rate,1))+" kg a settimana: è la velocità giusta."}
 else if(rate>0){v="Non toccare niente";delta=0;mot="Peso in leggera salita e girovita "+(gv?(gv.d<0?"in calo":"fermo"):"ancora senza abbastanza misure")+": stai mettendo muscolo. Lo scenario migliore possibile."}
 else{v="Non toccare niente";delta=0;mot="Niente da segnalare. Media "+nfmt(R(bd.b,1))+" &rarr; "+nfmt(R(bd.a,1))+" kg."}
 const kr=TG().riposo.kcal+delta;
 if(delta<0&&kr<DB.kmin){v="Non toccare niente";mot+=" Scendere porterebbe sotto le "+DB.kmin+" kcal, e sotto non si va qualunque cosa dica la bilancia.";delta=0}
 return {stato:"ok",v:v,delta:delta,mot:mot,rate:rate,gv:gv}}
function applyProto(delta){if(!delta)return;
 const t=JSON.parse(JSON.stringify(TG()));t.allen.kcal+=delta;t.riposo.kcal+=delta;
 t.allen.c=Math.max(100,t.allen.c+Math.round(delta/4));t.riposo.c=Math.max(100,t.riposo.c+Math.round(delta/4));
 S.tg=t;S.lastAdj=today();save();haptic();renderMisure()}
function protoCard(){const p=proto();
 let h='<div class="card r1 pad"><div class="row"><b>Protocollo dei 14 giorni</b><span class="mut3">propone, non applica</span></div>';
 if(p.stato!=="ok")h+='<div class="mut" style="margin-top:6px">'+p.txt+'</div>';
 else{h+='<div style="font-size:19px;font-weight:600;margin:8px 0 4px">'+p.v+'</div><div class="mut">'+p.mot+'</div>'
  +'<div class="mut3" style="margin-top:8px">Peso: '+segno(p.rate,"kg a settimana")+(p.gv?' &middot; girovita: '+segno(p.gv.d,"cm")+' in '+p.gv.span+' giorni':' &middot; girovita: servono più misure')+'</div>'
  +(p.delta?'<button class="btn acc w" style="margin-top:10px" onclick="applyProto('+p.delta+')">Applica: target a '+(TG().allen.kcal+p.delta)+' / '+(TG().riposo.kcal+p.delta)+'</button>'
   +'<div class="mut3" style="margin-top:6px">Dopo l\'applicazione tace per 14 giorni. Mai più di '+DB.passo+' alla volta, mai sotto '+DB.kmin+'.</div>':'')}
 return h+'</div>'}

function renderMisure(){const m=S.meas[cur]||{};
 const s=serie("w");
 const m7=s.v.length?media(s.v.slice(-7)):null,m14=s.v.length>=8?media(s.v.slice(-14)):null;
 const bd=bloccoDelta();
 let h='<div class="card r1 pad">'+datenav()
  +'<div class="grid2" style="margin-top:4px"><div><span class="big">'+(m7?nfmt(R(m7,1)):"--")+'</span><div class="mut3">kg, media 7 giorni</div></div>'
  +'<div><span class="big" style="color:var(--tx2)">'+(m14?nfmt(R(m14,1)):"--")+'</span><div class="mut3">media 14 giorni</div></div></div>'
  +'<div class="mut3" style="margin:6px 0 10px">Il numero del giorno oscilla di un chilo. La 14 è più liscia ma ritarda: per decidere si usa il confronto sotto.</div>'
  +'<label class="mut3">Peso di stamattina (kg)</label>'
  +'<input type="number" step="0.1" inputmode="decimal" value="'+(m.w||"")+'" onchange="setM(\'w\',this.value)">'
  +'<div class="grid2" style="margin-top:12px">'
  +'<div><label class="mut3">Girovita (cm)</label><input type="number" step="0.5" inputmode="decimal" value="'+(m.v||"")+'" onchange="setM(\'v\',this.value)"></div>'
  +'<div><label class="mut3">Fianchi (cm)</label><input type="number" step="0.5" inputmode="decimal" value="'+(m.f||"")+'" onchange="setM(\'f\',this.value)"></div></div>'
  +'<div class="mut3" style="margin-top:8px">Girovita e fianchi: una volta a settimana, stesso giorno, a digiuno, a fine espirazione.</div></div>';
 h+='<div class="slab">Settimana contro settimana</div><div class="card r2 pad">';
 if(bd){h+='<div class="row" style="align-items:baseline"><div><span class="big">'+segno(bd.d,"kg")+'</span></div>'
  +'<span class="mut3">'+nfmt(R(bd.b,1))+' &rarr; '+nfmt(R(bd.a,1))+'</span></div>'
  +'<div class="mut3" style="margin-top:4px">Media degli ultimi 7 giorni contro i 7 precedenti. Nessun giorno in comune: la differenza è reale.</div>'}
 else{h+='<div class="mut">Servono 14 pesate.</div><div class="mut3" style="margin-top:4px">Ne hai '+s.v.length+'.</div>'}
 const sv=serie("v"),sf=serie("f");
 if(sv.v.length>=2||sf.v.length>=2){h+='<div class="grid2" style="margin-top:12px">';
  if(sv.v.length>=2)h+='<div><div class="mut3">Girovita</div><div style="font-size:17px;font-weight:600">'
   +segno(sv.v[sv.v.length-1]-sv.v[sv.v.length-2],"cm")+'</div></div>';
  if(sf.v.length>=2)h+='<div><div class="mut3">Fianchi</div><div style="font-size:17px;font-weight:600">'
   +segno(sf.v[sf.v.length-1]-sf.v[sf.v.length-2],"cm")+'</div></div>';
  h+='</div><div class="mut3" style="margin-top:6px">Rispetto alla misura precedente.</div>'}
 h+='</div>';
 h+='<div class="slab">Ogni 14 giorni</div>'+protoCard();
 h+='<div class="slab">Ultimi 7 giorni</div>'+weekly();
 h+='<div class="slab">Impostazioni</div>'+settingsCard();
 h+='<div class="card r3 pad"><div class="row"><b style="font-size:14px">Dati</b><span class="mut3">'+(S.persist===true?"protetti dal sistema":S.persist===false?"non protetti":"")+'</span></div>'
  +'<div class="mut3" style="margin:4px 0 10px">'+(S.persist===true?"Android non li cancellera per liberare spazio. Il backup serve comunque: telefono perso, reset, cambio.":"Stanno solo su questo telefono. Il backup è l\'unica copia.")+'</div>'
  +'<button class="btn acc w" onclick="shareJ()">Condividi backup</button>'
  +'<div class="grid2" style="margin-top:8px"><button class="btn" onclick="exportJ()">Scarica file</button>'
  +'<button class="btn" onclick="$(\'imp\').click()">Importa backup</button></div>'
  +'<input type="file" id="imp" accept=".json,application/json" style="display:none" onchange="importJ(this)">'
  +'<div class="mut3" style="margin-top:8px">'+(S.lastBackup?"Ultimo backup: "+human(S.lastBackup):"Nessun backup fatto")+'</div></div>';
 if(needBackup())h+='<div class="note w">È passato più di un mese dall\'ultimo backup. Condividilo su Drive adesso: sono dieci secondi.</div>';
 h+='<div class="dl">v'+DB.ver+' &middot; '+DB.data+'</div>';
 $("mis-dyn").innerHTML=h}

function tgField(pre,k,lab,v){return '<div><label class="mut3">'+lab+'</label>'
 +'<input id="'+pre+'-'+k+'" type="number" inputmode="numeric" value="'+v+'"></div>'}
function settingsCard(){const t=TG(),p=PR();
 return '<details class="card r2 pad"><summary style="font-weight:600">Target e profilo</summary>'
  +'<div class="mut3" style="margin:8px 0">Restano salvati sul telefono. Aggiornare l\'app non li tocca.</div>'
  +'<div class="slab">Profilo</div><div class="grid2">'
  +'<div><label class="mut3">Peso di riferimento (kg)</label><input id="s-peso" type="number" step="0.1" inputmode="decimal" value="'+p.peso+'"></div>'
  +'<div><label class="mut3">Età</label><input id="s-eta" type="number" inputmode="numeric" value="'+p.eta+'"></div>'
  +'<div><label class="mut3">Altezza (cm)</label><input id="s-alt" type="number" inputmode="numeric" value="'+p.altezza+'"></div>'
  +'</div>'
  +'<button class="btn w" style="margin-top:10px" onclick="calcTg()">Calcola i target dal peso</button>'
  +'<div class="note" id="calcnote" style="display:none">Numeri proposti, non applicati: controllali e premi Salva. Dispendio stimato meno '+DB.deficit+' kcal, il deficit minimo del piano. Il peso di queste settimane contiene l\'acqua della creatina: non ricalcolare prima della terza settimana.</div>'
  +'<div class="slab">Giorno di allenamento</div><div class="grid2">'
  +tgField("ta","kcal","kcal",t.allen.kcal)+tgField("ta","p","Proteine",t.allen.p)
  +tgField("ta","f","Grassi",t.allen.f)+tgField("ta","c","Carboidrati",t.allen.c)
  +tgField("ta","fib","Fibra",t.allen.fib)+'</div>'
  +'<div class="slab">Giorno di riposo</div><div class="grid2">'
  +tgField("tr","kcal","kcal",t.riposo.kcal)+tgField("tr","p","Proteine",t.riposo.p)
  +tgField("tr","f","Grassi",t.riposo.f)+tgField("tr","c","Carboidrati",t.riposo.c)
  +tgField("tr","fib","Fibra",t.riposo.fib)+'</div>'
  +'<div class="slab">Settimana storta (mantenimento)</div><div class="grid2">'
  +tgField("ts","kcal","kcal",t.storta.kcal)+tgField("ts","p","Proteine",t.storta.p)
  +tgField("ts","f","Grassi",t.storta.f)+tgField("ts","c","Carboidrati",t.storta.c)
  +tgField("ts","fib","Fibra",t.storta.fib)+'</div>'
  +'<div class="mut3" style="margin-top:8px">Le proteine restano uguali in tutti i giorni: è la parte che non si tocca mai.</div>'
  +'<button class="btn acc w" style="margin-top:12px" onclick="saveTg()">Salva</button>'
  +'<button class="btn w" style="margin-top:8px" onclick="resetTg()">Torna ai valori del piano</button>'
  +'</details>'}
function calcTg(){const p=+$("s-peso").value||PR().peso,e=+$("s-eta").value||PR().eta,a=+$("s-alt").value||PR().altezza;
 const bmr=10*p+6.25*a-5*e+5,tdee=bmr*DB.att;
 const kc=Math.round((tdee-DB.deficit)/5)*5,kr=kc-DB.dRip,ks=Math.round(tdee*0.94/5)*5;
 const pr=Math.round(p*1.9/5)*5,ga=Math.round(p*1.0/5)*5,gr=ga-5;
 $("ta-kcal").value=kc;$("tr-kcal").value=kr;$("ts-kcal").value=ks;
 $("ta-p").value=pr;$("tr-p").value=pr;$("ts-p").value=pr;
 $("ta-f").value=ga;$("tr-f").value=gr;$("ts-f").value=ga;
 $("ta-c").value=Math.round((kc-pr*4-ga*9)/4);
 $("tr-c").value=Math.round((kr-pr*4-gr*9)/4);
 $("ts-c").value=Math.round((ks-pr*4-ga*9)/4);
 $("ta-fib").value=22;$("tr-fib").value=22;$("ts-fib").value=22;
 $("calcnote").style.display="block"}
function saveTg(){const tg={allen:{},riposo:{},storta:{}};
 ["kcal","p","f","c","fib"].forEach(k=>{tg.allen[k]=+$("ta-"+k).value||0;tg.riposo[k]=+$("tr-"+k).value||0;tg.storta[k]=+$("ts-"+k).value||0});
 S.tg=tg;
 S.prof={peso:+$("s-peso").value||PR().peso,eta:+$("s-eta").value||PR().eta,altezza:+$("s-alt").value||PR().altezza};
 save();haptic();render()}
function resetTg(){if(!confirm("Torno ai target scritti nel piano?"))return;
 S.tg=null;S.prof=null;save();render()}

function setM(f,v){if(!S.meas[cur])S.meas[cur]={};
 if(v===""){delete S.meas[cur][f];save();renderMisure();return}
 const n=+v;
 if(f==="w"&&(n<40||n>150)&&!confirm("Peso "+nfmt(n)+" kg: è giusto? Fuori dal normale, potrebbe essere un errore di battitura.")){renderMisure();return}
 if(f!=="w"&&(n<40||n>200)&&!confirm(nfmt(n)+" cm: è giusto?")){renderMisure();return}
 S.meas[cur][f]=n;save();haptic();renderMisure()}
function needBackup(){if(!S.lastBackup)return Object.keys(S.days).length>7;
 return diffDays(S.lastBackup,today())>30}
function weekly(){let nk=0,sk=0,sp=0,ws=0,wc=0;const goal=isStorta(cur)?2:4;
 for(let i=6;i>=0;i--){const k=shift(cur,-i),d=S.days[k];if(!d)continue;const t=tot(day(k));
  if(t.kcal>0){nk++;sk+=t.kcal;sp+=t.p}if(d.w&&d.w.done){ws++;if(d.w.corta)wc++}}
 return '<div class="card r2 pad"><div class="grid2">'
 +'<div><div class="mut3">Media calorie</div><div style="font-size:19px;font-weight:600">'+(nk?R(sk/nk):"--")+'</div></div>'
 +'<div><div class="mut3">Media proteine</div><div style="font-size:19px;font-weight:600">'+(nk?R(sp/nk)+" g":"--")+'</div></div>'
 +'<div><div class="mut3">Giorni registrati</div><div style="font-size:19px;font-weight:600">'+nk+' / 7</div></div>'
 +'<div><div class="mut3">Sedute fatte</div><div style="font-size:19px;font-weight:600">'+ws+' / '+goal+'</div></div></div>'
 +(wc?'<div class="mut3" style="margin-top:8px">Di cui '+wc+' in versione corta.</div>':'')+'</div>'}
function backupBlob(){S.lastBackup=today();save();return new Blob([JSON.stringify(S)],{type:"application/json"})}
function exportJ(){const b=backupBlob();
 const a=document.createElement("a");a.href=URL.createObjectURL(b);
 a.download="ricomp-backup-"+today()+".json";document.body.appendChild(a);a.click();
 a.remove();renderMisure()}
function shareJ(){const name="ricomp-backup-"+today()+".json";
 try{const file=new File([JSON.stringify(S)],name,{type:"application/json"});
  if(navigator.canShare&&navigator.canShare({files:[file]})){
   navigator.share({files:[file],title:name}).then(()=>{S.lastBackup=today();save();renderMisure()}).catch(()=>{});return}}
 catch(e){}
 exportJ()}
function importJ(el){const f=el.files[0];if(!f)return;const r=new FileReader();
 r.onload=()=>{try{const o=JSON.parse(r.result);if(!o.days)throw 0;
  if(confirm("Sostituisco tutti i dati attuali con il backup?")){S=Object.assign(blank(),o);
   migraS();save();render()}}
  catch(e){alert("File non valido")}};r.readAsText(f)}
"""


# Parte 6: grafici interattivi, navigazione, avvio

JS6 = r"""
const CH={};
function mavg(a,n){return a.map((_,i)=>{const s=a.slice(Math.max(0,i-n+1),i+1);return media(s)})}
function lineChart(series,o){o=o||{};const W=300,H=o.h||110,L=26,B=16;
 let all=[];series.forEach(s=>s.pts.forEach(p=>all.push(p.y)));
 if(!all.length)return '<div class="mut3">Nessun dato ancora.</div>';
 let mn=o.min!==undefined?o.min:Math.min.apply(null,all),mx=o.max!==undefined?o.max:Math.max.apply(null,all);
 if(mx===mn){mx=mn+1;mn=mn-1}
 const n=Math.max.apply(null,series.map(s=>s.pts.length?Math.max.apply(null,s.pts.map(p=>p.i))+1:0));
 const X=i=>L+(n<2?0:(W-L-4)*i/(n-1)),Y=v=>4+(H-B-4)*(1-(v-mn)/(mx-mn));
 let g='';[0,0.5,1].forEach(t=>{const y=4+(H-B-4)*t,v=mx-(mx-mn)*t;
  g+='<line x1="'+L+'" y1="'+y+'" x2="'+W+'" y2="'+y+'" stroke="var(--line)" stroke-width="1"/>'
   +'<text x="0" y="'+(y+3)+'" font-size="9" fill="var(--tx3)">'+(o.d?v.toFixed(1):Math.round(v))+'</text>'});
 series.forEach(s=>{if(!s.pts.length)return;
  if(s.pts.length>1)g+='<polyline fill="none" stroke="'+s.c+'" stroke-width="'+(s.w||1.8)+'" points="'
   +s.pts.map(p=>X(p.i)+','+Y(p.y)).join(" ")+'"/>';
  if(s.dots||s.pts.length===1)s.pts.forEach(p=>{g+='<circle cx="'+X(p.i)+'" cy="'+Y(p.y)+'" r="3" fill="'+s.c+'"/>'})});
 let id="";
 if(o.id){id=o.id;CH[id]={n:n,L:L,W:W,labels:o.labels||[],series:series};
  g+='<line id="cl-'+id+'" x1="-10" y1="4" x2="-10" y2="'+(H-B)+'" stroke="var(--tx3)" stroke-dasharray="2 2"/>'}
 return '<div class="chw" data-id="'+id+'"><svg class="ch" viewBox="0 0 '+W+' '+H+'">'+g+'</svg></div>'
  +(id?'<div class="chtip" id="tip-'+id+'">tocca il grafico per leggere un valore</div>':'')}
function chTouch(e){const w=e.target.closest?e.target.closest(".chw"):null;if(!w||!w.dataset.id)return;
 const c=CH[w.dataset.id];if(!c||c.n<1)return;
 const r=w.getBoundingClientRect(),cx=(e.touches?e.touches[0].clientX:e.clientX);
 const x=(cx-r.left)/r.width*c.W;
 let i=c.n<2?0:Math.round((x-c.L)/((c.W-c.L-4)/(c.n-1)));i=Math.max(0,Math.min(c.n-1,i));
 const parts=c.series.map(s=>{const p=s.pts.find(p=>p.i===i);return p?(s.name?s.name+" ":"")+nfmt(R(p.y,1)):null}).filter(Boolean);
 const t=$("tip-"+w.dataset.id);if(t)t.textContent=(c.labels[i]?c.labels[i]+"  ":"")+parts.join("  ·  ");
 const l=$("cl-"+w.dataset.id);if(l){const X=c.L+(c.n<2?0:(c.W-c.L-4)*i/(c.n-1));l.setAttribute("x1",X);l.setAttribute("x2",X)}}
document.addEventListener("touchstart",chTouch,{passive:true});
document.addEventListener("touchmove",chTouch,{passive:true});
document.addEventListener("mousemove",e=>{if(e.buttons)chTouch(e)});
document.addEventListener("click",chTouch);
function barChart(v,l,ref){const W=300,H=90,B=16,n=v.length;
 if(!n)return '<div class="mut3">Nessun dato ancora.</div>';
 let mx=Math.max(ref||0,Math.max.apply(null,v));if(!mx)mx=1;
 let g='';
 if(ref){const y=4+(H-B-4)*(1-ref/mx);
  g+='<line x1="0" y1="'+y+'" x2="'+W+'" y2="'+y+'" stroke="var(--tx3)" stroke-dasharray="3 3" stroke-width="1"/>'}
 v.forEach((val,i)=>{const h=(H-B-4)*val/mx,x=2+i*((W-4)/n);
  g+='<rect x="'+x+'" y="'+(H-B-h)+'" width="'+((W-4)/n-6)+'" height="'+h+'" rx="2" fill="var(--acc)"/>'
   +'<text x="'+(x+((W-4)/n-6)/2)+'" y="'+(H-4)+'" font-size="9" fill="var(--tx3)" text-anchor="middle">'+l[i]+'</text>'});
 return '<svg class="ch" viewBox="0 0 '+W+' '+H+'">'+g+'</svg>'}
function weeks(){const o={v:[],l:[]},end=today();
 for(let w=7;w>=0;w--){let n=0;for(let i=0;i<7;i++){const k=shift(end,-(w*7+i));
  const d=S.days[k];if(d&&d.w&&d.w.done)n++}o.v.push(n);o.l.push(w===0?"ora":"-"+w)}
 return o}
function adherence(){const wk=weeks(),l4=wk.v.slice(-4),av=media(l4);
 return '<div class="mut3" style="margin-top:6px">Aderenza ultime 4 settimane: '+R(av,1)+' sedute a settimana su 4.</div>'}
function hipChart(){const ks=Object.keys(S.days).sort().filter(k=>S.days[k].hip!==null&&S.days[k].hip!==undefined);
 const bassa=[],alta=[],base=[];
 ks.forEach((k,i)=>{const d=S.days[k],p=S.days[shift(k,-1)];
  const s=p&&p.w&&p.w.done&&p.w.sed?DB.sedute[p.w.sed].zona:null;
  (s==="bassa"?bassa:s==="alta"?alta:base).push({i:i,y:d.hip})});
 let h='<div class="card r3 pad"><div class="row"><b>Voto anca</b><span class="mut3">'+ks.length+' giorni</span></div>';
 if(ks.length>=8){
  h+='<div class="lg"><span><i class="dot" style="background:#d85a30"></i>dopo parte bassa</span>'
   +'<span><i class="dot" style="background:#7f77dd"></i>dopo parte alta</span>'
   +'<span><i class="dot" style="background:#9a9891"></i>nessuna seduta ieri</span></div>'
   +lineChart([{pts:base,c:"var(--tx3)",dots:1,w:1,name:"base"},
               {pts:bassa,c:"#d85a30",dots:1,w:1,name:"bassa"},
               {pts:alta,c:"#7f77dd",dots:1,w:1,name:"alta"}],{min:0,max:3,id:"hip",labels:ks.map(corto)})
   +'<div class="mut3" style="margin-top:6px">Base '+nfmt(R(media(base.map(p=>p.y))||0,1))+' &middot; dopo bassa '+nfmt(R(media(bassa.map(p=>p.y))||0,1))+' &middot; dopo alta '+nfmt(R(media(alta.map(p=>p.y))||0,1))+'. Conta la differenza tra la base e il dopo-seduta, non il numero da solo.</div>'}
 else{h+='<div class="mut3" style="margin-top:6px">Sotto gli 8 giorni votati non si legge niente. Vota anche nei giorni di riposo: senza la linea di base un 1 dopo la seduta non dice nulla.</div>'}
 return h+'</div>'}
function exChart(){const sc=exScore();
 const ns=Object.keys(sc).filter(n=>sc[n].s!==0).sort((a,b)=>sc[b].s-sc[a].s);
 if(!ns.length)return '';
 const mx=Math.max.apply(null,ns.map(n=>Math.abs(sc[n].s)));
 let h='<div class="card r2 pad"><div class="row"><b>Progressione per esercizio</b></div>'
  +'<div class="mut3" style="margin-bottom:8px">Somma di quante volte sei andato sopra o sotto il previsto.</div>';
 ns.forEach(n=>{const s=sc[n].s,w=Math.abs(s)/mx*100;
  h+='<div style="padding:5px 0"><div class="row" style="font-size:13px"><span>'+esc(n)+'</span>'
   +'<span class="mut">'+(s>0?"+":"")+s+'</span></div>'
   +'<div class="bar s"><i style="width:'+w.toFixed(0)+'%;background:'+(s>0?"var(--ok)":"var(--warn)")+'"></i></div></div>'});
 return h+'</div>'}
function renderGrafici(){
 const dk=Object.keys(S.days).sort().filter(k=>tot(day(k)).kcal>0);
 const kc=dk.map(k=>tot(day(k)).kcal),pr=dk.map(k=>tot(day(k)).p);
 const sw=serie("w"),sv=serie("v"),sf=serie("f");
 let h='<div class="slab">Alimentazione</div>';
 h+='<div class="card r2 pad"><div class="row"><b>Calorie</b><span class="mut3">'+dk.length+' giorni</span></div>'
  +'<div class="lg"><span><i class="dot" style="background:#9a9891"></i>giorno</span>'
  +'<span><i class="dot" style="background:#534ab7"></i>media 7 gg</span></div>'
  +lineChart([{pts:kc.map((y,i)=>({i:i,y:y})),c:"var(--tx3)",w:1,name:"giorno"},
              {pts:mavg(kc,7).map((y,i)=>({i:i,y:y})),c:"var(--acc)",name:"media"}],{id:"kcal",labels:dk.map(corto)})+'</div>';
 h+='<div class="card r2 pad"><div class="row"><b>Proteine</b><span class="mut3">obiettivo '+TG().allen.p+' g</span></div>'
  +lineChart([{pts:pr.map((y,i)=>({i:i,y:y})),c:"var(--tx3)",w:1,name:"giorno"},
              {pts:mavg(pr,7).map((y,i)=>({i:i,y:y})),c:"var(--acc)",name:"media"}],{id:"prot",labels:dk.map(corto)})+'</div>';
 h+='<div class="slab">Misure</div>';
 h+='<div class="card r1 pad"><div class="row"><b>Peso</b><span class="mut3">'+sw.v.length+' misure</span></div>'
  +'<div class="lg"><span><i class="dot" style="background:#9a9891"></i>giorno</span>'
  +'<span><i class="dot" style="background:#534ab7"></i>media 7 gg</span></div>'
  +lineChart([{pts:sw.v.map((y,i)=>({i:i,y:y})),c:"var(--tx3)",w:1,name:"giorno"},
              {pts:mavg(sw.v,7).map((y,i)=>({i:i,y:y})),c:"var(--acc)",name:"media"}],{d:1,id:"peso",labels:sw.ks.map(corto)})+'</div>';
 const vk=sv.ks.concat(sf.ks).filter((k,i,a)=>a.indexOf(k)===i).sort();
 h+='<div class="card r1 pad"><div class="row"><b>Girovita e fianchi</b></div>'
  +'<div class="lg"><span><i class="dot" style="background:#d85a30"></i>girovita</span>'
  +'<span><i class="dot" style="background:#7f77dd"></i>fianchi</span></div>'
  +lineChart([{pts:sv.ks.map((k,j)=>({i:vk.indexOf(k),y:sv.v[j]})),c:"#d85a30",dots:1,name:"girovita"},
              {pts:sf.ks.map((k,j)=>({i:vk.indexOf(k),y:sf.v[j]})),c:"#7f77dd",dots:1,name:"fianchi"}],{d:1,id:"giro",labels:vk.map(corto)})
  +adherence()+'</div>';
 h+='<div class="slab">Allenamento</div>';
 const wk=weeks();
 h+='<div class="card r2 pad"><div class="row"><b>Sedute a settimana</b><span class="mut3">obiettivo 4</span></div>'
  +barChart(wk.v,wk.l,4)+'</div>'+hipChart()+exChart();
 $("graf-dyn").innerHTML=h}

/* --- navigazione --- */
const TABS=["oggi","piano","allen","mis","graf"];
function setTab(t){tab=t;TABS.forEach(x=>{
 $("t-"+x).style.display=x===t?"block":"none";$("n-"+x).classList.toggle("on",x===t)});
 try{window.scrollTo(0,0)}catch(e){}render()}
function render(){if(tab==="oggi")renderOggi();else if(tab==="piano")renderPiano();else if(tab==="allen")renderAllen();
 else if(tab==="mis")renderMisure();else renderGrafici()}

/* scorrimento laterale per cambiare giorno */
(function(){let x0=null,y0=null,t0=0;
 const app=document.getElementById("app");
 app.addEventListener("touchstart",e=>{if(e.target.closest&&e.target.closest(".chw,.chips,input"))return;
  x0=e.touches[0].clientX;y0=e.touches[0].clientY;t0=Date.now()},{passive:true});
 app.addEventListener("touchend",e=>{if(x0===null)return;const dx=e.changedTouches[0].clientX-x0,dy=e.changedTouches[0].clientY-y0;
  x0=null;if(Date.now()-t0>600)return;
  if(Math.abs(dx)>70&&Math.abs(dy)<40&&tab!=="graf"){go(dx<0?1:-1);haptic(8)}},{passive:true})})();

/* archiviazione persistente: Android non cancella i dati per liberare spazio */
if(navigator.storage&&navigator.storage.persist){
 navigator.storage.persisted().then(p=>{if(p){if(S.persist!==true){S.persist=true;save()}return}
  return navigator.storage.persist().then(r=>{S.persist=!!r;save();if(tab==="mis")renderMisure()})}).catch(()=>{})}

setTab("oggi");
if("serviceWorker" in navigator){window.addEventListener("load",()=>{
 navigator.serviceWorker.register("sw.js").catch(()=>{})})}
"""


# --------------------------------------------------------- HTML, SW, manifest

ICON_OGGI = ('<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="3.5"/>'
             '<path d="M12 3.5v2M12 18.5v2M3.5 12h2M18.5 12h2"/></svg>')
ICON_PIANO = ('<svg viewBox="0 0 24 24"><path d="M5 4h14v16H5z"/><path d="M8.5 9h7M8.5 12.5h7M8.5 16h4.5"/></svg>')
ICON_ALLEN = ('<svg viewBox="0 0 24 24"><path d="M3 10v4M6 8v8M18 8v8M21 10v4M6 12h12"/></svg>')
ICON_MIS = ('<svg viewBox="0 0 24 24"><path d="M4 7h16v10H4z"/><path d="M8 7v3.5M12 7v5M16 7v3.5"/></svg>')
ICON_GRAF = ('<svg viewBox="0 0 24 24"><path d="M4 19V5M4 19h16"/><path d="M8 15l3.5-4 3 2.5L19 8"/></svg>')

HTML = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#faf9f7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#17171a" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>%(nome)s</title>
<link rel="manifest" href="manifest.json">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<style>%(css)s</style>
</head>
<body>
<div id="app">

<section id="t-oggi"><div id="oggi-dyn"></div></section>

<section id="t-piano" style="display:none">
 <div id="piano-dyn"></div>
 <div id="regole-src" style="display:none">%(regole)s</div>
</section>

<section id="t-allen" style="display:none">
 <div id="allen-dyn"></div>
 <details class="card pad" style="margin-top:16px"><summary style="font-weight:600">Le quattro sedute</summary>
  %(sedute)s
 </details>
 <details class="card pad"><summary style="font-weight:600">Appendice: i 23 esercizi</summary>
  <div class="mut3" style="margin:6px 0 4px">Ogni esercizio: come si fa, cosa controllare prima, cosa guardare durante, note per anca e gomito. Dalla seduta si apre toccando il nome.</div>
  %(appendice)s
 </details>
</section>

<section id="t-mis" style="display:none"><div id="mis-dyn"></div></section>
<section id="t-graf" style="display:none"><div id="graf-dyn"></div></section>

</div>

<div class="undo" id="undo"><span id="utxt">Voce eliminata</span><button onclick="undo()">Annulla</button></div>
<div class="tbar" id="tbar"><span>Recupero</span><b id="tval">0:00</b><span><button onclick="timerPlus()">+30 s</button> <button onclick="timerStop()">Stop</button></span></div>

<nav>
 <button id="n-oggi" onclick="setTab('oggi')">%(iOggi)sOggi</button>
 <button id="n-piano" onclick="setTab('piano')">%(iPiano)sPiano</button>
 <button id="n-allen" onclick="setTab('allen')">%(iAllen)sAllenamento</button>
 <button id="n-mis" onclick="setTab('mis')">%(iMis)sMisure</button>
 <button id="n-graf" onclick="setTab('graf')">%(iGraf)sGrafici</button>
</nav>

<div class="sheet" id="sheet">
 <div class="sheeth"><button class="btn" id="sclose" onclick="closePick()">Chiudi</button>
  <b id="stitle" style="white-space:nowrap">Pasto</b>
  <input id="sq" placeholder="Cerca (anche con errori di battitura)" oninput="pSearch(this.value)" autocomplete="off"></div>
 <div class="sheetb" id="sbody"></div>
</div>

<div class="sheet" id="sheet2">
 <div class="sheeth"><button class="btn" onclick="closeSheet2()">Chiudi</button><b id="s2title"></b></div>
 <div class="sheetb" id="s2body"></div>
</div>

<script>
const DB=%(db)s;
const SVG=%(svg)s;
%(js)s
</script>
</body>
</html>
"""

SW = """const V="ricomp-v%(ver)d";
const FILES=["./","./index.html","./manifest.json","./icon-192.png","./icon-512.png","./icon-maskable-512.png"];
self.addEventListener("install",e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(FILES)));self.skipWaiting()});
self.addEventListener("activate",e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(
 ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener("fetch",e=>{if(e.request.method!=="GET")return;
 const nav=e.request.mode==="navigate";
 e.respondWith(fetch(e.request,nav?{cache:"no-cache"}:undefined).then(r=>{
  const cp=r.clone();caches.open(V).then(c=>c.put(e.request,cp));return r
 }).catch(()=>caches.match(e.request).then(m=>m||caches.match("./index.html"))))});
"""

MANIFEST = {
    "name": NOME_LUNGO,
    "short_name": NOME,
    "start_url": "./index.html",
    "scope": "./",
    "display": "standalone",
    "orientation": "portrait",
    "background_color": "#534ab7",
    "theme_color": "#534ab7",
    "lang": "it",
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png",
         "purpose": "maskable"},
    ],
}


def main():
    db = build_db()
    js = JS1 + JS2 + JS3 + JS4 + JS5 + JS6
    html = HTML % {
        "nome": NOME, "css": CSS,
        "regole": html_regole(), "sedute": html_sedute(db["sedute"]),
        "appendice": html_appendice(),
        "iOggi": ICON_OGGI, "iPiano": ICON_PIANO, "iAllen": ICON_ALLEN,
        "iMis": ICON_MIS, "iGraf": ICON_GRAF,
        "db": json.dumps(db, ensure_ascii=False, separators=(",", ":")),
        "svg": json.dumps(svg_map(), ensure_ascii=False, separators=(",", ":")),
        "js": js,
    }
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    with open(os.path.join(OUT, "sw.js"), "w", encoding="utf-8") as f:
        f.write(SW % {"ver": VERSIONE})
    with open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(MANIFEST, f, ensure_ascii=False, indent=2)
    n_opt = sum(len(v) for v in db["meals"].values())
    print("index.html: %d KB, %d alimenti, %d opzioni, %d piatti, %d esercizi, versione %d"
          % (len(html.encode("utf-8")) // 1024, len(db["foods"]), n_opt,
             len(db["piatti"]), len(db["ex"]), VERSIONE))


if __name__ == "__main__":
    main()
