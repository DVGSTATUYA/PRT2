import pytest
import requests
import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    """Тест корневого endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert "endpoints" in data

def test_health_check():
    """Тест проверки здоровья"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "integration-api"

def test_create_item():
    """Тест создания элемента"""
    item_data = {
        "name": "Тестовый элемент",
        "description": "Описание тестового элемента",
        "price": 99.99,
        "quantity": 5
    }
    
    response = client.post("/items", json=item_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["name"] == item_data["name"]
    assert data["description"] == item_data["description"]
    assert data["price"] == item_data["price"]
    assert data["quantity"] == item_data["quantity"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data
    
    # Удаляем созданный элемент
    item_id = data["id"]
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 200

def test_get_all_items():
    """Тест получения всех элементов"""
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_item_by_id():
    """Тест получения элемента по ID"""
    # Сначала создаем элемент
    item_data = {
        "name": "Элемент для получения",
        "price": 50.0
    }
    create_response = client.post("/items", json=item_data)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # Получаем элемент по ID
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == item_id
    assert data["name"] == item_data["name"]
    
    # Очистка
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 200

def test_update_item():
    """Тест обновления элемента"""
    # Создаем элемент
    item_data = {
        "name": "Старое имя",
        "price": 100.0
    }
    create_response = client.post("/items", json=item_data)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # Обновляем элемент
    update_data = {
        "name": "Новое имя",
        "price": 150.0,
        "quantity": 10
    }
    response = client.put(f"/items/{item_id}", json=update_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["price"] == update_data["price"]
    assert data["quantity"] == update_data["quantity"]
    
    # Очистка
    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 200

def test_delete_item():
    """Тест удаления элемента"""
    # Создаем элемент
    item_data = {"name": "Элемент для удаления"}
    create_response = client.post("/items", json=item_data)
    assert create_response.status_code == 201
    item_id = create_response.json()["id"]
    
    # Удаляем элемент
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Запись с ID {item_id} успешно удалена"
    
    # Проверяем, что элемент удален
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404

def test_invalid_data_handling():
    """Тест обработки некорректных данных"""
    # Пустое имя (теперь ожидаем 422 вместо 400)
    invalid_item = {"name": ""}
    response = client.post("/items", json=invalid_item)
    assert response.status_code == 422  # Изменено с 400 на 422
    
    # Отрицательная цена
    invalid_item = {"name": "Тест", "price": -10}
    response = client.post("/items", json=invalid_item)
    assert response.status_code == 422
    
    # Несуществующий ID
    response = client.get("/items/999999")
    assert response.status_code == 404

def test_nonexistent_endpoint():
    """Тест запроса несуществующего endpoint"""
    response = client.get("/nonexistent")
    assert response.status_code == 404

def test_empty_items_list():
    """Тест получения пустого списка элементов"""
    # Получаем все элементы
    response = client.get("/items")
    assert response.status_code == 200
    items = response.json()
    
    # Удаляем все существующие элементы
    for item in items:
        delete_response = client.delete(f"/items/{item['id']}")
        assert delete_response.status_code == 200
    
    # Проверяем, что список пуст
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

if __name__ == "__main__":
    # Запуск тестов
    import sys
    import os
    
    # Добавляем текущую директорию в путь для импортов
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Запускаем pytest
    retcode = pytest.main([__file__, "-v", "--tb=short", "-W", "ignore::pytest.PytestReturnNotNoneWarning"])
    sys.exit(retcode)