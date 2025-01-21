import aiohttp
from config import API_TEMP
# функция для получения температуры по названию города
async def get_current_temperature(city, api_key=API_TEMP):
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                response.raise_for_status()
                data = await response.json()
                temperature = data["main"]["temp"]
                return temperature
    except aiohttp.ClientError as e:
        print(f"Ошибка запроса к API: {e}")
        return None

# функция расчета нормы воды на основе температуры воздуха, веса и активности
async def norm_water(weight, minutes, city):
    # Формула - Базовая норма=Вес×30мл/кг   +500мл за каждые 30 минут активности.  +500−1000мл за жаркую погоду (> 25°C).
    temperature = await get_current_temperature(city)
    norm = float(weight) * 30
    if int(minutes) > 0:
        norm = norm + (float(minutes) // 30) * 500
    if isinstance(temperature, float):
        temperature = float(temperature)
        if temperature > 25:
            norm = norm + 500
    else:
        print("Ошибка температуры")
        return norm
    return norm

# функция для расчета ккал в день на основе формулы ВОЗ, учитывает пол, активность, возраст
def norm_calories(weight, gender, age, minutes):
    '''
    Формула Всемирной организации здравоохранения (ВОЗ)

    Всемирная организация здравоохранения дает рекомендации, как рассчитать калорийность суточного рациона:

        Для женщин от 18 до 30 лет (0,062 х вес в кг + 2,036) х 240 х КФА;
        Для женщин от 31 до 60 лет (0,034 х вес в кг + 3,538) х 240 х КФА;
        Для женщин старше 60 лет (0,038 х вес в кг + 2,755) × 240 х КФА;
        Для мужчин от 18 до 30 лет (0,063 х вес тела в кг + 2,896) х 240 х КФА;
        Для мужчин от 31 до 60 лет (0,048 х вес тела в кг + 3,653) х 240 х КФА;
        Для мужчин старше 60 лет (0,049 х вес тела в кг + 2,459) х 240 х КФА.

    Где КФА – коэффициент физической активности: 1 - низкая, 1,3 – средняя, 1,5 – высокая.
        1,2 – минимальный (сидячая работа, отсутствие физических нагрузок);
        1,375 – низкий (тренировки не менее 20 мин 1-3 раза в неделю);
        1,55 – умеренный (тренировки 30-60 мин 3-4 раза в неделю);
        1,7 – высокий (тренировки 30-60 мин 5-7 раза в неделю; тяжелая физическая работа);
        1,9 – экстремальный (несколько интенсивных тренировок в день 6-7 раз в неделю; очень трудоемкая работа).
    '''
    if float(minutes) // 30 < 1:
        kfa = 1.2
    elif float(minutes) // 30 == 1:
        kfa = 1.375
    elif float(minutes) // 30 == 2:
        kfa = 1.55
    elif float(minutes) // 30 == 3:
        kfa = 1.7
    elif float(minutes) // 30 > 3:
        kfa = 1.9


    if gender == "женщина":
        if age < 31:
            calories = (0.062 * weight + 2.036) * 240 * kfa
            return calories
        elif 30 < age < 61:
            calories = (0.034 * weight + 3.538) * 240 * kfa
            return calories
        elif age > 60:
            calories = (0.038 * weight + 2.755) * 240 * kfa
            return calories
    elif gender == "мужчина":
        if age < 31:
            calories = (0.063 * weight + 2.896) * 240 * kfa
            return calories
        elif 30 < age < 61:
            calories = (0.048 * weight + 3.653) * 240 * kfa
            return calories
        elif age > 60:
            calories = (0.049 * weight + 2.459) * 240 * kfa
            return calories
