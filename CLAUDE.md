# Règles pour ce dépôt

- Ne jamais ajouter de ligne `Co-Authored-By` ni aucune mention d'attribution Claude (Claude-Session, "Generated with Claude Code", etc.) dans les messages de commit, les PR ou les fichiers.
- Les mises à jour se poussent directement sur `main` (GitHub Pages sert la racine de `main`).
- L'adresse du dépôt affichée sur la page est la constante `REPO_URL` de `source/build.py` (à changer si le dépôt déménage).
- La page publiée est `index.html`, générée depuis `source/` (`python3 source/build.py`, puis copier `produit-scalaire-electoral.html` vers `index.html`).
- Cohésion des groupes : `source/votes_groupes.json` (relevé datan.fr, [pour, contre, abstention] par groupe) ; `python3 source/add_cohesion.py` écrit le champ `split` dans `questions.json`, à relancer avant `build.py` quand on ajoute un scrutin.
