# Validation de la préparation

Contrôles effectués les 10 et 11 septembre 2026 :

- 29 noms d'artefacts uniques ; doublons ChatGPT éliminés par comparaison du contenu.
- Tous les artefacts sont du YAML bloc, avec VQL multiligne lisible.
- Chargement syntaxique des 29 artefacts réussi avec Velociraptor 0.77.2.
- OpenClaw : les 12 définitions finales du dossier de recherche ont été reprises.
  Leur campagne source rapporte 12/12 exécutions terminées sur macOS ARM avec
  OpenClaw 2026.6.9 ; TCC n'a produit aucune ligne à cause d'un refus macOS
  `operation not permitted`, documenté comme une limite d'accès.
- Correction Codex CLI : tests synthétiques de portée entre deux bases, texte
  Unicode, nombre de parties, commandes, prompts de rollout et événements de jetons.
- Vérification ciblée des fichiers retenus pour exclure configurations d'accès,
  clés privées, identifiants de machines/clients/flows et adresses du laboratoire.

```sh
velociraptor --nocolor artifacts verify artifacts integrations
```

## Ce que ces contrôles ne prouvent pas

La préparation du dépôt n'a lancé aucune nouvelle collecte distante.
Les validations Windows et macOS antérieures sont résumées par application et ne sont
pas rejouées ici. Codex PromptExtraction corrigé est validé syntaxiquement et
sur fixtures locales, pas sur Windows. L'intégration M365 exige un bundle et
une URL configurés : une validation syntaxique ne valide pas ces dépendances.
Les schémas applicatifs différents et l'exhaustivité des conversations ne sont
pas garantis. Les résultats, logs et fixtures contenant les données de recherche
ne sont pas inclus dans ce dépôt minimal.
