# Base Gas Checker + Telegram Alerts.

Простой и быстрый чекер цены газа в сети **Base** с мгновенными уведомлениями в Telegram, когда газ падает ниже заданного порога.  
Подходит для снайперов, мемкоин-охотников и всех, кто ждёт дешёвый газ.

## 🚀 Функции

- Обновление каждые **5–6 секунд**
- Telegram-уведомления, когда газ **ниже заданного порога**
- Минимальная нагрузка
- Работает на **VPS, Render, Railway, Fly.io, локальном ПК**

## 📦 Установка и запуск

### 1. Клонируем репозиторий

```bash
git clone https://github.com/hudsoonme/base-gas-checker.git
cd base-gas-checker
```

### 2. Устанавливаем зависимости

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Настраиваем `.env`

```bash
cp .env.example .env
nano .env
```

Заполните:

```
TELEGRAM_BOT_TOKEN=твой_токен
TELEGRAM_CHAT_ID=твой_chat_id_или_канал
GAS_THRESHOLD_GWEI=5        # ниже какого газа слать алерт
CHECK_INTERVAL=6            # частота проверки в секундах
```

### 4. Как создать Telegram-бота

1. Написать **@BotFather**
2. Команда `/newbot` → придумать имя
3. Получите токен формата:

```
123456:ABC-DEF1234...
```

4. Добавьте бота в чат / канал или напишите ему в ЛС
5. Узнайте `chat_id`:

Перейдите:

```
https://api.telegram.org/bot<ТОКЕН>/getUpdates
```

или используйте @userinfobot

### 5. Запуск

```bash
python checker.py
```

## 🟢 Запуск 24/7 (рекомендуется)

### Через `screen` (самый простой вариант)

```bash
screen -S basegas
python checker.py
```

Отсоединиться: **Ctrl+A**, затем **D**  
Вернуться:

```bash
screen -r basegas
```

### Через `systemd` (для VPS)

Создать файл:

**/etc/systemd/system/basegas.service**

```ini
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
```

Активировать:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now basegas.service
```

## Готово!

Теперь ты всегда будешь знать, когда газ в Base становится дешёвым.

Автор: **[@margo_hud](https://x.com/margo_hud)**






