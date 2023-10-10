## Quiz Game API

https://docs.google.com/document/d/1MPStlOFfvF9YWEx-0I1EwvWE9paKkhvFWyq7tRvcdc0/edit

Этот проект представляет собой API для викторины, который предоставляет возможность генерации случайных вопросов, получения случайного вопроса и отправки ответа на вопрос. 

## Стэк

- Python
- FastAPI
- PostgreSQL 
- SQLAlchemy
- Docker

## Дополнительный функционал 
1. Тестирование
   ```bash
   pytest 
2. Написаны дополнительные функции для игры в квиз
   - `/get-random-question/`: Запрос для получения случайного вопроса
   - `/submit-answer/`: Отправка ответа на вопрос
3. Документация Swagger: `/docs/`

## Инструкция по запуску 
1. Склонируйте репозиторий с вашим приложением на свой локальный компьютер
   ```bash
   git clone https://github.com/DeLaVerrierr/TS-for-Bewise.ai.git
   cd app
2. Отредактируйте файл docker-compose.yml в корне вашего проекта, чтобы настроить подключение к PostgreSQL базе данных в сервисе backend:
   - DATABASE_HOST
   - DATABASE_PORT (по умолчанию 5432)
   - DATABASE_NAME
   - DATABASE_USER
   - DATABASE_PASSWORD
3. Запустите Docker Compose 
   ```bash
   docker-compose up --build

## Контакты 
- Электронная почта: amir.66garaev@gmail.com
- Телеграм: @de_la_verrier


