#!/bin/bash
#
# Script de téléchargement de fichiers vidéo de test
# Utilise des sources alternatives plus fiables
#

echo "==================================================="
echo "  Téléchargement de fichiers vidéo de test"
echo "==================================================="
echo ""

# Créer le dossier s'il n'existe pas
mkdir -p test_videos
cd test_videos

# Fonction pour télécharger avec barre de progression
download_file() {
    local url=$1
    local filename=$2
    local format=$3

    echo "📥 Téléchargement: $filename ($format)"

    if [ -f "$filename" ]; then
        echo "   ⚠️  Fichier déjà existant, ignoré"
        echo ""
        return
    fi

    curl -L -o "$filename" "$url" --progress-bar --max-time 60

    if [ $? -eq 0 ] && [ -f "$filename" ]; then
        local size=$(ls -lh "$filename" | awk '{print $5}')
        echo "   ✅ Téléchargé avec succès ($size)"
    else
        echo "   ❌ Échec du téléchargement"
        rm -f "$filename" 2>/dev/null
    fi
    echo ""
}

# Téléchargement de fichiers de test depuis des sources alternatives
echo "=== Fichiers de test vidéo ==="

# Fichiers MP4 depuis file-examples.com
download_file "https://file-examples.com/storage/fe0a257b56a281fba71e8d0/2017/04/file_example_MP4_480_1_5MG.mp4" \
    "test_480p.mp4" "MP4"

download_file "https://file-examples.com/storage/fe0a257b56a281fba71e8d0/2017/04/file_example_MP4_640_3MG.mp4" \
    "test_640p.mp4" "MP4"

download_file "https://file-examples.com/storage/fe0a257b56a281fba71e8d0/2017/04/file_example_MP4_1280_10MG.mp4" \
    "test_1280p.mp4" "MP4"

# Fichiers AVI depuis file-examples.com
download_file "https://file-examples.com/storage/fe0a257b56a281fba71e8d0/2017/04/file_example_AVI_480_750kB.avi" \
    "test_480p.avi" "AVI"

download_file "https://file-examples.com/storage/fe0a257b56a281fba71e8d0/2017/04/file_example_AVI_1280_1_5MG.avi" \
    "test_1280p.avi" "AVI"

# Fichiers MKV depuis file-examples.com
download_file "https://file-examples.com/storage/fe0a257b56a281fba71e8d0/2020/03/file_example_MKV_1280_10MG.mkv" \
    "test_1280p.mkv" "MKV"

# Fichiers MOV depuis file-examples.com
download_file "https://file-examples.com/storage/fe0a257b56a281fba71e8d0/2017/04/file_example_MOV_480_700kB.mov" \
    "test_480p.mov" "MOV"

download_file "https://file-examples.com/storage/fe0a257b56a281fba71e8d0/2017/04/file_example_MOV_1280_1_4MB.mov" \
    "test_1280p.mov" "MOV"

echo ""
echo "==================================================="
echo "  ✅ Téléchargement terminé!"
echo "==================================================="
echo ""
echo "Fichiers téléchargés dans: $(pwd)"
echo ""

# Afficher la liste des fichiers téléchargés
count=$(ls -1 *.mp4 *.mov *.avi *.mkv *.mpeg 2>/dev/null | wc -l | tr -d ' ')

if [ "$count" -gt 0 ]; then
    echo "Fichiers disponibles:"
    ls -lh *.mp4 *.mov *.avi *.mkv *.mpeg 2>/dev/null | awk '{printf "  - %-25s %s\n", $9, $5}'
    echo ""
    echo "✅ $count fichier(s) prêt(s) pour les tests!"
else
    echo "⚠️  Aucun fichier n'a pu être téléchargé."
    echo ""
    echo "Vous pouvez télécharger manuellement des fichiers de test depuis:"
    echo "  - https://file-examples.com/index.php/sample-video-files/"
    echo "  - https://getsamplefiles.com/sample-video-files"
    echo "  - https://freetestdata.com/video-files/"
fi

echo ""
echo "Vous pouvez maintenant tester l'application avec ces fichiers!"
echo ""
