import requests


class YandexApiClient:
    def __init__(self, geocoder_key, static_maps_key):
        self.geocoder_key = geocoder_key
        self.static_maps_key = static_maps_key

    def geocode(self, query):
        """Возвращает (lon, lat) или None, если ничего не найдено."""
        url = "https://geocode-maps.yandex.ru/1.x/"
        params = {
            "geocode": query,
            "format": "json",
            "apikey": self.geocoder_key
        }
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        feature_member = data['response']['GeoObjectCollection']['featureMember']
        if not feature_member:
            return None

        pos = feature_member[0]['GeoObject']['Point']['pos']
        lon, lat = pos.split()
        return float(lon), float(lat)

    def get_static_map(self, lon, lat, zoom, size=(250, 250), marker=None):
        url = "https://static-maps.yandex.ru/1.x/"
        params = {
            "ll": f"{lon},{lat}",
            "z": zoom,
            "size": f"{size[0]},{size[1]}",
            "l": "map",
            "apikey": self.static_maps_key
        }
        if marker:
            params["pt"] = f"{marker[0]},{marker[1]},pm2rdl"

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.content
        return None
