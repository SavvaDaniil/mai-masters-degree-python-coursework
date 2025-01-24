FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

RUN apt-get update && apt-get install && pip install --upgrade pip

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файлы
COPY . .

#RUN python manage.py migrate

# Открываем порт
EXPOSE 5000

#CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]
CMD ["sh", "-c", "./docker-entrypoint.sh"]