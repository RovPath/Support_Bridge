# 🤝 Support_Bridge Bot

A powerful asynchronous Telegram bot designed to create and manage **child support bots**. It streamlines help desk operations by forwarding all user requests from multiple bots into a single, centralized chat for efficient response management.

## 📌 Purpose

The bot simplifies multi-bot administration and support workflows by providing:

* **On-the-fly Bot Creation**: Register and launch new support bots instantly using Telegram bot tokens.
* **Centralized Communication**: Bind specific groups, channels, or private chats to receive all incoming user requests.
* **Full Media Support**: Forwards photos, videos, documents, voice messages, stickers, GIFs, locations, and polls.
* **Seamless Replies**: Support agents can reply to a forwarded message in the central chat to send a response back to the user via the child bot.
* **Persistence & Localization**: SQLite-driven storage for user preferences and bilingual support (EN/RU).

## 🛠 Available Commands & Buttons

* `/start` — Open the main menu with interactive inline buttons.
* `/help` — Display detailed feature lists and usage instructions.

### Inline Menu Options

* **📬 Receive here** — Automatically set the current chat as the target for all incoming requests.
* **🔗 Bind chat** — Manually specify a target Chat ID for message forwarding.
* **🤖 Create support bot** — Initialize a new child bot instance by providing its token.
* **ℹ️ Status** — View active child bots and verify current chat bindings.

---

## 🚀 Installation & Setup

### 1. Prerequisites

Ensure you have **Python 3.11** or higher. It is highly recommended to use [uv](https://docs.astral.sh/uv/) for faster dependency resolution.

### 2. Install uv (Package Manager)

**Windows (PowerShell):**

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

```

**Linux / macOS:**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

```

### 3. Configuration

Clone the repository and create a `.env` file in the root directory:

```env
TG_TOKEN=your_main_bot_token_here
USE_PROXY=False
PROXY_URL=socks5://user:pass@host:port

```

### 4. Install Dependencies

Sync your environment using `uv`:

```bash
uv pip install -r requirements.txt
# Or manual install
uv pip install aiogram python-dotenv aiosqlite aiohttp-socks

```

### 5. Launch the Bot

**Using uv (Recommended):**

```bash
uv run run.py

```

**Standard Python:**

```bash
python run.py

```

---

## 📁 Project Structure

* `run.py` — Main entry point and execution logic.
* `config.py` — Environment configuration and path management.
* `database/` — Async SQLite manager for language settings and chat bindings.
* `app/handlers/` — Command and callback query logic.
* `app/middlewares/` — Localization (L10n) and Bot Instance management.
* `app/states/` — FSM (Finite State Machine) for handling token and ID inputs.
* `app/utils/` — Helper functions and bilingual text strings.

## 🌐 Proxy Support

The system provides global proxy support for both the main controller and all child instances. Configure `USE_PROXY=True` in your `.env` to enable `socks5`, `http`, or `https` tunneling, ensuring stability in restricted network environments.
