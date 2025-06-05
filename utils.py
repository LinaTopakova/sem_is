import requests
from datetime import datetime
from telegram import ReplyKeyboardMarkup
from data import API_KEY

def get_city_coords(city_name):
    url = "https://catalog.api.2gis.com/3.0/items"
    params = {
        "q": city_name,
        "key": API_KEY,
        "fields": "items.point"
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print(f"Ошибка запроса get_city_coords: {resp.status_code}")
        return None
    data = resp.json()
    if data.get("meta", {}).get("code") != 200 or not data.get("result", {}).get("items"):
        print("Город не найден или ошибка в ответе get_city_coords")
        return None
    point = data["result"]["items"][0].get("point")
    if not point or "lat" not in point or "lon" not in point:
        print("Координаты города отсутствуют")
        return None
    return point["lat"], point["lon"]

def search_attractions(lat, lon, radius=5000, limit=20):
    url = "https://catalog.api.2gis.com/3.0/items"
    params = {
        "q": "достопримечательность",
        "location": f"{lon},{lat}",
        "key": API_KEY
    }
    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print(f"Ошибка запроса search_attractions: {resp.status_code}")
        return []
    data = resp.json()
    if data.get("meta", {}).get("code") != 200:
        print(f"Ошибка в ответе search_attractions: {data.get('meta', {}).get('message')}")
        return []
    items = data.get("result", {}).get("items", [])
    return items

def log_dialog(user_id, text):
    filename = f"log/{user_id}.log"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{now}] {text}\n")

def get_main_keyboard():
    keyboard = [
        ["/start"], ["/search"],
        ["/random"], ["/help"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
