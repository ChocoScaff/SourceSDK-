import string
import vpk
import tkinter as tk
import sourceSDK
from tkinter import filedialog, ttk
import os
import subprocess
import tempfile
from texture import Texture
from PIL import Image, ImageTk

class VPK:
    """
    Class for handling VPK file operations.
    """
    sdk: sourceSDK
    vpk_path: string
    tree: ttk.Treeview

    def __init__(self, sourceSDK) -> None:
        """
        Initialize the VPK class with a given sourceSDK instance.
        """
        self.sdk = sourceSDK
        self.vpk_file = None
        self.thumbnails = {}

    def display_vpk_contents(self, file=""):
        """
        Display the contents of a VPK file in a Treeview.
        """
        if file == "":
            # Open file dialog to select a VPK file
            self.vpk_path = filedialog.askopenfilename(title="Select VPK file", filetypes=[("VPK files", "*.vpk")])
            if not self.vpk_path:
                return  # User cancelled selection or closed dialog
        else:
            self.vpk_path = file

        print(self.vpk_path)

        # Create Tkinter window
        popup = tk.Toplevel()
        popup.title("VPK Contents")
        popup.geometry("600x400")

        # Search Label and Entry
        search_frame = tk.Frame(popup)
        search_frame.pack(fill="x", padx=10, pady=5)
        search_label = tk.Label(search_frame, text="Search:")
        search_label.pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(fill="x", expand=True, side="left")
        self.search_entry.bind("<KeyRelease>", self.search_files)

        frame = tk.Frame(popup)
        frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(frame)
        self.tree.pack(fill="both", expand=True, side="left")

        scrollbar = tk.Scrollbar(frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.config(yscrollcommand=scrollbar.set)

        self.tree.heading("#0", text="Contents", anchor='w')

        with vpk.open(self.vpk_path) as self.vpk_file:
            files = self.list_vpk_files()
            self.populate_tree(files)

        self.tree.bind("<Double-Button-1>", self.open_file_in_vpk)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def list_vpk_files(self):
        """
        List all files in the VPK archive.

        Returns:
            files (dict): A dictionary representing the folder structure.
        """
        files = {}
        
        for file_path in self.vpk_file:
            folder_path, file_name = os.path.split(file_path)
            if folder_path not in files:
                files[folder_path] = []
            files[folder_path].append(file_name)

        return files

    def populate_tree(self, files):
        """
        Populate the Treeview with the files and folders.

        Args:
            files (dict): A dictionary representing the folder structure.
        """
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
            try:
                pakfile = self.vpk_file.get_file(path)
                if pakfile:
                    file_content = pakfile.read()
                    temp_file_path = os.path.join(temp_dir, os.path.basename(path))
                    with open(temp_file_path, 'wb') as temp_file:
                        temp_file.write(file_content)
                    return temp_file_path
                else:
                    print(f"File {path} not found in VPK.")
                    return None
            except KeyError:
                print(f"KeyError: {path} does not exist in the VPK archive.")
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

        """"
        # Ensure all required files are present
        if len(related_files) != len(related_extensions):
            print(f"Missing related files for {file_name}.")
            return
        """
            
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

    def extract_and_save_file(self, file_name, destination_folder):
        """
        Extract a file from the VPK archive to a specified folder.
        """
        if not self.vpk_file:
            print("VPK file is not loaded.")
            return

        related_extensions = [".dx80.vtx", ".dx90.vtx", ".sw.vtx", ".phy", ".vvd"]

        def extract_file(path):
            pakfile = self.vpk_file.get_file(path)
            if pakfile:
                file_content = pakfile.read()
                temp_file_path = os.path.join(destination_folder, os.path.basename(path))
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
            for ext in related_extensions:
                try:
                    extract_file(base_name + ext)
                except OSError:
                    print("mdl error")

        print(f"File {file_name} extracted to {destination_folder}")

    def create_VPK(self):
        """
        Create a VPK file from a selected directory.
        """
        directory = filedialog.askdirectory(title="Select a Directory")
        command = f'"{self.sdk.bin_folder}/vpk.exe" "{directory}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

    def extract_VPK(self):
        """
        Extract the contents of a selected VPK file.
        """
        filename_vpk = filedialog.askopenfile(title="Select .vpk file", filetypes=[("VPK files", "*.vpk")], initialdir=self.sdk.selected_folder)
        command = f'"{self.sdk.bin_folder}/vpk.exe" "{filename_vpk.name}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

    def display_VPK(self):
        """
        Display the contents of a selected VPK file.
        """
        filename_vpk = filedialog.askopenfile(title="Select .vpk file", filetypes=[("VPK files", "*.vpk")], initialdir=self.sdk.selected_folder)
        command = f'"{self.sdk.bin_folder}/vpk.exe" L "{filename_vpk.name}"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

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

    def show_context_menu(self, event):
        """
        Show the context menu on right-click.
        """
        selected_item = self.tree.identify_row(event.y)
        if selected_item:
            self.tree.selection_set(selected_item)
            self.context_menu = tk.Menu(self.tree, tearoff=0)
            self.context_menu.add_command(label="Extract to...", command=self.extract_to)
            self.context_menu.post(event.x_root, event.y_root)

    def extract_to(self):
        """
        Extract the selected file to a user-selected folder.
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

        destination_folder = filedialog.askdirectory(title="Select Destination Folder")
        if destination_folder:
            self.extract_and_save_file(file_path, destination_folder)
    
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
                image.thumbnail((16, 16), Image.Resampling.LANCZOS)
                thumbnail = ImageTk.PhotoImage(image)
                self.thumbnails[file_path] = thumbnail
                return thumbnail
        except MemoryError:
            print("MemoryError: Failed to allocate bitmap for", file_path)
        except Exception as e:
            print("Error loading thumbnail:", e)
        return None
