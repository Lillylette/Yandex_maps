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
    QComboBox,
)


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Карта")
        self.resize(300, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.Map_itself = QLabel()
        self.Map_itself.setFixedSize(250, 250)
        self.Map_itself.setStyleSheet("border: 1px solid black; background-color: white;")
        self.Map_itself.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Map_itself.setText("Введите координаты и нажмите кнопку")
        self.layout.addWidget(self.Map_itself)

        self.lon_edit = QLineEdit()
        self.lat_edit = QLineEdit()
        self.lon_edit.setPlaceholderText("Долгота (например, 37.6176)")
        self.lat_edit.setPlaceholderText("Широта (например, 55.7558)")
        self.lon_edit.setText("37.6176")
        self.lat_edit.setText("55.7558")
        self.layout.addWidget(self.lon_edit)
        self.layout.addWidget(self.lat_edit)

        self.btn_show = QPushButton("Показать карту")
        self.layout.addWidget(self.btn_show)

        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Светлая тема")
        self.theme_combo.addItem("Тёмная тема")
        self.layout.addWidget(self.theme_combo)

        self.btn_show.clicked.connect(self.show_map)
        self.theme_combo.currentIndexChanged.connect(self.apply_theme)

        self.current_zoom = 12

        self.apply_theme()
        self.show_map()

    def apply_theme(self):
        if self.theme_combo.currentIndex() == 0:
            self.central_widget.setStyleSheet("background-color: #f0f0f0;")
            self.Map_itself.setStyleSheet("border: 1px solid black; background-color: white;")
            self.lon_edit.setStyleSheet("")
            self.lat_edit.setStyleSheet("")
            self.btn_show.setStyleSheet("")
            self.theme_combo.setStyleSheet("")
        else:
            self.central_widget.setStyleSheet("background-color: #2b2b2b;")
            self.Map_itself.setStyleSheet("border: 1px solid #555; background-color: #1e1e1e;")
            self.lon_edit.setStyleSheet("background-color: #3c3c3c; color: white; border: 1px solid #555;")
            self.lat_edit.setStyleSheet("background-color: #3c3c3c; color: white; border: 1px solid #555;")
            self.btn_show.setStyleSheet("background-color: #3c3c3c; color: white; border: 1px solid #555;")
            self.theme_combo.setStyleSheet("background-color: #3c3c3c; color: white; border: 1px solid #555;")

    def show_map(self):
        self.Map_itself.clear()
        self.Map_itself.setText("Загрузка...")
        QApplication.processEvents()

        lon = self.lon_edit.text().strip()
        lat = self.lat_edit.text().strip()
        coords = f"{lon},{lat}"
        zoom = str(self.current_zoom)
        size = "250,250"
        map_type = "map"

        url = f"https://static-maps.yandex.ru/1.x/?ll={coords}&z={zoom}&size={size}&l={map_type}&pt={coords},pm2rdl"
        print(f"URL: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                pixmap = QPixmap()
                if pixmap.loadFromData(response.content):
                    self.Map_itself.setPixmap(pixmap)
                    self.Map_itself.setText("")
                else:
                    self.Map_itself.setText("Ошибка загрузки изображения")
            else:
                self.Map_itself.setText(f"Ошибка HTTP {response.status_code}")
        except requests.exceptions.ConnectionError:
            self.Map_itself.setText("Ошибка соединения\nПроверьте интернет")
        except requests.exceptions.Timeout:
            self.Map_itself.setText("Тайм-аут запроса")
        except Exception as e:
            self.Map_itself.setText(f"Неизвестная ошибка")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp and self.current_zoom < 23:
            self.current_zoom += 1
            self.show_map()
        elif event.key() == Qt.Key.Key_PageDown and self.current_zoom > 0:
            self.current_zoom -= 1
            self.show_map()
        else:
            super().keyPressEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
