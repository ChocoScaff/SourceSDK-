import sourceSDK
from PyQt5.QtWidgets import QFileDialog, QMessageBox
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
    
    def build_caption(self):
        """
        Compile caption
        """

        filenameTXT, _ = QFileDialog.getOpenFileName(None, "Select .txt file", self.sdk.selected_folder + "/resource", "TXT files (closecaption*.txt)")        
        captioncompiler = (self.sdk.bin_folder + "/captioncompiler.exe")
        command = ('"' + captioncompiler + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " " + '"' + filenameTXT.name + '"')
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