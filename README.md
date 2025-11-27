# Telegram Copy-Paste Bot

A lightweight automation bot that **monitors one Telegram channel** and
automatically **copies/forwards messages** to another channel.

This project demonstrates: - Telegram Bot API integration\
- Automation scripting in Python\
- Real-time message monitoring\
- Clean and minimal bot architecture

------------------------------------------------------------------------

## ⭐ Features

-   Copy messages from a source channel\
-   Forward/paste messages into a destination channel\
-   Supports **text**, **photos**, **videos**, **documents**, and
    forwarded messages\
-   Works for **private** and **public** channels (bot must be admin)\
-   Environment variables for clean configuration\
-   100% Python-based & easy to deploy

------------------------------------------------------------------------

## 📦 Tech Stack

-   **Python 3.8+**\
-   **python-telegram-bot**\
-   **dotenv**\
-   **Telegram Bot API**

------------------------------------------------------------------------

## 📁 Project Structure

    .
    ├── main.py
    ├── requirements.txt
    ├── .env (not included in repo)
    └── README.md

------------------------------------------------------------------------

## ⚙️ Installation

### 1. Clone the repository

``` bash
git clone https://github.com/arshiarasekhizadeh/bot_copy_pate.git
cd bot_copy_pate
```

### 2. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🔧 Configuration

Create a `.env` file in the root directory:

    BOT_TOKEN=your_bot_token_here
    SOURCE_CHAT_ID=-1001234567890
    DESTINATION_CHAT_ID=-1009876543210

------------------------------------------------------------------------

## ▶️ Running the Bot

``` bash
python main.py
```

------------------------------------------------------------------------

## 🔍 How It Works (Architecture)

    ┌──────────────────┐        ┌────────────────────────┐
    │ Source Channel    │        │ Destination Channel    │
    └───────▲──────────┘        └──────────▲────────────┘
            │                               │
            │ new message event             │ forwarded message
            │                               │
    ┌───────┴────────────────────────────────────────────┐
    │        Telegram Copy-Paste Bot (main.py)           │
    └────────────────────────────────────────────────────┘

------------------------------------------------------------------------

## 🛡️ Requirements & Permissions

-   Bot must be **admin** in both channels\
-   Telegram privacy limits still apply

------------------------------------------------------------------------

## 📈 Possible Improvements

-   Logging\
-   Docker support\
-   Multi-channel forwarding\
-   Message filters

------------------------------------------------------------------------

## 📄 License

MIT License

------------------------------------------------------------------------

## 📬 Contact

Email: rasekhizadearshia@gmail.com
