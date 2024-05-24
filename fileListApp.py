import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from sourceSDK import SourceSDK
from open import Open

class FileListApp:
    sdk: SourceSDK
    root: tk.Tk

    def __init__(self, sourceSDK, root):
        self.sdk = sourceSDK
        self.root = root
        self.current_folder = self.sdk.selected_folder
        self.firstfolder = self.sdk.selected_folder
        self.thumbnails = {}

        self.create_widgets()
        self.load_files(self.current_folder)

    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, bg='white')
        self.scroll_y = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)

        self.scroll_frame = ttk.Frame(self.canvas)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.up_button = ttk.Button(self.root, text="Up", command=self.go_up)
        self.up_button.pack(pady=5)

        self.open_dir_button = ttk.Button(self.root, text="Open Directory", command=self.open_directory)
        self.open_dir_button.pack(pady=5)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

    def load_files(self, folder):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.current_folder = folder
        self.files = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f)) or f.endswith((
            ".vmf", ".txt", ".cfg", ".vtf", ".vmt", ".qc", ".mdl", ".vcd", ".res", ".bsp", "dir.vpk", ".tga", ".wav", ".mp3", ".sln"))]

        columns = int(self.root.winfo_width() / 150)
        if columns < 1:
            columns = 1
        row = 0
        col = 0

        for file in self.files:
            file_path = os.path.join(self.current_folder, file)
            frame = ttk.Frame(self.scroll_frame, width=140, height=140, relief="solid", borderwidth=1)
            frame.grid_propagate(False)
            frame.grid(row=row, column=col, padx=5, pady=5)

            label = ttk.Label(frame, text=file, wraplength=130, anchor="center")
            label.place(relx=0.5, rely=0.1, anchor='center')

            thumbnail = self.load_thumbnail(file_path)
            if thumbnail:
                thumbnail_label = ttk.Label(frame, image=thumbnail)
                thumbnail_label.image = thumbnail  # Keep a reference to avoid garbage collection
                thumbnail_label.place(relx=0.5, rely=0.55, anchor='center')

            if os.path.isdir(file_path):
                frame.bind("<Double-Button-1>", lambda e, path=file_path: self.load_files(path))
                label.bind("<Double-Button-1>", lambda e, path=file_path: self.load_files(path))
                if thumbnail:
                    thumbnail_label.bind("<Double-Button-1>", lambda e, path=file_path: self.load_files(path))
            else:
                frame.bind("<Double-Button-1>", lambda e, path=file_path: self.open_file(path))
                label.bind("<Double-Button-1>", lambda e, path=file_path: self.open_file(path))
                if thumbnail:
                    thumbnail_label.bind("<Double-Button-1>", lambda e, path=file_path: self.open_file(path))

            col += 1
            if col >= columns:
                col = 0
                row += 1

        self.canvas.yview_moveto(0.0)

    def load_thumbnail(self, file_path):
        try:
            image = None
            base_path = os.path.dirname(os.path.abspath(__file__))

            if file_path.endswith(".vtf"):
                image = Image.open(os.path.join(base_path, "icons", "VTFEdit.png"))
            elif file_path.endswith(".mdl"):
                image = Image.open(os.path.join(base_path, "icons", "hlmv.png"))
            elif file_path.endswith(".tga"):
                image = Image.open(file_path)
            elif file_path.endswith(".vmf"):
                image = Image.open(os.path.join(base_path, "icons", "hammer.png"))
            elif file_path.endswith(".vcd"):
                image = Image.open(os.path.join(base_path, "icons", "hlposer.png"))
            elif file_path.endswith(".bsp"):
                image = Image.open(os.path.join(base_path, "icons", "source.png"))
            elif os.path.isdir(file_path):
                image = Image.open(os.path.join(base_path, "icons", "fileexplorer.png"))
            elif file_path.endswith(".txt") or file_path.endswith(".res") or file_path.endswith(".vmt") or file_path.endswith(".qc") or file_path.endswith(".smd") or file_path.endswith(".cfg"):
                image = Image.open(os.path.join(base_path, "icons", "txt.png"))
            elif file_path.endswith(".sln"):
                image = Image.open(os.path.join(base_path, "icons", "Visual_Studio.png"))

            if image:
                image.thumbnail((50, 50))
                thumbnail = ImageTk.PhotoImage(image)
                self.thumbnails[file_path] = thumbnail
                return thumbnail

        except Exception as e:
            print("Error loading thumbnail:", e)
        return None

    def go_up(self):
        parent_dir = os.path.dirname(self.current_folder)
        if parent_dir and self.current_folder != self.firstfolder:
            self.load_files(parent_dir)

    def open_directory(self):
        open_instance = Open(self.sdk)
        open_instance.open_directory(self.current_folder)

    def open_file(self, pathFile):
        open_instance = Open(self.sdk)
        open_instance.open_file(localpath=pathFile)

