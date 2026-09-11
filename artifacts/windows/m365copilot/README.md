# M365 Copilot

| Fichier | Fonction | Limite principale |
|---|---|---|
| Inventory.yaml | Présence, package, profils et fichiers | Métadonnées |
| Collection.yaml | Fichiers OfficeHub, cache et notifications | Collecte brute, pas parsing des messages |
| DiskPromptQueries.yaml | Texte décodé des paramètres q dans History | Seulement les URL microsoft365.com/hwav2/search/main prises en charge |
| History.yaml | Visites et titres de navigation | Un titre n'est pas un message |
| Notifications.yaml | XML de notifications et inscriptions M365 | Lecture live ntfs : WAL non garanti |
| MemoryContent.yaml | Contextes mémoire via règles YARA explicites | Option volatile, pas une source persistante |

Le dossier WebView observé est sous le package
`Microsoft.MicrosoftOfficeHub_*/LocalState/EBWebView/`.
La sélection actuelle garde les versions des artefacts présentes en fin de
recherche. Aucune extension de domaine ou de schéma n'est inventée ici.

`regex` est facultatif. Sa portée dépend de l'artefact : texte décodé pour
DiskPromptQueries, XML/identifiants pour Notifications, chemins pour Collection,
contextes pour MemoryContent. Le laisser vide dans Collection pour conserver
les compagnons de bases. Les diagnostics restent des sources distinctes.

DiskPromptQueries parse directement côté client, sur une copie temporaire de
History avec les WAL/SHM disponibles. Son EvidenceType est URLQueryText ; Role
et identifiants de messages sont inconnus. Les autres messages du composeur ne
sont pas garantis. Le domaine m365.cloud.microsoft a été observé en recherche,
mais ne fait pas partie du filtre de cet artefact : couverture partielle explicite.

Notifications distingue émetteur et référence à M365 dans le contenu d'une
notification Store. Un handler ne prouve pas un affichage. Pour exploiter une
collecte avec WAL, utiliser des copies reconstituées et Accessor=file. Les fichiers
sparse transférés doivent être reconstruits avec leurs index avant parsing.

Les titres GetChats nécessitent [l'intégration Python](../../../integrations/m365copilot/README.md)
exécutée sur le client. Un titre peut correspondre à une demande, mais n'est pas
un transcript. Aucun extracteur de réponses complètes depuis le disque n'est
revendiqué dans ce dépôt. La mémoire reste une option séparée.

Importer les YAML par leur champ `name`. Les contrôles de préparation sont
décrits dans [VALIDATION.md](../../../docs/VALIDATION.md).
