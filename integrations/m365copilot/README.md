# M365 : titres du cache HTTP sur le client

Cette intégration associe `ChatTitlesExec.yaml` au script
`extract_chat_titles_live.py`. L'artefact utilise execve pour lancer un Python
portable sur le poste ; ce n'est pas du VQL pur. Le cache est d'abord copié dans
un répertoire temporaire via ntfs, décodé localement, puis seuls les résultats
structurés sont retournés.

## Configuration obligatoire

La dernière version source utilisait un bundle spécifique au laboratoire.
L'adresse privée a été remplacée par `https://example.invalid/M365ChatTitlesPy.zip` :
cette URL est volontairement non opérationnelle. Configurer le tool avant de
lancer cet artefact.

Préparer une archive ZIP avec, à sa racine :

```text
python.exe
python311.dll
python311.zip
python311._pth
extract_chat_titles_live.py
Lib/site-packages/ccl_chromium_reader/
... dépendances et DLL nécessaires ...
```

Utiliser un CPython Windows portable compatible avec l'architecture cible.
Le bundle de recherche utilisait Python 3.11, `ccl_chromium_reader`, Brotli et
zstd. Le runtime et les bibliothèques tierces ne sont pas inclus dans ce dépôt.
Le fichier `_pth` doit permettre le chargement des paquets sous Lib/site-packages.
Le script Python fourni est celui de la dernière version source.

Héberger l'archive à une adresse accessible au serveur Velociraptor, remplacer
`tools[0].url`, puis ajouter `expected_hash` avec le SHA-256 de l'archive finale.
Le tool s'appelle `M365ChatTitlesPy` et `serve_locally: true` permet au serveur
de le distribuer aux clients. Importer ensuite l'artefact et vérifier le tool
dans l'inventaire Velociraptor avant collecte.

## Résultats et limites

Paramètres : `ProfileGlob`, `KeyRegex` et `regex`. Ce dernier est interprété par
Python re et filtre ChatName. Les sources sont ConversationTitles et Diagnostics.
Le résultat est une liste de titres GetChats avec identifiants et provenance
cache ; ni rôle utilisateur garanti ni réponse complète. Le dédoublonnage garde
l'observation de cache la plus récente pour un même couple identifiant/titre.
La sortie execve est plafonnée ; surveiller erreurs et diagnostics.

Le bundle original a été validé sur Windows pendant la recherche. Le template
portable du dépôt passe la validation syntaxique, mais doit être revalidé avec
le bundle et l'URL de votre déploiement. Le corps du script est inchangé ; aucun
binaire, cache ou configuration du laboratoire n'est livré.
