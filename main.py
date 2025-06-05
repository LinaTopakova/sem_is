from telegram.ext import ApplicationBuilder, CommandHandler
from handlers import *
from data import TOKEN

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("setcity", setcity))
app.add_handler(CommandHandler("search", search))
app.add_handler(CommandHandler("random", random_attraction))

print("Бот запущен")
app.run_polling()

