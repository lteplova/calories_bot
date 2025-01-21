# Telegram-бот для расчёта нормы воды, калорий и трекинга активности

### Имя бота в telegram @HealthAssistantStudyBot

### Установка сервиса 

сервис состоит из файлов:  
`bot.py` - файл для запуска приложения  
`config.py` - конфигурационный файл, содержит необходимые токены для подключения к API  
`handlers.py` - содержит все функции, которые реализует бот  
`norms.py` - вспомогательные функции для расчета норм  
`plot_graph.py` - вспомогательные функции для построения графиков  
`сalories_activity.py` - вспомогательные функции для расчета каллорий и подключению к API  
`states.py`  - вспомогательный файл с состояниями  

### Функционал сервиса

Доступные команды:  
`/start` - Начало работы  
<img width="720" alt="image" src="https://github.com/user-attachments/assets/92fc3171-ae80-4873-abfa-0c2c8bdfecf8" />

`/set_profile` - Настройка вашего профиля  

<img width="666" alt="image" src="https://github.com/user-attachments/assets/b9142e43-d263-4b14-bc97-b08a8d6de8a4" />


`/log_water` - Логирование воды  

<img width="653" alt="image" src="https://github.com/user-attachments/assets/d6fb7c9e-1bf4-4e7b-a675-bac582db5d0f" />

`/log_food` - Добавить прием еды 

<img width="648" alt="image" src="https://github.com/user-attachments/assets/7affbf73-bc79-4e42-9c5d-a554be3cf663" />

`/log_workout` - Логирование тренировок  

<img width="647" alt="image" src="https://github.com/user-attachments/assets/a302af3c-39fa-49df-94b7-0a79dbc06769" />

`/check_progress` - Прогресс по воде и калориям  
<img width="649" alt="image" src="https://github.com/user-attachments/assets/f315b24b-2848-4343-b1b9-fe03ef6a41b3" />

####Дополнительно:  
`/norms` - Нормы воды и калорий  
`/plot_water_progress` - График потребления воды  
`/plot_calories_progress` - График изменения калорий  
`/show_profile` - Показать профиль  


### Результат деплоя на render.com

![image](https://github.com/user-attachments/assets/34ff31e4-2c7b-4231-ab84-3608cbbf2bfa)

Логи бота

![image](https://github.com/user-attachments/assets/8936812d-2679-403c-8b37-fd79ea56bb5a)

