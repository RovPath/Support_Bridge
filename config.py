import os
from dotenv import load_dotenv
from aiohttp_socks import ProxyConnector
from aiohttp import ClientSession, TCPConnector

load_dotenv()

BOT_TOKEN = os.getenv("TG_TOKEN")
if not BOT_TOKEN:
    raise ValueError("TG_TOKEN не задан в .env")

USE_PROXY = os.getenv("USE_PROXY", "False").lower() == "true"
PROXY_URL = os.getenv("PROXY_URL")

def get_proxy_connector():
    if USE_PROXY and PROXY_URL:
        try:
            return ProxyConnector.from_url(PROXY_URL)
        except Exception as e:
            print(f"Ошибка создания прокси-коннектора: {e}")
            return None
    return None

def get_client_session():
    connector = get_proxy_connector()
    if connector:
        return ClientSession(connector=connector)
    return ClientSession(connector=TCPConnector())

DB_PATH = "database/users.db"
os.makedirs("database", exist_ok=True)