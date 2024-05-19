import tkinter as tk
import sourceSDK
from tkinter import filedialog
import os
import subprocess
from model import Model
from texture import Texture
from openSLN import OpenSLN
from download import Download

class Button:

    sdk : sourceSDK
    openSLN : OpenSLN
    iconHpp : tk.PhotoImage
    iconHammer : tk.PhotoImage
    iconSource : tk.PhotoImage
    iconHLMV : tk.PhotoImage
    iconQc_eyes : tk.PhotoImage
    iconHlposer : tk.PhotoImage
    iconVisualStudio : tk.PhotoImage
    iconVTFEdit : tk.PhotoImage

    btn_hammer : tk.Button
    btn_hammer_plus_plus : tk.Button
    btn_hlmv : tk.Button
    btn_qc_eyes : tk.Button
    btn_hlfaceposer : tk.Button
    btn_vtf_edit : tk.Button
    btn_games : tk.Button
    btn_everything : tk.Button
    btn_particle : tk.Button
    btn_Launch_dev : tk.Button
    btn_Launch : tk.Button

    model : Model
    texture : Texture

    def __init__(self,sourceSDK):
        self.sdk = sourceSDK
        self.model = Model(self.sdk)
        self.texture = Texture(self.sdk)
        self.openSLN = OpenSLN(self.sdk)

        base_path = os.path.dirname(os.path.abspath(__file__))
        self.iconHpp = tk.PhotoImage(file=os.path.join(base_path, "icons", "hpp.png"))
        self.iconHammer = tk.PhotoImage(file=os.path.join(base_path, "icons", "hammer.png"))
        self.iconSource = tk.PhotoImage(file=os.path.join(base_path, "icons", "source.png"))
        self.iconHLMV = tk.PhotoImage(file=os.path.join(base_path, "icons", "hlmv.png"))
        self.iconQc_eyes = tk.PhotoImage(file=os.path.join(base_path, "icons", "qc_eyes.png"))
        self.iconHlposer = tk.PhotoImage(file=os.path.join(base_path, "icons", "hlposer.png"))
        self.iconVisualStudio = tk.PhotoImage(file=os.path.join(base_path, "icons", "Visual_Studio.png"))
        self.iconVTFEdit = tk.PhotoImage(file=os.path.join(base_path, "icons", "VTFEdit.png"))

    def display(self):

        if os.path.isfile(self.sdk.bin_folder + "/hammer.exe"):
            self.btn_hammer = tk.Button(self.sdk.root, text="hammer", command=self.open_hammer,image=self.iconHammer,compound=tk.LEFT, background="#4c5844",fg="white")
            self.btn_hammer.pack(side="left")
        
        if os.path.isfile(self.sdk.bin_folder + "/hammerplusplus.exe"):
            self.btn_hammer_plus_plus = tk.Button(self.sdk.root, text="hammer++", command=self.open_hammer_plus_plus, image=self.iconHpp, compound=tk.LEFT, background="#4c5844",fg="white")    
            self.btn_hammer_plus_plus.pack(side="left")

        if os.path.isfile(self.sdk.bin_folder + "/hlmv.exe"):
            self.btn_hlmv = tk.Button(self.sdk.root, text="hlmv", command=self.model.open_hlmv, image=self.iconHLMV, compound=tk.LEFT, background="#4c5844",fg="white")
            self.btn_hlmv.pack(side="left")

        if os.path.isfile(self.sdk.bin_folder + "/qc_eyes.exe"):
            self.btn_qc_eyes= tk.Button(self.sdk.root, text="qc_eyes", command=self.open_qc_eyes, image=self.iconQc_eyes, compound=tk.LEFT, background="#4c5844",fg="white")
            self.btn_qc_eyes.pack(side="left")

        if os.path.isfile(self.sdk.bin_folder + "/hlfaceposer.exe"):
            self.btn_hlfaceposer = tk.Button(self.sdk.root, text="hlfaceposer", command=self.open_hlfaceposer, image=self.iconHlposer, compound=tk.LEFT, background="#4c5844",fg="white")
            self.btn_hlfaceposer.pack(side="left")

        if os.path.isfile(os.getcwd() + "/VTfEdit/x64/VTFEdit.exe"):
            self.btn_vtf_edit = tk.Button(self.sdk.root, text="vtfEdit", command=self.texture.open_VTF, image=self.iconVTFEdit, compound=tk.LEFT, background="#4c5844",fg="white")
            self.btn_vtf_edit.pack(side="left")
        else:
            Download.download_VTF_Edit()
            self.btn_vtf_edit = tk.Button(self.sdk.root, text="vtfEdit", command=self.texture.open_VTF, image=self.iconVTFEdit, compound=tk.LEFT, background="#4c5844",fg="white")
            self.btn_vtf_edit.pack(side="left")
        
        if os.path.exists(self.sdk.selected_folder + "/src/games.sln"):
            self.btn_games = tk.Button(self.sdk.root, text="games", command=self.openSLN.open_games, image=self.iconVisualStudio, compound=tk.LEFT, background="#4c5844",fg="white")
            self.btn_games.pack(side="left")

        if os.path.exists(self.sdk.selected_folder + "/src/everything.sln"):
            self.btn_everything = tk.Button(self.sdk.root, text="everything", command=self.openSLN.open_everything, image=self.iconVisualStudio, compound=tk.LEFT, background="#4c5844",fg="white")
            self.btn_everything.pack(side="left")

        self.btn_particle = tk.Button(self.sdk.root, text="Particle", command=self.particle, image=self.iconSource, compound=tk.LEFT, background="#4c5844",fg="white")
        self.btn_particle.pack(side="left")

        self.btn_Launch_dev = tk.Button(self.sdk.root, text="Launch Dev", command=self.Launch_dev, image=self.iconSource, compound=tk.LEFT, background="#4c5844",fg="white")
        self.btn_Launch_dev.pack(side="left")

        self.btn_Launch = tk.Button(self.sdk.root, text="Launch", command=self.Launch, image=self.iconSource, compound=tk.LEFT, background="#4c5844",fg="white")
        self.btn_Launch.pack(side="left")
    
    def open_hammer(self,file=""):
        subprocess.Popen([self.sdk.bin_folder + "/hammer.exe"])

    def open_hammer_plus_plus(self):
        subprocess.Popen([self.sdk.bin_folder + "/hammerplusplus.exe"])

    def open_qc_eyes(self):
        subprocess.Popen([self.sdk.bin_folder + "/qc_eyes.exe"])

    def open_hlfaceposer(self):
        subprocess.Popen([self.sdk.bin_folder + "/hlfaceposer.exe"])

    def particle(self):
        command = ('"' + self.sdk.executable_game + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " -tools -nop4 -dev -sw -console")
        print(command)
        subprocess.Popen(command)

    def Launch_dev(self):
        command = ('"' + self.sdk.executable_game + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " -console -dev -w 1280 -h 720 -sw +sv_cheats 1")
        print(command)
        subprocess.Popen(command)

    def Launch(self):
        command = ('"' + self.sdk.executable_game + '"' + " -game " + '"' + self.sdk.selected_folder + '"')
        print(command)
        subprocess.Popen(command)
