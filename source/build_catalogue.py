# Génère catalogue-questions.html : toutes les questions de questions.json, lisibles d'un coup, regroupées par thème.
# Usage : python3 build_catalogue.py   (appelé aussi automatiquement à la fin de build.py)
import json, html, os
here = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(here, 'questions.json')))
e = lambda s: html.escape(str(s))
parties = d['parties']
pname = {p['id']: p['name'] for p in parties}
REL = {1: 'faible', 2: 'moyenne', 3: 'bonne'}

by_theme = {}
for q in d['questions']:
    by_theme.setdefault(q['theme'], []).append(q)
order = [t for t in d['themes'] if t in by_theme] + [t for t in by_theme if t not in d['themes']]

def question_html(n, q):
    opts = q['options']
    rows = []
    for i, o in enumerate(opts):
        sp = q.get('split', {})
        def lab(p):
            c = sp.get(p); n = pname.get(p, p)
            if c and (c[0]-c[1])/sum(c) < 0.9: n += f" ({round(100*c[0]/sum(c))} % du groupe : {c[0]} dans ce sens, {c[1]} en sens inverse, {c[2]} abst.)"
            return n
        who = [lab(p) for p in pname if q['positions'].get(p) == i]
        who += [p for p, v in q['positions'].items() if v == i and p not in pname]
        rows.append(f'<tr><td class="opt"><b>{chr(65+i)}.</b> {e(o)}</td><td>{e(", ".join(who)) or "<span class=muted>aucun parti</span>"}</td></tr>')
    unknown = [pname[p] for p in pname if p not in q['positions']]
    if unknown:
        rows.append(f'<tr class="muted"><td class="opt">Position non établie</td><td>{e(", ".join(unknown))}</td></tr>')
    r = q.get('reliability', 0)
    src = ' · '.join(f'<a href="{e(s["url"])}" target="_blank" rel="noopener">{e(s["name"])}</a>' for s in q.get('sources', []))
    ordered = '<p class="note">Options graduées (de l’une à l’autre extrémité).</p>' if q.get('ordered') else ''
    nuance = f'<p><b>Nuance :</b> {e(q["nuance"])}</p>' if q.get('nuance') else ''
    ctx = f'<details open><summary>Contexte (i)</summary><p>{e(q["contexte"])}</p></details>' if q.get('contexte') else ''
    return f'''<article id="{e(q["id"])}">
  <h3><span class="num">{n}</span> {e(q["question"])}</h3>
  <p class="meta">{e(q.get("date",""))} · réf. <code>{e(q["id"])}</code> · fiabilité <span class="dots">{"●"*r}{"○"*(3-r)}</span> {REL.get(r,"?")}</p>
  <p class="situation">{e(q["situation"])}</p>
  {ordered}<table><thead><tr><th>Réponse</th><th>Partis</th></tr></thead><tbody>{"".join(rows)}</tbody></table>
  <p><b>Source du placement :</b> {e(q.get("actor",""))}</p>{nuance}{'<p class="note">Cohésion des groupes relevée sur datan.fr. Un groupe divisé pèse moins dans le calcul.</p>' if q.get('split') else ''}
  <p class="src">{src}</p>{ctx}
</article>'''

body, toc, n = [], [], 0
for t in order:
    label = d['themes'].get(t, t)
    toc.append(f'<li><a href="#t-{e(t)}">{e(label)}</a> ({len(by_theme[t])})</li>')
    arts = []
    for q in by_theme[t]:
        n += 1
        arts.append(question_html(n, q))
    body.append(f'<section id="t-{e(t)}"><h2>{e(label)}</h2>{"".join(arts)}</section>')

page = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Catalogue des questions</title><style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--muted:#6b6a65;--line:#e2dfd8;--card:#fff;--accent:#2f5d8a}}
@media (prefers-color-scheme:dark){{:root{{--bg:#161615;--fg:#ecebe6;--muted:#9a988f;--line:#33322f;--card:#1f1f1d;--accent:#8cb8e6}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.55 ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif}}
main{{max-width:860px;margin:0 auto;padding:24px 16px 80px}}
h1{{margin:0 0 4px}} h2{{margin:48px 0 12px;padding-bottom:6px;border-bottom:2px solid var(--fg)}}
h3{{margin:0 0 4px;font-size:1.1em}} .num{{color:var(--muted);font-weight:400;margin-right:4px}}
article{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin:14px 0}}
.meta,.muted,.note,.src{{color:var(--muted);font-size:.9em}} .situation{{font-style:italic}}
table{{width:100%;border-collapse:collapse;margin:10px 0;font-size:.95em}} th,td{{text-align:left;vertical-align:top;padding:6px 8px;border-top:1px solid var(--line)}}
th{{font-size:.8em;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}} td.opt{{width:45%}}
a{{color:var(--accent)}} .dots{{letter-spacing:1px}} details summary{{cursor:pointer;color:var(--accent)}}
.toc{{columns:2;padding-left:18px}} @media (max-width:560px){{.toc{{columns:1}} td.opt{{width:auto}}}}
@media print{{details{{display:block}} details>*{{display:block}} article{{break-inside:avoid}}}}
</style></head><body><main>
<h1>Catalogue des questions</h1>
<p class="meta">Banque du {e(d.get("version",""))} · {n} questions · {len(parties)} partis. Généré depuis <code>questions.json</code>.</p>
<p class="meta">Fiabilité : à quel point le placement des partis est solide (●●● vote nominatif à l’Assemblée groupe par groupe, ●●○ position publique ou vote partiel rapporté par la presse, ●○○ cas municipal). « Position non établie » : parti absent du vote ou sans position connue, non compté dans le calcul.</p>
<ul class="toc">{"".join(toc)}</ul>
{"".join(body)}
</main></body></html>
'''
out = os.path.join(here, 'catalogue-questions.html')
open(out, 'w').write(page)
print('catalogue ok', n, 'questions ->', out)
