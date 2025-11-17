# checker.py
import time
import requests
import logging
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, GAS_THRESHOLD_GWEI, CHECK_INTERVAL

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Base RPC
BASE_RPC = "https://mainnet.base.org"

headers = {"Content-Type": "application/json"}

payload = {
    "jsonrpc": "2.0",
    "method": "eth_gasPrice",
    "params": [],
    "id": 1
}

last_notified_gas = None
notified_low = False

def get_gas_price_gwei():
    try:
        response = requests.post(BASE_RPC, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            gas_price_wei = int(response.json()["result"], 16)
            gas_price_gwei = gas_price_wei / 1e9
            return round(gas_price_gwei, 3)
        else:
            logging.error(f"RPC error: {response.status_code}")
            return None
    except Exception as e:
        logging.error(f"Request failed: {e}")
        return None

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=data, timeout=10)
    except Exception as e:
        logging.error(f"Telegram send failed: {e}")

def main():
    global last_notified_gas, notified_low

    logging.info("Base Gas Checker запущен...")
    send_telegram_message("🚀 <b>Base Gas Checker запущен</b>\nОжидаю низкий газ...")

    while True:
        gas = get_gas_price_gwei()
        if gas is None:
            time.sleep(CHECK_INTERVAL)
            continue

        status = "🟡 Нормальный" if gas > GAS_THRESHOLD_GWEI else "🟢 НИЗКИЙ!"
        message = f"<b>Base Gas Price</b>\n{status} <code>{gas}</code> gwei"

        # Уведомляем только при смене состояния или каждые 10+ gwei изменения
        should_notify = False
        if gas <= GAS_THRESHOLD_GWEI and not notified_low:
            should_notify = True
            notified_low = True
            message = f"🚨 <b>ГАЗ НИЗКИЙ НА BASE!</b> 🚨\n<code>{gas}</code> gwei\nПора снайпить!"
        elif gas > GAS_THRESHOLD_GWEI and notified_low:
            should_notify = True
            notified_low = False
            message = f"🔥 Газ снова вырос: <code>{gas}</code> gwei"

        # Дополнительно шлём каждые ~15 gwei изменения (опционально)
        if last_notified_gas is not None and abs(gas - last_notified_gas) >= 15:
            should_notify = True

        if should_notify or last_notified_gas is None:
            logging.info(message.replace("<code>", "").replace("</code>", ""))
            send_telegram_message(message)
            last_notified_gas = gas

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
