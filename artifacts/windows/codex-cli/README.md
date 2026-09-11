# Codex CLI

| Fichier | Fonction |
|---|---|
| Collection.yaml | Collecte ciblée du dossier `.codex`, sessions et bases |
| PromptExtraction.yaml | Six sources VQL : threads, éléments, activité, jetons, imports de configuration et messages JSONL |

Paramètres : `RootGlob` (défaut `C:/Users/*/.codex`), `Accessor` (défaut `ntfs`).
La collecte propose `IncludeAuth`, désactivé par défaut. Aucun filtre `regex`
commun n'est ajouté aux extracteurs dans cette livraison.

L'extracteur lit les tables `threads` et `thread_items` et certains événements
de rollout. Il expose le premier fragment de contenu et `ContentPartCount` ;
ce n'est pas une reconstruction de toutes les pièces jointes. Certaines sources
retournent des champs bruts pour les types encore non caractérisés.

Correction de préparation : quatre `LET` placés dans des blocs `foreach` non
acceptés par le parseur ont été déplacés en requêtes différées, sans modifier
les sélections SQL ni les champs. Le test synthétique vérifie deux bases,
Unicode, activité de commande, prompts JSONL et événements de jetons.
La version corrigée n'a pas été exécutée sur un endpoint Windows lors de cette
préparation. Les lectures SQLite via ntfs ne garantissent pas la prise en compte
du WAL ; un schéma différent peut produire des erreurs ou des résultats vides.

Importer les YAML par leur champ `name`. Les contrôles de préparation sont
décrits dans [VALIDATION.md](../../../docs/VALIDATION.md).
