import sourceSDK
from tkinter import filedialog
import os
import subprocess

class Caption:
    """
    @brief Class Model
    """

    sdk : sourceSDK

    def __init__(self, sourceSDK) -> None:
        """
        """

        self.sdk = sourceSDK
    
    def build_caption(self, file=None):
        """
        Compile caption
        """
        if file == None:
            filenameTXT = filedialog.askopenfile(title="Select .txt file", filetypes=[("TXT files", "closecaption*.txt")], initialdir=self.sdk.selected_folder + "/resource")
            file = filenameTXT.name
        
        captioncompiler = (self.sdk.bin_folder + "/captioncompiler.exe")
        command = ('"' + captioncompiler + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " " + '"' + file + '"')
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

    def build_all_caption(self):
        """
        compile all captions in ressource folder
        """

        print("wait...")
        captioncompiler = (self.sdk.bin_folder + "/captioncompiler.exe")
        for root, dirs, files in os.walk(self.sdk.selected_folder + "/resource"):
            for file in files:
                if file.startswith("closecaption") and file.endswith(".txt"):
                    caption_file_path = os.path.join(root, file)
                    command = ('"' + captioncompiler + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " " + '"' + caption_file_path + '"')
                    print(command)
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    print(result)