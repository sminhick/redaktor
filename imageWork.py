import os
from PyQt5.QtWidgets import QFileDialog

class ImageWorkdir:
    def __init__(self):
        self.extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        self.workdir = ''

    def filter_files(self, files):
        res = []
        for file in files:
            for ext in self.extensions:
                if file.lower().endswith(ext):
                    res.append(file)
        return res

    def choose_workdir(self):
        self.workdir = QFileDialog.getExistingDirectory()
        return self.workdir

    def get_image_filenames(self, directory=None):
        directory = directory or self.workdir
        return self.filter_files(os.listdir(directory))

    def show_filenames_in_list(self, list_widget):
        if self.choose_workdir():
            list_widget.clear()
            list_widget.addItems(self.get_image_filenames())
