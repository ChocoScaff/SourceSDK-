import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QFileDialog, QAction, QLabel,
    QVBoxLayout, QWidget, QMessageBox
)
from PyQt5.QtGui import QColor, QTextCharFormat
import sys
import shutil
import git
import urllib.request
import json
import webbrowser
import re

from sourceSDK import SourceSDK
from texture import Texture
from model import Model
from map import Map
from _vpk import VPK
from file import File
from button import Button
from caption import Caption

class Terminal(QTextEdit):
    """
    Terminal on the GUI
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)

    def write(self, message, message_type="stdout"):
        format = QTextCharFormat()
        if message_type == "stderr":
            format.setForeground(QColor("red"))
        else:
            format.setForeground(QColor("black"))

        self.setCurrentCharFormat(format)
        self.append(message)
        self.moveCursor(self.textCursor().End)

    def flush(self):
        pass

class AssetsBrowser(QMainWindow):
    """
    Class for managing assets
    """

    def __init__(self):
        super().__init__()
        self.sdk = SourceSDK()

        self.sdk.selected_folder = None
        self.sdk.game_name = None
        self.sdk.parent_folder = None
        self.sdk.bin_folder = None
        self.sdk.executable_game = None
        self.sdk.first_init = 0
        self.sdk.game_path = []
        self.sdk.texture_menu = None
        self.sdk.map_menu = None
        self.sdk.model_menu = None
        self.sdk.other_menu = None

        self.texture = None
        self.model = None
        self.map = None
        self.vpk = None
        self.file = None
        self.button = None
        self.caption = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Source SDK : assetsBrowser")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.terminal = Terminal(self)
        layout.addWidget(self.terminal)

        self.create_menu_bar()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        help_menu = menu_bar.addMenu("Help")

        new_action = QAction("New", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)

        open_action = QAction("Open", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.init_sdk)
        file_menu.addAction(open_action)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.launch_exit)
        file_menu.addAction(exit_action)

        doc_action = QAction("SDK Doc", self)
        doc_action.triggered.connect(self.sdk_doc)
        help_menu.addAction(doc_action)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.open_about_window)
        help_menu.addAction(about_action)

    def parse_gameinfo_txt(self):
        gameinfo_path = os.path.join(self.sdk.selected_folder, "gameinfo.txt")
        print(gameinfo_path)

        inside_search_paths = False
        game_path_pattern = re.compile(r'^\s*game\s+([^\s]+)', re.MULTILINE)

        if os.path.isfile(gameinfo_path):
            with open(gameinfo_path, 'r') as file:
                for line in file:
                    if re.search(r'^\s*SearchPaths', line):
                        inside_search_paths = True
                        continue
                    if inside_search_paths and re.search(r'^\s*}', line):
                        inside_search_paths = False
                        continue
                    if inside_search_paths:
                        line = line.lower()
                        if '|all_source_engine_paths|' in line:
                            line = line.replace('|all_source_engine_paths|', '')
                        match = game_path_pattern.match(line)
                        if match:
                            self.sdk.game_path.append(match.group(1).strip())
        print(self.sdk.game_path)

    def bin_folder(self, folder_path):
        binFolder = os.path.join(self.sdk.parent_folder, "bin")
        if os.path.exists(binFolder):
            pass
        else:
            folder = QFileDialog.getExistingDirectory(self, "Open bin Engine path", self.sdk.parent_folder)
            binFolder = self.bin_folder(folder)
        return binFolder

    def find_executable_game(self, folder_path):
        executables = []
        for root, dirs, files in os.walk(self.sdk.parent_folder):
            for file in files:
                if file.endswith('.exe'):
                    executables.append(os.path.join(root, file))
        return executables[0]

    def find_game_name(self, folder_path):
        game_name = os.path.basename(folder_path)
        return game_name

    def find_gameinfo_folder(self):
        selected_folder = QFileDialog.getExistingDirectory(self, "Select Directory")
        gameinfo_path = os.path.join(selected_folder, "gameinfo.txt")
        if os.path.isfile(gameinfo_path):
            command = f'setx VProject "{selected_folder}"'
            result = subprocess.run(command, shell=True)
            print(result)
            return selected_folder
        else:
            print("gameinfo.txt not found in selected folder.")
            return -1

    def init_sdk(self, folder=False):
        print("Wait...")

        if not folder:
            if self.sdk.first_init == 1:
                self.button.destroy_button()
            self.sdk.selected_folder = self.find_gameinfo_folder()
            if self.sdk.selected_folder == -1:
                return
        else:
            if self.sdk.first_init == 1:
                self.button.destroy_button()
            self.sdk.selected_folder = folder

        print(f"selected directory : {self.sdk.selected_folder}")

        self.sdk.game_name = self.find_game_name(self.sdk.selected_folder)
        print(f"game name : {self.sdk.game_name}")

        self.sdk.parent_folder = os.path.dirname(self.sdk.selected_folder)

        self.sdk.bin_folder = self.bin_folder(self.sdk.selected_folder)
        print(f"bin directory : {self.sdk.bin_folder}")

        self.sdk.executable_game = self.find_executable_game(self.sdk.bin_folder)
        print(f"executable game : {self.sdk.executable_game}")

        self.parse_gameinfo_txt()

        try:
            self.setWindowIcon(QIcon(os.path.join(self.sdk.selected_folder, 'resource', 'game.ico')))
        except Exception:
            print("Error: Failed to set icon.")

        print("Project open")

        lbl_result = QLabel("Tools")
        lbl_result.setStyleSheet("background-color: #3e4637; color: white;")
        layout = self.centralWidget().layout()
        layout.addWidget(lbl_result)

        self.texture = Texture(self.sdk)
        self.model = Model(self.sdk)
        self.map = Map(self.sdk)
        self.vpk = VPK(self.sdk)
        self.file = File(self.sdk)
        self.button = Button(self.sdk)
        self.caption = Caption(self.sdk)

        self.label_init()

        self.file.display_files()

    def label_init(self):
        self.button.display()

        if self.sdk.first_init == 0:
            self.sdk.texture_menu = self.menuBar().addMenu("Texture")
            self.sdk.map_menu = self.menuBar().addMenu("Map")
            self.sdk.model_menu = self.menuBar().addMenu("Model")
            self.sdk.other_menu = self.menuBar().addMenu("Other")

            self.sdk.map_menu.addAction("Build Map", self.map.build_map)
            self.sdk.map_menu.addAction("Build All Maps", self.map.build_all_map)
            self.sdk.map_menu.addAction("Info Map", self.map.info_map)

            self.sdk.texture_menu.addAction("Build Texture", self.texture.build_texture)
            self.sdk.texture_menu.addAction("Build All Textures", self.texture.build_all_texture)
            self.sdk.texture_menu.addAction("See Texture", self.texture.open_vtf)
            self.sdk.texture_menu.addAction("Texture To TGA", self.texture.texture_to_tga)
            self.sdk.texture_menu.addAction("Generate vmt", self.texture.generate_vmt)

            self.sdk.model_menu.addAction("Build Model", self.model.build_model)
            self.sdk.model_menu.addAction("Build All Models", self.model.build_all_model)
            self.sdk.model_menu.addAction("Generate QC File", self.model.generate_qc_file)

            self.sdk.other_menu.addAction("Create VPK", self.vpk.create_VPK)
            self.sdk.other_menu.addAction("Display VPK", self.vpk.display_VPK)
            self.sdk.other_menu.addAction("Display VPK Contents", self.vpk.display_vpk_contents)
            self.sdk.other_menu.addAction("Extract VPK", self.vpk.extract_VPK)

            self.sdk.other_menu.addAction("Build Caption", self.caption.build_caption)
            self.sdk.other_menu.addAction("Build All Captions", self.caption.build_all_captions)

            self.sdk.first_init = 1

    def new_project(self):
        pass  # Placeholder for new project functionality

    def launch_exit(self):
        print("Exit application.")
        QApplication.instance().quit()

    def sdk_doc(self):
        url = "https://developer.valvesoftware.com/wiki/SDK_Docs"
        webbrowser.open(url)

    def open_about_window(self):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("About")
        msg_box.setText("About Source SDK : assetsBrowser")
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = AssetsBrowser()
    browser.show()
    sys.stdout = browser.terminal
    sys.stderr = browser.terminal
    sys.exit(app.exec_())
