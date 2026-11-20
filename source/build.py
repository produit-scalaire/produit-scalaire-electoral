# Assemble the single offline page from template.html + questions.json + disclaimer.md + animation-axes.html.
import json,re,html,os
ROOT='/mnt/project-files/comparateur/'
here=os.path.dirname(os.path.abspath(__file__))
t=open(os.path.join(here,'template.html')).read()
d=json.load(open(os.path.join(here,'questions.json')))
data=json.dumps(d,ensure_ascii=False).replace('</','<\\/')

def inline(s):
    s=html.escape(s,quote=False)
    s=re.sub(r'\[([^\]]+)\]\((https?://[^)\s]+)\)',r'<a href="\2" target="_blank" rel="noopener">\1</a>',s)
    return re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',s)
def md(src):
    out=[];ul=False
    for line in src.splitlines():
        if line.startswith('- '):
            if not ul: out.append('<ul>');ul=True
            out.append('<li>'+inline(line[2:])+'</li>');continue
        if ul: out.append('</ul>');ul=False
        if line.startswith('## '): out.append('<h2>'+inline(line[3:])+'</h2>')
        elif line.startswith('# '): out.append('<h1>'+inline(line[2:])+'</h1>')
        elif line.strip(): out.append('<p>'+inline(line)+'</p>')
    if ul: out.append('</ul>')
    return '\n'.join(out)
# ADRESSE DU DÉPÔT PUBLIC : à changer ici seulement (texte « Méthode » et pied de page)
REPO_URL='https://github.com/produit-scalaire/produit-scalaire-electoral'
PAGE_URL='https://produit-scalaire.github.io/produit-scalaire-electoral/'
# Lien à partager : changer le numéro de version pour forcer les applications à recharger l'aperçu
SHARE_URL=PAGE_URL+'?v=2'
# Aperçu du lien (WhatsApp, iMessage, réseaux) : image preview.png à la racine du site, régénérée depuis apercu-lien.html
DESC="Répondez aux vrais votes de l'Assemblée nationale et mesurez votre proximité avec chaque parti, sujet par sujet."
FAV="data:image/svg+xml,"+__import__('urllib.parse').parse.quote('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 30 30"><rect width="30" height="30" rx="6" fill="#0f1633"/><path d="M5 25 L25 21" stroke="#8ea2ff" stroke-width="3" stroke-linecap="round"/><path d="M5 25 L19 6" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>')
META=f'''<meta name="description" content="{html.escape(DESC)}">
<link rel="icon" href="{FAV}">
<meta property="og:type" content="website"><meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Produit scalaire électoral">
<meta property="og:title" content="Quel parti vote vraiment comme vous ?">
<meta property="og:description" content="{html.escape(DESC)}">
<meta property="og:url" content="{SHARE_URL}">
<meta property="og:image" content="{PAGE_URL}preview.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="L'hémicycle de l'Assemblée nationale et la question : quel parti vote vraiment comme vous ?">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="Quel parti vote vraiment comme vous ?">
<meta name="twitter:description" content="{html.escape(DESC)}"><meta name="twitter:image" content="{PAGE_URL}preview.png">
'''
about=md(open(ROOT+'disclaimer.md').read().replace('__REPO__',REPO_URL).replace('__PAGE__',PAGE_URL))
# sous-onglets : une section par titre de niveau 2
SHORT={'Notre intention':'Intention','Notre méthode':'Méthode','Les limites à garder en tête':'Limites','Collecte des données : aucune':'Données','Remerciements':'Merci'}
parts=re.split(r'(?=<h2>)',about)
head,secs=parts[0],parts[1:]
if secs:
    btns=[];panels=[]
    for i,sec in enumerate(secs):
        h2t=re.match(r'<h2>(.*?)</h2>',sec).group(1);lab=SHORT.get(html.unescape(re.sub('<[^>]+>','',h2t)),h2t)
        btns.append(f'<button role="tab" data-sub="{i}" aria-selected="{"true" if i==0 else "false"}">{lab}</button>')
        panels.append(f'<div class="subpanel" data-subpanel="{i}"{"" if i==0 else " hidden"}>{sec}</div>')
    about=head+'<nav class="tabs subtabs" role="tablist" aria-label="Sous-sections">'+''.join(btns)+'</nav>'+''.join(panels)

a=open(ROOT+'animation-axes.html').read().replace('__NQ__',str(len(d['questions'])))
a=re.sub(r'<link[^>]*fonts\.(googleapis|gstatic)[^>]*>\s*','',a)
a=re.sub(r'--display:[^;]*;','--display:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;',a)
a=re.sub(r'--body:[^;]*;','--body:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;',a)
a=re.sub(r'--mono:[^;]*;','--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;',a)
a=re.sub(r'<meta name="claude:viewport-fit-sides"[^>]*>','',a)
assert 'googleapis' not in a and 'http' not in re.sub(r'href="https?://[^"]*"','',a).split('<script>')[0], 'external resource left in animation'
a=a+'<style>@media (max-width:620px){body{padding-left:8px!important;padding-right:8px!important}figure{padding:4px!important}svg .lab{font-size:21px}svg .lab.pour{font-size:21px}svg .plabel{font-size:22px}svg .cap{font-size:17px}svg .big{font-size:44px}}</style>'
a='<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><base target="_blank"></head><body style="margin:0">'+a+'</body></html>'
anim=a.replace('&','&amp;').replace('"','&quot;')

dl_top='<a class="dl" href="" download="produit-scalaire-electoral.html" onclick="this.href=location.href.split(\'#\')[0]">Télécharger la page</a>'
dl2='<p class="label"><a href="" download="produit-scalaire-electoral.html" onclick="this.href=location.href.split(\'#\')[0]">Téléchargez la page</a> pour l’utiliser hors connexion.</p>'
base=t.replace('__SHARE__',SHARE_URL).replace('__REPO__',REPO_URL).replace('__DATA__',data).replace('__ABOUT__',about).replace('__ANIM__',anim)
std=base.replace('__DOWNLOAD_TOP__',dl_top).replace('__DOWNLOAD2__',dl2)
art=base.replace('__DOWNLOAD_TOP__','').replace('__DOWNLOAD2__','')
open(os.path.join(here,'produit-scalaire-electoral.html'),'w').write('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'+META+std.replace('<div class="shell"','</head><body>\n<div class="shell"',1)+'\n</body></html>\n')
open(os.path.join(here,'artifact.html'),'w').write(art)
print('ok',len(d['questions']),'questions')

# Régénère aussi le catalogue lisible des questions
import subprocess,sys
subprocess.run([sys.executable,os.path.join(here,'build_catalogue.py')],check=True)
