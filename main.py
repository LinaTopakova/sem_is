from telegram.ext import ApplicationBuilder, CommandHandler #ApplicationBuilder - создание экземпляра бота, CommandHandler — обработка команд от user
from handlers import *
from data import TOKEN

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("setcity", setcity))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("random", random_attraction))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), city_name_handler))

print("Бот запущен")
app.run_polling() 

