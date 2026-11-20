# Ajoute à questions.json, pour chaque question adossée à un scrutin, la répartition des votes de chaque groupe
# (votes_groupes.json, relevé sur datan.fr). Champ écrit : q["split"][parti] = [avec sa position, contre, abstention].
# Usage : python3 add_cohesion.py   (puis python3 build.py)
import json, os
here = os.path.dirname(os.path.abspath(__file__))
QP = os.path.join(here, 'questions.json')
d = json.load(open(QP)); V = json.load(open(os.path.join(here, 'votes_groupes.json')))
GROUPES = {'RE':'REN','EPR':'REN','RN':'RN','LFI-NUPES':'LFI','LFI-NFP':'LFI','LR':'LR','DR':'LR','DEM':'MODEM',
           'SOC':'PS','SOC-A':'PS','HOR':'HOR','ECOLO':'ECO','ECOS':'ECO','LIOT':'LIOT','GDR':'PCF','GDR-NUPES':'PCF','UDR':'UDR'}
done = 0
for q in d['questions']:
    q.pop('split', None)
    if q['id'] not in V or len(q['options']) != 2: continue
    v = {GROUPES[g]: c for g, c in V[q['id']].items()}
    # quelle option correspond au « pour » ? on la déduit des groupes majoritairement pour ou contre
    pour_opt = set()
    for p, pos in q['positions'].items():
        c = v.get(p)
        if not c or sum(c) == 0 or c[2] >= max(c[0], c[1]): continue
        pour_opt.add(pos if c[0] > c[1] else 1 - pos)
    if len(pour_opt) != 1:
        print('incohérent, ignoré :', q['id'], pour_opt); continue
    po = pour_opt.pop(); split = {}
    for p, pos in q['positions'].items():
        c = v.get(p)
        if not c or sum(c) == 0: continue
        w, a = (c[0], c[1]) if pos == po else (c[1], c[0])
        if w < a or c[2] > w: continue   # position fixée autrement que par ce vote : on ne touche pas
        split[p] = [w, a, c[2]]
    q['split'] = split; done += 1
json.dump(d, open(QP, 'w'), ensure_ascii=False, indent=1)
print('cohésion ajoutée sur', done, 'questions')
