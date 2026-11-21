# Site équipe — Seno Mining Services

Le site qui s'affiche quand on touche une carte NFC d'un employé SMS.
Chaque personne a sa page (`traore.html`, `sissoko.html`, …) avec ses numéros, son e-mail,
WhatsApp et un bouton « Enregistrer le contact ».

**Les liens de carte ne changent jamais** : `https://<ton-site>.pages.dev/sissoko` reste le même,
même si on change sa photo ou qu'on ajoute d'autres personnes.

## Ajouter un nouvel employé (depuis GitHub, sans ordinateur)

1. Ouvrir le dossier `photos/` sur GitHub → **Add file → Upload files** → envoyer sa photo
   (ex. `koné.jpg`). Une photo bien cadrée sur le visage suffit, le site la recadre tout seul.
2. Ouvrir `data/team.json` → crayon (**Edit**) en haut à droite.
3. Copier un bloc `{ ... }` existant, coller une virgule après, et changer les valeurs :
   - `slug` : utilisé dans le lien, sans accent ni espace (ex. `"kone"`)
   - `first`, `last`, `role`, `email`
   - `tel` : les numéros à afficher
   - `wa` : le numéro WhatsApp, sans le `+` ni espace
   - `photo` : le nom exact du fichier mis à l'étape 1
4. **Commit changes** en bas de page.

Quelques minutes après, le site se reconstruit tout seul et sa page est en ligne à
`https://<ton-site>.pages.dev/<slug>`. C'est ce lien qu'il faut programmer dans sa puce NFC.

## Modifier une personne ou l'enlever

- **Changer un numéro, l'e-mail ou le poste** : modifier son bloc dans `data/team.json`, Commit.
- **Changer sa photo** : uploader la nouvelle dans `photos/` avec le même nom, Commit.
- **Quelqu'un quitte l'entreprise** : ne pas juste supprimer son bloc (sa carte déjà imprimée
  mènerait vers une erreur). Mieux : créer une redirection dans `site/_redirects`
  (`/ancien-slug  /  301`) ou refaire pointer sa carte vers une autre page.

## Modifier les informations de l'entreprise

Tout est dans `data/company.json` : présentation, services, chiffres clés, parcours,
adresse, réseaux sociaux. Même principe : modifier, Commit, ça se republie tout seul.

## Brancher Cloudflare Pages (gratuit)

1. dash.cloudflare.com → **Workers & Pages** → **Créer** → **Pages** → **Connecter à Git**.
2. Choisir ce dépôt GitHub.
3. Réglages de build :
   - **Commande de build** : laisser vide
   - **Dossier de sortie (build output)** : `site`
4. Déployer. Le site est en ligne sur `https://<nom-du-projet>.pages.dev`.

Chaque modification poussée sur GitHub (étapes ci-dessus) reconstruit `site/` automatiquement,
puis Cloudflare republie le site tout seul — rien à refaire à la main.

## Travailler en local (pour Claude ou un développeur)

```bash
pip install pillow
python3 scripts/build_site.py   # régénère le dossier site/
```
