from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command
from states import Form
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from norms import norm_water, norm_calories
import re
from сalories_activity import NutritionixAPI
from datetime import datetime
from plot_graph import plot_water, plot_calories

router = Router()
users = {}


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Добро пожаловать!\n"
                         "Я помогаю рассчитать дневные нормы воды и калорий и отслеживать тренировки и питание!\n"
                         "Начните с настройки вашего профиля - /set_profile\n"
                         "Все команды: /help")


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(
        "Доступные команды:\n"
        "/start - Начало работы\n"
        "/set_profile - Настройка вашего профиля\n"
        "/show_profile - Показать профиль\n"
        "/log_water - Логирование воды\n"
        "/log_food - Добавить прием еды\n"
        "/log_workout - Логирование тренировок\n"
        "/check_progress - Прогресс по воде и калориям\n"
        "/norms - Нормы воды и калорий\n"
        "/plot_water_progress - График потребления воды\n"
        "/plot_calories_progress - График изменения калорий"

    )


@router.message(Command("set_profile"))
async def start_set_profile(message: Message, state: FSMContext):
    await message.reply("⚖️Введите ваш вес (в кг)")
    await state.set_state(Form.weight)


@router.message(Form.weight)
async def proc_profile_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text)
        if 20 <= weight <= 200:
            await state.update_data(weight=weight)
            await message.reply("📏Введите ваш рост (в см)")
            await state.set_state(Form.height)
        else:
            await message.reply(
                "Введите корректный вес от 20 до 200 кг. "
            )
    except ValueError:
        await message.reply(
            "Введите число от 20 до 200"
        )


@router.message(Form.height)
async def proc_profile_height(message: Message, state: FSMContext):
    try:
        height = float(message.text)
        if 50 <= height <= 220:
            await state.update_data(height=height)
            await message.reply("👕Введите ваш пол - м (мужчина) или ж (женщина)")
            await state.set_state(Form.gender)
        else:
            await message.reply(
                "Введите корректный рост от 50 до 220 см "
            )
    except ValueError:
        await message.reply(
            "Введите число от 50 до 220"
        )


@router.message(Form.gender)
async def proc_profile_age(message: Message, state: FSMContext):
    try:
        gender = str(message.text)
        if gender == "м":
            genders = "мужчина"
            await state.update_data(gender=genders)
            await state.set_state(Form.age)
            await message.reply("👶Введите ваш возраст")

        elif gender == "ж":
            genders = "женщина"
            await state.update_data(gender=genders)
            await state.set_state(Form.age)
            await message.reply("👶Введите ваш возраст")
        else:
            raise ValueError("Некорректный ввод пола")

    except ValueError:
        await message.reply(
            "Введите корректно пол (м/ж)"
        )


@router.message(Form.age)
async def proc_profile_minutes(message: Message, state: FSMContext):
    try:
        age = float(message.text)
        if 18 <= age <= 150:
            await state.update_data(age=age)
            await message.reply("🕘Сколько минут активности у вас в день?")
            await state.set_state(Form.minutes)
        else:
            await message.reply(
                "Введите возраст числом от 18 до 150"
            )
    except ValueError:
        await message.reply(
            "Возраст введен некорректно, укажите число от 18 до 150"
        )


@router.message(Form.minutes)
async def proc_profile_city(message: Message, state: FSMContext):
    try:
        minutes = float(message.text)
        if 0 <= minutes < 1440:
            await state.update_data(minutes=minutes)
            await message.reply("🌃 В каком городе вы находитесь?")
            await state.set_state(Form.city)
        else:
            await message.reply(
                "Введите корректно время тренировок"
            )
    except ValueError:
        await message.reply(
            "Время введено неправильно, укажите время тренировок в минутах"
        )


@router.message(Form.city)
async def profile(message: Message, state: FSMContext):
    try:
        city = str(message.text)
        pattern = '[а-яА-Яa-zA-Z]+$'
        a = re.findall(pattern, city)
        if len(a) != 0 and 2 <= len(city) <= 170:
            data = await state.get_data()
            user_id = message.from_user.id
            weight = data.get("weight")
            height = data.get("height")
            gender = data.get("gender")
            age = data.get("age")
            minutes = data.get("minutes")
            city = city
            water = await norm_water(weight, int(minutes), str(city))
            calories = norm_calories(float(weight), gender, int(age), int(minutes))

            await message.reply(f"✅ Ваш профиль создан:\n "
                                f"Вес: {weight} кг \n "
                                f"Рост: {height} см \n "
                                f"Возраст: {age} лет \n "
                                f"Пол: {gender}  \n "
                                f"Активность: {minutes} мин \n "
                                f"Город: {city} \n\n "
                                f"Норма воды в день: {water} мл \n "
                                f"Норма калорий в день: {calories:.2f} ккал \n ")
            await state.clear()

            users[user_id] = {
                "weight": weight,
                "height": height,
                "age": age,
                "gender": gender,
                "activity": minutes,
                "city": city,
                "water_goal": water,
                "calorie_goal": calories,
                "logged_water": 0,
                "logged_calories": 0,
                "burned_calories": 0,
                "workouts": [],
                "foods": []
            }
        else:
            await message.reply(
                "Неверный ввод города, название города нужно указать буквами, длина от 2 до 170"
            )

    except ValueError:
        await message.reply(
            "Неверный ввод города, название города нужно указать буквами, длина от 2 до 170"
        )


@router.message(Command("show_profile"))
async def water_progress(message: Message):
    if message.from_user.id not in users:
        await message.reply("❗️Сначала создайте профиль с помощью /set_profile")
        return

    user_data = users[message.from_user.id]
    await message.reply(f"💼 Ваш профиль: \n"
                        f"Вес: {user_data['weight']} кг \n"
                        f"Рост: {user_data['height']} см \n"
                        f"Возраст: {user_data['age']} лет \n"
                        f"Пол: {user_data['gender']} \n"
                        f"Активность: {user_data['activity']} мин \n"
                        f"Город: {user_data['city']} \n\n"
                        f"Сожжено калорий: {user_data['burned_calories']:.2f}\n"
                        f"Тренировки: {user_data['workouts']}\n"
                        f"Что было съедено: {user_data['foods']}\n"
                        f"Норма воды в день: {user_data['water_goal']:.2f} мл \n"
                        f"Норма калорий в день: {user_data['calorie_goal']:.2f} ккал \n")


@router.message(Command("log_water"))
async def log_water(message: Message, state: FSMContext):
    if message.from_user.id not in users:
        await message.reply("❗️Сначала создайте профиль с помощью /set_profile")
        return

    try:
        _, water_amount = message.text.split()
        water_amount = int(water_amount)
    except (ValueError, TypeError):
        await message.reply("Используйте формат: /log_water <количество>")
        return

    user_data = users[message.from_user.id]

    if 'water_log_history' not in user_data:
        user_data['water_log_history'] = []

    water_entry = {
        'amount': user_data['logged_water'] + water_amount,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    user_data['water_log_history'].append(water_entry)
    user_data['logged_water'] += water_amount
    remaining_water = max(0, user_data['water_goal'] - user_data['logged_water'])

    await message.reply(
        f"Вы выпили {water_amount:.2f} мл воды.\n"
        f"Цель по воде: {user_data['water_goal']:.2f} мл\n"
        f"Выпито: {user_data['logged_water']:.2f} мл\n"
        f"Осталось выпить: {remaining_water:.2f} мл"
    )
    await state.clear()

    if user_data['logged_water'] >= user_data['water_goal']:
        await message.reply("🎉 Поздравляем! Вы достигли дневной нормы воды!")


@router.message(Command("log_food"))
async def log_food(message: Message, state: FSMContext):
    if message.from_user.id not in users:
        await message.reply("❗️Сначала создайте профиль с помощью /set_profile")
        return

    try:
        _, food = message.text.split()
        nutritionix_api = NutritionixAPI()
        meal = await nutritionix_api.search_food(food)
        if meal:
            await state.update_data(
                food_name=meal["original_query"],
                calories_per_100g=meal["calories"]
            )

            await state.set_state(Form.food_weight)
            meal_f = meal["original_query"]
            meal_c = meal["calories"]

            await message.reply(
                f"Вaше блюдо: {meal_f}\n"
                f"Калории на 100 грамм: {meal_c:.2f}\n"
                f"Сколько грамм вы съели?"
            )

            user_data = users[message.from_user.id]
            user_data['foods'].append([meal_f, meal_c])

        else:
            await message.reply("Неизвестное блюдо")
    except (ValueError, TypeError):
        await message.reply("Используйте формат: /log_food <блюдо>")
        return


@router.message(Form.food_weight)
async def process_food_weight(message: Message, state: FSMContext):
    try:
        weight = float(message.text.replace(',', '.'))
        data = await state.get_data()
        calories_per_100g = data['calories_per_100g']
        calories_consumed = round((calories_per_100g * weight) / 100, 1)
        user_data = users[message.from_user.id]

        calories_entry = {
            'amount': user_data['logged_calories'] + calories_consumed,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if 'calorie_log_history' not in user_data:
            user_data['calorie_log_history'] = []
        user_data['calorie_log_history'].append(calories_entry)
        user_data['logged_calories'] += calories_consumed

        await message.reply(
            f"Записано: {calories_consumed:.2f} ккал.\n"
            f"Всего съедено за день: {user_data['logged_calories']:.2f} ккал"
        )
        if user_data['logged_calories'] > user_data['calorie_goal']:
            await message.reply(
                "⚠️ Вы превысили дневную норму калорий! "
                f"Осталось: {(user_data['calorie_goal'] - user_data['logged_calories']):.2f} ккал"
            )
        await state.clear()

    except ValueError:
        await message.reply(
            "Пожалуйста, введите корректный вес в граммах. "
            "Например: 150 или 75.5"
        )


@router.message(Command("log_workout"))
async def log_food(message: Message, state: FSMContext):
    if message.from_user.id not in users:
        await message.reply("❗️Сначала создайте профиль с помощью /set_profile")
        return

    try:
        user_data = users[message.from_user.id]
        _, activity, duration_min = message.text.split()
        nutritionix_api = NutritionixAPI()
        workout = await nutritionix_api.calculate_calories_burned(activity, duration_min, user_data["weight"])

        if workout:
            burned_calories = workout["calories_burned"]
            activity = workout["description"]
            time = workout["duration_min"]

            if 'calorie_log_history' not in user_data:
                user_data['calorie_log_history'] = []

            calories_entry = {
                'amount': user_data['logged_calories'] - burned_calories,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            user_data['calorie_log_history'].append(calories_entry)
            user_data['workouts'].append([activity, time])
            user_data['burned_calories'] += float(burned_calories)
            add_water = float(time) * 200 / 30
            user_data['water_goal'] += add_water

            await message.reply(
                f"{activity} {time} минут - {burned_calories:.2f} ккал\n"
                f"Дополнительно: выпейте {add_water:.2f} мл воды\n"
            )
            await state.clear()

        else:
            await message.reply("Неизвестная активность")

    except (ValueError, TypeError):
        await message.reply("Используйте формат: /log_workout  <тип тренировки> <время (мин)>")
        return


@router.message(Command("norms"))
async def log_food(message: Message, state: FSMContext):
    if message.from_user.id not in users:
        await message.reply("❗️Сначала создайте профиль с помощью /set_profile")
        return
    user_data = users[message.from_user.id]
    await message.reply(
        f"Вам нужно пить не менее {user_data['water_goal']:.2f} мл воды в день\n"
        f"Норма калорий в день: {user_data['calorie_goal']:.2f} ккал\n"
    )


@router.message(Command("check_progress"))
async def log_food(message: Message, state: FSMContext):
    if message.from_user.id not in users:
        await message.reply("❗️Сначала создайте профиль с помощью /set_profile")
        return

    user_data = users[message.from_user.id]
    await message.reply(
        f"📊Прогресс:\n\n"
        f"💦Вода:\n"
        f"Выпито: {user_data['logged_water']:.2f} мл из {user_data['water_goal']:.2f} мл \n\n"
        f"🔥Калории:\n"
        f"Потреблено: {user_data['logged_calories']:.2f} ккал из {user_data['calorie_goal']:.2f} ккал\n"
        f"Сожжено: {user_data['burned_calories']:.2f} ккал\n"
        f"Баланс: {(user_data['logged_calories'] - user_data['burned_calories']):.2f} ккал\n"

    )


@router.message(Command("plot_water_progress"))
async def water_progress(message: Message):
    if message.from_user.id not in users:
        await message.reply("❗️Сначала создайте профиль с помощью /set_profile")
        return

    user_data = users[message.from_user.id]
    if 'water_log_history' not in user_data or len(user_data['water_log_history']) < 2:
        await message.reply(
            "Недостаточно данных для построения графика. Добавьте еще записи о воде через /log_water <количество>")
        return

    try:
        plot_file = plot_water(user_data)

        await message.answer_photo(
            photo=FSInputFile(plot_file),
            caption=(
                f"📊 Прогресс потребления воды\n"
                f"Цель: {user_data['water_goal']:.2f} мл\n"
                f"Всего выпито: {user_data['logged_water']:.2f} мл"
            )
        )

    except Exception as e:
        await message.reply(f"Ошибка при создании графика: {str(e)}")


@router.message(Command("plot_calories_progress"))
async def water_progress(message: Message):
    if message.from_user.id not in users:
        await message.reply("❗️Сначала создайте профиль с помощью /set_profile")
        return

    user_data = users[message.from_user.id]
    if 'calorie_log_history' not in user_data or len(user_data['calorie_log_history']) < 2:
        await message.reply(
            "Недостаточно данных для построения графика. Добавьте еще записи о калориях через /log_food <блюдо>")
        return

    try:
        plot_file = plot_calories(user_data)

        await message.answer_photo(
            photo=FSInputFile(plot_file),
            caption=(
                f"🔥Калории:\n"
                f"Потреблено: {user_data['logged_calories']:.2f} ккал из {user_data['calorie_goal']:.2f} ккал\n"
                f"Сожжено: {user_data['burned_calories']:.2f} ккал\n"
                f"Баланс: {(user_data['logged_calories'] - user_data['burned_calories']):.2f} ккал\n"
            )
        )

    except Exception as e:
        await message.reply(f"Ошибка при создании графика: {str(e)}")
