
import sourceSDK
from tkinter import filedialog
import os
import subprocess
import srctools
import shutil


class Map:
    """
    @brief Class Map
    """

    sdk : sourceSDK

    def __init__(self, sourceSDK) -> None:
        """
        """
        self.sdk = sourceSDK

    def build_map(self, file=None):
        """
        """

        mapsrc_directory = os.path.join(self.sdk.selected_folder, "mapsrc")
        map_directory = os.path.join(self.sdk.selected_folder, "maps")
        
        if file == None:
            filenameVMF = filedialog.askopenfile(title="Select .vmf file", filetypes=[("VMF files", "*.vmf")], initialdir=mapsrc_directory)
            file = filenameVMF.name

        print("file =", file)
        # Execute vbsp.exe

        fileBSP = file
        #file_directory = os.path.dirname(fileBSP)
        fileBSP = os.path.splitext(os.path.basename(fileBSP))[0]

        # Create the new .bsp file path
        fileBSP = fileBSP + ".bsp"
        print("bsp =", fileBSP)

        print(self.sdk.bin_folder)

        vbsp = (self.sdk.bin_folder + "/vbsp.exe")
        command = ('"' + vbsp + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " " + '"' + file + '"')
        print(command)
        #Execute the command in cmd
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

        vvis = (self.sdk.bin_folder + "/vvis.exe")
        command = ('"' + vvis + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " " + '"' + mapsrc_directory + "/" + fileBSP + '"')
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

        vrad = (self.sdk.bin_folder + "/vrad.exe")
        command = ('"' + vrad + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " " + '"' + mapsrc_directory + "/" + fileBSP + '"')
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

        try:
            os.makedirs(map_directory, exist_ok=True)
        except OSError as e:
            print(f"Error creating folder: {e}")

        # Move bsp file to maps directory
        directoryBSP = mapsrc_directory + "/" + fileBSP
        try:
            os.remove(map_directory + "/" + fileBSP)
        except os.error:
            print("cant remove :" + map_directory + "/" + fileBSP)
        
        shutil.move(directoryBSP, map_directory)
    
    def build_all_map(self):
        """
        """

        print("wait...")
        mapsrc_directory = os.path.join(self.sdk.selected_folder, "mapsrc")
        map_directory = os.path.join(self.sdk.selected_folder, "maps")
        vbsp = (self.sdk.bin_folder + "/vbsp.exe")
        vvis = (self.sdk.bin_folder + "/vvis.exe")
        vrad = (self.sdk.bin_folder + "/vrad.exe")

        try:
            os.makedirs(map_directory, exist_ok=True)
        except OSError as e:
            print(f"Error creating folder: {e}")

        for root, dirs, files in os.walk(self.sdk.selected_folder + "/mapsrc"):
            for file in files:
                if file.endswith(".vmf"):
                        vmf_file_path = os.path.join(root, file)
                        command = ('"' + vbsp + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " " + '"' + vmf_file_path + '"')
                        print(command)
                        #Execute the command in cmd
                        result = subprocess.run(command, shell=True, capture_output=True, text=True)
                        print(result)

                        fileBSP = vmf_file_path
                        #file_directory = os.path.dirname(fileBSP)
                        fileBSP = os.path.splitext(os.path.basename(fileBSP))[0]

                        # Create the new .bsp file path
                        fileBSP = fileBSP + ".bsp"

                        command = ('"' + vvis + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " " + '"' + mapsrc_directory + "/" + fileBSP + '"')
                        print(command)
                        result = subprocess.run(command, shell=True, capture_output=True, text=True)
                        print(result)

                        command = ('"' + vrad + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " " + '"' + mapsrc_directory + "/" + fileBSP + '"')
                        print(command)
                        result = subprocess.run(command, shell=True, capture_output=True, text=True)
                        print(result)

                        # Move bsp file to maps directory
                        directoryBSP = mapsrc_directory + "/" + fileBSP
                        try:
                            os.remove(map_directory + "/" + fileBSP)
                        except os.error:
                            print("cant remove :" + map_directory + "/" + fileBSP)
                        
                        shutil.move(directoryBSP, map_directory)
    
    def info_map(self):
        """
        """

        filenamevmf = filedialog.askopenfile(title="Select .vmf file", filetypes=[("VMF files", "*.vmf")], initialdir=self.sdk.selected_folder + "/mapsrc")
        vmf = srctools.VMF.parse(filenamevmf.name)
        entities = vmf.entities
        print("Number of entities in the VMF:", len(entities))
        print(entities)
        cameras = vmf.cameras
        print("Number of cameras in the VMF:", len(cameras))
        print(cameras)