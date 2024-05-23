import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import subprocess
from texture import Texture
from sourceSDK import SourceSDK
import tempfile

class FileListAppVPK:
    sdk: SourceSDK
    root: tk.Tk

    def __init__(self, sourceSDK, root , vpk_path, files):
        self.sdk = sourceSDK
        self.root = root
        self.current_folder = vpk_path
        self.thumbnails = {}
        self.files = files

        self.create_widgets()
        self.load_files()

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

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

    def load_files(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        columns = int(self.root.winfo_width() / 80)
        if columns < 1:
            columns = 1
        row = 0
        col = 0

        for file in self.files:
            file_path = os.path.join(self.current_folder, file)
            frame = ttk.Frame(self.scroll_frame, width=100, height=100, relief="solid", borderwidth=1)
            frame.grid_propagate(False)
            frame.grid(row=row, column=col, padx=5, pady=5)

            label = ttk.Label(frame, text=file, wraplength=130, anchor="center")
            label.place(relx=0.5, rely=0.1, anchor='center')

            thumbnail = self.load_thumbnail(file_path)
            if thumbnail:
                thumbnail_label = ttk.Label(frame, image=thumbnail)
                thumbnail_label.image = thumbnail  # Keep a reference to avoid garbage collection
                thumbnail_label.place(relx=0.5, rely=0.55, anchor='center')

            if file_path.endswith("/"):  # Assuming directories end with a slash in the list
                label.bind("<Double-Button-1>", lambda e, path=file_path: self.load_files(path))
            else:
                label.bind("<Double-Button-1>", lambda e, path=file_path: self.open_file_in_vpk(path))

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
            elif file_path.endswith(".txt") or file_path.endswith(".res") or file_path.endswith(".vmt") or file_path.endswith(".qc") or file_path.endswith(".smd"):
                image = Image.open(os.path.join(base_path, "icons", "txt.png"))

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
        if parent_dir:
            self.load_files(parent_dir)

    def open_file_in_vpk(self, event):
        """
        Open the selected file from the Treeview.
        """
        selected_item = self.tree.selection()[0]
        item_text = self.tree.item(selected_item, "text")
        parent_item = self.tree.parent(selected_item)
        file_path_parts = [item_text]

        while parent_item:
            item_text = self.tree.item(parent_item, "text")
            file_path_parts.append(item_text)
            parent_item = self.tree.parent(parent_item)

        file_path_parts.reverse()
        file_path = "/".join(file_path_parts)  # Use '/' as VPK paths use forward slashes
        self.extract_and_open_file_in_vpk(file_path)

    def extract_and_open_file_in_vpk(self, file_name):
        """
        Extract and open a file from the VPK archive.
        """
        if not self.vpk_file:
            print("VPK file is not loaded.")
            return

        related_extensions = [".dx80.vtx", ".dx90.vtx", ".sw.vtx", ".phy", ".vvd"]
        temp_dir = tempfile.mkdtemp()

        def extract_file(path):
            pakfile = self.vpk_file.get_file(path)
            if pakfile:
                file_content = pakfile.read()
                temp_file_path = os.path.join(temp_dir, os.path.basename(path))
                with open(temp_file_path, 'wb') as temp_file:
                    temp_file.write(file_content)
                return temp_file_path
            return None

        # Extract the primary file
        primary_temp_path = extract_file(file_name)
        if not primary_temp_path:
            print(f"File {file_name} not found in VPK.")
            return

        # Extract related files for .mdl if required
        if file_name.endswith(".mdl"):
            base_name = os.path.splitext(file_name)[0]
            related_files = []
            for ext in related_extensions:
                related_temp_path = extract_file(base_name + ext)
                if related_temp_path:
                    related_files.append(related_temp_path)

            # Ensure all required files are present
            if len(related_files) != len(related_extensions):
                print(f"Missing related files for {file_name}.")
                return

        # Open the file with the appropriate application
        file_name, file_extension = os.path.splitext(primary_temp_path)

        if file_extension == ".vtf":
            texture = Texture(self.sdk)
            texture.open_VTF(primary_temp_path)
        elif file_extension == ".mdl":
            command = f'"{self.sdk.bin_folder}/hlmv.exe" "{primary_temp_path}"'
            subprocess.Popen(command)
        elif file_extension == ".vcd":
            command = f'"{self.sdk.bin_folder}/hlfaceposer.exe" "{primary_temp_path}"'
            subprocess.Popen(command)
        else:
            try:
                os.startfile(primary_temp_path)
            except Exception as e:
                print(f"Failed to open file {primary_temp_path}: {e}")