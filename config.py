# config.py
from decouple import config

TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID    = config('TELEGRAM_CHAT_ID')
GAS_THRESHOLD_GWEI  = config('GAS_THRESHOLD_GWEI', default=5, cast=int)  # порог в gwei
CHECK_INTERVAL      = config('CHECK_INTERVAL', default=6, cast=int)      # секунд
