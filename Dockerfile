# Используем официальный python образ
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей (создадим далее)
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код приложения
COPY main.py .

# Запускаем приложение с uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]