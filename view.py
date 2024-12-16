from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider, QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class FitsView(QWidget):
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Interface d'affichage")
        self.resize(1000, 800)

        # Boutons
        self.buttonGenerer = QPushButton("Charger les fichiers FITS")
        self.buttonAffichage = QPushButton("Afficher l'image")

        # Label pour afficher l'image
        self.imageLabel = QLabel(self)
        self.imageLabel.setText("Aucune image chargée")
        self.imageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.imageLabel.setFixedSize(800, 800)

        # Sliders pour ajuster les canaux RGB
        self.sliderRed = QSlider(Qt.Orientation.Vertical)
        self.sliderRed.setRange(1, 200)  
        self.sliderRed.setValue(100)  
        self.sliderRed.setTickPosition(QSlider.TickPosition.TicksRight)

        self.sliderGreen = QSlider(Qt.Orientation.Vertical)
        self.sliderGreen.setRange(1, 200)
        self.sliderGreen.setValue(100)
        self.sliderGreen.setTickPosition(QSlider.TickPosition.TicksRight)

        self.sliderBlue = QSlider(Qt.Orientation.Vertical)
        self.sliderBlue.setRange(1, 200)
        self.sliderBlue.setValue(100)
        self.sliderBlue.setTickPosition(QSlider.TickPosition.TicksRight)

        # Labels pour les sliders
        sliderLabelsLayout = QVBoxLayout()
        sliderLabelsLayout.addWidget(QLabel("Rouge"))
        sliderLabelsLayout.addWidget(self.sliderRed)
        sliderLabelsLayout.addWidget(QLabel("Vert"))
        sliderLabelsLayout.addWidget(self.sliderGreen)
        sliderLabelsLayout.addWidget(QLabel("Bleu"))
        sliderLabelsLayout.addWidget(self.sliderBlue)

        # Layout pour les sliders
        sliderLayout = QVBoxLayout()
        sliderLayout.addLayout(sliderLabelsLayout)

        # Layout pour les boutons
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.buttonGenerer)
        buttonLayout.addWidget(self.buttonAffichage)

        # Layout principal
        mainLayout = QHBoxLayout()
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.imageLabel, alignment=Qt.AlignmentFlag.AlignCenter)
        leftLayout.addLayout(buttonLayout)

        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(sliderLayout)

        self.setLayout(mainLayout)

    def update_image(self, pixmap):
        scaled_pixmap = pixmap.scaled(self.imageLabel.size(),Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
        self.imageLabel.setPixmap(scaled_pixmap)