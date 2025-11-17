# Base Gas Checker + Telegram Alerts

Простой и быстрый чекер цены газа в сети **Base** с мгновенными уведомлениями в Telegram, когда газ падает ниже заданного порога.

Идеально для снайперов, мемкоин-охотников и всех, кто ждёт дешёвый газ.

## Функции
- Обновление каждые ~5–6 секунд
- Уведомления только при низком газе (настраиваемый порог)
- Минимальная нагрузка
- Работает на любом VPS, Render, Railway, Fly.io и даже на домашнем ПК

## Установка и запуск

### 1. Клонируем репозиторий

git clone https://github.com/hudsoonme/base-gas-checker.git
cd base-gas-checker

### 2. Устанавливаем зависимостиbash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 3. Настраиваем .envbash

cp .env.example .env
nano .env

Заполни:

TELEGRAM_BOT_TOKEN=твой_токен
TELEGRAM_CHAT_ID=твой_chat_id_или_канал
GAS_THRESHOLD_GWEI=5        # ниже какого газа слать алерт
CHECK_INTERVAL=6            # частота проверки в секундах

### 4. Как создать Telegram-ботаНапиши @BotFather
    
 → /newbot → придумай имя
Получишь токен вида 123456:ABC-...
Добавь бота в любой чат/канал или напиши ему в ЛС
Узнай chat_id: перейди на https://api.telegram.org/bot<ТОКЕН>/getUpdates (или используй @userinfobot)

### 5. Запускаем:

python checker.py

____________________________________________________________________________________________________________
Чтобы работал 24/7 (рекомендуется)
Используй screen, tmux или systemd:

Через screen (самый простой способ)

screen -S basegas
python checker.py
# Нажми Ctrl+A, потом D — чтобы отсоединиться
# Вернуться: screen -r basegas

Через systemd (для VPS)
Создай файл /etc/systemd/system/basegas.service:ini

[Unit]
Description=Base Gas Checker
After=network.target

[Service]
WorkingDirectory=/home/user/base-gas-checker
ExecStart=/home/user/base-gas-checker/venv/bin/python /home/user/base-gas-checker/checker.py
Restart=always
User=user

[Install]
WantedBy=multi-user.target

Затем:

sudo systemctl daemon-reload
sudo systemctl enable --now basegas.service

Готово! Теперь ты всегда будешь знать, когда газ на Base дешёвый 

Автор: [@margo_hud](https://x.com/margo_hud)






