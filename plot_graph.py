
import matplotlib.pyplot as plt
import seaborn as sns
# функция для построения графика потребления воды на основе логирования воды
def plot_water(user_data):
    sns.set_theme(palette='pastel', font_scale=0.8)
    plt.figure(figsize=(8, 6))
    plt.title('Прогресс потребления воды')

    dates = [entry['timestamp'].split()[1] for entry in user_data['water_log_history']]
    amounts = [entry['amount'] for entry in user_data['water_log_history']]
    sns.lineplot(x=dates, y=amounts, marker='o', color='#1f77b4', label='Потребление воды')

    plt.axhline(y=user_data['water_goal'], color='#d62728', linestyle='--',  label='Цель')

    plt.xlabel('Время')
    plt.ylabel('Количество воды (мл)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = f'water.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

    return filename

# функция для построения динамики набора и сжигания калорий в течении дня
def plot_calories(user_data):
    sns.set_theme(palette='pastel', font_scale=0.8)
    plt.figure(figsize=(8, 6))
    plt.title('Прогресс расхода и потребления калорий')

    dates = [entry['timestamp'].split()[1] for entry in user_data['calorie_log_history']]
    amounts = [entry['amount'] for entry in user_data['calorie_log_history']]
    sns.lineplot(x=dates, y=amounts, marker='o', color='#1f77b4', label='Потребление и расход калорий')

    plt.axhline(y=user_data['water_goal'], color='#d62728', linestyle='--',  label='Цель')

    plt.xlabel('Время')
    plt.ylabel('Количество калорий ккал')
    plt.xticks(rotation=45)
    plt.tight_layout()
    filename = f'calories.png'
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    plt.close()

    return filename
