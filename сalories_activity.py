from config import API_ID_NUTRITIONIX, API_KEY_NUTRITIONIX
import aiohttp
from deep_translator import GoogleTranslator
import certifi
import ssl
# Класс для работы с API сайта nutritionix.com, есть два метода - для получение калорийности продуктов и для расчета сожженых калорий в зависимости от тренировки
class NutritionixAPI:
    def __init__(self, app_id=API_ID_NUTRITIONIX, app_key=API_KEY_NUTRITIONIX):
        self.base_url = "https://trackapi.nutritionix.com/v2"
        self.headers = {
            "x-app-id": app_id,
            "x-app-key": app_key,
            "Content-Type": "application/json"
        }

    async def search_food(self, query):
        try:
            english_query = GoogleTranslator(source='ru', target='en').translate(query)
        except Exception as e:
            print(f"Ошибка перевода: {e}")
            english_query = query

        link = f"{self.base_url}/natural/nutrients"
        payload = {"query": english_query}

        ssl_context = ssl.create_default_context(cafile=certifi.where())

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(link, headers=self.headers, json=payload, ssl=ssl_context) as response:
                    response.raise_for_status()
                    data = await response.json()
                    return {
                        "calories": data['foods'][0]['nf_calories'],
                        "original_query": query
                    }
        except aiohttp.ClientError as e:
            print(f"Ошибка запроса к API NUTRITIONIX: {e}")
            return None

    async def calculate_calories_burned(self, activity, duration_min, weight_kg):
        try:
            english_activity = GoogleTranslator(source='ru', target='en').translate(activity)
        except Exception as e:
            print(f"Ошибка перевода: {e}")
            english_activity = activity

        link = f"{self.base_url}/natural/exercise"
        payload = {
            "query": f"{english_activity} for {duration_min} minutes",
            "weight_kg": weight_kg
        }
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(link, headers=self.headers, json=payload, ssl=ssl_context) as response:
                    response.raise_for_status()
                    data = await response.json()
                    if data.get('exercises'):
                        exercise = data['exercises'][0]

                        return {
                            "activity": exercise.get('name', activity),
                            "duration_min": duration_min,
                            "calories_burned": round(exercise.get('nf_calories', 0), 1),
                            "description": f"{activity}"
                        }
        except aiohttp.ClientError as e:
            print(f"Ошибка запроса к API NUTRITIONIX: {e}")
            return None
