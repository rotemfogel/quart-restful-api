import os

from quart.cli import load_dotenv

load_dotenv()
APP_ENV = os.getenv("APP_ENV") or "DEV"
DB_URL = f"postgresql://postgres:postgres@127.0.0.1:5432/postgres"
HTTP_PORT = int(os.getenv("APP_PORT") or 8000)
