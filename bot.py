import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# Set your API keys and Chat ID here
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID", "YOUR_TELEGRAM_CHAT_ID")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY", "YOUR_FINNHUB_API_KEY")

def get_banknifty_finnhub():
    url = f"https://finnhub.io/api/v1/quote?symbol=NSE:BANKNIFTY&token={FINNHUB_API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            current = data.get("c", "N/A")
            open_ = data.get("o", "N/A")
            high = data.get("h", "N/A")
            low = data.get("l", "N/A")
            change = round(((current - open_) / open_) * 100, 2) if current != "N/A" and open_ != 0 else "N/A"
            return f"🔔 BankNifty Update:\nPrice: {current}\nChange: {change}%\nHigh: {high}\nLow: {low}"
        else:
            return f"API Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Failed to send message: {e}")

def main():
    while True:
        message = get_banknifty_finnhub()
        print(f"Sending: {message}")
        send_telegram_message(message)
        time.sleep(900)  # every 15 minutes

if __name__ == "__main__":
    main()
