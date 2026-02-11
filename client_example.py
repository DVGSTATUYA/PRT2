import requests
import json
import time

BASE_URL = "http://localhost:8000"

def print_response(response, title=""):
    """Красивый вывод ответа"""
    print(f"\n{'='*50}")
    if title:
        print(f"{title}")
        print(f"{'='*50}")
    print(f"Статус: {response.status_code}")
    print("Ответ:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))

def test_api():
    """Тестирование всех endpoints API"""
    
    print("Тестирование API информационной системы")
    print(f"Базовый URL: {BASE_URL}")
    
    # 1. Получение корневого endpoint
    print("\n1. Получение информации о API:")
    response = requests.get(f"{BASE_URL}/")
    print_response(response, "Корневой endpoint")
    
    # 2. Проверка здоровья
    print("\n2. Проверка здоровья сервиса:")
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health check")
    
    # 3. Создание новой записи
    print("\n3. Создание новой записи:")
    new_item = {
        "name": "Тестовый элемент",
        "description": "Это тестовый элемент для демонстрации",
        "price": 100.50,
        "quantity": 10
    }
    response = requests.post(f"{BASE_URL}/items", json=new_item)
    print_response(response, "Создание записи")
    
    if response.status_code == 201:
        created_item = response.json()
        item_id = created_item["id"]
        
        # 4. Получение всех записей
        print("\n4. Получение всех записей:")
        response = requests.get(f"{BASE_URL}/items")
        print_response(response, "Все записи")
        
        # 5. Получение записи по ID
        print("\n5. Получение записи по ID:")
        response = requests.get(f"{BASE_URL}/items/{item_id}")
        print_response(response, f"Запись с ID {item_id}")
        
        # 6. Обновление записи
        print("\n6. Обновление записи:")
        update_data = {
            "name": "Обновленный элемент",
            "price": 150.75,
            "quantity": 5
        }
        response = requests.put(f"{BASE_URL}/items/{item_id}", json=update_data)
        print_response(response, f"Обновление записи {item_id}")
        
        # 7. Тестирование некорректных запросов
        print("\n7. Тестирование обработки ошибок:")
        
        # Несуществующий ID
        response = requests.get(f"{BASE_URL}/items/9999")
        print_response(response, "Запрос несуществующей записи")
        
        # Некорректные данные при создании
        invalid_item = {
            "name": "",  # Пустое имя
            "price": -10  # Отрицательная цена
        }
        response = requests.post(f"{BASE_URL}/items", json=invalid_item)
        print_response(response, "Создание с некорректными данными")
        
        # Несуществующий endpoint
        response = requests.get(f"{BASE_URL}/nonexistent")
        print_response(response, "Запрос несуществующего endpoint")
        
        # 8. Удаление записи
        print("\n8. Удаление записи:")
        response = requests.delete(f"{BASE_URL}/items/{item_id}")
        print_response(response, f"Удаление записи {item_id}")
        
        # 9. Проверка удаления
        print("\n9. Проверка удаленной записи:")
        response = requests.get(f"{BASE_URL}/items/{item_id}")
        print_response(response, f"Попытка получить удаленную запись {item_id}")
    
    print("\n" + "="*50)
    print("Тестирование завершено!")
    print("="*50)

if __name__ == "__main__":
    # Даем серверу время на запуск
    print("Ожидание запуска сервера...")
    time.sleep(2)
    
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("\nОшибка подключения к серверу!")
        print("Убедитесь, что сервер запущен на http://localhost:8000")
        print("Запустите сервер командой: uvicorn main:app --reload")