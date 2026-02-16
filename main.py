import sys
from PyQt6.QtWidgets import *


class MapWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Яндекс Карты")
        self.setGeometry(100, 100, 800, 600)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        input_panel = QHBoxLayout()
        input_panel.addWidget(QLabel("Долгота:"))
        self.lon_edit = QLineEdit()
        input_panel.addWidget(self.lon_edit)
        input_panel.addWidget(QLabel("Широта:"))
        self.lat_edit = QLineEdit()
        input_panel.addWidget(self.lat_edit)
        input_panel.addWidget(QLabel("Масштаб:"))
        self.zoom_edit = QLineEdit()
        input_panel.addWidget(self.zoom_edit)
        self.load_btn = QPushButton("Загрузить карту")
        self.load_btn.clicked.connect(self.dummy)
        input_panel.addWidget(self.load_btn)
        layout.addLayout(input_panel)

        self.map_label = QLabel()
        self.map_label.setMinimumSize(600, 400)
        self.map_label.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.map_label)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec())

