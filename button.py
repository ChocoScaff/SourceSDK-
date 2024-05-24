import os
import subprocess
from PyQt5.QtWidgets import QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon
from model import Model
from texture import Texture
from open import Open
from download import Download

class Button:
    """
    @brief Class Button
    """

    def __init__(self, sourceSDK, parent=None):
        """
        @param sourceSDK get class sourceSDK
        """
        self.sdk = sourceSDK
        self.model = Model(self.sdk)
        self.texture = Texture(self.sdk)
        self.open = Open(self.sdk)

        base_path = os.path.dirname(os.path.abspath(__file__))
        self.iconHpp = QIcon(os.path.join(base_path, "icons", "hpp.png"))
        self.iconHammer = QIcon(os.path.join(base_path, "icons", "hammer.png"))
        self.iconSource = QIcon(os.path.join(base_path, "icons", "source.png"))
        self.iconHLMV = QIcon(os.path.join(base_path, "icons", "hlmv.png"))
        self.iconQc_eyes = QIcon(os.path.join(base_path, "icons", "qc_eyes.png"))
        self.iconHlposer = QIcon(os.path.join(base_path, "icons", "hlposer.png"))
        self.iconVisualStudio = QIcon(os.path.join(base_path, "icons", "Visual_Studio.png"))
        self.iconVTFEdit = QIcon(os.path.join(base_path, "icons", "VTFEdit.png"))

        self.layout = QVBoxLayout(parent)
        self.parent = parent

    def destroy_button(self):
        """
        """
        print("reload")

        if os.path.isfile(self.sdk.bin_folder + "/hammer.exe"):
            self.btn_hammer.deleteLater()
        if os.path.isfile(self.sdk.bin_folder + "/hammerplusplus.exe"):
            self.btn_hammer_plus_plus.deleteLater()
        if os.path.isfile(self.sdk.bin_folder + "/qc_eyes.exe"):
            self.btn_qc_eyes.deleteLater()
        if os.path.exists(self.sdk.selected_folder + "/src/everything.sln"):
            self.btn_everything.deleteLater()
        if os.path.exists(self.sdk.selected_folder + "/src/games.sln"):
            self.btn_games.deleteLater()
        if os.path.isfile(self.sdk.bin_folder + "/hlmv.exe"):
            self.btn_hlmv.deleteLater()
        if os.path.isfile(self.sdk.bin_folder + "/hlfaceposer.exe"):
            self.btn_hlfaceposer.deleteLater()
        if os.path.isfile(os.getcwd() + "/VTfEdit/x64/VTFEdit.exe"):
            self.btn_vtf_edit.deleteLater()

        self.btn_Launch.deleteLater()
        self.btn_particle.deleteLater()
        self.btn_Launch_dev.deleteLater()

    def display(self):
        """
        display button on gui
        """
        if os.path.isfile(self.sdk.bin_folder + "/hammer.exe"):
            self.btn_hammer = QPushButton("hammer", self.parent)
            self.btn_hammer.setIcon(self.iconHammer)
            self.btn_hammer.clicked.connect(self.open_hammer)
            self.layout.addWidget(self.btn_hammer)

        if os.path.isfile(self.sdk.bin_folder + "/hammerplusplus.exe"):
            self.btn_hammer_plus_plus = QPushButton("hammer++", self.parent)
            self.btn_hammer_plus_plus.setIcon(self.iconHpp)
            self.btn_hammer_plus_plus.clicked.connect(self.open_hammer_plus_plus)
            self.layout.addWidget(self.btn_hammer_plus_plus)

        if os.path.isfile(self.sdk.bin_folder + "/hlmv.exe"):
            self.btn_hlmv = QPushButton("hlmv", self.parent)
            self.btn_hlmv.setIcon(self.iconHLMV)
            self.btn_hlmv.clicked.connect(self.model.open_hlmv)
            self.layout.addWidget(self.btn_hlmv)

        if os.path.isfile(self.sdk.bin_folder + "/qc_eyes.exe"):
            self.btn_qc_eyes = QPushButton("qc_eyes", self.parent)
            self.btn_qc_eyes.setIcon(self.iconQc_eyes)
            self.btn_qc_eyes.clicked.connect(self.open_qc_eyes)
            self.layout.addWidget(self.btn_qc_eyes)

        if os.path.isfile(self.sdk.bin_folder + "/hlfaceposer.exe"):
            self.btn_hlfaceposer = QPushButton("hlfaceposer", self.parent)
            self.btn_hlfaceposer.setIcon(self.iconHlposer)
            self.btn_hlfaceposer.clicked.connect(self.open_hlfaceposer)
            self.layout.addWidget(self.btn_hlfaceposer)

        if os.path.isfile(os.getcwd() + "/VTfEdit/x64/VTFEdit.exe"):
            self.btn_vtf_edit = QPushButton("vtfEdit", self.parent)
            self.btn_vtf_edit.setIcon(self.iconVTFEdit)
            self.btn_vtf_edit.clicked.connect(self.texture.open_VTF)
            self.layout.addWidget(self.btn_vtf_edit)
        else:
            Download.download_VTF_Edit()
            self.btn_vtf_edit = QPushButton("vtfEdit", self.parent)
            self.btn_vtf_edit.setIcon(self.iconVTFEdit)
            self.btn_vtf_edit.clicked.connect(self.texture.open_VTF)
            self.layout.addWidget(self.btn_vtf_edit)

        if os.path.exists(self.sdk.selected_folder + "/src/games.sln"):
            self.btn_games = QPushButton("games", self.parent)
            self.btn_games.setIcon(self.iconVisualStudio)
            self.btn_games.clicked.connect(self.open.open_games)
            self.layout.addWidget(self.btn_games)

        if os.path.exists(self.sdk.selected_folder + "/src/everything.sln"):
            self.btn_everything = QPushButton("everything", self.parent)
            self.btn_everything.setIcon(self.iconVisualStudio)
            self.btn_everything.clicked.connect(self.open.open_everything)
            self.layout.addWidget(self.btn_everything)

        self.btn_particle = QPushButton("Particle", self.parent)
        self.btn_particle.setIcon(self.iconSource)
        self.btn_particle.clicked.connect(self.particle)
        self.layout.addWidget(self.btn_particle)

        self.btn_Launch_dev = QPushButton("Launch Dev", self.parent)
        self.btn_Launch_dev.setIcon(self.iconSource)
        self.btn_Launch_dev.clicked.connect(self.Launch_dev)
        self.layout.addWidget(self.btn_Launch_dev)

        self.btn_Launch = QPushButton("Launch", self.parent)
        self.btn_Launch.setIcon(self.iconSource)
        self.btn_Launch.clicked.connect(self.Launch)
        self.layout.addWidget(self.btn_Launch)

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
