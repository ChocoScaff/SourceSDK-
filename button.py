import tkinter as tk
import sourceSDK
import os
import subprocess
from model import Model
from texture import Texture
from open import Open
from download import Download
from file import File

class Button:
    """
    @brief Class Button
    """

    sdk : sourceSDK
    open : Open
    iconHpp : tk.PhotoImage
    iconHammer : tk.PhotoImage
    iconSource : tk.PhotoImage
    iconHLMV : tk.PhotoImage
    iconQc_eyes : tk.PhotoImage
    iconHlposer : tk.PhotoImage
    iconVisualStudio : tk.PhotoImage
    iconVTFEdit : tk.PhotoImage
    iconExplorer : tk.PhotoImage

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
    btn_file_explorer : tk.Button

    model : Model
    texture : Texture

    def __init__(self,sourceSDK):
        """
        @param sourceSDK get class sourceSDK
        """

        self.sdk = sourceSDK
        self.model = Model(self.sdk)
        self.texture = Texture(self.sdk)
        self.open = Open(self.sdk)

        base_path = os.path.dirname(os.path.abspath(__file__))
        self.iconExplorer = tk.PhotoImage(file=os.path.join(base_path, "icons", "fileexplorer.png"))
        self.iconHpp = tk.PhotoImage(file=os.path.join(base_path, "icons", "hpp.png"))
        self.iconHammer = tk.PhotoImage(file=os.path.join(base_path, "icons", "hammer.png"))
        self.iconSource = tk.PhotoImage(file=os.path.join(base_path, "icons", "source.png"))
        self.iconHLMV = tk.PhotoImage(file=os.path.join(base_path, "icons", "hlmv.png"))
        self.iconQc_eyes = tk.PhotoImage(file=os.path.join(base_path, "icons", "qc_eyes.png"))
        self.iconHlposer = tk.PhotoImage(file=os.path.join(base_path, "icons", "hlposer.png"))
        self.iconVisualStudio = tk.PhotoImage(file=os.path.join(base_path, "icons", "Visual_Studio.png"))
        self.iconVTFEdit = tk.PhotoImage(file=os.path.join(base_path, "icons", "VTFEdit.png"))

    def destroy_button(self):
        """
        """

        print("reload")   

        self.btn_file_explorer.destroy()

        if os.path.isfile(self.sdk.bin_folder + "/hammer.exe"):
            self.btn_hammer.destroy()
        if os.path.isfile(self.sdk.bin_folder + "/hammerplusplus.exe"):
            self.btn_hammer_plus_plus.destroy()
        if os.path.isfile(self.sdk.bin_folder + "/qc_eyes.exe"):
            self.btn_qc_eyes.destroy()
        if os.path.exists(self.sdk.selected_folder + "/src/everything.sln"):
            self.btn_everything.destroy()
        if os.path.exists(self.sdk.selected_folder + "/src/games.sln"):
            self.btn_games.destroy()
        if os.path.isfile(self.sdk.bin_folder + "/hlmv.exe"):
            self.btn_hlmv.destroy()
        if os.path.isfile(self.sdk.bin_folder + "/hlfaceposer.exe"):
            self.btn_hlfaceposer.destroy()
        if os.path.isfile(os.getcwd() + "/VTfEdit/x64/VTFEdit.exe"):
            self.btn_vtf_edit.destroy()

        self.btn_Launch.destroy()
        self.btn_particle.destroy()
        self.btn_Launch_dev.destroy()

    def display(self):
        """
        display button on gui
        """
        
        file = File(self.sdk)
        self.btn_file_explorer = tk.Button(self.sdk.root, text="Files", command=file.display_files,image=self.iconExplorer,compound=tk.LEFT, background="#4c5844",fg="white")
        self.btn_file_explorer.pack(side="left")

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
            self.btn_games = tk.Button(self.sdk.root, text="games", command=self.open.open_games, image=self.iconVisualStudio, compound=tk.LEFT, background="#4c5844",fg="white")
            self.btn_games.pack(side="left")

        if os.path.exists(self.sdk.selected_folder + "/src/everything.sln"):
            self.btn_everything = tk.Button(self.sdk.root, text="everything", command=self.open.open_everything, image=self.iconVisualStudio, compound=tk.LEFT, background="#4c5844",fg="white")
            self.btn_everything.pack(side="left")

        self.btn_particle = tk.Button(self.sdk.root, text="Particle", command=self.particle, image=self.iconSource, compound=tk.LEFT, background="#4c5844",fg="white")
        self.btn_particle.pack(side="left")

        self.btn_Launch_dev = tk.Button(self.sdk.root, text="Launch Dev", command=self.Launch_dev, image=self.iconSource, compound=tk.LEFT, background="#4c5844",fg="white")
        self.btn_Launch_dev.pack(side="left")

        self.btn_Launch = tk.Button(self.sdk.root, text="Launch", command=self.Launch, image=self.iconSource, compound=tk.LEFT, background="#4c5844",fg="white")
        self.btn_Launch.pack(side="left")
    
    def open_hammer(self):
        """
        """
        subprocess.Popen([self.sdk.bin_folder + "/hammer.exe"])

    def open_hammer_plus_plus(self):
        """
        """
        subprocess.Popen([self.sdk.bin_folder + "/hammerplusplus.exe"])

    def open_qc_eyes(self):
        """
        """
        subprocess.Popen([self.sdk.bin_folder + "/qc_eyes.exe"])

    def open_hlfaceposer(self):
        """
        """
        subprocess.Popen([self.sdk.bin_folder + "/hlfaceposer.exe"])

    def particle(self):
        """
        """
        command = ('"' + self.sdk.executable_game + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " -tools -nop4 -dev -sw -console")
        print(command)
        subprocess.Popen(command)

    def Launch_dev(self):
        """
        """
        command = ('"' + self.sdk.executable_game + '"' + " -game " + '"' + self.sdk.selected_folder + '"' + " -console -dev -w 1280 -h 720 -sw +sv_cheats 1")
        print(command)
        subprocess.Popen(command)

    def Launch(self):
        """
        """
        command = ('"' + self.sdk.executable_game + '"' + " -game " + '"' + self.sdk.selected_folder + '"')
        print(command)
        subprocess.Popen(command)
