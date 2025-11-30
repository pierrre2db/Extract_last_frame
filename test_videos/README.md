# Fichiers vidéo de test

Ce dossier est destiné à contenir des fichiers vidéo de test pour l'application Video Frame Extractor.

## Comment obtenir des fichiers de test

### Option 1 : Téléchargement manuel (recommandé)

Visitez l'un de ces sites et téléchargez des fichiers de test dans différents formats :

#### **File-Examples.com** (Recommandé)
🔗 https://file-examples.com/index.php/sample-video-files/

Formats disponibles : MP4, AVI, MOV, MKV, WEBM, FLV
- Cliquez sur le format souhaité
- Choisissez une résolution (480p, 720p, 1080p)
- Cliquez sur "Download sample"
- Enregistrez le fichier dans ce dossier `test_videos/`

#### **GetSampleFiles.com**
🔗 https://getsamplefiles.com/sample-video-files

Formats disponibles : MP4, AVI, MOV, MKV
- Sélectionnez le format dans la liste
- Cliquez sur le bouton de téléchargement
- Enregistrez dans ce dossier

#### **FreeTestData.com**
🔗 https://freetestdata.com/video-files/

Formats disponibles : MP4, AVI, MOV, WMV, WEBM
- Choisissez la taille de fichier souhaitée
- Cliquez sur le lien de téléchargement
- Enregistrez dans ce dossier

### Option 2 : Vidéos de test Big Buck Bunny

Le projet Blender propose des vidéos de test gratuites :

🔗 https://download.blender.org/demo/movies/

Fichiers disponibles :
- `BBB/bbb_sunflower_1080p_30fps_normal.mp4` (355 MB)
- `BBB/bbb_sunflower_2160p_30fps_normal.mp4` (738 MB)

Utilisez `curl` ou `wget` pour télécharger :
```bash
cd test_videos/
curl -O https://download.blender.org/demo/movies/BBB/bbb_sunflower_1080p_30fps_normal.mp4
```

### Option 3 : Créer vos propres vidéos de test

Sur macOS, vous pouvez créer des vidéos de test rapides :

**Avec QuickTime Player :**
1. Ouvrir QuickTime Player
2. Fichier > Nouvel enregistrement d'écran
3. Enregistrer quelques secondes
4. Fichier > Exporter > Choisir le format

**Avec la ligne de commande (ffmpeg) :**
```bash
# Installer ffmpeg si nécessaire
brew install ffmpeg

# Créer une vidéo de test de 5 secondes
ffmpeg -f lavfi -i testsrc=duration=5:size=1280x720:rate=30 test.mp4
ffmpeg -f lavfi -i testsrc=duration=5:size=1280x720:rate=30 test.mov
ffmpeg -f lavfi -i testsrc=duration=5:size=1280x720:rate=30 test.avi
ffmpeg -f lavfi -i testsrc=duration=5:size=1280x720:rate=30 test.mkv
```

## Formats recommandés pour les tests

Pour tester complètement l'application, téléchargez au moins un fichier de chaque format :

- ✅ **MP4** - Format le plus courant
- ✅ **MOV** - Format natif macOS/QuickTime
- ✅ **M4V** - Variante Apple
- ✅ **AVI** - Format classique
- ✅ **MKV** - Format conteneur moderne
- ✅ **MPEG** - Format MPEG standard

## Structure recommandée

```
test_videos/
├── test_small.mp4       # ~1-5 MB
├── test_medium.mp4      # ~10-50 MB
├── test_large.mp4       # ~100+ MB
├── test.mov
├── test.avi
├── test.mkv
└── test.mpeg
```

## Tester l'application

Une fois que vous avez téléchargé des fichiers de test :

1. Lancez `Video Frame Extractor.app`
2. Cliquez sur "📂 Parcourir..."
3. Naviguez vers ce dossier `test_videos/`
4. Sélectionnez un fichier vidéo
5. Cliquez sur "🎯 Extraire la dernière frame"
6. Vérifiez l'aperçu
7. Sauvegardez l'image extraite

Testez avec différents formats pour vérifier la compatibilité !
