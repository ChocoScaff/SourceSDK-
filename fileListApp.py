import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QScrollArea, QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QIcon
from PIL import Image

class FileListApp(QMainWindow):
    def __init__(self, sourceSDK):
        super().__init__()
        self.sdk = sourceSDK
        self.current_folder = self.sdk.selected_folder
        self.firstfolder = self.sdk.selected_folder
        self.thumbnails = {}

        self.initUI()
        self.load_files(self.current_folder)

    def initUI(self):
        self.setWindowTitle("File List App")
        self.setGeometry(100, 100, 800, 600)

        main_layout = QVBoxLayout()
        button_layout = QHBoxLayout()

        self.up_button = QPushButton("Up")
        self.up_button.clicked.connect(self.go_up)
        button_layout.addWidget(self.up_button)

        self.open_button = QPushButton("Open Directory")
        self.open_button.clicked.connect(self.open_directory)
        button_layout.addWidget(self.open_button)

        main_layout.addLayout(button_layout)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(self.scroll_area)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QGridLayout(self.scroll_content)

        main_layout.addWidget(self.scroll_area)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def load_files(self, folder):
        for i in reversed(range(self.scroll_layout.count())):
            widget_to_remove = self.scroll_layout.itemAt(i).widget()
            self.scroll_layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        self.current_folder = folder
        self.files = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f)) or f.endswith((
            ".vmf", ".txt", ".cfg", ".vtf", ".vmt", ".qc", ".mdl", ".vcd", ".res", ".bsp", "dir.vpk", ".tga", ".wav", ".mp3", ".sln"))]

        columns = self.width() // 150
        if columns < 1:
            columns = 1
        row = 0
        col = 0

        for file in self.files:
            file_path = os.path.join(self.current_folder, file)
            file_frame = QWidget()
            file_layout = QVBoxLayout()
            file_frame.setLayout(file_layout)
            file_frame.setStyleSheet("border: 1px solid black;")

            file_label = QLabel(file)
            file_label.setAlignment(Qt.AlignCenter)
            file_label.setWordWrap(True)
            file_layout.addWidget(file_label)

            thumbnail = self.load_thumbnail(file_path)
            if thumbnail:
                thumbnail_label = QLabel()
                thumbnail_label.setPixmap(thumbnail)
                thumbnail_label.setAlignment(Qt.AlignCenter)
                file_layout.addWidget(thumbnail_label)

            if os.path.isdir(file_path):
                file_label.mouseDoubleClickEvent = lambda event, path=file_path: self.load_files(path)
            else:
                file_label.mouseDoubleClickEvent = lambda event, path=file_path: self.open_file(path)

            self.scroll_layout.addWidget(file_frame, row, col)
            col += 1
            if col >= columns:
                col = 0
                row += 1

    def load_thumbnail(self, file_path):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))

            if file_path.endswith(".vtf"):
                image = Image.open(os.path.join(base_path, "icons", "VTFEdit.png"))
            elif file_path.endswith(".mdl"):
                image = Image.open(os.path.join(base_path, "icons", "hlmv.png"))
            elif file_path.endswith(".tga"):
                image = Image.open(file_path)
            elif file_path.endswith(".vmf"):
                image = Image.open(os.path.join(base_path, "icons", "hammer.png"))
            elif file_path.endswith(".vcd"):
                image = Image.open(os.path.join(base_path, "icons", "hlposer.png"))
            elif file_path.endswith(".bsp"):
                image = Image.open(os.path.join(base_path, "icons", "source.png"))
            elif os.path.isdir(file_path):
                image = Image.open(os.path.join(base_path, "icons", "fileexplorer.png"))
            elif file_path.endswith(".txt") or file_path.endswith(".res") or file_path.endswith(".vmt") or file_path.endswith(".qc") or file_path.endswith(".smd") or file_path.endswith(".cfg"):
                image = Image.open(os.path.join(base_path, "icons", "txt.png"))
            elif file_path.endswith(".slb"):
                image = Image.open(os.path.join(base_path, "icons", "Visual_Studio.png"))

            if image:
                image.thumbnail((50, 50))
                thumbnail = QPixmap.fromImage(ImageQt(image))
                self.thumbnails[file_path] = thumbnail
                return thumbnail

        except Exception as e:
            print("Error loading thumbnail:", e)
        return None

    def go_up(self):
        parent_dir = os.path.dirname(self.current_folder)
        if parent_dir and self.current_folder != self.firstfolder:
            self.load_files(parent_dir)

    def open_directory(self):
        open_instance = Open(self.sdk)
        open_instance.open_directory(self.current_folder)

    def open_file(self, pathFile):
        open_instance = Open(self.sdk)
        open_instance.open_file(localpath=pathFile)

if __name__ == "__main__":
    sourceSDK = SourceSDK()
    app = QApplication(sys.argv)
    window = FileListApp(sourceSDK)
    window.show()
    sys.exit(app.exec_())
