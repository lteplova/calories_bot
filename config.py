import os
from dotenv import load_dotenv
import logging
logging.basicConfig(level=logging.DEBUG)

aiohttp_logger = logging.getLogger("aiohttp")
aiohttp_logger.setLevel(logging.DEBUG)

load_dotenv()
# токен для бота
TOKEN = os.getenv("BOT_TOKEN")
# токет для погодного серфиса
API_TEMP = os.getenv("OPEN_WEATHER_MAP")
# токен для NUTRITIONIX
API_ID_NUTRITIONIX = os.getenv("API_ID_NUTRITIONIX")
API_KEY_NUTRITIONIX = os.getenv("API_KEY_NUTRITIONIX")

if not TOKEN:
    raise ValueError("BOT_TOKEN не установлен!")

if not API_TEMP:
    raise ValueError("API weather не установлен!")

if not API_ID_NUTRITIONIX:
    raise ValueError("API ID NUTRITIONIX не установлен!")

if not API_KEY_NUTRITIONIX:
    raise ValueError("API KEY NUTRITIONIX не установлен!")


