import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from open import Open

class FileListApp:
    def __init__(self, sourceSDK, root):
        """
        """
        self.sdk = sourceSDK
        self.root = tk.Frame(root, width=1000, height=600)
        self.root.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

        self.current_folder = self.sdk.selected_folder
        self.first_folder = self.sdk.selected_folder
        self.thumbnails = {}

        self.create_widgets()
        self.load_files(self.current_folder)

        self.previous_width = None

    def create_widgets(self):
        """
        """
        self.up_button = ttk.Button(self.root, text="Up", command=self.go_up)
        self.up_button.pack(side="top", pady=5)

        self.open_dir_button = ttk.Button(self.root, text="Open Directory", command=self.open_directory)
        self.open_dir_button.pack(side="top", pady=5)

        self.canvas = tk.Canvas(self.root, bg='white')
        self.scroll_y = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll_y.set)

        self.scroll_frame = ttk.Frame(self.canvas)
        self.scroll_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        # Bind mouse wheel events to the canvas
        self.canvas.bind("<Enter>", self.bind_mouse_wheel)
        self.canvas.bind("<Leave>", self.unbind_mouse_wheel)

    def bind_mouse_wheel(self, event):
        """
        """
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def unbind_mouse_wheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def on_mouse_wheel(self, event):
        """
        """
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def load_files(self, folder):
        """
        """
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.current_folder = folder
        self.files = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f)) or f.endswith(
            (".vmf", ".txt", ".cfg", ".vtf", ".vmt", ".qc", ".mdl", ".vcd", ".res", ".bsp", "dir.vpk", ".tga", ".wav", ".mp3", ".sln", ".bik", ".bat"))]

        columns = max(1, int(self.root.winfo_width() / 150))
        row = col = 0

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
                bind_func = lambda e, path=file_path: self.load_files(path)
            else:
                bind_func = lambda e, path=file_path: self.open_file(path)

            frame.bind("<Double-Button-1>", bind_func)
            label.bind("<Double-Button-1>", bind_func)
            if thumbnail:
                thumbnail_label.bind("<Double-Button-1>", bind_func)

            col += 1
            if col >= columns:
                col = 0
                row += 1

        self.canvas.yview_moveto(0.0)

        # Bind the <Configure> event to handle resizing
        self.root.bind("<Configure>", self.resize)

        # Initialize the previous width
        self.previous_width = self.root.winfo_width()

    def load_thumbnail(self, file_path):
        """
        """
        try:
            image = None
            base_path = os.path.dirname(os.path.abspath(__file__))

            file_icons = {
                ".vtf": "VTFEdit.png",
                ".mdl": "hlmv.png",
                ".tga": None,
                ".vmf": "hammer.png",
                ".vcd": "hlposer.png",
                ".bsp": "source.png",
                ".txt": "txt.png",
                ".res": "txt.png",
                ".vmt": "txt.png",
                ".qc": "txt.png",
                ".smd": "txt.png",
                ".cfg": "txt.png",
                ".sln": "Visual_Studio.png"
            }

            ext = os.path.splitext(file_path)[1]
            if ext in file_icons:
                if file_icons[ext]:
                    image = Image.open(os.path.join(base_path, "icons", file_icons[ext]))
                else:
                    image = Image.open(file_path)
            elif os.path.isdir(file_path):
                image = Image.open(os.path.join(base_path, "icons", "fileexplorer.png"))

            if image:
                image.thumbnail((50, 50))
                thumbnail = ImageTk.PhotoImage(image)
                self.thumbnails[file_path] = thumbnail
                return thumbnail

        except Exception as e:
            print("Error loading thumbnail:", e)
        return None

    def go_up(self):
        """
        """
        parent_dir = os.path.dirname(self.current_folder)
        if parent_dir:
            self.load_files(parent_dir)

    def open_directory(self):
        """
        """
        open_instance = Open(self.sdk)
        open_instance.open_directory(self.current_folder)

    def open_file(self, pathFile):
        """
        """
        open_instance = Open(self.sdk)
        open_instance.open_file(localpath=pathFile)
    
    def resize(self, event):
        """
        Handle the window resize event.
        """
        new_width = self.root.winfo_width()
        if new_width != self.previous_width:
            self.previous_width = new_width
            # Add the code you want to execute when the width changes
            self.load_files(self.current_folder)