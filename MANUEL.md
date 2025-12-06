# Video Frame Extractor - Mini Manuel d'Utilisation

## Installation Rapide

1. Copiez `Video Frame Extractor.app` dans votre dossier `/Applications`
2. Au premier lancement : clic droit > Ouvrir (pour contourner la sécurité macOS)

## Utilisation Mode Graphique

### Méthode Simple
1. Double-cliquez sur l'application
2. Cliquez sur **"Parcourir..."**
3. Sélectionnez votre vidéo
4. Cliquez sur **"Extraire la dernière frame"**
5. Attendez la fin de l'extraction
6. Cliquez sur **"Sauvegarder l'image"**
7. Choisissez l'emplacement et le nom du fichier JPEG

### Informations Affichées
- Résolution de la vidéo (ex: 1280x720)
- Durée totale
- Nombre de frames par seconde (FPS)
- Aperçu de l'image extraite

## Utilisation en Ligne de Commande

### Syntaxe de Base

```bash
"Video Frame Extractor.app/Contents/MacOS/Video Frame Extractor" -g /chemin/vers/video.mp4
```

ou

```bash
"Video Frame Extractor.app/Contents/MacOS/Video Frame Extractor" /chemin/vers/video.mp4
```

### Exemples Concrets

**Depuis Applications :**
```bash
"/Applications/Video Frame Extractor.app/Contents/MacOS/Video Frame Extractor" -g ~/Videos/vacances.mp4
```

**Depuis le dossier du projet :**
```bash
"dist/Video Frame Extractor.app/Contents/MacOS/Video Frame Extractor" ~/Desktop/film.mov
```

**Avec un fichier sur le Bureau :**
```bash
"/Applications/Video Frame Extractor.app/Contents/MacOS/Video Frame Extractor" ~/Desktop/video.mp4
```

### Points Importants

- Utilisez des **chemins absolus** (commençant par `/` ou `~/`)
- Mettez les chemins entre guillemets s'ils contiennent des espaces
- L'application s'ouvre avec la vidéo déjà chargée
- Vous pouvez ensuite utiliser l'interface normalement

### Afficher l'Aide

```bash
"Video Frame Extractor.app/Contents/MacOS/Video Frame Extractor" --help
```

## Formats Vidéo Supportés

- MP4
- MOV
- M4V
- AVI
- MKV
- MPEG / MPG

## Qualité de l'Image

- Format de sortie : **JPEG**
- Qualité : **95%** (haute qualité)
- Résolution : **Identique à la vidéo** (pas de redimensionnement)

## Raccourcis et Astuces

### Créer un Alias Bash (optionnel)

Ajoutez ceci dans votre `~/.zshrc` ou `~/.bashrc` :

```bash
alias extract-frame="/Applications/Video\ Frame\ Extractor.app/Contents/MacOS/Video\ Frame\ Extractor"
```

Puis rechargez :
```bash
source ~/.zshrc
```

Maintenant vous pouvez simplement taper :
```bash
extract-frame -g ~/Videos/ma_video.mp4
```

### Glisser-Déposer

Vous pouvez aussi glisser un fichier vidéo directement sur l'icône de l'application dans le Finder (si configuré).

## Résolution de Problèmes

### "L'application est endommagée"
- Faites un **clic droit** > **Ouvrir** au lieu de double-cliquer
- Ou dans Préférences Système > Sécurité, autorisez l'application

### "Le fichier n'existe pas" (en CLI)
- Vérifiez que vous utilisez un chemin absolu
- Vérifiez l'orthographe du chemin
- Utilisez `ls` pour confirmer l'emplacement du fichier

### "Format non supporté"
- Vérifiez que votre vidéo est dans un format supporté (voir liste ci-dessus)
- Certains codecs rares peuvent ne pas fonctionner

### L'aperçu ne s'affiche pas
- C'est normal, l'aperçu apparaît après l'extraction
- Cliquez d'abord sur "Extraire la dernière frame"

## Workflow Recommandé

### Pour un Fichier Unique
```bash
# 1. Lancer avec le fichier
"/Applications/Video Frame Extractor.app/Contents/MacOS/Video Frame Extractor" -g ~/Videos/video.mp4

# 2. Dans l'interface :
#    - Cliquer sur "Extraire la dernière frame"
#    - Vérifier l'aperçu
#    - Cliquer sur "Sauvegarder l'image"
```

### Pour Plusieurs Fichiers
1. Lancez l'application normalement (sans CLI)
2. Extrayez la première vidéo
3. Sauvegardez l'image
4. Cliquez à nouveau sur "Parcourir..." pour la suivante
5. Répétez

## Support et Questions

Pour des questions ou des problèmes :
- Vérifiez d'abord ce manuel
- Consultez le README.md complet pour plus de détails techniques
- Vérifiez que vous avez macOS 11.0 ou supérieur

---

**Version 1.1.0** - Mise à jour : 2024
**Auteur** : Pierre
**Licence** : Usage personnel et éducatif
