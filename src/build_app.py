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
from fonts_data import FONTS
from ristoranti import LOCALI, CONDIMENTO
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


def build_rist():
    """Locali per le stime da ristorante: ogni voce diventa {n, t, g}.
    t = "u" alimento a pezzi, "g" alimento a peso (g grammi per +), "p" piatto."""
    piatti = {p[0] for p in PIATTI}
    out = []
    for nome, voci in LOCALI:
        items = []
        for v in voci:
            if isinstance(v, tuple):
                n, g = v
                if n not in BYNAME:
                    err("ristoranti, %s: '%s' non è tra gli alimenti" % (nome, n))
                items.append({"n": n, "t": "g", "g": g})
            elif v in piatti:
                items.append({"n": v, "t": "p"})
            elif v in BYNAME and BYNAME[v].get("u"):
                items.append({"n": v, "t": "u"})
            elif v in BYNAME:
                err("ristoranti, %s: '%s' è a peso, scrivilo come (nome, grammi)" % (nome, v))
            else:
                err("ristoranti, %s: '%s' non esiste" % (nome, v))
        out.append({"n": nome, "items": items})
    return out


def build_db():
    piatti = {p[0] for p in PIATTI}
    for old, new in RINOMINATI.items():
        if new not in BYNAME and new not in piatti:
            err("RINOMINATI: '%s' non esiste tra gli alimenti" % new)
        if old in BYNAME or old in piatti:
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
                        "errori": e["errori"], "perche": e["perche"], "male": e["male"],
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
        "rist": build_rist(), "cond": CONDIMENTO,
        "ver": VERSIONE,
        "data": DATA_BUILD,
    }


# ------------------------------------------------------------------ CSS

CSS = """
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
:root{--bg:#f4f1ea;--card:#fff;--soft:#f1ece2;--line:#ebe5d9;--line2:#e2dbcc;--btnbg:#fbfaf7;--seg:#eae5da;
--tx:#1e1c24;--tx2:#55505f;--tx3:#6e6878;--tx4:#9a93a3;
--acc:#5a4fcf;--accbg:#eceafb;--ok:#1f7a63;--okbg:#e2f1ec;--warn:#9a5a0c;--warnbg:#fbefdf;--warnbar:#d8892b;
--cor:#a63d2a;--corbg:#f8e6e1;--blu:#1f5f9e;--blubg:#e3eefa;--macbar:#8a8494;
--sh:0 1px 2px rgba(30,28,36,.05),0 6px 20px rgba(30,28,36,.045);--cardb:transparent;
--fig:#1e1c24;--fig2:#55505f;--fig3:#9a93a3;--figline:#cfc6b4;--figar:#c4552f;--figband:#7f77dd;
--disp:"Fraunces",Georgia,"Times New Roman",serif}
@media(prefers-color-scheme:dark){:root{--bg:#141318;--card:#1e1d24;--soft:#2a2831;--line:#2e2c36;--line2:#3a3843;
--btnbg:#24232b;--seg:#26252d;--tx:#f1eee7;--tx2:#b8b2c2;--tx3:#9690a1;--tx4:#6f6a79;
--acc:#a89ff0;--accbg:#2a2650;--ok:#5cc6a2;--okbg:#123a30;--warn:#f0b866;--warnbg:#3d2a0e;--warnbar:#d8892b;
--cor:#f0917a;--corbg:#3a1d16;--blu:#8fc0f0;--blubg:#12304d;--macbar:#8f899a;--sh:none;--cardb:#2e2c36;
--fig:#e6e2da;--fig2:#b8b2c2;--fig3:#6f6a79;--figline:#4a4752;--figar:#e2a074;--figband:#9a92e8}}
html,body{margin:0;padding:0;background:var(--bg);color:var(--tx);
font-family:"Figtree",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
font-size:15px;line-height:1.5;-webkit-text-size-adjust:100%;overscroll-behavior-y:contain;
font-variant-numeric:tabular-nums;font-feature-settings:"tnum" 1}
#app{max-width:520px;margin:0 auto;padding:6px 14px 104px}
h2{font-family:var(--disp);font-size:20px;font-weight:600;margin:20px 0 8px;letter-spacing:-.2px}
h3{font-family:var(--disp);font-size:18px;font-weight:600;margin:18px 0 6px}
.disp{font-family:var(--disp);font-weight:600;letter-spacing:-.2px}
summary{cursor:pointer;list-style:none;font-weight:600}
summary::-webkit-details-marker{display:none}
summary::after{content:"+";float:right;color:var(--tx3);font-size:20px;line-height:1}
details[open]>summary::after{content:"\\2013"}
.card{background:var(--card);border:1px solid var(--cardb);border-radius:22px;margin:12px 0;box-shadow:var(--sh)}
.card.r1,.card.r2,.card.r3{border-left:1px solid var(--cardb)}
.card.dim{opacity:.6}
.pad{padding:16px 18px}
.slab{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:var(--tx3);font-weight:700;margin:22px 4px 4px}
.row{display:flex;align-items:center;justify-content:space-between;gap:10px}
.mut{color:var(--tx2);font-size:13px}.mut3{color:var(--tx3);font-size:12px}
.big{font-family:var(--disp);font-size:32px;font-weight:600;line-height:1.1;letter-spacing:-.5px}
.bar{height:8px;background:var(--soft);border-radius:4px;overflow:hidden}
.bar>i{display:block;height:100%;background:var(--acc);border-radius:4px}
.bar.s{height:5px}.bar.s>i{background:var(--macbar)}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:10px 14px}
.seg{display:flex;gap:4px;padding:4px;background:var(--seg);border-radius:16px}
.seg>button{flex:1;border:0;background:transparent;color:var(--tx2);font-size:14px;font-weight:600;padding:8px 6px;
font-family:inherit;min-height:42px;border-radius:12px}
.seg>button.on{background:var(--card);color:var(--tx);font-weight:700;box-shadow:0 1px 3px rgba(30,28,36,.12)}
.seg.day>button.on.st{background:var(--warnbg);color:var(--warn)}
button{font-family:inherit;cursor:pointer}
.btn{background:var(--btnbg);border:1px solid var(--line2);border-radius:14px;padding:10px 14px;color:var(--tx);
font-size:15px;font-weight:600;min-height:46px}
.btn:active{transform:scale(.98)}
.btn.acc{background:var(--tx);color:var(--bg);border-color:var(--tx)}
.btn.ok{background:var(--ok);color:#fff;border-color:var(--ok)}
.btn.w{width:100%}
.btn.sm{padding:8px 12px;font-size:14px;min-height:44px}
.ico{display:inline-flex;align-items:center;justify-content:center;gap:8px}
.ico svg{width:16px;height:16px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;flex:0 0 16px}
.mhead{display:flex;align-items:baseline;justify-content:space-between;gap:10px}
.mname{font-family:var(--disp);font-weight:600;font-size:21px;letter-spacing:-.2px}
.mtot{font-size:14px;white-space:nowrap}.mtot b{font-weight:700}.mtot span{color:var(--tx3)}
.mtot.over{color:var(--warn)}.mtot.over span{color:var(--warn)}
.mover{display:flex;align-items:center;gap:8px;margin:8px 0 2px}
.mover .mb{flex:1}
.ovb{font-size:12px;font-weight:700;color:var(--warn);background:var(--warnbg);padding:2px 8px;border-radius:10px}
.frow{display:flex;align-items:center;gap:8px;padding:9px 0;border-bottom:1px solid var(--soft)}
.frow:last-of-type{border-bottom:0}
.fn{flex:1;min-width:0;font-size:15px;font-weight:600;line-height:1.35;padding:2px 0}
.fg{color:var(--tx3);font-weight:400}
.fk{font-size:13px;color:var(--tx);white-space:nowrap;text-align:right;line-height:1.45}
.fk b{font-weight:700}.fk .p{color:var(--ok);font-weight:600}
.fx{border:0;background:transparent;color:var(--tx4);font-size:22px;line-height:1;
width:44px;height:44px;margin-right:-12px;display:flex;align-items:center;justify-content:center}
.pill{display:inline-flex;align-items:center;font-size:14px;font-weight:600;padding:0 16px;border-radius:20px;
border:1px solid var(--line2);color:var(--tx2);background:var(--card);margin:0 6px 8px 0;min-height:40px}
.pill.on{background:var(--tx);color:var(--bg);border-color:var(--tx)}
.lab{display:inline-block;font-size:10px;text-transform:uppercase;letter-spacing:.5px;font-weight:700;
padding:2px 7px;border-radius:6px;margin-left:6px;vertical-align:2px}
.lab.densa{background:var(--warnbg);color:var(--warn)}
.lab.media{background:var(--accbg);color:var(--acc)}
.lab.voluminosa{background:var(--okbg);color:var(--ok)}
.lab.liquida{background:var(--blubg);color:var(--blu)}
nav{position:fixed;left:0;right:0;bottom:0;background:var(--card);border-top:1px solid var(--line);
display:grid;grid-template-columns:repeat(5,1fr);z-index:40;padding:6px 4px calc(8px + env(safe-area-inset-bottom))}
nav button{border:0;background:transparent;color:var(--tx3);font-size:11px;font-weight:600;padding:2px 0;
display:flex;flex-direction:column;align-items:center;gap:3px}
nav button span{width:54px;height:30px;border-radius:15px;display:flex;align-items:center;justify-content:center}
nav button.on{color:var(--acc);font-weight:700}
nav button.on span{background:var(--accbg)}
nav svg{width:22px;height:22px;display:block;stroke:currentColor;fill:none;stroke-width:1.9;stroke-linecap:round;stroke-linejoin:round}
.sheet{position:fixed;inset:0;background:var(--bg);z-index:60;display:none;flex-direction:column}
.sheet.on{display:flex}
.sheeth{padding:10px 14px;border-bottom:1px solid var(--line);background:var(--card);display:flex;gap:10px;align-items:center}
.sheeth b{font-family:var(--disp);font-size:18px;font-weight:600}
.sheetb{flex:1;overflow:auto;padding:0 14px 28px;max-width:520px;margin:0 auto;width:100%}
.added{background:var(--okbg);color:var(--ok);border-radius:12px;padding:10px 14px;font-size:14px;margin:10px 0 4px;display:flex;justify-content:space-between;gap:8px}
input,select,textarea{font-family:inherit;font-size:16px;background:var(--card);color:var(--tx);
border:1px solid var(--line2);border-radius:12px;padding:10px 12px;width:100%;min-height:46px}
input:focus,select:focus{outline:2px solid var(--acc);outline-offset:-1px}
label.mut3{display:block;margin:0 0 3px 2px;font-weight:600}
.lrow{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px 2px;border-bottom:1px solid var(--soft);min-height:56px}
.lrow:active{background:var(--soft)}
.lrow.dim{opacity:.45}
.bdg{display:inline-block;font-size:10px;text-transform:uppercase;letter-spacing:.5px;
color:var(--tx3);border:1px solid var(--line2);border-radius:6px;padding:1px 6px;margin-left:6px;
vertical-align:1px;font-weight:700}
.bdg.p{color:var(--acc);border-color:var(--acc)}
.cdot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:8px;vertical-align:1px}
.chips{display:flex;gap:6px;overflow-x:auto;padding:10px 0 4px;scrollbar-width:none}
.chips::-webkit-scrollbar{display:none}
.mac{font-size:12px;margin-top:2px;font-weight:400;color:var(--tx3);font-variant-numeric:tabular-nums}
.chips button{white-space:nowrap;border:1px solid var(--line2);background:var(--card);color:var(--tx2);
border-radius:18px;padding:7px 14px;font-size:14px;font-weight:600;min-height:40px}
.chips button.on{background:var(--tx);color:var(--bg);border-color:var(--tx)}
.qb{width:44px;height:44px;border-radius:14px;border:1px solid var(--line2);background:var(--btnbg);
color:var(--tx2);font-size:20px;display:flex;align-items:center;justify-content:center}
.qb.up{background:var(--okbg);color:var(--ok);border-color:var(--okbg)}
.qb.dn{background:var(--warnbg);color:var(--warn);border-color:var(--warnbg)}
.g4{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.g4 button{padding:10px 0;border-radius:12px;border:1px solid var(--line2);background:var(--btnbg);color:var(--tx2);font-size:15px;font-weight:600;min-height:46px}
.g4 button.on{background:var(--tx);color:var(--bg);border-color:var(--tx)}
.note{background:var(--accbg);color:var(--acc);border-radius:16px;padding:12px 14px;font-size:14px;line-height:1.5;margin:12px 0}
.note.w{background:var(--warnbg);color:var(--warn)}
.note.g{background:var(--okbg);color:var(--ok)}
.prow{padding:12px 0;border-bottom:1px solid var(--soft)}
.pn{font-weight:700;font-size:15px}
.pq{font-size:13px;color:var(--tx2);margin-top:3px;line-height:1.5}
.pnote{font-size:12px;color:var(--tx3);margin-top:2px;line-height:1.45}
.pm{font-size:12px;color:var(--acc);margin-top:4px;font-weight:600}
.srow{display:flex;justify-content:space-between;padding:9px 0;border-bottom:1px solid var(--soft);font-size:14px}
.exc{padding:16px 0;border-bottom:1px solid var(--soft)}
.dgw{margin:8px 0}
.dgw svg{width:100%;height:auto;max-width:420px;display:block;margin:0 auto}
.attl{font-size:12px;text-transform:uppercase;letter-spacing:1px;color:var(--acc);font-weight:700;margin:14px 0 4px}
.attl.k{color:var(--acc)}
.attbox{background:var(--corbg);border-radius:18px;padding:14px 16px;margin:12px 0}
.attbox .attl{color:var(--cor);margin:0 0 6px;display:flex;align-items:center;gap:8px}
.attbox .attl svg{width:16px;height:16px;stroke:currentColor;fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}
.attbox div.ai{font-size:15px;line-height:1.45;color:var(--tx);margin-top:6px}
ul.att{margin:0;font-size:14px;color:var(--tx2);background:var(--corbg);border-radius:14px;padding:10px 12px 10px 28px}
ul.att li{margin-bottom:3px}
.exbody{font-size:15px;line-height:1.5;color:var(--tx)}
.new{font-size:10px;font-weight:700;color:var(--ok);background:var(--okbg);padding:2px 7px;border-radius:7px;margin-left:8px;letter-spacing:.3px}
.exrow{padding:12px 0;border-bottom:1px solid var(--soft)}
.exrow:last-child{border-bottom:0}
.exn{font-size:15px;font-weight:700;flex:1;min-width:0;padding:6px 0}
.exn i{font-style:normal;color:var(--tx3);font-weight:400}
.expr{font-family:var(--disp);font-size:19px;font-weight:600;color:var(--tx)}
.sugg{font-size:13px;color:var(--ok);background:var(--okbg);border-radius:12px;padding:8px 12px;margin-top:8px;display:flex;align-items:center;justify-content:space-between;gap:8px}
.sugg button{border:0;background:var(--ok);color:#fff;border-radius:10px;padding:6px 12px;font-weight:700;font-size:13px;min-height:36px}
.tbtn{border:1px solid var(--line2);background:var(--btnbg);color:var(--tx2);border-radius:12px;padding:6px 12px;font-size:13px;font-weight:600;min-height:40px}
.pm2{display:flex;gap:6px}
.undo{position:fixed;left:14px;right:14px;bottom:84px;background:var(--tx);color:var(--bg);border-radius:14px;
padding:12px 16px;display:none;z-index:50;font-size:14px;align-items:center;justify-content:space-between;
max-width:492px;margin:0 auto;gap:10px;box-shadow:0 8px 24px rgba(0,0,0,.18)}
.undo.on{display:flex}
.undo button{background:transparent;border:0;color:var(--bg);font-weight:700;font-size:14px;text-decoration:underline;min-height:32px}
.tbar{position:fixed;left:14px;right:14px;bottom:84px;background:var(--acc);color:#fff;border-radius:14px;
padding:10px 16px;display:none;z-index:55;align-items:center;justify-content:space-between;max-width:492px;margin:0 auto;gap:10px}
.tbar.on{display:flex}
.tbar.done{background:var(--ok)}
.tbar b{font-family:var(--disp);font-size:24px;font-variant-numeric:tabular-nums}
.tbar button{background:rgba(255,255,255,.18);border:0;color:#fff;border-radius:10px;padding:7px 11px;font-size:13px;font-weight:600;min-height:36px}
svg.ch{width:100%;height:auto;display:block}
.chw{touch-action:pan-y}
.chtip{font-size:12px;color:var(--tx2);min-height:18px;margin-top:4px}
.lg{display:flex;gap:14px;font-size:12px;color:var(--tx2);margin:4px 0 8px;flex-wrap:wrap}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:5px}
.dl{font-size:12px;color:var(--tx3);text-align:center;padding:16px 0 4px}
/* oggi */
.dnav{display:flex;align-items:center;justify-content:space-between;gap:8px;margin:4px 0 10px}
.cbtn{width:44px;height:44px;border-radius:22px;border:1px solid var(--line2);background:var(--card);color:var(--tx);
display:flex;align-items:center;justify-content:center;padding:0;flex:0 0 44px}
.cbtn svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.dn2{text-align:center;flex:1;cursor:pointer}
.dn2 b{font-family:var(--disp);font-size:26px;font-weight:600;display:block;letter-spacing:-.3px;line-height:1.15}
.wk{display:grid;grid-template-columns:repeat(7,1fr);gap:6px;margin:0 0 12px}
.wk button{border:1px solid transparent;background:transparent;padding:7px 0 6px;border-radius:14px;display:flex;flex-direction:column;align-items:center;gap:4px;color:var(--tx3);font-size:11px;font-weight:700}
.wk i{font-style:normal;width:30px;height:30px;border-radius:15px;display:flex;align-items:center;justify-content:center;font-size:13px;font-weight:600;border:1.5px dashed var(--line2);color:var(--tx3)}
.wk i.f{background:var(--tx);border:0;color:var(--bg)}
.wk u{display:block;width:14px;height:3px;border-radius:2px;background:transparent;text-decoration:none}
.wk u.t{background:var(--ok)}
.wk button.on{background:var(--card);border-color:var(--line2);color:var(--acc)}
.wk button.on i{background:var(--acc);color:#fff;border:0}
.rings{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.rg{display:flex;flex-direction:column;align-items:center;gap:8px}
.rgw{position:relative;width:132px;height:132px}
.rgw svg{width:132px;height:132px;display:block}
.rgv{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.rgv b{font-family:var(--disp);font-size:30px;font-weight:600;line-height:1}
.rgv span{font-size:12px;color:var(--tx3);margin-top:4px}
.rgl{text-align:center;font-size:13px;color:var(--tx2)}
.rgl div{font-size:12px;font-weight:700;letter-spacing:.5px;text-transform:uppercase}
.hr{height:1px;background:var(--soft);margin:16px 0 14px}
.mbw{margin-bottom:12px}.mbw:last-child{margin-bottom:0}
.mbh{display:flex;justify-content:space-between;font-size:13px;margin-bottom:6px}
.mbh span:first-child{color:var(--tx2);font-weight:600}
.mbh b{font-weight:700}.mbh em{font-style:normal;color:var(--tx3)}
.mb{position:relative;height:8px;border-radius:4px;background:var(--soft)}
.mb>i{position:absolute;left:0;top:0;bottom:0;border-radius:4px;background:var(--macbar)}
.mb>i.o{background:var(--warnbar)}
.mb>s{position:absolute;top:-3px;width:2px;height:14px;border-radius:1px;background:var(--tx)}
.mb.th{height:6px}
.stg{display:none}
.sw{width:44px;height:26px;border-radius:13px;background:var(--line2);position:relative;border:0;padding:0;flex:0 0 44px}
.sw::after{content:"";position:absolute;top:3px;left:3px;width:20px;height:20px;border-radius:50%;background:#fff;transition:left .15s}
.sw.on{background:var(--warn)}.sw.on::after{left:21px}
.ing{display:flex;justify-content:space-between;padding:7px 0;border-bottom:1px solid var(--soft);font-size:14px}
.ing:last-child{border-bottom:0}
.ring{width:84px;height:84px;flex:0 0 84px}
/* ristorante */
.cnt{display:flex;align-items:center;gap:6px}
.cnt b{min-width:26px;text-align:center;font-family:var(--disp);font-size:19px}
.cnt button{width:40px;height:40px;border-radius:20px;border:1px solid var(--line2);background:var(--btnbg);color:var(--tx);font-size:19px;padding:0}
.rtot{position:sticky;bottom:-28px;background:var(--bg);padding:12px 0 34px;margin-top:6px;border-top:1px solid var(--line)}
/* modalità seduta */
.sess{position:fixed;inset:0;z-index:70;background:#17161c;color:#f4f1ea;display:none;flex-direction:column;
padding:calc(14px + env(safe-area-inset-top)) 20px calc(20px + env(safe-area-inset-bottom));overflow:auto}
.sess.on{display:flex}
.sess .cb{width:44px;height:44px;border-radius:22px;border:1px solid #34313d;background:transparent;color:#f4f1ea;display:flex;align-items:center;justify-content:center;padding:0;flex:0 0 44px}
.sess .cb svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.sess .kick{font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#a9a3b4}
.sess .ttl{font-family:var(--disp);font-size:20px;font-weight:600}
.sprog{display:flex;gap:4px;margin:16px 0 4px}
.sprog i{flex:1;height:6px;border-radius:3px;background:#34313d}
.sprog i.d{background:#3cb894}.sprog i.c{background:#f4f1ea}
.slg{display:flex;gap:14px;justify-content:center;font-size:12px;color:#a9a3b4;margin:6px 0 0;flex-wrap:wrap}
.slg span{display:flex;align-items:center;gap:6px}.slg i{width:10px;height:10px;border-radius:5px;display:inline-block}
.phase{font-size:13px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#17161c;padding:6px 14px;border-radius:14px;align-self:center;margin-top:18px}
.ph-w{background:#3cb894}.ph-r{background:#a89ff0}.ph-g{background:#e0a04a}.ph-s{background:#f4f1ea}
.tring{position:relative;width:250px;height:250px;align-self:center;margin:14px 0 6px}
.tring svg{width:250px;height:250px;display:block}
.tring div{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:2px}
.tring b{font-family:var(--disp);font-size:78px;font-weight:600;line-height:1;letter-spacing:-2px}
.tring span{font-size:14px;color:#a9a3b4}
.sname{font-family:var(--disp);font-size:27px;font-weight:600;text-align:center;line-height:1.15}
.ssub{font-size:14px;color:#a9a3b4;text-align:center;margin-top:4px}
.satt{display:flex;gap:10px;align-items:flex-start;background:#2b1f1c;border:1px solid #4a2e27;border-radius:16px;padding:12px 14px;margin-top:16px;font-size:14px;line-height:1.45;color:#f6dcd4}
.satt svg{width:18px;height:18px;flex:0 0 18px;stroke:#f0917a;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;margin-top:1px}
.snext{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:12px 14px;border-radius:16px;background:#211f27;margin-top:10px}
.snext div div:first-child{font-size:12px;font-weight:700;letter-spacing:1px;text-transform:uppercase;color:#a89ff0}
.snext div div:last-child{font-size:15px;font-weight:600}
.sctl{display:flex;align-items:center;justify-content:center;gap:22px;margin-top:auto;padding-top:20px}
.sctl button{width:60px;height:60px;border-radius:30px;border:1px solid #34313d;background:transparent;color:#f4f1ea;display:flex;align-items:center;justify-content:center;padding:0}
.sctl button svg{width:22px;height:22px;stroke:currentColor;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}
.sctl button.main{width:84px;height:84px;border-radius:42px;border:0;background:#f4f1ea;color:#17161c}
.sctl button.main svg{width:30px;height:30px;fill:currentColor;stroke:none}
.sbig{display:block;width:100%;min-height:58px;border-radius:18px;border:0;background:#3cb894;color:#17161c;font-size:17px;font-weight:700;margin-top:16px}
.sreps{font-family:var(--disp);font-size:64px;font-weight:600;text-align:center;line-height:1;margin-top:26px}
.sser{display:flex;gap:8px;justify-content:center;margin-top:14px}
.sser i{width:14px;height:14px;border-radius:7px;background:#34313d}.sser i.d{background:#3cb894}.sser i.c{background:#f4f1ea}
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


ICON_WARN = ('<svg viewBox="0 0 24 24"><path d="M12 3l9 16H3z"/><path d="M12 10v4M12 17v.5"/></svg>')


def box_attenzione(e):
    return ('<div class="attbox"><div class="attl">%sAttenzione</div>%s</div>'
            % (ICON_WARN, "".join('<div class="ai">%s</div>' % a for a in e["att"])))


def blocco_esercizio(e):
    """Testo della scheda dopo il disegno: stesso ordine della scheda aperta dalla seduta."""
    err_ = "".join('<div style="margin-bottom:6px">%s</div>' % x for x in e["errori"])
    return ('<div class="exbody">%s</div>'
            '<div class="attl">Prima</div><div class="exbody">%s</div>'
            '<div class="attl">Durante</div><div class="exbody">%s</div>'
            '<div class="attl">Errori comuni</div><div class="exbody">%s</div>'
            '<div class="attl">Perché lo fai</div><div class="exbody">%s</div>'
            '<div class="attl">Se fa male</div><div class="exbody">%s</div>'
            % (e["desc"], e.get("prima", ""), e.get("durante", ""), err_, e["perche"], e["male"]))


def html_appendice():
    h = []
    for e in ESERCIZI:
        h.append('<div class="exc"><div class="disp" style="font-size:19px">%s</div>'
                 '<div class="pnote">Sedute: %s</div>%s'
                 '<div class="dgw">%s</div>%s</div>'
                 % (e["n"], e["sedute"], box_attenzione(e), e["svg"], blocco_esercizio(e)))
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

function blank(){return{v:DB.ver,days:{},meas:{},custom:[],ovr:{},sch:{1:"A",2:"B",4:"C",6:"D"},
 lastBackup:null,tg:null,prof:null,lastQty:{},seenVer:null,lastAdj:null,check21:null,
 storta:{on:false,from:null,log:[]},persist:null,prog:{}}}
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
function migraS(){const v0=S.v||1;if(v0>=DB.ver)return false;
 if(v0<3){const mv=[];Object.keys(S.days).forEach(k=>{const d=S.days[k];if(!d)return;
  if(d.hip!==null&&d.hip!==undefined){mv.push([shift(k,1),d.hip]);d.hip=null}});
 mv.forEach(([k,v])=>{day(k).hip=v})}
 /* 3.1: nella v3 l'interruttore storta non si spegneva, quindi quello che c'è è un errore */
 if(v0<3.1)S.storta={on:false,from:null,log:[]};
 /* nomi di alimenti e piatti cambiati: vale per ogni versione precedente */
 Object.keys(S.days).forEach(k=>{const d=S.days[k];if(!d)return;
  Object.keys(d.m||{}).forEach(m=>(d.m[m]||[]).forEach(i=>{if(DB.ren[i.n])i.n=DB.ren[i.n]}))});
 if(!S.prog)S.prog={};
 S.v=DB.ver;return true}
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
/* Il periodo attivo va da s.from a oggi; quelli chiusi stanno in s.log.
   Spegnere su un giorno lo toglie dal periodo: il periodo finisce il giorno prima
   (se il giorno era il primo, il periodo sparisce). Sui giorni passati
   l'interruttore segna o toglie quel giorno solo. */
function stortaOff(k){const s=S.storta,out=[];
 (s.log||[]).forEach(p=>{if(k<p.from||k>p.to){out.push(p);return}
  if(p.from<k)out.push({from:p.from,to:shift(k,-1)});
  if(p.to>k)out.push({from:shift(k,1),to:p.to})});
 s.log=out;
 if(s.on&&s.from&&k>=s.from){
  if(s.from<k)s.log.push({from:s.from,to:shift(k,-1)});
  if(k>=today()){s.on=false;s.from=null}else s.from=shift(k,1)}}
function toggleStorta(){const s=S.storta,k=cur,t=today();
 if(isStorta(k))stortaOff(k);
 else if(k>=t){s.on=true;s.from=t}
 else (s.log=s.log||[]).push({from:k,to:k});
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
function qLab(i){
 if(i.u)return nfmt(i.q)+" "+plur(i.u,i.q)+" &middot; "+nfmt(i.g)+" g";
 if(i.pz)return nfmt(i.pz)+" "+(i.pz===1?"porzione":"porzioni");
 if(i.st)return "stima";
 if(i.g)return nfmt(i.g)+" g";
 return ""}

/* ---- icone piccole usate nei pulsanti ---- */
const IC={
 prev:'<svg viewBox="0 0 24 24"><path d="M15 6l-6 6 6 6"/></svg>',
 next:'<svg viewBox="0 0 24 24"><path d="M9 6l6 6-6 6"/></svg>',
 rep:'<svg viewBox="0 0 24 24"><path d="M4 12a8 8 0 1 0 2.3-5.7"/><path d="M4 4v4h4"/></svg>',
 plan:'<svg viewBox="0 0 24 24"><rect x="5" y="3" width="14" height="18" rx="2"/><path d="M9 8h6M9 12h6M9 16h4"/></svg>',
 search:'<svg viewBox="0 0 24 24"><circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/></svg>',
 rest:'<svg viewBox="0 0 24 24"><path d="M4 11h16v8H4zM7 11V7h10v4"/></svg>',
 warn:'<svg viewBox="0 0 24 24"><path d="M12 3l9 16H3z"/><path d="M12 10v4M12 17v.5"/></svg>',
 play:'<svg viewBox="0 0 24 24"><path d="M7 5l12 7-12 7z"/></svg>',
 pause:'<svg viewBox="0 0 24 24"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>',
 back:'<svg viewBox="0 0 24 24"><path d="M18 6l-8 6 8 6z"/><path d="M6 6v12"/></svg>',
 fwd:'<svg viewBox="0 0 24 24"><path d="M6 6l8 6-8 6z"/><path d="M18 6v12"/></svg>',
 x:'<svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18"/></svg>'};
function bigRing(v,max,col,bg,val,lab){const r=56,c=2*Math.PI*r,f=Math.max(0,Math.min(1,max?v/max:0));
 return '<div class="rgw"><svg viewBox="0 0 132 132"><circle cx="66" cy="66" r="'+r+'" fill="none" stroke="'+bg+'" stroke-width="11"/>'
 +'<circle cx="66" cy="66" r="'+r+'" fill="none" stroke="'+col+'" stroke-width="11" stroke-linecap="round" stroke-dasharray="'
 +(c*f).toFixed(1)+' '+c.toFixed(1)+'" transform="rotate(-90 66 66)"/></svg>'
 +'<div class="rgv"><b>'+val+'</b><span>'+lab+'</span></div></div>'}
/* barra con tacca: la pista arriva al 130% del target, la tacca segna il 100% */
function mbar(v,t,warn,th){const f=t?Math.min(v/t,1.3)/1.3*100:0,o=warn&&t&&v>t*1.1;
 return '<div class="mb'+(th?" th":"")+'"><i class="'+(o?"o":"")+'" style="width:'+f.toFixed(1)+'%"></i><s style="left:'+(100/1.3).toFixed(1)+'%"></s></div>'}
function mrow(l,v,t,u,warn){return '<div class="mbw"><div class="mbh"><span>'+l+'</span><span><b>'+R(v)+'</b><em> / '+t+' '+u+'</em></span></div>'+mbar(v,t,warn)+'</div>'}
function ring(v,max){return bigRing(v,max,"var(--acc)","var(--accbg)",R(v),"")}
function datenav(){const t=today(),d=parseIso(cur);
 const top=cur===t?"oggi":(cur>t?"futuro":"tocca per tornare a oggi");
 return '<div class="dnav"><button class="cbtn" onclick="go(-1)" aria-label="giorno precedente">'+IC.prev+'</button>'
 +'<div class="dn2" onclick="goToday()"><b>'+cap(GG[d.getDay()])+' '+d.getDate()+'</b>'
 +'<div class="mut3">'+MM[d.getMonth()]+' &middot; '+top+'</div></div>'
 +'<button class="cbtn" onclick="go(1)" aria-label="giorno successivo">'+IC.next+'</button></div>'}
function weekStrip(){let h='<div class="wk">';
 for(let i=6;i>=0;i--){const k=shift(cur,-i),d=S.days[k];const f=d&&tot(day(k)).kcal>0,t=d&&d.w&&d.w.done;
  h+='<button class="'+(i===0?"on":"")+'" onclick="goDay(\''+k+'\')">'+GGS[parseIso(k).getDay()]
   +'<i class="'+(f?"f":"")+'">'+parseIso(k).getDate()+'</i><u class="'+(t?"t":"")+'"></u></button>'}
 return h+'</div>'}
/* tipo di giornata: allenamento, riposo o storta. La storta è un periodo: resta attiva finché scegli altro. */
function setDayType(x){const k=cur;
 if(x==="storta"){if(!isStorta(k))toggleStorta();return}
 if(isStorta(k))stortaOff(k);
 day(k).tr=(x==="allen");save();haptic();render()}

function renderOggi(){const d=day(cur),t=tot(d),g=target(cur),k=cur;
 const manca=Math.max(0,g.p-t.p),rest=g.kcal-t.kcal,st=isStorta(k);
 let h="";
 if(S.seenVer!==DB.ver)h+='<div class="card pad"><div class="row"><b class="disp" style="font-size:19px">Novità della v'+DB.ver+'</b><span class="mut3">'+DB.data+'</span></div>'
  +'<ul style="margin:8px 0 10px;padding-left:18px;font-size:14px;color:var(--tx2)">'+DB.novita.map(x=>'<li>'+esc(x)+'</li>').join("")+'</ul>'
  +'<button class="btn w" onclick="S.seenVer=DB.ver;save();renderOggi()">Ok, visto</button></div>';
 h+=datenav()+weekStrip();
 const dt=st?"storta":(d.tr?"allen":"riposo");
 h+='<div class="seg day"><button class="'+(dt==="allen"?"on":"")+'" onclick="setDayType(\'allen\')">Allenamento</button>'
  +'<button class="'+(dt==="riposo"?"on":"")+'" onclick="setDayType(\'riposo\')">Riposo</button>'
  +'<button class="'+(dt==="storta"?"on st":"")+'" onclick="setDayType(\'storta\')">Storta</button></div>';
 if(st)h+='<div class="mut3" style="margin:8px 4px 0">Tre pasti, mantenimento, sedute A e B corte. Resta attiva nei giorni successivi finché scegli un\'altra opzione.</div>';
 const ov=rest<0;
 h+='<div class="card pad"><div class="rings">'
  +'<div class="rg">'+bigRing(t.kcal,g.kcal,ov?"var(--warnbar)":"var(--acc)",ov?"var(--warnbg)":"var(--accbg)",R(Math.abs(rest)),ov?"kcal oltre":"kcal restano")
  +'<div class="rgl"><div style="color:'+(ov?"var(--warn)":"var(--acc)")+'">Calorie</div>'+fmtK(t.kcal)+' di '+fmtK(g.kcal)+'</div></div>'
  +'<div class="rg">'+bigRing(t.p,g.p,"var(--ok)","var(--okbg)",manca>0?R(manca)+" g":"&#10003;",manca>0?"mancano":"fatte")
  +'<div class="rgl"><div style="color:var(--ok)">Proteine</div>'+R(t.p)+' di '+g.p+' g</div></div></div>'
  +'<div class="hr"></div>'
  +mrow("Grassi",t.f,g.f,"g",1)+mrow("Carboidrati",t.c,g.c,"g",1)+mrow("Fibra",t.fib,g.fib,"g",0)
  +'</div>';
 h+=check21Card();
 h+='<div class="slab">I pasti</div>';
 const ms=mealsFor(k),sh=shareFor(k);
 ms.forEach(m=>{const it=d.m[m];
  const s=it.reduce((a,i)=>{a.k+=i.kcal;a.p+=i.p;return a},{k:0,p:0});
  const q=Math.round(g.kcal*sh[m]/5)*5,over=it.length&&s.k>q*1.1;
  const y=S.days[shift(k,-1)],hasY=y&&y.m&&y.m[m]&&y.m[m].length;
  h+='<div class="card pad"><div class="mhead"><div class="mname">'+MLAB[m]+'</div>'
   +(it.length?'<div class="mtot'+(over?" over":"")+'"><b>'+fmtK(s.k)+'</b><span> / '+q+' kcal</span></div>'
     :'<div class="mut3">obiettivo ~'+q+' kcal</div>')+'</div>';
  if(over)h+='<div class="mover">'+mbar(s.k,q,1,1)+'<span class="ovb">+'+fmtK(s.k-q)+'</span></div>';
  if(it.length){h+='<div style="margin-top:4px">'+it.map((i,ix)=>
    '<div class="frow"><div class="fn" onclick="editItem(\''+m+'\','+ix+')">'+esc(i.n)+' <span class="fg">'+qLab(i)+'</span>'
    +'<div class="mac">G '+nfmt(R(i.f,1))+' &middot; C '+nfmt(R(i.c,1))+' &middot; fibra '+nfmt(R(i.fib||0,1))+'</div></div>'
    +'<div class="fk" onclick="editItem(\''+m+'\','+ix+')"><b>'+fmtK(i.kcal)+'</b> kcal<br><span class="p">'+nfmt(R(i.p,1))+' g P</span></div>'
    +'<button class="fx" onclick="rm(\''+m+'\','+ix+')" aria-label="elimina">&times;</button></div>'
   ).join("")+'</div>'
   +'<button class="btn w" style="margin-top:10px" onclick="pick(\''+m+'\')">+ Aggiungi</button>'}
  else{h+='<div class="grid2" style="margin-top:12px;gap:8px">'
   +'<button class="btn ico" '+(hasY?'onclick="ripeti(\''+m+'\')"':'disabled style="opacity:.4"')+'>'+IC.rep+'Ripeti ieri</button>'
   +'<button class="btn ico" onclick="pick(\''+m+'\',\'__piano\')">'+IC.plan+'Dal piano</button></div>'
   +'<button class="btn acc w ico" style="margin-top:8px" onclick="pick(\''+m+'\')">'+IC.search+'Cerca un alimento</button>'}
  h+='</div>'});
 if(st&&d.m.spuntino.length){h+='<div class="card pad"><div class="mname">Spuntino</div><div class="mut3">registrato prima della settimana storta</div>'
  +d.m.spuntino.map(i=>'<div class="frow"><div class="fn">'+esc(i.n)+' <span class="fg">'+qLab(i)+'</span></div><div class="fk"><b>'+fmtK(i.kcal)+'</b> kcal</div></div>').join("")+'</div>'}
 if(t.f>0&&t.f<55&&t.kcal>1200)h+='<div class="note w">Grassi sotto i 55 g. Aggiungi 15 g di mandorle o frutta secca.</div>';
 if(t.fib>0&&t.fib<18&&t.kcal>1200)h+='<div class="note w">Fibra sotto i 18 g. Un frutto o 10 g di semi di chia sistemano la giornata.</div>';
 h+='<div class="card pad"><div class="disp" style="font-size:19px;margin-bottom:12px">Integratori e acqua</div><div>';
 SUP.forEach(s=>{h+='<button class="pill '+(d.sup[s[0]]?"on":"")+'" onclick="sup(\''+s[0]+'\')">'
  +(d.sup[s[0]]?"&#10003;&nbsp;":"")+s[1]+'</button>'});
 h+='</div><div class="row" style="margin-top:6px"><span class="mut" style="font-size:14px">Acqua &middot; <b style="color:var(--tx)">'+d.water+' bicchieri</b> ('
  +nfmt(R(d.water*0.25,2))+' L)</span><span style="display:flex;gap:8px"><button class="cbtn" onclick="water(-1)" aria-label="un bicchiere in meno">&minus;</button>'
  +'<button class="cbtn" onclick="water(1)" aria-label="un bicchiere in più">+</button></span></div></div>';
 $("oggi-dyn").innerHTML=h}
function fmtK(n){n=R(n);const s=String(Math.abs(n));return (n<0?"-":"")+(s.length>3?s.slice(0,-3)+"."+s.slice(-3):s)}
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
 else if(ub.type==="prog"){if(ub.prev)S.prog[ub.key]=ub.prev;else delete S.prog[ub.key]}
 ub=null;save();render();if($("sheet").classList.contains("on"))renderPick()}
 $("undo").classList.remove("on")}
function ripeti(m){const y=S.days[shift(cur,-1)];if(!y||!y.m||!y.m[m]||!y.m[m].length)return;
 const arr=y.m[m].map(i=>Object.assign({},i));day(cur).m[m].push(...arr);ub={type:"add",m:m,n:arr.length};
 save();haptic();renderOggi();showUndo("Copiate "+arr.length+" voci da ieri")}
"""


# Parte 2: inserimento cibo, quantità, ricerca

JS2 = r"""
let pSlot=null,pQ="",pCat=null,qEdit=null,pAdded=[];
function pick(m,cat){pSlot=m;pQ="";pCat=cat||null;qEdit=null;pAdded=[];rLoc=null;rCnt={};rCond=false;
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
   +'<button class="'+(pCat==="__rist"?"on":"")+'" onclick="pSetCat(\'__rist\')">Ristorante</button>'
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
 else if(pCat==="__rist"){h+=htmlRist();$("sbody").innerHTML=h;return}
 else{const l=allFoods().filter(f=>(f.cat||"nuovi")===pCat).sort((a,b)=>a.n.localeCompare(b.n));
  h+=l.map(rowFood).join("")}
 h+='<div class="grid2" style="margin:20px 0 8px">'
  +'<button class="btn" onclick="openNuovo()">Nuovo alimento</button>'
  +'<button class="btn" onclick="openStima()">Stima rapida</button></div>';
 $("sbody").innerHTML=h;$("sbody").scrollTop=0}


/* ---------------- stime da ristorante ---------------- */
const PIATN={};DB.piatti.forEach(p=>{PIATN[p.n]=p});
let rLoc=null,rCnt={},rCond=false;
function rUnit(it){/* valori per un tocco di + */
 if(it.t==="p"){const p=PIATN[it.n];const o={kcal:p.kcal,p:p.p,f:p.f,c:p.c,fib:p.fib||0};
  if(rCond){const x=p.kcal*DB.cond;o.kcal+=x;o.f+=x/9}return o}
 const f=food(it.n),g=it.t==="u"?f.ug:it.g,k=g/100;
 return {kcal:f.kcal*k,p:f.p*k,f:f.f*k,c:f.c*k,fib:(f.fib||0)*k,g:g,u:f.u}}
function rSub(it){if(it.t==="p")return "a porzione";if(it.t==="u"){const f=food(it.n);return "a "+f.u+" &middot; "+nfmt(f.ug)+" g"}return "a porzione &middot; "+it.g+" g"}
function rLocal(i){rLoc=i;rCnt={};renderPick()}
function rAdj(i,d){const v=Math.max(0,(rCnt[i]||0)+d);if(v)rCnt[i]=v;else delete rCnt[i];haptic(8);renderPick()}
function rTog(){rCond=!rCond;renderPick()}
function rTot(){const L=DB.rist[rLoc],t={kcal:0,p:0,f:0,c:0,fib:0,n:0};
 Object.keys(rCnt).forEach(i=>{const u=rUnit(L.items[i]),c=rCnt[i];["kcal","p","f","c","fib"].forEach(x=>t[x]+=u[x]*c);t.n++});return t}
function rAddAll(){const L=DB.rist[rLoc],arr=[];
 Object.keys(rCnt).forEach(i=>{const it=L.items[i],u=rUnit(it),c=rCnt[i];
  const o={n:it.n,g:0,kcal:R(u.kcal*c),p:R(u.p*c,1),f:R(u.f*c,1),c:R(u.c*c,1),fib:R(u.fib*c,1)};
  if(it.t==="p"){o.pz=c;if(rCond)o.mod=1}
  else if(it.t==="u"){o.g=R(u.g*c,1);o.u=u.u;o.q=c}
  else o.g=R(u.g*c,1);
  arr.push(o)});
 if(!arr.length)return;
 haptic();day(cur).m[pSlot].push(...arr);pAdded.push(...arr);ub={type:"add",m:pSlot,n:arr.length};save();
 rCnt={};renderPick();showUndo(arr.length+(arr.length===1?" voce aggiunta":" voci aggiunte"))}
function htmlRist(){let h="";
 if(rLoc===null){h+='<div class="mut" style="margin:10px 2px 4px">Scegli il locale e componi il pasto con + e &minus;. I valori sono stime da ristorante: se hai l\'etichetta, usa quella.</div>';
  DB.rist.forEach((L,i)=>{h+='<div class="lrow" onclick="rLocal('+i+')"><span><b>'+esc(L.n)+'</b><div class="mut3">'+L.items.length+' voci</div></span><span class="mut">&rsaquo;</span></div>'});
  return h}
 const L=DB.rist[rLoc];
 h+='<div class="row" style="margin:12px 0 4px"><button class="btn sm" onclick="rLocal(null)">&lsaquo; Locali</button><b class="disp" style="font-size:19px">'+esc(L.n)+'</b></div>';
 L.items.forEach((it,i)=>{const u=rUnit(it),c=rCnt[i]||0;
  h+='<div class="lrow" style="cursor:default"><span>'+esc(it.n)+'<div class="mut3">'+R(u.kcal)+' kcal &middot; '+nfmt(R(u.p,1))+' g P '+rSub(it)+'</div></span>'
   +'<span class="cnt"><button onclick="rAdj('+i+',-1)" aria-label="meno"'+(c?'':' style="opacity:.35"')+'>&minus;</button><b>'+c+'</b><button onclick="rAdj('+i+',1)" aria-label="più">+</button></span></div>'});
 const t=rTot();
 h+='<div class="rtot"><div class="row" style="margin-bottom:10px"><span class="mut" style="font-size:14px">Condimento da ristorante<div class="mut3">+'+R(DB.cond*100)+'% sulle calorie dei piatti, come olio</div></span>'
  +'<button class="sw '+(rCond?"on":"")+'" onclick="rTog()" aria-label="condimento da ristorante"></button></div>'
  +'<button class="btn acc w" '+(t.n?'':'disabled style="opacity:.4"')+' onclick="rAddAll()">'
  +(t.n?'Aggiungi a '+MLAB[pSlot]+' &middot; '+fmtK(t.kcal)+' kcal, '+R(t.p)+' g P':'Aggiungi a '+MLAB[pSlot])+'</button></div>';
 return h}

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
 let s=R(f.kcal*k)+' kcal &middot; '+R(f.p*k,1)+' g P &middot; '+R(f.f*k,1)+' g G &middot; '+R(f.c*k,1)+' g C &middot; '+R((f.fib||0)*k,1)+' g fibra';
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
 +'<div><label class="mut3">Proteine (g)</label><input id="e-p" type="number" inputmode="decimal" value="'+(pre.p||"")+'"></div>'
 +'<div><label class="mut3">Grassi (g)</label><input id="e-f" type="number" inputmode="decimal" value="'+(pre.f||"")+'"></div>'
 +'<div><label class="mut3">Carboidrati (g)</label><input id="e-c" type="number" inputmode="decimal" value="'+(pre.c||"")+'"></div>'
 +'<div><label class="mut3">Fibra (g)</label><input id="e-fb" type="number" inputmode="decimal" value="'+(pre.fib||"")+'"></div></div>'
 +'<button class="btn acc w" style="margin-top:12px" onclick="addStima()">'+(qEdit?"Salva":"Aggiungi")+'</button>'
 +'<button class="btn w" style="margin-top:8px" onclick="renderPick()">Annulla</button>'}
function addStima(){putItem({n:($("e-n").value.trim()||"Stima rapida"),g:0,st:1,
 kcal:+$("e-k").value||0,p:+$("e-p").value||0,f:+$("e-f").value||0,c:+$("e-c").value||0,fib:+$("e-fb").value||0})}
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
 +'<div><label class="mut3">Unità (fetta, vasetto)</label><input id="n-u" placeholder="facoltativo"></div>'
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
scorciatoia();
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


# Parte 7: allenamento (progressione, scheda esercizio, modalità seduta)

JS7 = r"""
/* ---------------- progressione ----------------
   Il piano: una leva alla volta, nell'ordine serie, ripetizioni, elastico più duro, tempo.
   S.prog["C|Piegamenti sulle braccia"]={lv:1,at:"2026-09-21"}: livello raggiunto e da quando. */
function parsePr(pr){let m=pr.match(/^(\d+) giri x (\d+) s$/);
 if(m)return {giri:+m[1],secs:+m[2]};
 m=pr.match(/^(\d+) x (\d+)(?:-(\d+))?( s)?( per lato)?$/);
 if(!m)return null;
 return {sets:+m[1],a:+m[2],b:m[3]?+m[3]:null,t:!!m[4],lato:!!m[5]}}
function fmtPr(p){if(p.giri)return p.giri+" giri x "+p.secs+" s";
 return p.sets+" x "+p.a+(p.b?"-"+p.b:"")+(p.t?" s":"")+(p.lato?" per lato":"")}
function usaElastico(n){return /elastico|band|Ponte glutei a terra/.test(n)}
/* passi possibili per un esercizio, in ordine */
function levers(n,p){const L=[];
 if(!p||p.giri)return L;
 if(p.sets<5)L.push({k:"serie"});
 L.push({k:"rip"});
 if(usaElastico(n))L.push({k:"elastico"});
 if(!p.t)L.push({k:"tempo"});
 return L}
function applyLever(p,lv){p=Object.assign({},p);const st=p.t?5:(Math.max(p.a,p.b||0)<=6?1:2);
 if(lv.k==="serie")p.sets++;
 if(lv.k==="rip"){p.a+=st;if(p.b)p.b+=st}
 return p}
/* prescrizione attuale per quella seduta, con eventuali passi applicati */
function prFor(sed,e){const key=sed+"|"+e.n,g=S.prog&&S.prog[key],base=parsePr(e.pr);
 const lv=g?g.lv:0;if(!base||!lv)return {pr:e.pr,p:base,lv:0,note:[],key:key};
 const L=levers(e.n,base);let p=base,note=[];
 for(let i=0;i<lv;i++){const x=L[Math.min(i,L.length-1)];
  if(i>=L.length&&x.k!=="rip"){p=applyLever(p,{k:"rip"});continue}
  p=applyLever(p,x);if(x.k==="elastico")note.push("elastico più duro");if(x.k==="tempo")note.push("3 secondi in discesa")}
 return {pr:fmtPr(p),p:p,lv:lv,note:note,key:key}}
function nextStep(sed,e){const cur=prFor(sed,e),base=parsePr(e.pr);if(!base||base.giri)return null;
 const L=levers(e.n,base),i=cur.lv,x=i<L.length?L[i]:{k:"rip"};
 if(x.k==="elastico"||x.k==="tempo")return {txt:fmtPr(cur.p)+", "+(x.k==="elastico"?"elastico più duro":"3 secondi in discesa")};
 return {txt:fmtPr(applyLever(cur.p,x))}}
/* sedute fatte con quell'esercizio, dopo l'ultimo aumento: servono due + di fila */
function exHistory(sed,n,since){const out=[];
 Object.keys(S.days).sort().forEach(k=>{if(since&&k<=since)return;const w=S.days[k].w;
  if(w&&w.done&&!w.corta&&w.sed===sed&&w.ex&&(n in w.ex||DB.sedute[sed].ex.some(x=>x.n===n)))out.push({k:k,v:w.ex[n]||0})});return out}
function suggest(sed,e){const key=sed+"|"+e.n,g=S.prog&&S.prog[key];
 const h=exHistory(sed,e.n,g?g.at:null);if(h.length<2)return null;
 const a=h[h.length-1],b=h[h.length-2];if(a.v!==1||b.v!==1)return null;
 const nx=nextStep(sed,e);if(!nx)return null;
 const hv=S.days[shift(a.k,1)]&&S.days[shift(a.k,1)].hip;
 if(hv!==null&&hv!==undefined&&hv>=2)return {blocked:1,hip:hv,txt:nx.txt};
 return {txt:nx.txt,at:a.k}}
function applySugg(sed,n){const key=sed+"|"+n;if(!S.prog)S.prog={};const g=S.prog[key]||{lv:0};
 S.prog[key]={lv:g.lv+1,at:today()};save();haptic();renderAllen();showUndo("Aumento applicato");ub={type:"prog",key:key,prev:g.lv?g:null}}
function resetProg(sed,n){if(S.prog)delete S.prog[sed+"|"+n];save();closeSheet2();renderAllen()}

/* ---------------- scheda esercizio ---------------- */
function exSheet(n){const e=DB.ex[n];if(!e)return;
 let ex=null,sed=null;Object.keys(DB.sedute).forEach(k=>DB.sedute[k].ex.forEach(x=>{if(x.n===n&&!ex){ex=x;sed=k}}));
 const d=day(cur);if(d.w.sed&&DB.sedute[d.w.sed].ex.some(x=>x.n===n)){ex=DB.sedute[d.w.sed].ex.find(x=>x.n===n);sed=d.w.sed}
 const pf=ex?prFor(sed,ex):null;
 let h='<div class="mut3" style="font-weight:700;letter-spacing:.8px;text-transform:uppercase;color:var(--ok);margin-top:12px">Sedute '+esc(e.sedute)+'</div>';
 if(pf)h+='<div style="display:flex;gap:8px;flex-wrap:wrap;margin:10px 0 2px"><span class="pill on" style="cursor:default">'+esc(pf.pr)+'</span>'
  +pf.note.map(x=>'<span class="pill" style="cursor:default">'+esc(x)+'</span>').join("")
  +'<span class="pill" style="cursor:default">recupero '+ex.rest+' s</span></div>';
 h+='<div class="attbox"><div class="attl">'+IC.warn+'Attenzione</div>'+e.att.map(a=>'<div class="ai">'+a+'</div>').join("")+'</div>'
  +'<div class="card pad"><div class="dgw">'+(SVG[n]||"")+'</div></div>'
  +'<div class="card pad"><div class="exbody">'+e.desc+'</div>'
  +'<div class="attl">Prima</div><div class="exbody">'+e.prima+'</div>'
  +'<div class="attl">Durante</div><div class="exbody">'+e.durante+'</div>'
  +'<div class="attl">Errori comuni</div><div class="exbody">'+e.errori.map(x=>'<div style="margin-bottom:6px">'+x+'</div>').join("")+'</div>'
  +'<div class="attl">Perché lo fai</div><div class="exbody">'+e.perche+'</div>'
  +'<div class="attl">Se fa male</div><div class="exbody">'+e.male+'</div></div>';
 if(ex)h+='<button class="btn acc w" onclick="timer('+ex.rest+')">Avvia recupero &middot; '+ex.rest+' s</button>';
 if(pf&&pf.lv)h+='<button class="btn w" style="margin-top:8px" onclick="resetProg(\''+sed+'\',\''+n.replace(/'/g,"\\'")+'\')">Torna allo schema del piano ('+esc(ex.pr)+')</button>';
 h+='<button class="btn w" style="margin:8px 0 10px" onclick="closeSheet2()">Chiudi</button>';
 sheet2(n,h)}

/* ---------------- scheda Allenamento ---------------- */
function renderAllen(){const d=day(cur),pk=shift(cur,-1),pd=S.days[pk],st=isStorta(cur);
 const sed=d.w.sed;
 let h=datenav()+'<div class="card pad">'
  +'<div class="row"><div><div class="disp" style="font-size:21px">'+(sed?"Seduta "+sed:"Nessuna seduta")+'</div>'
  +'<div class="mut3">'+(sed?esc(DB.sedute[sed].nome):"Giorno di riposo")+'</div></div>'
  +'<div class="seg" style="width:140px"><button class="'+(d.w.done?"on":"")+'" onclick="wdone(1)">Fatta</button>'
  +'<button class="'+(d.w.done?"":"on")+'" onclick="wdone(0)">No</button></div></div>'
  +'<div style="margin-top:12px">'+["A","B","C","D"].map(s=>'<button class="pill '+(sed===s?"on":"")+'" onclick="wsed(\''+s+'\')">'+s+'</button>').join("")+'</div>'
  +'<div class="seg" style="margin-top:4px"><button class="'+(!d.w.corta?"on":"")+'" onclick="wcorta(0)">30 minuti</button>'
  +'<button class="'+(d.w.corta?"on":"")+'" onclick="wcorta(1)">15 minuti</button></div>'
  +(sed&&!d.w.done?'<button class="btn acc w ico" style="margin-top:12px;min-height:52px" onclick="sessOpen()">'+IC.play+'Inizia la seduta</button>':'')
  +(st?'<div class="note w" style="margin-bottom:0">Settimana storta: due sedute, A e B, in versione corta. L\'obiettivo è non perdere terreno, non progredire.</div>':'')
  +'</div>';
 if(sed){const z=DB.sedute[sed].zona,w=DB.warm[z];
  h+='<details class="card pad"><summary>Riscaldamento &middot; '+(d.w.presto?8:5)+' min<span class="mut3" style="font-weight:400"> &middot; parte '+z+'</span></summary>'
   +'<ul style="margin:10px 0;padding-left:18px;font-size:14px;color:var(--tx2)">'+w.map(x=>'<li>'+esc(x)+'</li>').join("")+'</ul>'
   +'<div class="seg"><button class="'+(!d.w.presto?"on":"")+'" onclick="wpresto(0)">Orario normale</button>'
   +'<button class="'+(d.w.presto?"on":"")+'" onclick="wpresto(1)">Entro un\'ora dal risveglio</button></div>'
   +(d.w.presto?'<div class="note w" style="margin-bottom:0">'+esc(DB.notaMattino)+'</div>':'')
   +(z==="bassa"?'<div class="mut3" style="margin-top:8px">Niente stretching dei flessori e niente piccione prima di allenarti.</div>':'')
   +'</details>'}
 if(sed){const lst=sedEx(sed,d.w.corta),s=DB.sedute[sed];
  h+='<div class="slab">'+(d.w.corta?"Versione da 15 minuti":"Esercizi")+(d.w.done?" &middot; segna solo se è andata diversamente":"")+'</div>'
   +'<div class="card pad">'+(s.nota?'<div class="mut3" style="margin-bottom:6px">'+esc(s.nota)+'</div>':'');
  lst.forEach(e=>{const v=d.w.ex[e.n]||0,en=e.n.replace(/'/g,"\\'"),pf=prFor(sed,e),sg=d.w.corta?null:suggest(sed,e);
   h+='<div class="exrow"><div class="row"><div class="exn" onclick="exSheet(\''+en+'\')">'+esc(e.n)+' <i>&rsaquo;</i></div>'
   +(d.w.done?'<div class="pm2"><button class="qb '+(v===-1?"dn":"")+'" onclick="wex(\''+en+'\',-1)" aria-label="meno del previsto">&minus;</button>'
   +'<button class="qb '+(v===1?"up":"")+'" onclick="wex(\''+en+'\',1)" aria-label="più del previsto">+</button></div>':'')+'</div>'
   +'<div class="row" style="margin-top:2px"><div><span class="expr">'+esc(pf.pr)+'</span>'
   +(pf.note.length?' <span class="mut3">&middot; '+esc(pf.note.join(", "))+'</span>':'')
   +(v===1?' <span class="mut3">&middot; più del previsto</span>':v===-1?' <span class="mut3">&middot; meno del previsto</span>':'')+'</div>'
   +'<button class="tbtn" onclick="timer('+e.rest+')">&#9201; '+e.rest+' s</button></div>'
   +(sg?(sg.blocked?'<div class="note w" style="margin:8px 0 0">Due volte sopra il previsto, ma il giorno dopo l\'anca era a '+sg.hip+'. Niente aumento finché non torna sotto 2.</div>'
     :'<div class="sugg"><span>Prossima volta: <b>'+esc(sg.txt)+'</b></span><button onclick="applySugg(\''+sed+'\',\''+en+'\')">Applica</button></div>'):'')
   +'</div>'});
  h+='</div>'}
 h+='<div class="slab">Anche oggi</div><div class="card pad">'
  +'<div style="font-weight:600">Come stanno le anche oggi?</div>'
  +'<div class="mut3" style="margin-bottom:10px">'+(pd&&pd.w&&pd.w.done?"Ieri: seduta "+pd.w.sed+(pd.w.corta?" corta":""):"Ieri: nessuna seduta, vale come linea di base")+'</div><div class="g4">'
  +[0,1,2,3].map(v=>'<button class="'+(d.hip===v?"on":"")+'" onclick="hip('+v+')">'+v+'</button>').join("")
  +'</div><div class="mut3" style="margin-top:8px">0 niente &middot; 1 lo sento ma passa &middot; 2 fastidio tutto il giorno &middot; 3 dolore</div>'
  +(d.hip>=2&&pd&&pd.w&&pd.w.done?'<div class="note w" style="margin-bottom:0">Voto '+d.hip+' dopo la seduta '+pd.w.sed+'. Al 2 dimezzi il range dell\'esercizio sospetto, al 3 lo togli. Se c\'è anche senza allenarti o ti sveglia la notte, chiami l\'ortopedico.</div>':'')
  +(d.hip>=2&&!(pd&&pd.w&&pd.w.done)?'<div class="note w" style="margin-bottom:0">Voto '+d.hip+' senza seduta il giorno prima. Se si ripete, è un segnale da portare all\'ortopedico, non da allenare.</div>':'')
  +'</div>';
 const cw=corteWeek();
 if(cw>2&&!st)h+='<div class="note w">'+cw+' sedute corte in questi sette giorni. La settimana prossima non aumentare niente: resta sui numeri di prima.</div>';
 const tp=progTips();if(tp.length)h+=tp.map(t=>'<div class="note w">'+esc(t)+'</div>').join("");
 $("allen-dyn").innerHTML=h}
function progTips(){const sc=exScore(),o=[];
 Object.keys(sc).forEach(n=>{if(sc[n].run>=2&&sc[n].last===-1)
  o.push(n+": due volte sotto il previsto. Non aumentare niente, e guarda il protocollo in Misure.")});
 return o.slice(0,3)}

/* ---------------- modalità seduta ----------------
   Un piano di passi: w lavoro a tempo, s serie a ripetizioni (la chiudi tu), r recupero, g pausa tra i giri. */
const SS={on:false,plan:[],i:0,end:0,left:0,paused:false,iv:null,lock:null,sed:null,beeped:-1};
function attKey(n){const a=DB.ex[n].att;return a.find(x=>/\bnon\b|\bmai\b|NIENTE|PICCOLO/i.test(x))||a[0]}
function sessPlan(sed,corta){const s=DB.sedute[sed],lst=sedEx(sed,corta),P=[];
 if(sed==="D"){const g=parsePr(lst[0].pr)||{giri:4,secs:40},giri=corta?Math.min(3,g.giri):g.giri;
  for(let r=1;r<=giri;r++)lst.forEach((e,j)=>{const last=j===lst.length-1;
   P.push({k:"w",n:e.n,secs:g.secs,st:j+1,of:lst.length,giro:r,giri:giri});
   if(!(last&&r===giri))P.push(last?{k:"g",secs:60,giro:r,giri:giri}:{k:"r",secs:e.rest,giro:r,giri:giri})});
  return P}
 lst.forEach((e,j)=>{const pf=prFor(sed,e),p=pf.p||{sets:1,a:0},last=j===lst.length-1;
  for(let k=1;k<=p.sets;k++){
   if(p.t){const secs=p.b||p.a;
    if(p.lato){P.push({k:"w",n:e.n,secs:secs,set:k,of:p.sets,ex:j+1,exOf:lst.length,side:"lato destro"});
     P.push({k:"r",secs:5,sw:1,ex:j+1,exOf:lst.length});
     P.push({k:"w",n:e.n,secs:secs,set:k,of:p.sets,ex:j+1,exOf:lst.length,side:"lato sinistro"})}
    else P.push({k:"w",n:e.n,secs:secs,set:k,of:p.sets,ex:j+1,exOf:lst.length})}
   else P.push({k:"s",n:e.n,pr:pf.pr,reps:p.a+(p.b?"-"+p.b:"")+(p.lato?" per lato":""),set:k,of:p.sets,ex:j+1,exOf:lst.length});
   if(!(last&&k===p.sets))P.push({k:"r",secs:e.rest,ex:j+1,exOf:lst.length})}});
 return P}
async function wakeOn(){try{if(navigator.wakeLock)SS.lock=await navigator.wakeLock.request("screen")}catch(e){}}
function wakeOff(){try{if(SS.lock)SS.lock.release()}catch(e){}SS.lock=null}
function sessOpen(){const d=day(cur);if(!d.w.sed)return;
 SS.sed=d.w.sed;SS.plan=sessPlan(d.w.sed,d.w.corta);SS.i=0;SS.paused=false;SS.on=true;timerStop();
 $("sess").classList.add("on");wakeOn();sessStart();}
function sessClose(){SS.on=false;clearInterval(SS.iv);SS.iv=null;wakeOff();$("sess").classList.remove("on");renderAllen()}
function sessStart(){clearInterval(SS.iv);SS.iv=null;SS.beeped=-1;const p=SS.plan[SS.i];
 if(!p){sessRender();return}
 if(p.secs){SS.left=p.secs;SS.end=Date.now()+p.secs*1000;haptic(p.k==="w"?[60,40,60]:30);
  if(!SS.paused)SS.iv=setInterval(sessTick,200)}
 sessRender()}
function sessTick(){const p=SS.plan[SS.i];if(!p||!p.secs||SS.paused)return;
 const r=Math.max(0,Math.ceil((SS.end-Date.now())/1000));
 if(r!==SS.left){SS.left=r;if(r<=3&&r>0&&SS.beeped!==r){SS.beeped=r;haptic(40)}sessRender()}
 if(r<=0){haptic([200,80,200]);SS.i++;sessStart()}}
function sessPause(){const p=SS.plan[SS.i];if(!p||!p.secs)return;
 if(SS.paused){SS.paused=false;SS.end=Date.now()+SS.left*1000;SS.iv=setInterval(sessTick,200)}
 else{SS.paused=true;clearInterval(SS.iv);SS.iv=null}
 sessRender()}
function sessNext(){if(SS.i<SS.plan.length){SS.i++;sessStart()}}
function sessPrev(){if(SS.i>0){SS.i--;sessStart()}}
function sessPlus(){const p=SS.plan[SS.i];if(!p||!p.secs)return;SS.end+=10000;SS.left+=10;sessRender()}
function sessDone(){const d=day(cur);d.w.done=true;d.w.sed=SS.sed;save();haptic();sessClose()}
function nextWork(i){for(let j=i+1;j<SS.plan.length;j++){const q=SS.plan[j];if(q.k==="w"||q.k==="s")return q}return null}
function sessRender(){const P=SS.plan,p=P[SS.i],s=DB.sedute[SS.sed],circ=SS.sed==="D";
 let h='<div class="row"><button class="cb" onclick="sessClose()" aria-label="chiudi la seduta">'+IC.x+'</button>'
  +'<div style="text-align:center;flex:1"><div class="kick">Seduta '+SS.sed+(circ?" &middot; circuito":"")+'</div>'
  +'<div class="ttl">'+(p?(circ?"Giro "+p.giro+" di "+p.giri:"Esercizio "+p.ex+" di "+p.exOf):"Finita")+'</div></div>'
  +'<div style="width:44px"></div></div>';
 if(!p){h+='<div style="margin:auto 0;text-align:center"><div class="sname" style="font-size:34px">Seduta finita</div>'
  +'<div class="ssub" style="margin-top:8px">Domattina il voto alle anche, come sempre.</div></div>'
  +'<button class="sbig" onclick="sessDone()">Segna come fatta</button>'
  +'<button class="sbig" style="background:transparent;color:#f4f1ea;border:1px solid #34313d" onclick="sessClose()">Chiudi senza segnare</button>';
  $("sess").innerHTML=h;return}
 /* barra di avanzamento: stazioni del giro o esercizi della seduta */
 const tot=circ?p.of||sedEx(SS.sed,day(cur).w.corta).length:p.exOf,curx=circ?(p.st||0):p.ex;
 h+='<div class="sprog">';for(let j=1;j<=tot;j++)h+='<i class="'+(j<curx||(p.k==="g"&&circ)?"d":j===curx?"c":"")+'"></i>';h+='</div>';
 if(circ)h+='<div class="slg"><span><i style="background:#3cb894"></i>lavoro '+(P.find(x=>x.k==="w")||{}).secs+' s</span><span><i style="background:#a89ff0"></i>pausa</span><span><i style="background:#e0a04a"></i>tra i giri 60 s</span></div>';
 const lab={w:"Lavoro",r:p.sw?"Cambia lato":(circ?"Pausa":"Recupero"),g:"Tra i giri",s:"Serie"}[p.k],cl={w:"ph-w",r:"ph-r",g:"ph-g",s:"ph-s"}[p.k];
 h+='<div class="phase '+cl+'">'+lab+(SS.paused?" &middot; in pausa":"")+'</div>';
 if(p.secs){const c=2*Math.PI*112,f=Math.max(0,SS.left/p.secs),col={w:"#3cb894",r:"#a89ff0",g:"#e0a04a"}[p.k];
  h+='<div class="tring"><svg viewBox="0 0 250 250"><circle cx="125" cy="125" r="112" fill="none" stroke="#2a2832" stroke-width="12"/>'
   +'<circle cx="125" cy="125" r="112" fill="none" stroke="'+col+'" stroke-width="12" stroke-linecap="round" stroke-dasharray="'+(c*f).toFixed(1)+' '+c.toFixed(1)+'" transform="rotate(-90 125 125)"/></svg>'
   +'<div><b>'+fmtT(SS.left)+'</b><span>di '+p.secs+' secondi</span></div></div>'}
 else h+='<div class="sreps">'+esc(p.reps)+'</div><div class="ssub">ripetizioni</div>';
 const show=(p.k==="w"||p.k==="s")?p:nextWork(SS.i);
 if(show){const sub=p.k==="w"||p.k==="s"?(circ?"Stazione "+show.st+" di "+show.of:"Serie "+show.set+" di "+show.of+(show.side?" &middot; "+show.side:"")):"Dopo: "+(circ?"stazione "+show.st:"serie "+show.set+" di "+show.of);
  h+='<div class="sname" style="margin-top:'+(p.secs?"4px":"18px")+'">'+esc(show.n)+'</div><div class="ssub">'+sub+'</div>';
  if(p.k==="s"){h+='<div class="sser">';for(let j=1;j<=p.of;j++)h+='<i class="'+(j<p.set?"d":j===p.set?"c":"")+'"></i>';h+='</div>'}
  h+='<div class="satt">'+IC.warn+'<span>'+attKey(show.n)+'</span></div>'}
 if(p.k==="w"||p.k==="s"){const q=P[SS.i+1],nw=nextWork(SS.i);
  if(q)h+='<div class="snext"><div><div>Poi &middot; '+(q.k==="r"?(q.sw?"cambio lato 5 s":(circ?"pausa ":"recupero ")+q.secs+" s"):q.k==="g"?"pausa tra i giri 60 s":"subito")+'</div><div>'+(nw?esc(nw.n)+(circ?"":" &middot; serie "+nw.set+(nw.side?", "+nw.side:"")):"fine seduta")+'</div></div></div>'}
 if(p.k==="s")h+='<button class="sbig" onclick="sessNext()">Serie fatta</button>';
 h+='<div class="sctl"><button onclick="sessPrev()" aria-label="indietro">'+IC.back+'</button>'
  +(p.secs?'<button class="main" onclick="sessPause()" aria-label="'+(SS.paused?"riprendi":"pausa")+'">'+(SS.paused?IC.play:IC.pause)+'</button>'
   :'<button class="main" style="opacity:.25" disabled aria-label="pausa">'+IC.pause+'</button>')
  +'<button onclick="sessNext()" aria-label="avanti">'+IC.fwd+'</button></div>'
  +(p.secs?'<div style="text-align:center;margin-top:10px"><button class="tbtn" style="background:transparent;color:#a9a3b4;border-color:#34313d" onclick="sessPlus()">+10 s</button></div>':'');
 $("sess").innerHTML=h}
document.addEventListener("visibilitychange",()=>{if(SS.on&&document.visibilityState==="visible"){wakeOn();sessTick()}});

/* ---------------- scorciatoie dall'icona ---------------- */
function scorciatoia(){let a=null;try{a=new URLSearchParams(location.search).get("a")}catch(e){}
 if(!a)return;try{history.replaceState(null,"",location.pathname)}catch(e){}
 cur=today();
 if(a==="peso"){setTab("mis");setTimeout(()=>{const x=document.querySelector("#mis-dyn input");if(x){x.focus();x.scrollIntoView({block:"center"})}},150)}
 else if(a==="allen")setTab("allen");
 else if(a==="pasto"){setTab("oggi");const h=new Date().getHours();
  const m=h<11?"colazione":h<15?"pranzo":h<18?"spuntino":"cena";pick(mealsFor(cur).indexOf(m)>=0?m:"cena")}}
"""


HTML = """<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#f4f1ea" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#141318" media="(prefers-color-scheme: dark)">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<title>%(nome)s</title>
<link rel="manifest" href="manifest.json">
<link rel="icon" href="icon-192.png">
<link rel="apple-touch-icon" href="icon-192.png">
<style>%(fonts)s%(css)s</style>
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
 <details class="card pad" style="margin-top:16px"><summary>Le quattro sedute</summary>
  %(sedute)s
 </details>
 <details class="card pad"><summary>Appendice: i 23 esercizi</summary>
  <div class="mut3" style="margin:6px 0 4px">Ogni esercizio: attenzione, come si fa, prima, durante, errori comuni, perché lo fai, se fa male. Dalla seduta si apre toccando il nome.</div>
  %(appendice)s
 </details>
</section>

<section id="t-mis" style="display:none"><div id="mis-dyn"></div></section>
<section id="t-graf" style="display:none"><div id="graf-dyn"></div></section>

</div>

<div class="undo" id="undo"><span id="utxt">Voce eliminata</span><button onclick="undo()">Annulla</button></div>
<div class="tbar" id="tbar"><span>Recupero</span><b id="tval">0:00</b><span><button onclick="timerPlus()">+30 s</button> <button onclick="timerStop()">Stop</button></span></div>

<nav>
 <button id="n-oggi" onclick="setTab('oggi')"><span>%(iOggi)s</span>Oggi</button>
 <button id="n-piano" onclick="setTab('piano')"><span>%(iPiano)s</span>Piano</button>
 <button id="n-allen" onclick="setTab('allen')"><span>%(iAllen)s</span>Allenamento</button>
 <button id="n-mis" onclick="setTab('mis')"><span>%(iMis)s</span>Misure</button>
 <button id="n-graf" onclick="setTab('graf')"><span>%(iGraf)s</span>Grafici</button>
</nav>

<div class="sheet" id="sheet">
 <div class="sheeth"><button class="btn" id="sclose" onclick="closePick()">Chiudi</button>
  <b id="stitle" style="white-space:nowrap">Pasto</b>
  <input id="sq" placeholder="Cerca (anche con errori di battitura)" oninput="pSearch(this.value)" autocomplete="off"></div>
 <div class="sheetb" id="sbody"></div>
</div>

<div class="sess" id="sess"></div>

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

SW = """const V="ricomp-v%(ver)s";
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
    "shortcuts": [
        {"name": "Peso di stamattina", "short_name": "Peso", "url": "./index.html?a=peso",
         "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}]},
        {"name": "Aggiungi pasto", "short_name": "Pasto", "url": "./index.html?a=pasto",
         "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}]},
        {"name": "Allenamento di oggi", "short_name": "Allenamento", "url": "./index.html?a=allen",
         "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"}]},
    ],
    "icons": [
        {"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
        {"src": "icon-512.png", "sizes": "512x512", "type": "image/png"},
        {"src": "icon-maskable-512.png", "sizes": "512x512", "type": "image/png",
         "purpose": "maskable"},
    ],
}


def font_css():
    out = []
    for fam, key, w in [("Fraunces", "fraunces-600", 600), ("Figtree", "figtree-400", 400),
                        ("Figtree", "figtree-600", 600), ("Figtree", "figtree-700", 700)]:
        out.append('@font-face{font-family:"%s";font-style:normal;font-weight:%d;font-display:swap;'
                   'src:url(data:font/woff2;base64,%s) format("woff2")}' % (fam, w, FONTS[key]))
    return "\n".join(out) + "\n"


def main():
    db = build_db()
    js = JS1 + JS2 + JS3 + JS4 + JS5 + JS7 + JS6
    html = HTML % {
        "nome": NOME, "css": CSS, "fonts": font_css(),
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
    print("index.html: %d KB, %d alimenti, %d opzioni, %d piatti, %d esercizi, versione %s"
          % (len(html.encode("utf-8")) // 1024, len(db["foods"]), n_opt,
             len(db["piatti"]), len(db["ex"]), VERSIONE))


if __name__ == "__main__":
    main()
