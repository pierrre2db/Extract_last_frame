"""
Configuration py2app pour créer l'application macOS
"""
from setuptools import setup

APP = ['extract_last_frame.py']
DATA_FILES = []

OPTIONS = {
    'argv_emulation': True,
    'packages': ['cv2', 'PIL', 'numpy', 'tkinter'],
    'includes': ['tkinter', 'tkinter.filedialog', 'tkinter.messagebox', 'tkinter.ttk',
                 '_tkinter', 'threading', 'platform'],
    'iconfile': None,  # Vous pouvez ajouter un fichier .icns ici
    'plist': {
        'CFBundleName': 'Video Frame Extractor',
        'CFBundleDisplayName': 'Video Frame Extractor',
        'CFBundleGetInfoString': "Extracteur de dernière frame vidéo",
        'CFBundleIdentifier': "com.pierre.videoframeextractor",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "© 2024 Pierre",
        'NSHighResolutionCapable': True,
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
