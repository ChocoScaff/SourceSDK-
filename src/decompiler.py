import os
from tkinter import filedialog
import subprocess
import sourceSDK

class Decompiler():
    
    def __init__(self, sourceSDK) -> None:
        """
        """

        self.sdk = sourceSDK

    def decompiler_file(self, file=None, folderOutput=None):
        """
        """

        if file == None:
            filenameMDL = filedialog.askopenfile(title="Select .mdl file", filetypes=[("MDL files", "*.mdl")], initialdir=self.sdk.selected_folder + "/models" )
            file= filenameMDL.name
        
        if folderOutput == None:
            folderOutput = filedialog.askdirectory(title="Select Destination Output", initialdir=self.sdk.selected_folder + "/modelsrc")
        
        mdl = (os.getcwd() + "\\CrowbarDecompiler.1.1\\CrowbarDecompiler(1.1).exe")
        command = '"' + mdl + '" ' + '"' + file + '" "' + folderOutput + '"'
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)