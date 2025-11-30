# Video Frame Extractor

Extracteur de dernière frame vidéo vers JPEG avec interface graphique pour macOS.

## Description

Video Frame Extractor est une application macOS native qui permet d'extraire la dernière frame d'une vidéo et de la sauvegarder en image JPEG de haute qualité. L'application dispose d'une interface graphique intuitive optimisée pour macOS.

**Formats vidéo supportés :** MP4, MOV, M4V, AVI, MKV, MPEG/MPG

## Fonctionnalités

- **Sélection de vidéo** : Interface de dialogue native macOS pour choisir une vidéo (MP4, MOV, M4V, AVI, MKV, MPEG)
- **Informations vidéo** : Affichage automatique des métadonnées (résolution, durée, FPS)
- **Extraction rapide** : Extraction de la dernière frame avec indicateur de progression
- **Aperçu en direct** : Visualisation de l'image extraite avant sauvegarde
- **Sauvegarde haute qualité** : Export en JPEG avec qualité 95%
- **Interface native macOS** : Utilisation du style Aqua et des conventions macOS

## Prérequis

Pour utiliser l'application compilée :
- macOS 11.0 ou supérieur
- Architecture ARM64 (Apple Silicon) ou Intel

Pour développer ou compiler :
- Python 3.13 ou supérieur
- pip (gestionnaire de paquets Python)

## Installation

### Utilisation de l'application compilée

1. Téléchargez l'application `Video Frame Extractor.app` depuis le dossier `dist/`
2. Déplacez l'application dans `/Applications` (optionnel)
3. Double-cliquez sur l'application pour la lancer

**Note** : Au premier lancement, macOS peut afficher un avertissement de sécurité. Faites un clic droit > Ouvrir pour autoriser l'application.

### Développement

1. Clonez ou téléchargez ce projet
2. Créez un environnement virtuel :
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Pour les outils de développement
   ```

## Utilisation

### Avec l'application compilée

1. Lancez `Video Frame Extractor.app`
2. Cliquez sur "Parcourir..." pour sélectionner une vidéo
3. Cliquez sur "Extraire la dernière frame"
4. Prévisualisez l'image extraite
5. Cliquez sur "Sauvegarder l'image" pour exporter en JPEG

### Avec le script Python

```bash
source venv/bin/activate
python3 extract_last_frame.py
```

## Compilation de l'application

Pour créer l'application macOS à partir du code source :

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Nettoyer les builds précédents (optionnel)
rm -rf build dist

# Compiler l'application
python setup.py py2app
```

L'application sera créée dans le dossier `dist/`.

### Options de compilation

Le fichier `setup.py` contient la configuration py2app. Vous pouvez personnaliser :

- **CFBundleName** : Nom de l'application
- **CFBundleIdentifier** : Identifiant unique (format : com.auteur.appname)
- **CFBundleVersion** : Version de l'application
- **iconfile** : Chemin vers une icône .icns (actuellement non défini)

## Structure du projet

```
LastFrame_extract/
├── extract_last_frame.py      # Script Python principal
├── setup.py                    # Configuration py2app
├── pytest.ini                  # Configuration des tests
├── requirements.txt            # Dépendances runtime
├── requirements-dev.txt        # Dépendances développement
├── LICENSE                     # Licence d'utilisation
├── README.md                   # Documentation (format Markdown)
├── tests/                      # Tests automatisés
│   ├── unit/                  # Tests unitaires
│   ├── integration/           # Tests d'intégration
│   └── conftest.py            # Fixtures pytest
├── venv/                       # Environnement virtuel Python (non suivi)
├── build/                      # Fichiers de compilation (non suivi)
└── dist/                       # Application compilée (non suivi)
    └── Video Frame Extractor.app
```

## Dépendances

Voir `requirements.txt` pour les dépendances exactes.

**Runtime** :
- **opencv-python** : Traitement vidéo et extraction de frames
- **Pillow** : Manipulation d'images et affichage
- **numpy** : Calculs numériques (dépendance OpenCV)
- **tkinter** : Interface graphique (inclus avec Python)

**Développement** (voir `requirements-dev.txt`) :
- **pytest** : Framework de tests
- **pytest-cov** : Couverture de code

## Spécifications techniques

- **Langage** : Python 3.13
- **Framework GUI** : tkinter avec style Aqua natif
- **Formats vidéo supportés** : MP4, MOV, M4V, AVI, MKV, MPEG/MPG
- **Format de sortie** : JPEG (qualité 95%)
- **Threading** : Extraction asynchrone pour interface réactive

## Fonctionnement technique

1. **Sélection vidéo** : Utilise `filedialog` de tkinter avec options macOS natives
2. **Lecture métadonnées** : OpenCV lit les propriétés de la vidéo (résolution, FPS, durée)
3. **Extraction frame** : Se positionne sur la dernière frame avec `CAP_PROP_POS_FRAMES`
4. **Conversion couleurs** : Conversion BGR (OpenCV) vers RGB (PIL/tkinter)
5. **Aperçu** : Redimensionnement proportionnel et affichage sur Canvas tkinter
6. **Sauvegarde** : Export JPEG avec paramètre de qualité 95%

## Compatibilité

- **macOS** : Optimisé pour macOS (styles natifs, dialogues adaptés)
- **Autres OS** : Le script Python fonctionne sur Windows/Linux mais l'application .app est spécifique macOS

## Limitations connues

- L'application doit être "autorisée" au premier lancement (sécurité macOS)
- L'application compilée ne fonctionne que sur l'architecture pour laquelle elle a été compilée
- Certains codecs vidéo spécifiques peuvent ne pas être supportés selon l'installation d'OpenCV

## Tests

Le projet inclut une suite de tests automatisés utilisant pytest.

**Exécuter les tests** :
```bash
pytest
```

**Avec couverture de code** :
```bash
pytest --cov
```

Les tests sont organisés en :
- **Tests unitaires** (`tests/unit/`) : Testent les fonctions individuelles
- **Tests d'intégration** (`tests/integration/`) : Testent les workflows complets

## Auteur

Pierre - 2024

## Licence

Usage personnel et éducatif. Voir le fichier [LICENSE](LICENSE) pour les termes complets.

Ce logiciel est fourni pour un usage personnel et éducatif uniquement. L'utilisation commerciale nécessite une autorisation écrite.

## Version

**1.0.0** - Version initiale
- Extraction de la dernière frame
- Interface graphique macOS native
- Aperçu et sauvegarde en JPEG
