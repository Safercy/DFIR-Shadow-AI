# AI Forensics — artefacts Velociraptor

Artefacts Windows et macOS pour l'investigation des assistants IA. Le dépôt contient les
versions finales sélectionnées des recherches, leurs requêtes VQL en YAML et
leur documentation. Les fichiers de recherche et les données collectées restent
hors du dépôt.

## Organisation

```text
artifacts/windows/
├── chatgpt-desktop/   # Présence et collecte du profil applicatif
├── codex-cli/         # Collecte .codex et extraction de contenu
├── cursor/            # Présence, collecte et trois extracteurs
└── m365copilot/       # Disque, notifications et option mémoire
artifacts/macos/
└── openclaw/           # Présence, conversations, état et collecte OpenClaw
integrations/
└── m365copilot/       # Titres du cache HTTP, avec outil Python externe
    ├── ChatTitlesExec.yaml
    ├── extract_chat_titles_live.py
    └── README.md
docs/
├── SOURCES.md         # Sélection des versions et empreintes originales
└── VALIDATION.md      # Contrôles réalisés et limites
```

Un README par application décrit les artefacts, paramètres et limites. Les noms
Velociraptor d'origine sont conservés, même si leur répertoire a changé.

## Catalogue

| Application | Artefacts autonomes | Contenu et portée |
|---|---:|---|
| [ChatGPT Desktop](artifacts/windows/chatgpt-desktop/README.md) | 2 | Présence et fichiers bruts ; pas d'extracteur de messages démontré |
| [Codex CLI](artifacts/windows/codex-cli/README.md) | 2 | Bases et sessions JSONL ; messages et activité selon les schémas pris en charge |
| [Cursor](artifacts/windows/cursor/README.md) | 6 | Messages, outils, autocomplétion et contexte de code |
| [M365 Copilot](artifacts/windows/m365copilot/README.md) | 6 | Requêtes URL, notifications, collecte et fragments mémoire optionnels |
| [OpenClaw](artifacts/macos/openclaw/README.md) | 12 | Sessions, configuration, état, persistance, réseau, logs et collecte macOS |
| [M365 — intégration Python](integrations/m365copilot/README.md) | 1 intégration | Titres de conversation dans le cache GetChats ; bundle à configurer |

## Installation

Importer les YAML souhaités via l'interface **Artifacts** de Velociraptor puis
sélectionner l'artefact par son champ `name` lors d'une collecte client.
Les fichiers sont des définitions d'artefacts ; il ne faut pas coller le YAML
entier dans une cellule VQL. Les plugins et artefacts natifs de Velociraptor restent
fournis par Velociraptor et ne sont pas dupliqués ici.

Validation syntaxique avec le binaire utilisé pendant la préparation :

```sh
velociraptor --nocolor artifacts verify artifacts integrations
```

Version de validation : **0.77.2**. Cela ne garantit pas la compatibilité de tous
les schémas applicatifs. Voir [les niveaux de validation](docs/VALIDATION.md).
L'intégration Python exige une préparation supplémentaire avant exécution.

## Interprétation des résultats

Les sources de données sont distinguées : message structuré, titre de
conversation, requête d'URL, fragment mémoire ou fichier brut. Aucun de ces
artefacts ne garantit une extraction exhaustive pour toutes les versions.
Les bases actives et leurs WAL doivent être interprétés selon les limites du
README de l'application. Vérifier les diagnostics et les logs après collecte.

## Ajouter un artefact

Conserver une seule version par `name`, dans le dossier de son application.
Écrire les requêtes en blocs `query: |`, documenter les paramètres, le stockage
lu et la validation effectuée. Ajouter seulement les scripts indispensables
à une intégration ; les binaires, preuves et historiques de recherche restent
à l'extérieur du dépôt.

## Licence

Aucune licence n'est imposée dans cette préparation. Ajouter la licence choisie
avant publication si le dépôt doit autoriser la réutilisation des artefacts.
