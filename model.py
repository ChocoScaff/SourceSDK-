import tkinter as tk
import sourceSDK
from tkinter import filedialog
import os
import subprocess

class Model:

    sdk : sourceSDK

    def __init__(self, sourceSDK) -> None:
        self.sdk = sourceSDK


    def open_hlmv(self):
        subprocess.Popen([self.sdk.bin_folder + "/hlmv.exe"])

    def build_model(self):
        filenameQC = filedialog.askopenfile(title="Select .qc file", filetypes=[("QC files", "*.qc")], initialdir=self.sdk.selected_folder + "/modelsrc")
        mdl = (self.sdk.bin_folder + "/studiomdl.exe")
        command = ('"' + mdl + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " " + '"' + filenameQC.name + '"')
        print(command)
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result)

    def build_all_model(self):
        print("wait...")
        mdl = (self.sdk.bin_folder + "/studiomdl.exe")
        for root, dirs, files in os.walk(self.sdk.selected_folder + "/modelsrc"):
            for file in files:
                if file.endswith(".qc"):
                    qc_file_path = os.path.join(root, file)
                    command = ('"' + mdl + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " " + '"' + qc_file_path + '"')
                    print(command)
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    print(result)
    
    def generate_qc_file(self):

        filenameModel = filedialog.askopenfile(title="Select .smd or .dmx file", filetypes=[("model file", "*.smd *.dmx")], initialdir=self.sdk.selected_folder + "/modelsrc")
        print(filenameModel)
        print(filenameModel.name)
        TexureDirectory = filedialog.askdirectory(title="Select Texure Directory",initialdir=self.sdk.selected_folder + "/materials/models")
        print(TexureDirectory)

        popup = tk.Toplevel()
        popup.title("Material Selector")

        materials = ["Concrete", "Wood", "Dirt", "Grass", "Water", "Ice", "Metal", "Sand", "Rock"]

        selected_materialTK = tk.StringVar()

        def select_material(material):
            selected_materialTK.set(material)
            popup.destroy() 

        for material in materials:
            button = tk.Button(popup, text=material, command=lambda m=material: select_material(m))
            button.pack()

        popup.wait_window()

        selected_material = selected_materialTK.get()

        qc_file="""
$modelname "modelNameToReplace"
$cdmaterials "textureDirectoryToReplace"
$collisionmodel	"modelToReplace"
$sequence idle	"modelToReplace"
$body bodystrToReplace "modelToReplace"
$surfaceprop sufaceReplace
$scale 1
    """

        modelNamestr = filenameModel.name[filenameModel.name.find("/modelsrc/") + 10:]
        texturestr = TexureDirectory[TexureDirectory.find("/materials/") + 11:]
        modelstr =modelNamestr[modelNamestr.find('/') + 1:]
        bodystr = modelstr[:-4]

        qc_file = qc_file.replace("modelNameToReplace",modelNamestr)
        qc_file = qc_file.replace("textureDirectoryToReplace",texturestr)
        qc_file = qc_file.replace("bodystrToReplace",bodystr)
        qc_file = qc_file.replace("sufaceReplace",selected_material)
        qc_file = qc_file.replace("modelToReplace",modelstr)

        print(qc_file)

        fileQC = self.sdk.selected_folder + "/modelsrc/" + modelNamestr[:-4] + ".qc"
        print(fileQC)

        try:
            with open(fileQC, 'w') as file:
                file.write(qc_file)
            print(f"String saved to '{filenameModel}' successfully.")
        except Exception as e:
            print(f"Error: {e}")