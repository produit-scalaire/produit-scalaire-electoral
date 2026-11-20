# Assemble the single offline page from template.html + questions.json + disclaimer.md + animation-axes.html.
import json,re,html,os
ROOT='/mnt/project-files/comparateur/'
here=os.path.dirname(os.path.abspath(__file__))
t=open(os.path.join(here,'template.html')).read()
d=json.load(open(os.path.join(here,'questions.json')))
data=json.dumps(d,ensure_ascii=False).replace('</','<\\/')

def inline(s):
    s=html.escape(s,quote=False)
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
about=md(open(ROOT+'disclaimer.md').read())

a=open(ROOT+'animation-axes.html').read()
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
base=t.replace('__DATA__',data).replace('__ABOUT__',about).replace('__ANIM__',anim)
std=base.replace('__DOWNLOAD_TOP__',dl_top).replace('__DOWNLOAD2__',dl2)
art=base.replace('__DOWNLOAD_TOP__','').replace('__DOWNLOAD2__','')
open(os.path.join(here,'produit-scalaire-electoral.html'),'w').write('<!doctype html>\n<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'+std.replace('<div class="shell"','</head><body>\n<div class="shell"',1)+'\n</body></html>\n')
open(os.path.join(here,'artifact.html'),'w').write(art)
print('ok',len(d['questions']),'questions')

# Régénère aussi le catalogue lisible des questions
import subprocess,sys
subprocess.run([sys.executable,os.path.join(here,'build_catalogue.py')],check=True)
