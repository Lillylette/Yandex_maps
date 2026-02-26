import sys
import requests
import os
from dotenv import load_dotenv

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
)

load_dotenv()


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Карта")
        self.resize(350, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        map_zoom_layout = QHBoxLayout()

        self.Map_itself = QLabel()
        self.Map_itself.setFixedSize(250, 250)
        self.Map_itself.setStyleSheet("border: 1px solid black; background-color: white;")
        self.Map_itself.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.Map_itself.setText("Введите координаты или название")
        self.Map_itself.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        map_zoom_layout.addWidget(self.Map_itself)

        zoom_buttons_layout = QVBoxLayout()

        zoom_buttons_layout.addStretch()

        self.zoom_in_btn = QPushButton("+")
        self.zoom_in_btn.setFixedSize(30, 30)
        self.zoom_in_btn.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.zoom_out_btn = QPushButton("-")
        self.zoom_out_btn.setFixedSize(30, 30)
        self.zoom_out_btn.setStyleSheet("font-size: 16px; font-weight: bold;")

        zoom_buttons_layout.addWidget(self.zoom_in_btn)
        zoom_buttons_layout.addWidget(self.zoom_out_btn)

        zoom_buttons_layout.addStretch()

        map_zoom_layout.addLayout(zoom_buttons_layout)

        self.main_layout.addLayout(map_zoom_layout)

        self.lon_edit = QLineEdit()
        self.lat_edit = QLineEdit()
        self.lon_edit.setPlaceholderText("Долгота (например, 37.6176)")
        self.lat_edit.setPlaceholderText("Широта (например, 55.7558)")
        self.lon_edit.setText("37.6176")
        self.lat_edit.setText("55.7558")
        self.main_layout.addWidget(self.lon_edit)
        self.main_layout.addWidget(self.lat_edit)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Введите название объекта для поиска")
        self.main_layout.addWidget(self.search_edit)

        self.btn_search = QPushButton("Искать")
        self.main_layout.addWidget(self.btn_search)

        self.btn_show = QPushButton("Показать карту")
        self.main_layout.addWidget(self.btn_show)

        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Светлая тема")
        self.theme_combo.addItem("Тёмная тема")
        self.main_layout.addWidget(self.theme_combo)

        self.btn_show.clicked.connect(self.show_map)
        self.btn_search.clicked.connect(self.search_object)
        self.search_edit.returnPressed.connect(self.search_object)
        self.theme_combo.currentIndexChanged.connect(self.apply_theme)
        self.zoom_in_btn.clicked.connect(self.zoom_in)
        self.zoom_out_btn.clicked.connect(self.zoom_out)

        self.current_zoom = 12
        self.MIN_LON = -180
        self.MAX_LON = 180
        self.MIN_LAT = -90
        self.MAX_LAT = 90

        self.GEOCODER_API_KEY = os.getenv('GEOCODER_API_KEY')
        self.STATIC_MAPS_API_KEY = os.getenv('STATIC_MAPS_API_KEY')

        if not self.GEOCODER_API_KEY or not self.STATIC_MAPS_API_KEY:
            print("ОШИБКА: API ключи не найдены в .env файле!")
            print("Убедитесь, что файл .env существует и содержит:")
            print("GEOCODER_API_KEY=ваш_ключ")
            print("STATIC_MAPS_API_KEY=ваш_ключ")
            sys.exit(1)

        self.current_lon = 37.6176
        self.current_lat = 55.7558
        self.marker_lon = 37.6176
        self.marker_lat = 55.7558
        self.has_marker = True

        self.apply_theme()
        self.show_map()
        self.Map_itself.setFocus()

    def apply_theme(self):
        if self.theme_combo.currentIndex() == 0:
            self.central_widget.setStyleSheet("background-color: #f0f0f0;")
            self.Map_itself.setStyleSheet("border: 1px solid black; background-color: white;")
            self.lon_edit.setStyleSheet("")
            self.lat_edit.setStyleSheet("")
            self.search_edit.setStyleSheet("")
            self.btn_search.setStyleSheet("")
            self.btn_show.setStyleSheet("")
            self.zoom_in_btn.setStyleSheet("font-size: 16px; font-weight: bold;")
            self.zoom_out_btn.setStyleSheet("font-size: 16px; font-weight: bold;")
            self.theme_combo.setStyleSheet("")
        else:
            self.central_widget.setStyleSheet("background-color: #2b2b2b;")
            self.Map_itself.setStyleSheet("border: 1px solid #555; background-color: #1e1e1e;")
            self.lon_edit.setStyleSheet("background-color: #3c3c3c; color: white; border: 1px solid #555;")
            self.lat_edit.setStyleSheet("background-color: #3c3c3c; color: white; border: 1px solid #555;")
            self.search_edit.setStyleSheet("background-color: #3c3c3c; color: white; border: 1px solid #555;")
            self.btn_search.setStyleSheet("background-color: #3c3c3c; color: white; border: 1px solid #555;")
            self.btn_show.setStyleSheet("background-color: #3c3c3c; color: white; border: 1px solid #555;")
            self.zoom_in_btn.setStyleSheet("background-color: #3c3c3c; color: white; border: 1px solid #555; font-size: 16px; font-weight: bold;")
            self.zoom_out_btn.setStyleSheet("background-color: #3c3c3c; color: white; border: 1px solid #555; font-size: 16px; font-weight: bold;")
            self.theme_combo.setStyleSheet("background-color: #3c3c3c; color: white; border: 1px solid #555;")

    def search_object(self):
        query = self.search_edit.text().strip()
        if not query:
            self.Map_itself.setText("Введите запрос для поиска")
            return

        self.Map_itself.clear()
        self.Map_itself.setText("Поиск...")
        QApplication.processEvents()

        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "geocode": query,
            "format": "json",
            "apikey": self.GEOCODER_API_KEY
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                feature_member = data['response']['GeoObjectCollection']['featureMember']
                if feature_member:
                    pos = feature_member[0]['GeoObject']['Point']['pos']
                    lon, lat = pos.split()

                    self.lon_edit.setText(lon)
                    self.lat_edit.setText(lat)

                    self.current_lon = float(lon)
                    self.current_lat = float(lat)
                    self.marker_lon = float(lon)
                    self.marker_lat = float(lat)
                    self.has_marker = True

                    self.show_map()
                else:
                    self.Map_itself.setText("Объект не найден")
            else:
                self.Map_itself.setText(f"Ошибка геокодера: {response.status_code}")
        except requests.exceptions.ConnectionError:
            self.Map_itself.setText("Ошибка соединения\nПроверьте интернет")
        except requests.exceptions.Timeout:
            self.Map_itself.setText("Тайм-аут запроса")
        except Exception as e:
            self.Map_itself.setText(f"Ошибка поиска: {str(e)[:30]}")

    def show_map(self):
        self.Map_itself.clear()
        self.Map_itself.setText("Загрузка карты...")
        QApplication.processEvents()

        try:
            lon = self.lon_edit.text().strip()
            lat = self.lat_edit.text().strip()

            if not lon or not lat:
                self.Map_itself.setText("Введите координаты")
                return

            self.current_lon = float(lon)
            self.current_lat = float(lat)

            coords = f"{lon},{lat}"
            zoom = str(self.current_zoom)
            size = "250,250"
            map_type = "map"

            url = f"https://static-maps.yandex.ru/1.x/?ll={coords}&z={zoom}&size={size}&l={map_type}&apikey={self.STATIC_MAPS_API_KEY}"

            if self.has_marker:
                marker_coords = f"{self.marker_lon},{self.marker_lat}"
                url += f"&pt={marker_coords},pm2rdl"

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                pixmap = QPixmap()
                if pixmap.loadFromData(response.content):
                    self.Map_itself.setPixmap(pixmap)
                    self.Map_itself.setText("")
                else:
                    self.Map_itself.setText("Ошибка загрузки изображения")
            else:
                self.Map_itself.setText(f"Ошибка карты: {response.status_code}")

        except requests.exceptions.ConnectionError:
            self.Map_itself.setText("Ошибка соединения\nПроверьте интернет")
        except requests.exceptions.Timeout:
            self.Map_itself.setText("Тайм-аут запроса")
        except ValueError:
            self.Map_itself.setText("Некорректные координаты")
        except Exception:
            self.Map_itself.setText("Неизвестная ошибка")

    def move_map(self, delta_lon, delta_lat):
        try:
            current_lon = float(self.lon_edit.text().strip())
            current_lat = float(self.lat_edit.text().strip())

            new_lon = current_lon + delta_lon
            new_lat = current_lat + delta_lat

            if new_lon < self.MIN_LON:
                new_lon = self.MIN_LON
            elif new_lon > self.MAX_LON:
                new_lon = self.MAX_LON

            if new_lat < self.MIN_LAT:
                new_lat = self.MIN_LAT
            elif new_lat > self.MAX_LAT:
                new_lat = self.MAX_LAT

            self.lon_edit.setText(f"{new_lon:.6f}")
            self.lat_edit.setText(f"{new_lat:.6f}")

            self.current_lon = new_lon
            self.current_lat = new_lat

            self.show_map()
        except ValueError:
            pass

    def zoom_in(self):
        if self.current_zoom < 23:
            self.current_zoom += 1
            self.show_map()

    def zoom_out(self):
        if self.current_zoom > 0:
            self.current_zoom -= 1
            self.show_map()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp and self.current_zoom < 23:
            self.current_zoom += 1
            self.show_map()
        elif event.key() == Qt.Key.Key_PageDown and self.current_zoom > 0:
            self.current_zoom -= 1
            self.show_map()
        elif event.key() == Qt.Key.Key_Up:
            self.move_map(0, -self.get_move_step())
        elif event.key() == Qt.Key.Key_Down:
            self.move_map(0, self.get_move_step())
        elif event.key() == Qt.Key.Key_Left:
            self.move_map(-self.get_move_step(), 0)
        elif event.key() == Qt.Key.Key_Right:
            self.move_map(self.get_move_step(), 0)
        else:
            super().keyPressEvent(event)

    def get_move_step(self):
        step_map = {
            1: 45.0, 2: 30.0, 3: 20.0, 4: 15.0, 5: 10.0,
            6: 7.0, 7: 5.0, 8: 3.5, 9: 2.5, 10: 1.8,
            11: 1.2, 12: 0.8, 13: 0.5, 14: 0.35, 15: 0.25,
            16: 0.18, 17: 0.12, 18: 0.08, 19: 0.05, 20: 0.035,
            21: 0.025, 22: 0.018, 23: 0.012
        }
        return step_map.get(self.current_zoom, 0.5)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())
