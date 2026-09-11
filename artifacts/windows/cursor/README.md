# Cursor

| Fichier | Fonction |
|---|---|
| Presence.yaml | Installation, version, processus et traces d'exécution |
| Inventory.yaml | Racines et métadonnées des données Cursor |
| Collection.yaml | Bases et compagnons, transcripts, logs et snapshots |
| PromptExtraction.yaml | Messages, outils, sessions, index et transcripts |
| AutocompleteExtraction.yaml | Diffs proposés par Tab et statistiques |
| ContextExtraction.yaml | Attribution du code, projets et checkpoints |

Les six versions sélectionnées correspondent au paquet de livraison final.
Dépendances natives : Windows.Sys.Users, Windows.Forensics.Prefetch,
Windows.Forensics.Bam. Aucun parseur externe requis pour les sources VQL.

Paramètres principaux : `AdditionalProfileGlobs`, `DatabaseGlobs`,
`TranscriptGlobs`, `TabLogGlobs`, `Accessor` et `LogTimezone` selon l'artefact.
`IncludeConfiguration` et `IncludeCaches` sont désactivés par défaut dans
Collection. Consulter le YAML pour les paramètres propres à chaque artefact.
Les limites par fichier/base et les sources Coverage doivent être contrôlées.

Validation de recherche : Windows 11 Pro 25H2, Cursor 3.19.13, Velociraptor
0.77.2 ; douze tests synthétiques consignés dans le dossier source. La préparation
du dépôt ne rejoue pas ces collectes distantes.

Un rôle user peut désigner une tâche de sous-agent. L'index SearchIndex ne
sépare pas les rôles ; les blobs inconnus restent signalés. Les diffs proposés
ne prouvent pas leur acceptation. Les copies de bases actives ne sont pas
atomiques ; la compatibilité des versions différentes reste à vérifier.

Importer les YAML par leur champ `name`. Les contrôles de préparation sont
décrits dans [VALIDATION.md](../../../docs/VALIDATION.md).
