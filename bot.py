from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from routeros_api import RouterOsApiPool

# Konfigurasi MikroTik dan Bot
MIKROTIK_IP = "192.168.88.1"  # Ganti dengan IP MikroTik Anda
MIKROTIK_USERNAME = "admin"   # Username MikroTik
MIKROTIK_PASSWORD = "password"  # Password MikroTik
MIKROTIK_PORT = 8728  # Port API MikroTik

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # Ganti dengan token bot Anda

# Fungsi untuk menghubungkan ke MikroTik
def connect_to_mikrotik():
    try:
        api_pool = RouterOsApiPool(MIKROTIK_IP, username=MIKROTIK_USERNAME, password=MIKROTIK_PASSWORD, port=MIKROTIK_PORT)
        api = api_pool.get_api()
        return api
    except Exception as e:
        print(f"Error connecting to MikroTik: {e}")
        return None

# Fungsi untuk mendapatkan data The Dude
def get_dude_info():
    api = connect_to_mikrotik()
    if not api:
        return "Gagal terhubung ke MikroTik."
    
    try:
        # Query informasi dari The Dude
        devices = api.get_resource('/dude/device').get()
        info = "Informasi The Dude:\n\n"
        for device in devices:
            name = device.get("name", "Unknown")
            status = device.get("status", "Unknown")
            address = device.get("address", "Unknown")
            info += f"Nama: {name}\nStatus: {status}\nAlamat: {address}\n\n"
        return info
    except Exception as e:
        return f"Error mendapatkan data: {e}"

# Command handler untuk Telegram
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Selamat datang! Ketik /dude untuk mendapatkan informasi dari The Dude.")

def dude(update: Update, context: CallbackContext):
    info = get_dude_info()
    update.message.reply_text(info)

# Main function
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("dude", dude))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
