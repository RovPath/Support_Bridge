# 🤝 Support_Bridge Bot

A powerful asynchronous Telegram bot that creates **child support bots** and forwards user requests to a central chat. Ideal for project support teams, help desks, and multi‑bot management.

## 📌 Purpose

- **Create support bots** on the fly – register any Telegram bot token.
- **Bind notification targets** – receive all user messages in a specific group, channel, or private chat.
- **Forward all media types** – photos, videos, documents, audio, voice, stickers, GIFs, contacts, locations, polls.
- **Reply to users** – support agents can answer directly from the bound chat (text, photo, video, sticker, etc.).
- **Multi‑language** – Russian and English interface.
- **Persistent storage** – SQLite keeps user language preferences and chat bindings.

## 🛠 Available Commands & Buttons

- `/start` – main menu with inline buttons.
- `/help` – list of features.

### Inline buttons
- **📬 Receive here** – bind the current chat as the target for incoming requests.
- **🔗 Bind chat** – specify another chat ID as the target.
- **🤖 Create support bot** – add a new child bot using its token.
- **ℹ️ Status** – show your active support bots and where messages are sent.

> **Support agent reply**: any message replied to a forwarded user request will be sent back to the user via the appropriate child bot.

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.11 or higher.
- [uv](https://docs.astral.sh/uv/) – recommended for fast dependency management.

Install `uv`:

**Windows (PowerShell)**
powershell
```powershell -c "irm https://astral.sh/uv/install.ps1 | iex"```
Linux / macOS

bash
```curl -LsSf https://astral.sh/uv/install.sh | sh```
Or via pip

bash
```pip install uv```
2. Clone the repository
bash
git clone https://github.com/RovPath/Support_Bridge.git
cd Support_Bridge
3. Configuration
Create a .env file in the root directory:

env
```
TG_TOKEN=your_main_bot_token_here
USE_PROXY=False
PROXY_URL=socks5://user:pass@host:port
```
TG_TOKEN – token of the main Support_Bridge bot.
USE_PROXY – set to True if you need a proxy (e.g., in restricted networks).
PROXY_URL – supports socks5://, http://, https:// protocols.

4. Install dependencies
bash
```uv pip install -r requirements.txt```
If you don't have requirements.txt, install manually:

bash
```uv pip install aiogram python-dotenv aiosqlite aiohttp-socks```
5. Launch the bot
bash
```uv run run.py```
Or using standard Python:

bash
```python run.py```
📁 Project Structure
Support_Bridge/
├── .env
├── run.py                 # Entry point
├── config.py              # Token, proxy, paths
├── database/
│   ├── manager.py         # Async SQLite (language + bindings)
├── app/
│   ├── handlers/          # All command and callback handlers
│   ├── middlewares/       # L10nMiddleware & BotManager
│   ├── states/            # FSM states (token, chat ID)
│   └── utils/             # Texts (RU/EN) and helpers
🧩 How It Works
Main bot listens for /start and inline buttons.

User creates a support bot – sends a token. The main bot spawns a BotInstance that starts polling user messages.

User binds a target chat – all incoming requests from child bots are forwarded there.

Support agent replies by replying to any forwarded message. The reply is sent back to the original user via the child bot.

🌐 Proxy Support
The main bot and every child bot can use the same proxy.

Set USE_PROXY=True and provide a valid PROXY_URL.

Works on Windows, Linux, macOS (requires aiohttp-socks).

❗ Notes
The main bot token must have no restrictions (can start child bots).

Child bots need only the message intent – no extra privileges required.

The bot does not store forwarded messages; only the mapping (chat_id, message_id) is kept temporarily in memory.