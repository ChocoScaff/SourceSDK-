import tkinter as tk
from tkinter import ttk
import os
import subprocess
from texture import Texture
from _vpk import VPK

class File:
    """
    A class to handle file operations within the source SDK environment.
    """

    def __init__(self, sourceSDK) -> None:
        """
        Initialize the File class with a given sourceSDK instance.
        """
        self.sdk = sourceSDK
        self.tree = None

    def list_files(self):
        """
        List all files in the selected folder and game paths with specified extensions.

        Returns:
            files (dict): A dictionary representing the folder structure.
        """
        target_extensions = [".vmf", ".txt", ".cfg", ".vtf", ".vmt", ".qc", ".mdl", ".vcd", ".res", ".bsp", "dir.vpk", ".tga", ".wav", ".mp3"]
        files = {}

        # Walk through the selected folder
        for root, dirs, files_in_dir in os.walk(self.sdk.selected_folder):
            relative_root = os.path.relpath(root, self.sdk.parent_folder)
            file_list = [file for file in files_in_dir if any(file.endswith(ext) for ext in target_extensions)]
            if file_list:
                files[relative_root] = file_list

        # Walk through other game paths
        for game in self.sdk.game_path:
            if self.sdk.game_name != game:
                game_folder = os.path.join(self.sdk.parent_folder, game)
                for root, dirs, files_in_dir in os.walk(game_folder):
                    relative_root = os.path.relpath(root, self.sdk.parent_folder)
                    file_list = [file for file in files_in_dir if any(file.endswith(ext) for ext in target_extensions)]
                    if file_list:
                        if relative_root not in files:
                            files[relative_root] = []
                        files[relative_root].extend(file_list)

        return files

    def display_files(self):
        """
        Display the files in a Tkinter Treeview within a new Toplevel window.
        """
        root = tk.Toplevel()
        root.title("File Explorer")
        root.geometry("600x400")

        files = self.list_files()

        # Create the Treeview widget
        self.tree = ttk.Treeview(root)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Insert folders and files into the Treeview
        for folder, file_list in files.items():
            parent = ""
            for subfolder in folder.split(os.sep):
                if not parent:
                    nodes = self.tree.get_children("")
                    if subfolder in [self.tree.item(node, "text") for node in nodes]:
                        parent = [node for node in nodes if self.tree.item(node, "text") == subfolder][0]
                    else:
                        parent = self.tree.insert("", "end", text=subfolder, open=True)
                else:
                    nodes = self.tree.get_children(parent)
                    if subfolder in [self.tree.item(node, "text") for node in nodes]:
                        parent = [node for node in nodes if self.tree.item(node, "text") == subfolder][0]
                    else:
                        parent = self.tree.insert(parent, "end", text=subfolder, open=True)
            for file_name in file_list:
                self.tree.insert(parent, "end", text=file_name, tags=(folder,))

        # Bind double-click event to open the selected file
        self.tree.bind("<Double-Button-1>", self.open_file)

    def open_file(self, event):
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
        file_path = os.path.join(self.sdk.parent_folder, *file_path_parts)
        file_name, file_extension = os.path.splitext(file_path)
        self.open_file_source_extension(file_extension, file_path, os.path.splitext(file_path_parts[-1])[0])

    def open_file_source_extension(self, file_extension, filepath, file):
        """
        Open a file based on its extension using appropriate methods or applications.

        Args:
            file_extension (str): The file extension to determine the opening method.
            filepath (str): The full path of the file to be opened.
            file (str): The relative path or name of the file for some operations.
        """
        if file_extension == ".vtf":
            texture = Texture(self.sdk)
            texture.open_VTF(filepath)
        elif file_extension == ".mdl":
            command = f'"{self.sdk.bin_folder}/hlmv.exe" "{filepath}"'
            subprocess.Popen(command)
        elif file_extension == ".vmf":
            command = f'"{self.sdk.bin_folder}/hammer.exe" "{filepath}"'
            subprocess.Popen(command)
        elif file_extension == ".vcd":
            command = f'"{self.sdk.bin_folder}/hlfaceposer.exe" "{filepath}"'
            subprocess.Popen(command)
        elif file_extension == ".bsp":
            command = f'"{self.sdk.executable_game}" -game "{self.sdk.selected_folder}" -console -dev -w 1280 -h 720 -sw +sv_cheats 1 +map {file}'
            subprocess.Popen(command)
        elif file_extension == ".vpk":
            vpk = VPK(self.sdk)
            vpk.display_vpk_contents(filepath)
        elif file_extension == ".tga":
            texture = Texture(self.sdk)
            texture.display_tga_file(filepath)
        else:
            try:
                os.startfile(filepath)
            except OSError as e:
                print("Error: Failed to open file:", e)