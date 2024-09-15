# Dockerfile для Vue.js
FROM node:16

WORKDIR /app

# Копіюємо package.json
COPY package*.json ./

# Встановлюємо залежності
RUN npm install

# Копіюємо решту файлів застосунку
COPY . .

# Збираємо Vue.js проєкт
RUN npm run build

# Відкриваємо порт для Vue.js
EXPOSE 8080

# Запускаємо сервер
CMD ["npm", "run", "serve"]
