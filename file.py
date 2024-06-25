import tkinter as tk
from tkinter import ttk
import os
from open import Open  # Assuming this is your custom module
from PIL import Image, ImageTk
from model import Model
from texture import Texture
from map import Map
from decompiler import Decompiler

class File:
    """
    A class to handle file operations within the source SDK environment.
    """

    root: tk.Tk

    def __init__(self, sourceSDK) -> None:
        """
        Initialize the File class with a given sourceSDK instance.
        """
        self.sdk = sourceSDK
        self.tree = None
        self.thumbnails = {}            
        self.init_grid = False

    def list_files(self):
        """
        List all files in the selected folder and game paths with specified extensions.

        Returns:
            files (dict): A dictionary representing the folder structure.
        """
        target_extensions = [".vmf", ".txt", ".cfg", ".vtf", ".vmt", ".qc", ".mdl", ".vcd", ".res", ".bsp", "dir.vpk", ".tga", ".wav", ".mp3", ".sln", ".bik", ".bat"]
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

    def display_files_tree(self):
        """
        Display the files in a Tkinter Treeview within a new Toplevel window.
        """
        self.main_root = tk.Toplevel(self.sdk.root)
        self.main_root.title("File Explorer")
        self.main_root.geometry("1400x600")

        self.root = tk.Frame(self.main_root, width=200, height=600)
        self.root.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")

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
                        parent = self.tree.insert("", "end", text=subfolder, open=False)
                else:
                    nodes = self.tree.get_children(parent)
                    if subfolder in [self.tree.item(node, "text") for node in nodes]:
                        parent = [node for node in nodes if self.tree.item(node, "text") == subfolder][0]
                    else:
                        parent = self.tree.insert(parent, "end", text=subfolder, open=False)
            
            for file_name in file_list:
                parent_folder_path = os.path.join(self.sdk.parent_folder, folder)  # Define parentFolder
                
                self.tree.insert(parent, "end", text=file_name, tags=(folder,))
                """
                thumbnail = self.load_thumbnail(file_name, parent_folder_path)
                if thumbnail:
                    self.tree.insert(parent, "end", text=file_name, image=thumbnail, tags=(folder,))
                else:
                    self.tree.insert(parent, "end", text=file_name, tags=(folder,))
                """
            
        # Bind double-click event to open the selected file
        self.tree.bind("<Double-Button-1>", self.open_file)
        self.tree.bind("<Button-3>", self.show_context_menu)

        self.load_files_grid_tree(self.sdk.selected_folder)

        # Set the minimum size of the cells in the grid to fit the frames
        self.main_root.grid_rowconfigure(0, weight=1)
        self.main_root.grid_columnconfigure(0, weight=1)
        self.main_root.grid_columnconfigure(1, weight=4)

    def open_file(self, event=None, pathFile=None):
        """
        Open the selected file from the Treeview.
        """
        open = Open(self.sdk)
        if pathFile is None:
            value = open.open_file_with_tree(tree=self.tree)
            if value is not None:
                self.load_files_grid_tree(value)
        else:
            open.open_file(localpath=pathFile)

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

    def load_thumbnail(self, file_path, parent=""):
        """
        Load the appropriate thumbnail for a given file path.

        Args:
            file_path (str): The path to the file.

        Returns:
            ImageTk.PhotoImage: The thumbnail image.
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
                ".sln": "Visual_Studio.png",
                ".wav": "audio.png",
                ".mp3": "audio.png",
                ".bik": "video.png",
                ".bat": "terminal.png"
            }

            file_name, file_extension = os.path.splitext(file_path)

            if file_extension in file_icons:
                if file_icons[file_extension]:
                    image = Image.open(os.path.join(base_path, "icons", file_icons[file_extension]))
                else:
                    image = Image.open(parent + "/" + file_path)
            elif os.path.isdir(file_path):
                image = Image.open(os.path.join(base_path, "icons", "fileexplorer.png"))
            

            if image:
                image.thumbnail((100, 100))
                thumbnail = ImageTk.PhotoImage(image)
                self.thumbnails[file_path] = thumbnail
                return thumbnail

        except Exception as e:
            print("Error loading thumbnail:", e)
        return None

    def show_context_menu(self, event, file_path=None):
        """
        Show the context menu on right-click.
        """
        if file_path is None:
            selected_item = self.tree.identify_row(event.y)
                
            if selected_item:
                self.tree.selection_set(selected_item)

                filename = self.tree.item(selected_item, 'text')
                print(filename)

                parent_item = self.tree.parent(selected_item)
                
                file_path_parts = [filename]

                while parent_item:
                    item_text = self.tree.item(parent_item, "text")
                    file_path_parts.append(item_text)
                    parent_item = self.tree.parent(parent_item)

                file_path_parts.reverse()
                file_path = os.path.join(self.sdk.parent_folder, *file_path_parts)

        else:
            file_name, file_extension = os.path.splitext(file_path)

        self.context_menu = tk.Menu(self.root, tearoff=0)

        if file_extension == ".qc":
            model = Model(self.sdk)
            self.context_menu.add_command(label="Compile Model", command=lambda: model.build_model(file_path))
        elif file_extension == ".tga":
            texture = Texture(self.sdk)
            self.context_menu.add_command(label="Compile Texture", command=lambda: texture.build_texture(file_path))
        elif file_extension == ".vmf":
            map = Map(self.sdk)
            self.context_menu.add_command(label="Compile Map", command=lambda: map.build_map(file_path))
        elif file_extension == ".mdl":
            decompiler = Decompiler(self.sdk)
            self.context_menu.add_command(label="Decompile Model", command=lambda: decompiler.decompiler_file(file=file_path))
        elif file_extension == ".vtf":
            texture = Texture(self.sdk)
            self.context_menu.add_command(label="Compile to tga", command=lambda: texture.texture_to_tga(file_path)) 

        self.context_menu.add_command(label="Delete", command=lambda: self.delete_file(file_path))

        self.context_menu.post(event.x_root, event.y_root)

    def delete_file(self, file_path, tree_item):
        """
        Delete the specified file and update the Treeview.
        """
        try:
            os.remove(file_path)
            self.tree.delete(tree_item)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error deleting file: {e}")
        
        self.load_files_grid_tree(self.current_folder)

    def load_files_grid_tree(self, folder):
        """
        Load the files in the grid view within the selected folder.
        """
        if self.init_grid == False:
            self.root = tk.Frame(self.main_root, width=1000, height=600)
            self.root.grid(row=0, column=1, padx=0, pady=0, sticky="nsew")

            self.current_folder = self.sdk.selected_folder
            self.thumbnails = {}

            self.create_widgets()

            self.previous_width = None

            self.init_grid = True

        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        self.current_folder = folder
        self.files = [f for f in os.listdir(self.current_folder) if os.path.isdir(os.path.join(self.current_folder, f)) or f.endswith(
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
            if (thumbnail):
                thumbnail_label = ttk.Label(frame, image=thumbnail)
                thumbnail_label.image = thumbnail  # Keep a reference to avoid garbage collection
                thumbnail_label.place(relx=0.5, rely=0.55, anchor='center')

            if os.path.isdir(file_path):
                bind_func = lambda e, path=file_path: self.load_files_grid_tree(path)
                bind_right = lambda e, path=file_path: self.show_context_menu(e, path)
            else:
                bind_func = lambda e, path=file_path: self.open_file(pathFile=path)
                bind_right = lambda e, path=file_path: self.show_context_menu(e, path)

            frame.bind("<Double-Button-1>", bind_func)
            label.bind("<Double-Button-1>", bind_func)
            frame.bind("<Button-3>", bind_right)
            label.bind("<Button-3>", bind_right)

            if thumbnail:
                thumbnail_label.bind("<Double-Button-1>", bind_func)
                thumbnail_label.bind("<Button-3>", bind_right)

            col += 1
            if col >= columns:
                col = 0
                row += 1

        self.canvas.yview_moveto(0.0)

        # Bind the <Configure> event to handle resizing
        self.root.bind("<Configure>", self.resize)

        # Initialize the previous width
        self.previous_width = self.root.winfo_width()

    def create_widgets(self):
        """
        Create the widgets for the grid view.
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
        Bind mouse wheel event for scrolling.
        """
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_wheel)

    def unbind_mouse_wheel(self, event):
        """
        Unbind mouse wheel event.
        """
        self.canvas.unbind_all("<MouseWheel>")

    def on_mouse_wheel(self, event):
        """
        Scroll the canvas with the mouse wheel.
        """
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def resize(self, event):
        """
        Handle the window resize event.
        """
        new_width = self.root.winfo_width()
        if new_width + 140 < self.previous_width or new_width - 140 > self.previous_width:
            self.previous_width = new_width
            self.load_files_grid_tree(self.current_folder)

    def go_up(self):
        """
        Go up one directory level.
        """
        parent_dir = os.path.dirname(self.current_folder)
        if parent_dir:
            self.load_files_grid_tree(parent_dir)

    def open_directory(self):
        """
        Open the selected directory.
        """
        open_instance = Open(self.sdk)
        open_instance.open_directory(self.current_folder)
