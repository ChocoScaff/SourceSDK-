import tkinter as tk
from tkinter import ttk
import os
from fileListApp import FileListApp
from open import Open

class File:
    """
    A class to handle file operations within the source SDK environment.
    """

    fileList : FileListApp
    root : tk.Tk

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

        self.root = tk.Toplevel(self.sdk.root)
        self.root.title("Contents")
        self.root.geometry("1250x800")

        # Search Label and Entry
        search_frame = tk.Frame(self.root)
        search_frame.pack(fill="x", padx=10, pady=5)
        search_label = tk.Label(search_frame, text="Search:")
        search_label.pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(fill="x", expand=True, side="left")
        self.search_entry.bind("<KeyRelease>", self.search_files)

        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(frame)
        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.config(yscrollcommand=scrollbar.set)

        self.tree.heading("#0", text="Contents", anchor='w')

        files = self.list_files()

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

        self.fileList = FileListApp(self.sdk, self.root)

    def open_file(self, event):
        """
        Open the selected file from the Treeview.
        """
        open = Open(self.sdk)
        open.open_file_with_tree(tree=self.tree, fileList=self.fileList)
        

    def search_files(self, event=None):
        """
        Display only files in the Treeview that contain the search text.
        """
        search_text = self.search_entry.get().lower()
        if search_text:
            self.clear_selections()  # Clear previous selections
            self.search_tree(self.tree.get_children(), search_text)
        else:
            self.clear_selections()  # Clear selections if search text is empty

    def search_tree(self, items, search_text):
        """
        Recursively search through the tree and select items containing the search text.

        Args:
            items (list): A list of items in the tree.
            search_text (str): The text to search for.
        """
        for item in items:
            item_text = self.tree.item(item, "text").lower()
            if search_text in item_text:
                self.tree.selection_add(item)
                self.tree.focus(item)
                self.tree.see(item)
            self.search_tree(self.tree.get_children(item), search_text)  # Recursively search subitems
    
    def clear_selections(self):
        """
        Clear all selections in the Treeview.
        """
        for item in self.tree.selection():
            self.tree.selection_remove(item)
