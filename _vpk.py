
import string
import vpk
import tkinter as tk
import sourceSDK
from tkinter import filedialog
import os
import subprocess
import tempfile

class VPK:

    sdk : sourceSDK
    vpk_path : string
    text_widget : tk.Text

    def __init__(self, sourceSDK) -> None:
        self.sdk = sourceSDK

    def display_vpk_contents(self, file=""):

        if file == "":
            # Open file dialog to select a VPK file
            self.vpk_path = filedialog.askopenfilename(title="Select VPK file", filetypes=[("VPK files", "*.vpk")])
            if not self.vpk_path:
                return  # User cancelled selection or closed dialog
        else:
            self.vpk_path=file
            
        print(self.vpk_path)

        # Create Tkinter window
        popup = tk.Toplevel()
        popup.title("vpk contents")

        self.text_widget = tk.Text(popup, wrap="none")
        self.text_widget.pack(fill="both", expand=True)

        # Display VPK file contents in text widget
        self.text_widget.insert("end", f"Contents of {os.path.basename(self.vpk_path)}:\n")
        with vpk.open(self.vpk_path) as self.vpk_file:
            for file_path in self.vpk_file:
                self.text_widget.insert("end", f"{file_path}\n")

        self.text_widget.bind("<Double-Button-1>", self.open_file_in_vpk)
        
    def extract_and_open_file_in_vpk(self,fileName):
        if not self.vpk_file:
            print("VPK file is not loaded.")
            return

        pakfile = self.vpk_file.get_file(fileName)
        if not pakfile:
            print(f"File {fileName} not found in VPK.")
            return

        # Read the file content
        file_content = pakfile.read()

        # Create a temporary file and write the content to it
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(fileName)[1]) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name

        # Open the file with the default associated application
        try:
            os.startfile(temp_file_path)
        except Exception as e:
            print(f"Failed to open file {temp_file_path}: {e}")
        
    def open_file_in_vpk(self,event):
        selected_index = self.text_widget.index(tk.CURRENT)
        line_num = int(selected_index.split('.')[0])
        line = self.text_widget.get(f"{line_num}.0", f"{line_num}.end")
        print(line)
        self.extract_and_open_file_in_vpk(line)

    def create_VPK(self):
        directory = filedialog.askdirectory(title="Select a Directory")
        command = '"' + self.sdk.bin_folder + "/vpk.exe" + '" ' + '"' + directory + '"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

    def extract_VPK(self):
        filenamevpk = filedialog.askopenfile(title="Select .vpk file", filetypes=[("VPK files", "*.vpk")], initialdir=self.sdk.selected_folder)
        command = '"' + self.sdk.bin_folder + "/vpk.exe" + '" ' + '"' + filenamevpk.name + '"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

    def display_VPK(self):
        filenamevpk = filedialog.askopenfile(title="Select .vpk file", filetypes=[("VPK files", "*.vpk")], initialdir=self.sdk.selected_folder)
        command = '"' + self.sdk.bin_folder + "/vpk.exe" + '"' + " L " + '"' + filenamevpk.name + '"'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)