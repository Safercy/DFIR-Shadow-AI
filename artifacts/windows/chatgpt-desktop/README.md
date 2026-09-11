# ChatGPT Desktop

Les variantes `presence_extended.yaml` et `collection_extended.yaml` sont
retenues : elles étendent les premiers fichiers et existent à l'identique dans
les deux copies de recherche.

| Fichier | Fonction |
|---|---|
| Presence.yaml | Installation, processus, Prefetch, Amcache, UserAssist et profils |
| Collection.yaml | Données applicatives et compagnons ; source Supplemental facultative |

`Collection` utilise `RootGlob`, `Accessor`, `IncludeCaches` (désactivé par défaut)
et `SupplementalGlobs`. Le périmètre historique inclut aussi certains profils
OpenAI Codex ; consulter RootGlob avant lancement. Les sessions sous `.codex`
sont traitées par les artefacts [Codex CLI](../codex-cli/README.md).

Dépendances natives : Windows.Forensics.Prefetch, Windows.Detection.Amcache,
Windows.Registry.UserAssist. Les fichiers bruts peuvent contenir des cookies et
métadonnées de session. Il n'y a ni déchiffrement ni parseur complet de messages
ChatGPT dans cette livraison. Les copies de bases actives ne sont pas atomiques.

Importer les YAML par leur champ `name`. Les contrôles de préparation sont
décrits dans [VALIDATION.md](../../../docs/VALIDATION.md).
