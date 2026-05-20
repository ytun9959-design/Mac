import os
import telebot
from flask import Flask
from threading import Thread
from scapy.all import ARP, Ether, srp, conf

# --- Configuration ---
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE" # ဤနေရာတွင် သင့် Bot Token ထည့်ပါ
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# --- Web Server (Render အတွက် လိုအပ်သည်) ---
@app.route('/')
def index():
    return "YourGod Bot is running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# --- Network Scanner Logic ---
@bot.message_handler(commands=['scan'])
def ask_for_ip(message):
    msg = bot.reply_to(message, "IP Range ကို ရိုက်ပေးပါ (ဥပမာ: 192.168.1.0/24)")
    bot.register_next_step_handler(msg, process_scan)

def process_scan(message):
    ip_range = message.text
    bot.reply_to(message, f"[*] Scanning: {ip_range} ...")
    
    try:
        conf.L3socket = None
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        result = srp(ether/arp, timeout=5, verbose=0)[0]
        
        output = f"--- Scan Result for {ip_range} ---\n"
        for sent, received in result:
            output += f"IP: {received.psrc} | MAC: {received.hwsrc}\n"
        
        if len(result) == 0:
            output = "[-] Device တစ်ခုမှ ရှာမတွေ့ပါ။"
            
        bot.reply_to(message, output)
    except Exception as e:
        bot.reply_to(message, f"[-] Error: {str(e)}")

# --- Main Start ---
if __name__ == "__main__":
    # Flask Server ကို Background မှာ အလုပ်လုပ်ခိုင်းခြင်း
    server_thread = Thread(target=run_flask)
    server_thread.start()
    
    # Telegram Bot ကို စတင်ခြင်း
    print("Bot is running...")
    bot.polling()