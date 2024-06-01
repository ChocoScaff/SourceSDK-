import sourceSDK
import os
from texture import Texture
import subprocess
from _vpk import VPK
from pathlib import Path

class Open:
    """
    @brief Class OpenSLN
    """

    sdk : sourceSDK

    def __init__(self, sourceSDK) -> None:
        """
        """
        self.sdk = sourceSDK

    def open_games(self):
        """
        """
        self.open_sln_file(self.sdk.selected_folder + "/src/games.sln")

    def open_everything(self):
        """
        """
        self.open_sln_file(self.sdk.selected_folder + "/src/everything.sln")
    
    def open_sln_file(self, sln_file_path):
        """
        """
        
        # Check if the .sln file exists
        if os.path.exists(sln_file_path):
            # Open the .sln file with the default application
            os.startfile(sln_file_path)
        else:
            print("Error: .sln file not found!")
    
    def open_file(self, localpath):
        file_name, file_extension = os.path.splitext(localpath)
        if file_extension == ".vtf":
            texture = Texture(self.sdk)
            texture.open_VTF(localpath)
        elif file_extension == ".mdl":
            command = f'"{self.sdk.bin_folder}/hlmv.exe" "{localpath}"'
            subprocess.Popen(command)
        elif file_extension == ".vmf":
            command = f'"{self.sdk.bin_folder}/hammer.exe" "{localpath}"'
            subprocess.Popen(command)
        elif file_extension == ".vcd":
            command = f'"{self.sdk.bin_folder}/hlfaceposer.exe" "{localpath}"'
            subprocess.Popen(command)
        elif file_extension == ".bsp":        
            path = Path(localpath)
            file_name = path.name
            command = f'"{self.sdk.executable_game}" -game "{self.sdk.selected_folder}" -console -dev -w 1280 -h 720 -sw +sv_cheats 1 +map {file_name}'
            print(command)
            subprocess.Popen(command)
        elif file_extension == ".vpk":
            vpk = VPK(self.sdk)
            vpk.display_vpk_contents(localpath)
        elif file_extension == ".tga":
            texture = Texture(self.sdk)
            texture.display_tga_file(localpath)
        else:
            try:
                os.startfile(localpath)
            except OSError as e:
                print("Error: Failed to open file:", e)




    def open_file_with_tree(self, tree, fileList):
        """
        Open the selected file from the Treeview.
        """
        self.fileList = fileList

        self.tree = tree

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
        elif os.path.isdir(filepath):
            self.fileList.load_files(filepath)
        else:
            try:
                os.startfile(filepath)
            except OSError as e:
                print("Error: Failed to open file:", e)
    
    def open_directory(self,folder):
        """
        """
        os.startfile(folder)