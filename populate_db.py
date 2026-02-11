import requests
import time

BASE_URL = "http://localhost:8000"

# Примеры данных
test_items = [
    {
        "name": "Ноутбук",
        "description": "Игровой ноутбук",
        "price": 1500.00,
        "quantity": 5
    },
    {
        "name": "Мышь",
        "description": "Игровая мышь",
        "price": 50.00,
        "quantity": 20
    },
    {
        "name": "Клавиатура",
        "description": "Механическая клавиатура",
        "price": 100.00,
        "quantity": 15
    },
    {
        "name": "Монитор",
        "description": "27-дюймовый 4K монитор",
        "price": 400.00,
        "quantity": 8
    }
]

def populate_database():
    """Заполнение базы данных тестовыми данными"""
    print("Заполнение базы данных тестовыми данными...")
    
    created_ids = []
    
    for item in test_items:
        response = requests.post(f"{BASE_URL}/items", json=item)
        if response.status_code == 201:
            created_item = response.json()
            created_ids.append(created_item["id"])
            print(f"✓ Создан элемент: {item['name']} (ID: {created_item['id']})")
        else:
            print(f"✗ Ошибка при создании: {item['name']}")
            print(f"  Статус: {response.status_code}")
            print(f"  Ответ: {response.text}")
        time.sleep(0.1)  # Небольшая задержка
    
    print(f"\nВсего создано элементов: {len(created_ids)}")
    
    # Показать все элементы
    print("\nТекущее содержимое базы:")
    response = requests.get(f"{BASE_URL}/items")
    if response.status_code == 200:
        items = response.json()
        for item in items:
            print(f"  - {item['id']}: {item['name']} - {item['price']}$ (кол-во: {item['quantity']})")
    
    # Сохранить IDs в файл для последующего удаления
    with open("created_items.txt", "w") as f:
        for item_id in created_ids:
            f.write(f"{item_id}\n")
    
    return created_ids

def clear_database(ids_to_delete=None):
    """Очистка базы данных"""
    print("\nОчистка базы данных...")
    
    if ids_to_delete is None:
        # Получить все элементы
        response = requests.get(f"{BASE_URL}/items")
        if response.status_code == 200:
            items = response.json()
            ids_to_delete = [item["id"] for item in items]
    
    deleted_count = 0
    for item_id in ids_to_delete:
        response = requests.delete(f"{BASE_URL}/items/{item_id}")
        if response.status_code == 200:
            deleted_count += 1
            print(f"✓ Удален элемент ID: {item_id}")
    
    print(f"Всего удалено элементов: {deleted_count}")

if __name__ == "__main__":
    # Проверяем, запущен ли сервер
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
        
        print("Выберите действие:")
        print("1. Заполнить базу данных тестовыми данными")
        print("2. Очистить базу данных")
        print("3. Показать текущие данные")
        
        choice = input("\nВведите номер (1-3): ").strip()
        
        if choice == "1":
            populate_database()
        elif choice == "2":
            # Загружаем сохраненные IDs или получаем текущие
            try:
                with open("created_items.txt", "r") as f:
                    ids = [int(line.strip()) for line in f if line.strip()]
                clear_database(ids)
            except FileNotFoundError:
                clear_database()
        elif choice == "3":
            response = requests.get(f"{BASE_URL}/items")
            if response.status_code == 200:
                items = response.json()
                print(f"\nВсего элементов: {len(items)}")
                for item in items:
                    print(f"\nID: {item['id']}")
                    print(f"  Название: {item['name']}")
                    print(f"  Описание: {item['description']}")
                    print(f"  Цена: {item['price']}$")
                    print(f"  Количество: {item['quantity']}")
                    print(f"  Создан: {item['created_at']}")
                    print(f"  Обновлен: {item['updated_at']}")
            else:
                print("Ошибка при получении данных")
        else:
            print("Неверный выбор")
            
    except requests.exceptions.ConnectionError:
        print("Ошибка: Сервер не запущен!")
        print("Запустите сервер командой: uvicorn main:app --reload")