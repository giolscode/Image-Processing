import os
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog, QApplication

class FitsController:
    
    def __init__(self, model, view):
        
        self.model = model
        self.view = view
        self.current_pixmap = None 
        self.view.buttonGenerer.clicked.connect(self.select_fits_files)
        self.view.buttonAffichage.clicked.connect(self.display_image)

    def select_fits_files(self):
        red_filter = QFileDialog.getOpenFileName(self.view, "Sélectionnez le fichier FITS Rouge")
        green_filter = QFileDialog.getOpenFileName(self.view, "Sélectionnez le fichier FITS Vert")
        blue_filter = QFileDialog.getOpenFileName(self.view, "Sélectionnez le fichier FITS Bleu")

        if red_filter and green_filter and blue_filter:
            self.model.load_fits(red_filter, green_filter, blue_filter)

    def display_image(self):
        try:
            output_path = self.model.process_fits()
            self.current_pixmap = QPixmap(output_path)
            self.update_image_label()
            QApplication.instance().aboutToQuit.connect(lambda: os.remove(output_path))

        except Exception as e:
            self.view.imageLabel.setText(f"Erreur : {e}")

    def update_image_label(self):
        if self.current_pixmap:
            scaled_pixmap = self.current_pixmap.scaled(self.view.imageLabel.size(),Qt.AspectRatioMode.KeepAspectRatio)
            self.view.update_image(scaled_pixmap)