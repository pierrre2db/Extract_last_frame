#!/usr/bin/env python3
"""
Extracteur de dernière frame vidéo vers JPEG avec interface graphique
Supporte MP4, MOV, M4V, AVI, MKV, MPEG
Compatible macOS
"""

import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import os
from PIL import Image, ImageTk
import threading
import platform

class VideoFrameExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Extracteur de frame vidéo")

        # Configuration spécifique macOS
        self.is_macos = platform.system() == 'Darwin'
        if self.is_macos:
            self.root.geometry("900x750")
            # Utiliser le style natif macOS
            try:
                self.root.tk.call('tk::unsupported::MacWindowStyle', 'style',
                                 self.root._w, 'document', 'closeBox collapseBox resizable')
            except:
                pass
        else:
            self.root.geometry("900x700")

        self.root.resizable(True, True)

        self.video_path = None
        self.output_path = None
        self.last_save_dir = str(Path.home() / "Downloads")
        self.preview_image = None
        self.current_frame_number = 0
        self.total_frames = 0
        self.video_fps = 0

        self.create_widgets()

    def create_widgets(self):
        # Style pour macOS
        style = ttk.Style()
        if self.is_macos:
            style.theme_use('aqua')

        # Frame principale avec padding adapté
        padding_size = "15" if self.is_macos else "10"
        main_frame = ttk.Frame(self.root, padding=padding_size)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configuration du redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # Titre
        title_label = ttk.Label(main_frame, text="🎬 Extracteur de frame vidéo",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 20))

        # Section sélection vidéo
        video_frame = ttk.LabelFrame(main_frame, text="1. Sélectionner la vidéo", padding="10")
        video_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        video_frame.columnconfigure(1, weight=1)

        self.video_label = ttk.Label(video_frame, text="Aucune vidéo sélectionnée")
        self.video_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        ttk.Button(video_frame, text="📂 Parcourir...",
                  command=self.select_video).grid(row=1, column=0, padx=5)

        self.video_info_label = ttk.Label(video_frame, text="", foreground="gray")
        self.video_info_label.grid(row=1, column=1, sticky=tk.W, padx=10)

        # Section navigation vidéo
        nav_frame = ttk.LabelFrame(main_frame, text="2. Naviguer dans la vidéo", padding="10")
        nav_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        nav_frame.columnconfigure(0, weight=1)

        # Slider de navigation
        slider_container = ttk.Frame(nav_frame)
        slider_container.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(5, 10))
        slider_container.columnconfigure(0, weight=1)

        self.frame_slider = ttk.Scale(slider_container, from_=0, to=100, orient=tk.HORIZONTAL,
                                      command=self.on_slider_change, state=tk.DISABLED)
        self.frame_slider.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5)

        # Indicateur de position
        self.frame_position_label = ttk.Label(nav_frame, text="Frame: 0 / 0 (0.0s)", foreground="gray")
        self.frame_position_label.grid(row=1, column=0, pady=(0, 10))

        # Boutons de navigation
        button_container = ttk.Frame(nav_frame)
        button_container.grid(row=2, column=0, pady=(0, 5))

        self.prev_frame_btn = ttk.Button(button_container, text="◀ Frame précédente",
                                         command=self.previous_frame, state=tk.DISABLED)
        self.prev_frame_btn.grid(row=0, column=0, padx=5)

        self.next_frame_btn = ttk.Button(button_container, text="Frame suivante ▶",
                                         command=self.next_frame, state=tk.DISABLED)
        self.next_frame_btn.grid(row=0, column=1, padx=5)

        self.goto_last_btn = ttk.Button(button_container, text="⏭ Dernière frame",
                                        command=self.goto_last_frame, state=tk.DISABLED)
        self.goto_last_btn.grid(row=0, column=2, padx=5)

        # Section extraction
        extract_frame = ttk.LabelFrame(main_frame, text="3. Extraire l'image", padding="10")
        extract_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        extract_frame.columnconfigure(0, weight=1)

        self.extract_btn = ttk.Button(extract_frame, text="🎯 Extraire la frame actuelle",
                                     command=self.extract_frame, state=tk.DISABLED)
        self.extract_btn.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))

        self.progress = ttk.Progressbar(extract_frame, mode='indeterminate')
        self.progress.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        # Section aperçu
        preview_frame = ttk.LabelFrame(main_frame, text="4. Aperçu de l'image", padding="10")
        preview_frame.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(0, weight=1)

        # Canvas pour l'aperçu avec scrollbar
        canvas_frame = ttk.Frame(preview_frame)
        canvas_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        canvas_frame.columnconfigure(0, weight=1)
        canvas_frame.rowconfigure(0, weight=1)

        self.preview_canvas = tk.Canvas(canvas_frame, bg="gray20", height=300)
        self.preview_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.preview_text = ttk.Label(preview_frame,
                                     text="L'aperçu de l'image apparaîtra ici après l'extraction",
                                     foreground="gray")
        self.preview_text.grid(row=0, column=0)

        # Section sauvegarde
        save_frame = ttk.LabelFrame(main_frame, text="5. Sauvegarder", padding="10")
        save_frame.grid(row=5, column=0, sticky=(tk.W, tk.E))
        save_frame.columnconfigure(0, weight=1)

        self.save_btn = ttk.Button(save_frame, text="💾 Sauvegarder l'image",
                                   command=self.save_image, state=tk.DISABLED)
        self.save_btn.grid(row=0, column=0, pady=5, sticky=(tk.W, tk.E))

        self.save_info_label = ttk.Label(save_frame, text="", foreground="green")
        self.save_info_label.grid(row=1, column=0, sticky=tk.W)

    def select_video(self):
        # Dialogue de sélection avec options macOS
        if self.is_macos:
            filename = filedialog.askopenfilename(
                title="Sélectionner une vidéo",
                filetypes=[
                    ("Fichiers vidéo", "*.mp4 *.MP4 *.mov *.MOV *.m4v *.M4V *.avi *.AVI *.mkv *.MKV *.mpeg *.MPEG *.mpg *.MPG"),
                    ("MP4", "*.mp4 *.MP4"),
                    ("MOV (QuickTime)", "*.mov *.MOV"),
                    ("M4V (Apple)", "*.m4v *.M4V"),
                    ("AVI", "*.avi *.AVI"),
                    ("MKV", "*.mkv *.MKV"),
                    ("MPEG", "*.mpeg *.MPEG *.mpg *.MPG"),
                    ("Tous les fichiers", "*.*")
                ],
                message="Choisissez une vidéo"
            )
        else:
            filename = filedialog.askopenfilename(
                title="Sélectionner une vidéo",
                filetypes=[
                    ("Fichiers vidéo", "*.mp4 *.mov *.m4v *.avi *.mkv *.mpeg *.mpg"),
                    ("MP4", "*.mp4"),
                    ("MOV", "*.mov"),
                    ("M4V", "*.m4v"),
                    ("AVI", "*.avi"),
                    ("MKV", "*.mkv"),
                    ("MPEG", "*.mpeg *.mpg"),
                    ("Tous les fichiers", "*.*")
                ]
            )

        if filename:
            self.video_path = filename
            self.video_label.config(text=f"📹 {os.path.basename(filename)}")
            self.extract_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.DISABLED)
            self.output_path = None
            self.save_info_label.config(text="")

            # Afficher les infos de la vidéo
            self.show_video_info()

            # Cacher l'aperçu précédent
            self.preview_canvas.delete("all")
            self.preview_text.grid(row=0, column=0)

    def show_video_info(self):
        try:
            cap = cv2.VideoCapture(self.video_path)
            if cap.isOpened():
                self.video_fps = cap.get(cv2.CAP_PROP_FPS)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                self.total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                duration = self.total_frames / self.video_fps if self.video_fps > 0 else 0

                info_text = f"{width}x{height} | {duration:.1f}s | {int(self.video_fps)} FPS"
                self.video_info_label.config(text=info_text)

                # Configurer le slider de navigation
                if self.total_frames > 0:
                    self.frame_slider.config(from_=0, to=self.total_frames - 1, state=tk.NORMAL)
                    self.current_frame_number = 0
                    self.frame_slider.set(0)

                    # Activer les boutons de navigation
                    self.next_frame_btn.config(state=tk.NORMAL)
                    self.goto_last_btn.config(state=tk.NORMAL)
                    self.prev_frame_btn.config(state=tk.DISABLED)  # Déjà à la frame 0

                    # Mettre à jour l'indicateur de position
                    self.update_frame_info()

                # Extraire et afficher la première frame comme aperçu
                ret, first_frame = cap.read()
                if ret:
                    # Convertir BGR vers RGB pour PIL
                    first_frame_rgb = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)
                    # Afficher l'aperçu de la première frame
                    self.show_preview(first_frame_rgb, is_first_frame=True)

                cap.release()
        except Exception as e:
            self.video_info_label.config(text="Erreur lors de la lecture des infos")

    def update_frame_info(self):
        """Met à jour l'indicateur de position de la frame"""
        if self.total_frames > 0 and self.video_fps > 0:
            time_seconds = self.current_frame_number / self.video_fps
            self.frame_position_label.config(
                text=f"Frame: {self.current_frame_number + 1} / {self.total_frames} ({time_seconds:.2f}s)"
            )

    def load_frame_at_position(self, frame_number):
        """Charge et affiche la frame à la position donnée"""
        try:
            cap = cv2.VideoCapture(self.video_path)
            if not cap.isOpened():
                return False

            # Se positionner à la frame demandée
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

            # Lire la frame
            ret, frame = cap.read()
            cap.release()

            if ret:
                # Convertir BGR vers RGB pour PIL
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Stocker la frame pour extraction ultérieure
                self.current_frame = frame

                # Afficher l'aperçu (sans le badge "première frame")
                self.show_preview(frame_rgb, is_first_frame=False)

                # Mettre à jour la position actuelle
                self.current_frame_number = frame_number
                self.update_frame_info()

                # Gérer l'état des boutons
                self.prev_frame_btn.config(
                    state=tk.NORMAL if frame_number > 0 else tk.DISABLED
                )
                self.next_frame_btn.config(
                    state=tk.NORMAL if frame_number < self.total_frames - 1 else tk.DISABLED
                )

                return True

        except Exception as e:
            print(f"Erreur lors du chargement de la frame: {e}")
            return False

    def on_slider_change(self, value):
        """Appelée quand le slider est déplacé"""
        frame_number = int(float(value))
        self.load_frame_at_position(frame_number)

    def previous_frame(self):
        """Aller à la frame précédente"""
        if self.current_frame_number > 0:
            new_frame = self.current_frame_number - 1
            self.frame_slider.set(new_frame)
            self.load_frame_at_position(new_frame)

    def next_frame(self):
        """Aller à la frame suivante"""
        if self.current_frame_number < self.total_frames - 1:
            new_frame = self.current_frame_number + 1
            self.frame_slider.set(new_frame)
            self.load_frame_at_position(new_frame)

    def goto_last_frame(self):
        """Aller directement à la dernière frame"""
        if self.total_frames > 0:
            last_frame = self.total_frames - 1
            self.frame_slider.set(last_frame)
            self.load_frame_at_position(last_frame)

    def extract_frame(self):
        if not self.video_path:
            return

        # Démarrer l'extraction dans un thread séparé
        self.extract_btn.config(state=tk.DISABLED)
        self.progress.start(10)

        thread = threading.Thread(target=self.do_extraction)
        thread.daemon = True
        thread.start()

    def do_extraction(self):
        try:
            cap = cv2.VideoCapture(self.video_path)

            if not cap.isOpened():
                self.root.after(0, lambda: messagebox.showerror("Erreur",
                    "Impossible d'ouvrir la vidéo"))
                return

            # Se positionner à la frame actuelle (définie par le slider)
            cap.set(cv2.CAP_PROP_POS_FRAMES, self.current_frame_number)

            # Lire la frame actuelle
            ret, frame = cap.read()
            cap.release()

            if not ret:
                self.root.after(0, lambda: messagebox.showerror("Erreur",
                    f"Impossible de lire la frame {self.current_frame_number + 1}"))
                return

            # Convertir BGR vers RGB pour PIL
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Stocker la frame pour la sauvegarde ultérieure
            self.current_frame = frame

            # Créer l'aperçu
            self.root.after(0, lambda: self.show_preview(frame_rgb, is_first_frame=False))

        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Erreur", str(e)))
        finally:
            self.root.after(0, self.extraction_complete)

    def show_preview(self, frame_rgb, is_first_frame=False):
        # Cacher le texte de placeholder
        self.preview_text.grid_remove()

        # Créer l'image PIL
        pil_image = Image.fromarray(frame_rgb)

        # Redimensionner pour l'aperçu (max 800x400)
        canvas_width = self.preview_canvas.winfo_width()
        if canvas_width <= 1:
            canvas_width = 800

        max_height = 400
        ratio = min(canvas_width / pil_image.width, max_height / pil_image.height)
        new_width = int(pil_image.width * ratio)
        new_height = int(pil_image.height * ratio)

        pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convertir pour tkinter
        self.preview_image = ImageTk.PhotoImage(pil_image)

        # Afficher sur le canvas
        self.preview_canvas.delete("all")
        self.preview_canvas.config(width=new_width, height=new_height)

        # Afficher l'image
        self.preview_canvas.create_image(0, 0, anchor=tk.NW, image=self.preview_image)

        # Ajouter un texte indicatif si c'est la première frame (aperçu)
        if is_first_frame:
            # Ajouter un texte "APERÇU - Première frame" en haut à gauche
            self.preview_canvas.create_rectangle(5, 5, 220, 35, fill='black', stipple='gray50')
            self.preview_canvas.create_text(10, 20, anchor=tk.W,
                                           text="APERÇU - Première frame",
                                           fill='yellow', font=('Arial', 12, 'bold'))

    def extraction_complete(self):
        self.progress.stop()
        self.extract_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.NORMAL)

    def save_image(self):
        if not hasattr(self, 'current_frame'):
            return

        # Générer le nom par défaut
        video_name = Path(self.video_path).stem
        default_name = f"{video_name}_last_frame.jpg"

        # Dialogue de sauvegarde adapté macOS
        if self.is_macos:
            filename = filedialog.asksaveasfilename(
                title="Sauvegarder l'image",
                initialdir=self.last_save_dir,
                initialfile=default_name,
                defaultextension=".jpg",
                filetypes=[("JPEG", "*.jpg *.jpeg"), ("Tous les fichiers", "*.*")],
                message="Enregistrer l'image extraite"
            )
        else:
            filename = filedialog.asksaveasfilename(
                title="Sauvegarder l'image",
                initialdir=self.last_save_dir,
                initialfile=default_name,
                defaultextension=".jpg",
                filetypes=[("JPEG", "*.jpg"), ("Tous les fichiers", "*.*")]
            )

        if filename:
            try:
                # Sauvegarder avec qualité 95%
                cv2.imwrite(filename, self.current_frame,
                           [cv2.IMWRITE_JPEG_QUALITY, 95])

                # Mémoriser le répertoire
                self.last_save_dir = str(Path(filename).parent)
                self.output_path = filename

                file_size = os.path.getsize(filename) / 1024
                self.save_info_label.config(
                    text=f"✅ Image sauvegardée: {os.path.basename(filename)} ({file_size:.1f} KB)"
                )

                messagebox.showinfo("Succès",
                    f"Image sauvegardée avec succès!\n\n{filename}")

            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde:\n{e}")

def main():
    root = tk.Tk()

    # Configuration spécifique macOS
    if platform.system() == 'Darwin':
        # Apporter l'application au premier plan sur macOS
        root.lift()
        root.attributes('-topmost', True)
        root.after_idle(root.attributes, '-topmost', False)

    app = VideoFrameExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
