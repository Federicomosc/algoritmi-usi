#!/usr/bin/env python3
"""Generate final/ exam study pages from finals_extract.json"""
import html
import json
import os

with open("/tmp/finals_extract.json") as f:
    all_ex = {e["num"]: e for e in json.load(f)}

categories = [
    {
        "id": "01-analisi-algoritmi",
        "folder": "01 - Analisi e miglioramento algoritmi",
        "title": "Analisi e miglioramento algoritmi",
        "subtitle": "Domanda tipo: «cosa fa Algo-X?» + scrivi Better-Algo-X più efficiente",
        "accent": "#c678dd",
        "items": [
            {"num": 257, "years": ["2021"], "strategy": [
                "**Cosa fa Algo-X:** ordina l'array per resto modulo 4 (bucket sort a inserimento). Complessità Θ(n²).",
                "**Better-Algo-X:** two pointers i/j; per ogni resto m mod 4, sposta elementi con scambi. O(n).",
                "**Pattern esame:** riconoscere semantica ad alto livello, poi partition O(n) se dominio piccolo.",
            ]},
            {"num": 273, "years": ["2022"], "strategy": [
                "**Cosa fa Algo-X:** verifica se A e B sono multiset uguali. Worst case Θ(n²).",
                "**Better-Algo-X:** ordina copie → confronta elemento per elemento. O(n log n).",
                "**Pattern:** confronto multiset → sort + scan.",
            ]},
            {"num": 276, "years": ["2022 B", "2022 C"], "dup": True, "strategy": [
                "**Cosa fa Algo-X:** max lunghezza sottosequenza contigua di A con somma in B. Θ(n⁴).",
                "**Better-Algo-X:** sliding sum — aggiorna somma in O(1) spostando finestra.",
                "**Pattern:** somme su sottosequenze contigue → prefix/sliding sum.",
            ]},
            {"num": 277, "years": ["2022 B", "2022 C"], "dup": True, "strategy": [
                "**Cosa fa Algo-Y:** stampa valori con frequenza massima. Θ(n²).",
                "**Better-Algo-Y:** sort + due scan lineari per max run. Θ(n log n).",
            ]},
            {"num": 293, "years": ["2023"], "strategy": [
                "**Cosa fa Algo-X:** multiset uguale su stringhe. Θ(n·m).",
                "**Better O(n log n):** sort + merge-like compare.",
                "**Bonus O(n):** counting array su alfabeto piccolo (ASCII m≤127).",
            ]},
            {"num": 304, "years": ["2024"], "strategy": [
                "**Cosa fa Algo-X:** max segmento dove B[j+c]=(A[i+c])². O(n²m).",
                "**DP:** DP[i,j]=1+DP[i-1,j-1] se A[i]²=B[j], else 0. O(nm).",
            ]},
            {"num": 306, "years": ["2024"], "strategy": [
                "**Cosa fa Algo-Y:** conta coppie con somma s. O(n²).",
                "**Better:** sort + two pointers. Bonus: gestire duplicati con combinatoria.",
            ]},
            {"num": 317, "years": ["2025"], "strategy": [
                "**Cosa fa Algo-X:** trova la lunghezza massima di una sottosequenza contigua con **esattamente k numeri pari**. Algo naïvo O(n²).",
                "**Linear-Algo-X:** sliding window [i,j): mantieni contatore e = pari nella finestra. Se e<k espandi j; se e>k restringi i; se e=k aggiorna max lunghezza. i,j solo aumentano → O(n).",
                "**Pattern esame:** «sottosequenza contigua con k elementi che soddisfano proprietà X» → sliding window + contatore.",
            ]},
        ],
    },
    {
        "folder": "02 - BST e alberi binari",
        "title": "BST e alberi binari",
        "subtitle": "Conteggio in range, rotazioni, campo size",
        "accent": "#98c379",
        "items": [
            {"num": 270, "years": ["2022"], "strategy": [
                "**BST-Count-In-Range:** poda ramo sinistro se key>b, destro se key<a; conta entrambi se in range.",
                "Worst Θ(n), best O(1) se range fuori dal sottoalbero.",
            ]},
            {"num": 274, "years": ["2022 B", "2022 C"], "dup": True, "strategy": [
                "**Outside [a,b]:** count(−∞,a)+count(b,+∞). Best O(1) se tutto in range.",
            ]},
            {"num": 305, "years": ["2024"], "strategy": [
                "**Rotate-Right:** rotazione + aggiorna size.",
                "**Count-In-Range O(h):** t.size − lessThan(a) − greaterThan(b) con walk O(h).",
            ]},
        ],
    },
    {
        "folder": "03 - Grafi BFS e connettivita",
        "title": "Grafi, BFS e connettività",
        "subtitle": "Componenti, raggio, reachability",
        "accent": "#61afef",
        "items": [
            {"num": 258, "years": ["2021"], "strategy": [
                "**Q1 (P):** conta grado di ogni persona, verifica ≥ℓ, conta quante ≥k.",
                "**Q2 (NP):** insieme indipendente size k — certificato S, verifica O(k²).",
            ]},
            {"num": 271, "years": ["2022"], "strategy": [
                "**Check-Connectivity:** grafo distanza≤r, BFS da base. O(n²).",
                "**Minimal-Range:** binary search su r monotono. O(n² log(r/t)).",
            ]},
            {"num": 275, "years": ["2022 B", "2022 C"], "dup": True, "strategy": [
                "**Diametro > d:** BFS da ogni u, se dist(a,b)>d → true. In P.",
            ]},
            {"num": 294, "years": ["2023"], "strategy": [
                "**Archi minimi:** c componenti → servono c−1 archi. BFS ripetuto.",
            ]},
            {"num": 303, "years": ["2024"], "strategy": [
                "**Interdependenza k:** BFS su grafo chiamate + grafo inverso per ogni f.",
            ]},
        ],
    },
    {
        "folder": "04 - Programmazione dinamica",
        "title": "Programmazione dinamica",
        "subtitle": "Giochi, coppie, sottosequenze speculari",
        "accent": "#e5953a",
        "items": [
            {"num": 259, "years": ["2021"], "strategy": [
                "**Algo-Y:** k coppie con A[j]²=A[i]. O(n²).",
                "**Better:** sort + two pointers (negativi a sinistra, positivi a destra).",
            ]},
            {"num": 260, "years": ["2021"], "strategy": [
                "**Mirror sequence:** sottosequenza contigua di A = reverse in B. DP O(n²).",
                "Esempio: 4,5,7 in A ↔ 7,5,4 in B → lunghezza 3.",
            ]},
            {"num": 272, "years": ["2022"], "strategy": [
                "**k coppie stessa somma:** genera tutte somme, sort, conta run ≥k. In P.",
            ]},
            {"num": 292, "years": ["2023"], "strategy": [
                "**Gioco carte:** DP(i,j) costo minimo + memo. In NP con certificato mosse.",
            ]},
        ],
    },
    {
        "folder": "05 - Heap",
        "title": "Heap",
        "subtitle": "Delete, extract, heapify",
        "accent": "#e8c547",
        "items": [
            {"num": 315, "years": ["2025"], "strategy": [
                "**Max-Heap-Delete(i):** H[i]←ultimo; heap-size−−; bubble up o max-heapify down. O(log n).",
                "Stessa idea di Extract-Max ma da posizione i.",
            ]},
        ],
    },
    {
        "folder": "06 - Array ordinati e two pointers",
        "title": "Array ordinati e two pointers",
        "subtitle": "Riordinare in O(n), ricostruzione",
        "accent": "#4ec9a8",
        "items": [
            {"num": 291, "years": ["2023"], "strategy": [
                "**Re-Sort:** negativi a sinistra, positivi a destra, zeri in mezzo. O(n) in-place.",
            ]},
        ],
    },
    {
        "folder": "07 - Stringhe e sequenze",
        "title": "Stringhe, sequenze e DNA",
        "subtitle": "Bilanciamento nucleotidi",
        "accent": "#61afef",
        "items": [
            {"num": 318, "years": ["2025"], "strategy": [
                "**Bilanciato:** stesso numero di due nucleotidi diversi (es. 2 A e 2 G). Vuoto = bilanciato.",
                "**Idea chiave:** per coppia (N1,N2), x(i) = bilancio A−C fino a posizione i (+1 per N1, −1 per N2). Sottosequenza [i,j] bilanciata su N1/N2 ⟺ x(i)=x(j).",
                "**Linear:** per ogni coppia tra 6 possibili, array First/Last per ogni valore x∈[−n,n]; max(Last[x]−First[x]). Totale O(n).",
                "**Pattern esame:** «sottosequenza contigua bilanciata» → prefix balance + hash/array su valori ripetuti.",
            ]},
        ],
    },
    {
        "folder": "08 - Problemi decisionali P e NP",
        "title": "Problemi decisionali (P e NP)",
        "subtitle": "Certificati, verificatori, algoritmi polinomiali",
        "accent": "#e06c75",
        "items": [
            {"num": 316, "years": ["2025"], "strategy": [
                "**Problema:** dato spazio x, esiste installazione funzionante di ≥1 sistema? Ogni Si ha Size(i) e Deps(i).",
                "**In NP:** certificato = insieme S di sistemi installati; Verify-Size controlla chiusura dipendenze + somma size ≤ x.",
                "**In P:** prova ogni u=1..n con Verify-Size(n,x,u) — al più n verifiche polinomiali.",
                "**Pattern esame:** dipendenze = grafo diretto; «funzionante» = chiusura transitiva delle dipendenze.",
            ]},
        ],
    },
]

STYLE = """
:root {
  --bg:#0e0e12;--bg2:#14141a;--bg3:#1c1c24;--bg4:#24242e;--border:#2e2e3e;
  --text:#d4d0c8;--text-dim:#7a7890;--text-bright:#f0ece0;
  --gold:#e8c547;--teal:#4ec9a8;--red:#e06c75;--blue:#61afef;
  --purple:#c678dd;--orange:#e5953a;--green:#98c379;--sidebar-w:260px;
  --accent:__ACCENT__;
}
html[data-theme="light"]{
  --bg:#f4f1ea;--bg2:#ebe6dc;--bg3:#fff;--bg4:#f0ece4;--border:#d4cfc4;
  --text:#3a3848;--text-dim:#6a6878;--text-bright:#1a1828;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;font-size:15px;line-height:1.7}
#sidebar{position:fixed;top:0;left:0;width:var(--sidebar-w);height:100vh;background:var(--bg2);border-right:1px solid var(--border);overflow-y:auto;z-index:100;padding-bottom:40px}
.sidebar-header{padding:24px 20px 16px;border-bottom:1px solid var(--border)}
.sidebar-header .title{color:var(--accent);font-family:'Lora',serif;font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.sidebar-header .sub{color:var(--text-dim);font-size:11px;margin-top:3px}
.nav-link{display:block;padding:5px 20px;color:var(--text-dim);text-decoration:none;font-size:13px;border-left:2px solid transparent}
.nav-link:hover{color:var(--text-bright);background:var(--bg3);border-left-color:var(--accent)}
#main{margin-left:var(--sidebar-w);max-width:880px;padding:48px 48px 80px}
.hero{background:linear-gradient(135deg,#1a1814,#12121c);border:1px solid var(--border);border-radius:12px;padding:36px 40px;margin-bottom:40px}
.hero h1{font-family:'Lora',serif;font-size:26px;color:var(--text-bright)}
.hero h1 span{color:var(--accent)}
.hero p{color:var(--text-dim);font-size:14px;margin-top:10px}
.hero-sub{font-size:13px;color:var(--teal);margin-top:8px;font-style:italic}
.ex-card{background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:24px;margin-bottom:28px;border-left:3px solid var(--accent)}
.ex-header{display:flex;gap:10px;align-items:center;margin-bottom:10px;flex-wrap:wrap}
.ex-badge{font-family:'JetBrains Mono',monospace;font-size:11px;font-weight:700;background:rgba(255,255,255,.06);padding:3px 10px;border-radius:4px;color:var(--accent)}
.ex-years{font-size:12px;color:var(--text-dim)}
.ex-card h3{font-size:15px;color:var(--text-bright);margin-bottom:12px;line-height:1.4}
.note-dup{font-size:12px;color:var(--orange);margin-bottom:10px}
.box{border-radius:8px;padding:16px 18px;margin:14px 0;border-left:3px solid}
.box-strat{background:rgba(78,201,168,.07);border-color:var(--teal)}
.box-label{font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--teal);margin-bottom:8px}
.strat-list{padding-left:18px}.strat-list li{margin-bottom:8px;font-size:14px}
details{background:var(--bg4);border:1px solid var(--border);border-radius:8px;margin:10px 0}
details summary{padding:12px 16px;cursor:pointer;font-weight:600;color:var(--text-bright);font-size:13px}
.detail-body{padding:0 16px 16px;border-top:1px solid var(--border)}
.code-block{background:var(--bg2);border-radius:6px;padding:14px;font-family:'JetBrains Mono',monospace;font-size:11px;line-height:1.55;overflow-x:auto;white-space:pre-wrap;word-break:break-word}
.code-block.sol{border-left:3px solid var(--accent)}
.theme-toggle{position:fixed;top:14px;right:14px;z-index:200;width:42px;height:42px;border-radius:50%;border:1px solid var(--border);background:var(--bg3);color:var(--accent);font-size:18px;cursor:pointer}
.back-link{display:inline-block;margin-bottom:24px;color:var(--accent);text-decoration:none;font-size:13px;font-weight:600}
@media(max-width:768px){#main{margin-left:0;padding:24px}}
"""

SCRIPT = """
const tb=document.getElementById('themeToggle');
const s=localStorage.getItem('algo-theme')||'dark';
document.documentElement.setAttribute('data-theme',s);
tb.textContent=s==='light'?'🌙':'☀';
tb.onclick=()=>{const n=document.documentElement.getAttribute('data-theme')==='light'?'dark':'light';document.documentElement.setAttribute('data-theme',n);localStorage.setItem('algo-theme',n);tb.textContent=n==='light'?'🌙':'☀';};
"""

BASE = "/Users/federico/Desktop/algoritmi final/final"


def render_exercise(item):
    ex = all_ex[item["num"]]
    years = ", ".join("Final " + y for y in item["years"])
    dup = '<p class="note-dup"><em>Stessa domanda in più sessioni d\'esame.</em></p>' if item.get("dup") else ""
    strat = "".join("<li>" + s + "</li>" for s in item["strategy"])
    prob = html.escape(ex["problem"][:2800])
    sol = html.escape(ex["solution"][:4000])
    title = html.escape(ex["title"][:140])
    return f"""
<article class="ex-card" id="ex-{ex['num']}">
  <div class="ex-header">
    <span class="ex-badge">Ex. {ex['num']}</span>
    <span class="ex-years">{years}</span>
  </div>
  <h3>{title}</h3>
  {dup}
  <div class="box box-strat">
    <div class="box-label">Come ragionare — passo per passo</div>
    <ol class="strat-list">{strat}</ol>
  </div>
  <details>
    <summary>Testo completo dell'esercizio (PDF)</summary>
    <div class="detail-body"><pre class="code-block">{prob}</pre></div>
  </details>
  <details>
    <summary>Soluzione ufficiale (PDF Carzaniga)</summary>
    <div class="detail-body"><pre class="code-block sol">{sol}</pre></div>
  </details>
</article>"""


nav_links = []
for cat in categories:
    folder = os.path.join(BASE, cat["folder"])
    os.makedirs(folder, exist_ok=True)
    nav_inner = "".join(
        f'<a class="nav-link" href="#ex-{it["num"]}">Ex. {it["num"]}</a>' for it in cat["items"]
    )
    cards = "".join(render_exercise(it) for it in cat["items"])
    css = STYLE.replace("__ACCENT__", cat["accent"])
    page = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(cat['title'])} — Final USI</title>
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;700&family=JetBrains+Mono&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>{css}</style>
</head>
<body>
<button class="theme-toggle" id="themeToggle">☀</button>
<nav id="sidebar">
  <div class="sidebar-header">
    <div class="title">Final · {html.escape(cat['title'][:22])}</div>
    <div class="sub">2021 – 2025</div>
  </div>
  <a class="nav-link" href="../index.html">← Indice Final</a>
  <a class="nav-link" href="../../index.html">← Indice corso</a>
  {nav_inner}
</nav>
<main id="main">
<a class="back-link" href="../index.html">← Torna all'indice Final</a>
<div class="hero">
  <h1><span>{html.escape(cat['title'])}</span></h1>
  <p>{html.escape(cat['subtitle'])}</p>
  <p class="hero-sub">Esercizi tratti dagli esami finali 2021–2025 (exercises-2.pdf, Carzaniga USI)</p>
</div>
{cards}
</main>
<script>{SCRIPT}</script>
</body>
</html>"""
    with open(os.path.join(folder, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    nav_links.append(cat)
    print("OK", cat["folder"])

# Final index
cards_html = ""
for cat in nav_links:
    n = len(cat["items"])
    cards_html += f"""
<a class="cat-card" style="--ca:{cat['accent']}" href="{html.escape(cat['folder'])}/index.html">
  <div class="cat-title">{html.escape(cat['title'])}</div>
  <div class="cat-sub">{html.escape(cat['subtitle'])}</div>
  <div class="cat-n">{n} esercizi · Final 2021–2025</div>
  <span class="cat-arrow">→</span>
</a>"""

sidebar_cats = "".join(
    f'<a href="{html.escape(c["folder"])}/index.html">{html.escape(c["title"])}</a>' for c in nav_links
)

final_index = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Esami Finali 2021–2025 — Algoritmi USI</title>
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@400;700&family=Inter:wght@400;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#0e0e12;--bg2:#14141a;--bg3:#1c1c24;--border:#2e2e3e;--text:#d4d0c8;--text-dim:#7a7890;--text-bright:#f0ece0;--gold:#e8c547;--red:#e06c75;--sidebar-w:260px}}
html[data-theme="light"]{{--bg:#f4f1ea;--bg2:#ebe6dc;--bg3:#fff;--border:#d4cfc4;--text:#3a3848;--text-dim:#6a6878;--text-bright:#1a1828}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--text);font-family:'Inter',sans-serif;font-size:15px;line-height:1.7}}
#sidebar{{position:fixed;top:0;left:0;width:var(--sidebar-w);height:100vh;background:var(--bg2);border-right:1px solid var(--border);padding:24px 20px;overflow-y:auto}}
#sidebar a{{display:block;color:var(--text-dim);text-decoration:none;font-size:13px;padding:6px 0}}
#sidebar a:hover{{color:var(--gold)}}
#main{{margin-left:var(--sidebar-w);max-width:960px;padding:48px 56px 80px}}
.hero{{background:linear-gradient(135deg,#1a1410,#12121c);border:1px solid var(--border);border-radius:12px;padding:40px;margin-bottom:40px}}
.hero h1{{font-family:'Lora',serif;font-size:28px;color:var(--text-bright)}}
.hero h1 span{{color:var(--red)}}
.hero p{{color:var(--text-dim);font-size:14px;margin-top:10px;max-width:640px}}
.box-tip{{background:rgba(224,108,117,.08);border:1px solid var(--red);border-radius:8px;padding:16px 20px;margin-bottom:32px;font-size:14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}}
.cat-card{{display:block;text-decoration:none;color:inherit;background:var(--bg3);border:1px solid var(--border);border-radius:10px;padding:22px;position:relative;transition:all .18s;border-left:3px solid var(--ca)}}
.cat-card:hover{{transform:translateY(-2px);border-color:var(--ca);box-shadow:0 8px 24px rgba(0,0,0,.25)}}
.cat-title{{font-weight:700;color:var(--text-bright);font-size:15px;margin-bottom:6px}}
.cat-sub{{font-size:12px;color:var(--text-dim);line-height:1.5;margin-bottom:12px}}
.cat-n{{font-size:11px;color:var(--ca);font-weight:600}}
.cat-arrow{{position:absolute;top:20px;right:16px;color:var(--text-dim)}}
.theme-toggle{{position:fixed;top:14px;right:14px;z-index:200;width:42px;height:42px;border-radius:50%;border:1px solid var(--border);background:var(--bg3);color:var(--red);font-size:18px;cursor:pointer}}
@media(max-width:768px){{#sidebar{{display:none}}#main{{margin-left:0;padding:24px}}}}
</style>
</head>
<body>
<button class="theme-toggle" id="themeToggle">☀</button>
<nav id="sidebar">
  <strong style="color:var(--red);font-size:12px;letter-spacing:.08em">FINAL 2021–2025</strong>
  <p style="font-size:11px;color:var(--text-dim);margin:8px 0 16px">Per tipo di domanda</p>
  <a href="../index.html">← Indice corso</a>
  {sidebar_cats}
</nav>
<main id="main">
<div class="hero">
  <h1><span>Esami Finali</span><br>2021 – 2025</h1>
  <p>Tutti gli esercizi dei finali degli ultimi 5 anni, raggruppati per <strong>tipo di domanda</strong>. Ogni scheda spiega il ragionamento per risolvere l'esercizio, con testo originale e soluzione dal PDF Carzaniga.</p>
</div>
<div class="box-tip">
  <strong>Come studiare:</strong> identifica il pattern (Algo-X, BST range, BFS, DP, P/NP…), leggi «Come ragionare», poi prova senza guardare la soluzione. Fonte: <code>exercises-2.pdf</code> ed. 3.14 (marzo 2026).
</div>
<div class="grid">{cards_html}</div>
</main>
<script>{SCRIPT}</script>
</body>
</html>"""

with open(os.path.join(BASE, "index.html"), "w", encoding="utf-8") as f:
    f.write(final_index)
print("OK final/index.html")
