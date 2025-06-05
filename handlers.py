import random
from telegram import Update
from telegram.ext import ContextTypes
from data import user_cities
from utils import get_city_coords, search_attractions, log_dialog, get_main_keyboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = "Привет! Я бот для поиска достопримечательностей. Используйте меню ниже для навигации."
    await update.message.reply_text(text, reply_markup=get_main_keyboard())
    log_dialog(user_id, f"User: /start\nBot: {text}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = (
        "Доступные команды:\n"
        "/start - приветствие\n"
        "/help - помощь\n"
        "/setcity <город> - установить город\n"
        "/search - поиск достопримечательностей в городе\n"
        "/random - случайная достопримечательность\n"
    )
    await update.message.reply_text(text, reply_markup=get_main_keyboard())
    log_dialog(user_id, f"User: /help\nBot: {text}")

async def setcity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not context.args:
        text = "Пожалуйста, укажите город после команды, например: /setcity Москва"
        await update.message.reply_text(text, reply_markup=get_main_keyboard())
        log_dialog(user_id, f"User: /setcity\nBot: {text}")
        return
    city = " ".join(context.args)
    coords = get_city_coords(city)
    if coords is None:
        text = f"Город '{city}' не найден."
        await update.message.reply_text(text, reply_markup=get_main_keyboard())
        log_dialog(user_id, f"User: /setcity {city}\nBot: {text}")
        return
    user_cities[user_id] = {"city": city, "coords": coords}
    text = f"Город установлен: {city}"
    await update.message.reply_text(text, reply_markup=get_main_keyboard())
    log_dialog(user_id, f"User: /setcity {city}\nBot: {text}")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_cities:
        text = "Сначала установите город командой /setcity"
        await update.message.reply_text(text, reply_markup=get_main_keyboard())
        log_dialog(user_id, f"User: /search\nBot: {text}")
        return
    city = user_cities[user_id]["city"]
    lat, lon = user_cities[user_id]["coords"]
    attractions = search_attractions(lat, lon)
    if not attractions:
        text = f"Достопримечательности для города {city} не найдены."
        await update.message.reply_text(text, reply_markup=get_main_keyboard())
        log_dialog(user_id, f"User: /search\nBot: {text}")
        return
    text = f"Достопримечательности в {city}:\n"
    for i, attr in enumerate(attractions[:10], 1):
        name = attr.get("name", "Без названия")
        address_name = attr.get("address_name", "")
        address_comment = attr.get("address_comment", "")
        address = address_name
        if address_comment:
            address += f", {address_comment}"
        if not address:
            address = "Адрес не указан"
        text += f"{i}. {name} — {address}\n"
    await update.message.reply_text(text, reply_markup=get_main_keyboard())
    log_dialog(user_id, f"User: /search\nBot: {text}")

async def random_attraction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_cities:
        text = "Сначала установите город командой /setcity"
        await update.message.reply_text(text, reply_markup=get_main_keyboard())
        log_dialog(user_id, f"User: /random\nBot: {text}")
        return

    city = user_cities[user_id]["city"]
    lat, lon = user_cities[user_id]["coords"]

    attractions = search_attractions(lat, lon, radius=5000, limit=100)
    if not attractions:
        text = f"Достопримечательности для города {city} не найдены."
        await update.message.reply_text(text, reply_markup=get_main_keyboard())
        log_dialog(user_id, f"User: /random\nBot: {text}")
        return

    random_attr = random.choice(attractions)
    name = random_attr.get("name", "Без названия")
    address_name = random_attr.get("address_name", "")
    address_comment = random_attr.get("address_comment", "")
    address = address_name
    if address_comment:
        address += f", {address_comment}"
    if not address:
        address = "Адрес не указан"

    text = f"Случайная достопримечательность в {city}:\n{name} — {address}"
    await update.message.reply_text(text, reply_markup=get_main_keyboard())
    log_dialog(user_id, f"User: /random\nBot: {text}")

