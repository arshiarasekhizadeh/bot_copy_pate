# Telegram Copy-Paste Bot

A simple and lightweight Telegram bot that automatically **copies messages** from one channel and **forwards/pastes** them into another channel.

This project demonstrates:
- Telegram Bot API usage  
- Automation with Python  
- Channel-to-channel message forwarding  

---

## 🚀 Features

- Copy messages from a source channel  
- Automatically forward/paste them into a destination channel  
- Supports text, media, and forwarded messages  
- Works on private & public channels (permissions required)

---

## 🛠️ Tech Stack

- Python  
- python-telegram-bot  
- Telegram Bot API  

---

## 📁 Project Structure

.
├── main.py
├── requirements.txt
└── README.md

---

## ⚙️ Setup & Usage

### 1. Install dependencies:
```bash
pip install -r requirements.txt
2. Add your Telegram bot token

Create a .env file (or edit config section):
TOKEN=your_telegram_bot_token
SOURCE_CHAT_ID=123456
DESTINATION_CHAT_ID=654321
3. Run the bot:
python main.py
📌 Notes

The bot must be an admin in both channels

If copying from private channels, the bot must be a member

For media forwarding, Telegram may apply restrictions

This bot is intended for automation/testing purposes
