import os
import telebot
import requests
from flask import Flask
from threading import Thread

BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE" # ဒီနေရာမှာ သင့် Bot Token အစစ်ထည့်ပါ
PHONE_SERVER_URL = "https://attractions-factors-permissions-demographic.trycloudflare.com/scan" # သင့် Cloudflare လင့်ခ်

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is online!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

@bot.message_handler(commands=['scan'])
def scan_network(message):
    try:
        response = requests.get(PHONE_SERVER_URL, timeout=15)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

if __name__ == "__main__":
    Thread(target=run_flask).start()
    bot.polling()
