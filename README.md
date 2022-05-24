# read_google_sheets
Инструкция:
1. Клонируйте репозиторий https://github.com/devbrest/read_google_sheets.git
2. Установите pip install google-api-python-client -t ./
3. Установите poetry python get-poetry.py --preview
4. Установите зависимости проекта poetry install --no-dev
5. Создайте ini файл с параметрами подключения к posgresql сохраните его под названием: database.ini
и следующим содержимым:
[postgresql]
host=localhost
database=db_customers_devbrest # название оставить так как есть
user=postgres
password=password

6. Для создания базы данных в терминале выполните команду poetry run create_database
7. Для однократного запуска скрипта выполните - poetry run exchange 
8. Чтобы запустить скрипт с обновлением каждую минуту выполните poetry run running_script

Путь к книге https://docs.google.com/spreadsheets/d/18GKiLKq4zcd1UlQQnrb_C686uJ6EY9YseLAizR36YAo
