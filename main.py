import sys
from PyQt6.QtWidgets import QApplication
from model import FitsModel
from view import FitsView
from controller import FitsController 

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    model = FitsModel()
    view = FitsView()
    controller = FitsController(model, view)

    view.show()
    sys.exit(app.exec())