# PRT2

# Интеграция программных модулей с использованием API

REST API для управления данными, разработанное на FastAPI + SQLite.

---

## Быстрый запуск

### 1. Установка зависимостей

```
pip install fastapi uvicorn httpx pytest requests
```

### 2. Запуск сервера

```
uvicorn main:app --reload
```
Сервер запустится по адресу: http://localhost:8000

### 3. Тестирование
1.
```
python client_example.py
```
2.
```
python test_api.py    
```
