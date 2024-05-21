import tkinter as tk
import sourceSDK
import os
import subprocess
from tkinter import Listbox, filedialog, messagebox
from texture import Texture
from _vpk import VPK
from PIL import Image, ImageTk

class File:
    """
    @brief Class File
    """

    sdk : sourceSDK
    listbox : Listbox
    scrollbar : tk.Scrollbar

    def __init__(self, sourceSDK) -> None:
        """
        """
        self.sdk = sourceSDK

    def list_files(self):
        """
        """
        target_extensions = [".vmf", ".txt", ".cfg", ".vtf", ".vmt", ".qc", ".mdl", ".vcd", ".res", ".bsp", "dir.vpk", ".tga"]
        files = []

        for root, dirs, files_in_dir in os.walk(self.sdk.selected_folder):
            for file_name in files_in_dir:
                for ext in target_extensions:
                    if file_name.endswith(ext):
                        files.append(os.path.relpath(os.path.join(root, file_name), self.sdk.parent_folder))

        for game in self.sdk.game_path:

            for root, dirs, files_in_dir in os.walk(os.path.join(self.sdk.parent_folder, game)):
                for file_name in files_in_dir:
                    for ext in target_extensions:
                        if file_name.endswith(ext):
                            files.append(os.path.relpath(os.path.join(root, file_name), self.sdk.parent_folder))

        files.sort()  # Sort files alphabetically
        return files

    def display_files(self):
        """
        """

        files = self.list_files()

        # Création du widget Listbox
        self.listbox = Listbox(self.sdk.FileWindow)
        
        # Création du widget Scrollbar
        self.scrollbar = tk.Scrollbar(self.sdk.FileWindow)
        
        # Configure the Listbox to use the Scrollbar
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Insert files into the Listbox
        for file in files:
            self.listbox.insert(tk.END, file)
        
        self.listbox.bind("<Double-Button-1>", self.open_file_listbox)

    def create_grid(self):

        files = self.list_files()

        for i in range(5):
            self.sdk.FileWindow.grid_rowconfigure(i, weight=1)
        for i in range(30):
            self.sdk.FileWindow.grid_columnconfigure(i, weight=1)

    def display_files_grid(self):

        self.create_grid()

        files = self.list_files()

        for i in range(30):
            for j in range(1,6):
                self.label = tk.Label(self.sdk.FileWindow, text=files[i*j+j], borderwidth=1, relief="solid")
                self.label.grid(row=i, column=j, sticky="nsew")
                self.label.bind("<Double-1>", lambda event, row=i, col=j: self.open_file_grid(event))
        

    def open_file_listbox(self, event):
        """
        """
        
        selected_index = self.listbox.curselection()

        if selected_index:
            file = self.listbox.get(selected_index)
            file_name, file_extension = os.path.splitext(file)
            print(file)
            self.open_file_source_extension(file_extension,self.sdk.parent_folder + "/" + file, file[5:-4])
    
    def open_file_grid(self, event):
        """
        """
        
        selected_text = event.widget.cget('text')

        if selected_text:
            file_name, file_extension = os.path.splitext(selected_text)
            
            self.open_file_source_extension(file_extension,self.sdk.parent_folder + "/" + selected_text, selected_text[5:-4])

    def open_file_source_extension(self, file_extension, filepath, file):
        """
        """
        if file_extension == ".vtf":   
            texture = Texture(self.sdk)
            texture.open_VTF(filepath)
            
        elif file_extension == ".mdl":
            command = '"' + self.sdk.bin_folder + "/hlmv.exe" + '"'+ ' "' + filepath + '"' 
            subprocess.Popen(command)
        elif file_extension == ".vmf":
            #subprocess.Popen([test.sdk.bin_folder + "/hammer.exe" + ' "' + file + '"'])
            command = '"' + self.sdk.bin_folder + "/hammer.exe" + '"'+ ' "' + filepath + '"' 
            subprocess.Popen(command)
        elif file_extension == ".vcd":
            command = '"' + self.sdk.bin_folder + "/hlfaceposer.exe" + '"'+ ' "' + filepath + '"' 
            subprocess.Popen(command)
        elif file_extension == ".bsp":
            command = ('"' + self.sdk.executable_game + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " -console -dev -w 1280 -h 720  -sw +sv_cheats 1 +map " + file)
            print(command)
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
                print("Error", f"Failed to open file: {e}")