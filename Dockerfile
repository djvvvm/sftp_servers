# Dockerfile для Flask API
FROM python:3.9-slim

WORKDIR /app

# Копіюємо Flask застосунок
COPY . .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Відкриваємо порт для Flask API
EXPOSE 5000

# Запускаємо Flask
CMD ["flask", "run", "--host=0.0.0.0"]
