import sys
import requests

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Карта")
        self.resize(300, 350)

        # Центральный виджет и layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Виджет для отображения карты
        self.Map_itself = QLabel()
        self.Map_itself.setFixedSize(250, 250)
        self.Map_itself.setStyleSheet("border: 1px solid black;")
        layout.addWidget(self.Map_itself)

        # Поля ввода координат
        self.lineEdit = QLineEdit()  # долгота
        self.lineEdit_2 = QLineEdit()  # широта
        self.lineEdit.setText("37.6176")
        self.lineEdit_2.setText("55.7558")
        layout.addWidget(self.lineEdit)
        layout.addWidget(self.lineEdit_2)

        # Кнопка загрузки карты
        self.pushButton_2 = QPushButton("Показать карту")
        layout.addWidget(self.pushButton_2)

        # Привязка обработчика
        self.pushButton_2.clicked.connect(self.show_map)

        # Текущий масштаб
        self.current_zoom = 12

        # Первоначальное отображение карты
        self.show_map()

    def show_map(self):
        coords = f"{self.lineEdit_2.text().strip()},{self.lineEdit.text().strip()}"
        # Используем текущее значение масштаба
        zoom = str(self.current_zoom)
        size = "250,250"
        map_type = "map"

        url = f"https://static-maps.yandex.ru/1.x/?ll={coords}&z={zoom}&size={size}&l={map_type}&pt={coords},pm2rdl"
        response = requests.get(url)

        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.Map_itself.setPixmap(pixmap)

    def keyPressEvent(self, event):
        """Обработка нажатий клавиш: PgUp и PgDown меняют масштаб."""
        if event.key() == Qt.Key.Key_PageUp:
            if self.current_zoom < 23:
                self.current_zoom += 1
                self.show_map()
        elif event.key() == Qt.Key.Key_PageDown:
            if self.current_zoom > 0:
                self.current_zoom -= 1
                self.show_map()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
