# OpenClaw sur macOS

Douze artefacts issus de la campagne finale OpenClaw. Ils ciblent le répertoire
`~/.openclaw`, les sessions JSONL, les bases SQLite et les traces macOS associées.

| Fichier | Fonction |
|---|---|
| `Custom.MacOS.Applications.OpenClaw.Presence.yaml` | Détection du répertoire d'état, de l'app, du LaunchAgent, du processus et des ports |
| `Custom.MacOS.Applications.OpenClaw.StateDir.yaml` | Inventaire de `~/.openclaw` et des sessions Pi éventuelles |
| `Custom.MacOS.Applications.OpenClaw.Sessions.yaml` | Prompts, réponses, appels et résultats d'outils depuis les transcripts JSONL |
| `Custom.MacOS.Applications.OpenClaw.Config.yaml` | Configuration et journal d'audit, avec masquage des secrets par défaut |
| `Custom.MacOS.Applications.OpenClaw.Auth.yaml` | Métadonnées d'authentification SQLite ; valeurs sensibles exclues par défaut |
| `Custom.MacOS.Applications.OpenClaw.Memory.yaml` | Sources, chunks et état de la mémoire indexée |
| `Custom.MacOS.Applications.OpenClaw.StateDB.yaml` | Base centrale : cron, tâches, subagents, appairages et diagnostics |
| `Custom.MacOS.Applications.OpenClaw.Persistence.yaml` | LaunchAgents, LaunchDaemons et wrapper d'environnement |
| `Custom.MacOS.Applications.OpenClaw.Network.yaml` | Ports OpenClaw enrichis des informations de processus |
| `Custom.MacOS.Applications.OpenClaw.Logs.yaml` | Logs quotidiens, stdout du gateway et paquets de stabilité |
| `Custom.MacOS.Applications.OpenClaw.TCC.yaml` | Autorisations TCC de l'app native et de Peekaboo |
| `Custom.MacOS.Applications.OpenClaw.Collection.yaml` | Collecte brute du périmètre OpenClaw |

## Ordre conseillé

Commencer par `Presence` et `StateDir`, puis lancer les extracteurs nécessaires.
Utiliser `Collection` pour préserver les fichiers bruts avant une désinstallation :
la suppression officielle d'OpenClaw peut effacer le répertoire d'état.

`Sessions` est l'extracteur principal des conversations. Il normalise le contenu
utilisateur stocké comme chaîne et les réponses assistant stockées comme tableaux
de blocs. `SourcePath`, `ConversationId`, `MessageId`, `ParentId`, `Role`, le
contenu brut et le contenu texte restent disponibles pour la provenance.

## Garde-fous

- `Config.RedactSecrets=Y` masque par défaut les clés dont le nom évoque un secret.
- `Auth.Unsafe_DumpValues=N` évite de retourner les jetons OAuth/API.
- `Memory.Include_ChunkText=N` exclut le texte indexé et les embeddings.
- `StateDir.Include_Npm=N` et `Collection.Include_Npm=N` excluent les dépendances npm.
- `StateDB.Table` vide désactive la requête libre `AnyTable`.

Ces protections réduisent l'exposition mais ne remplacent pas l'examen des champs
et des fichiers avant partage. `Collection` peut contenir des secrets en clair.

## Validation et limites

Les 12 artefacts ont été validés syntaxiquement avec Velociraptor 0.77.2. Leur
campagne source les a exécutés sur macOS ARM, OpenClaw 2026.6.9 : toutes les
collectes ont terminé sans erreur VQL. La lecture TCC a été refusée par macOS car
l'agent ne disposait pas de Full Disk Access ; zéro ligne ne signifie donc pas
absence d'autorisations. Les formats OpenClaw évoluent rapidement et doivent être
recroisés avec `SchemaDump` et les diagnostics.

Les descriptions ont été conservées car elles documentent les schémas observés,
mais les noms de machine, utilisateur, client, flows et hostnames de validation
ont été généralisés pour cette version publiable.

Voir [la validation transversale](../../../docs/VALIDATION.md) et
[la provenance](../../../docs/SOURCES.md).
