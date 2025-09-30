# Используем официальный Python-образ
FROM python:3.13-slim

# Установим системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем директорию приложения
WORKDIR /app

# Установка Poetry
RUN pip install poetry

# Копируем файл с зависимостями
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости в системный Python
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем весь проект
COPY . .

# Открываем порт для взаимодействия с проектом
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]