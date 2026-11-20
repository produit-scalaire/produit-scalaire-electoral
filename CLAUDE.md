# Règles pour ce dépôt

- Ne jamais ajouter de ligne `Co-Authored-By` ni aucune mention d'attribution Claude (Claude-Session, "Generated with Claude Code", etc.) dans les messages de commit, les PR ou les fichiers.
- Les mises à jour se poussent directement sur `main` (GitHub Pages sert la racine de `main`).
- La page publiée est `index.html`, générée depuis `source/` (`python3 source/build.py`, puis copier `produit-scalaire-electoral.html` vers `index.html`).
