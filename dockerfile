# Установка базового образа
FROM python:3.11

# Установка рабочей директории в контейнере
WORKDIR /

# Копирование зависимостей в контейнер
COPY ../requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода в контейнер
COPY .. .

ENV config=data/config.cfg
# Команда запуска приложения
CMD [ "python", "extract_and_send_xlsx.py" ]
