from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from database import init_db, get_all_items, get_item_by_id, create_item, update_item, delete_item
from models import Item, ItemCreate, ItemUpdate
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API интеграции модулей",
    description="API для обмена данными между компонентами информационной системы",
    version="1.0.0"
)

# Инициализация базы данных при запуске
@app.on_event("startup")
def startup_event():
    init_db()
    logger.info("База данных инициализирована")

# Корневой endpoint
@app.get("/")
def read_root():
    return {
        "message": "API информационной системы",
        "version": "1.0.0",
        "endpoints": {
            "GET /items": "Получить все записи",
            "GET /items/{id}": "Получить запись по ID",
            "POST /items": "Создать новую запись",
            "PUT /items/{id}": "Обновить запись",
            "DELETE /items/{id}": "Удалить запись"
        }
    }

# Получение всех записей
@app.get("/items", response_model=list[Item], status_code=status.HTTP_200_OK)
def read_items():
    """Получение всех записей из базы данных"""
    try:
        items = get_all_items()
        return items
    except Exception as e:
        logger.error(f"Ошибка при получении записей: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

# Получение записи по ID
@app.get("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def read_item(item_id: int):
    """Получение записи по идентификатору"""
    try:
        item = get_item_by_id(item_id)
        if item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Запись с ID {item_id} не найдена"
            )
        return item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении записи {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка сервера"
        )

# Создание новой записи
@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_new_item(item: ItemCreate):
    """Создание новой записи в базе данных"""
    try:
        new_item = create_item(item)
        logger.info(f"Создана новая запись с ID: {new_item['id']}")
        return new_item
    except Exception as e:
        logger.error(f"Ошибка при создании записи: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при создании записи"
        )

# Обновление записи
@app.put("/items/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def update_existing_item(item_id: int, item_update: ItemUpdate):
    """Обновление существующей записи"""
    try:
        # Проверяем существование записи
        existing_item = get_item_by_id(item_id)
        if existing_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Запись с ID {item_id} не найдена"
            )
        
        updated_item = update_item(item_id, item_update)
        logger.info(f"Обновлена запись с ID: {item_id}")
        return updated_item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при обновлении записи {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении записи"
        )

# Удаление записи
@app.delete("/items/{item_id}", status_code=status.HTTP_200_OK)
def delete_existing_item(item_id: int):
    """Удаление записи из базы данных"""
    try:
        # Проверяем существование записи
        existing_item = get_item_by_id(item_id)
        if existing_item is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Запись с ID {item_id} не найдена"
            )
        
        delete_item(item_id)
        logger.info(f"Удалена запись с ID: {item_id}")
        return {"message": f"Запись с ID {item_id} успешно удалена"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при удалении записи {item_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении записи"
        )

# Endpoint для проверки здоровья
@app.get("/health")
def health_check():
    """Проверка состояния API"""
    return {
        "status": "healthy",
        "service": "integration-api",
        "timestamp": "2024-01-01T00:00:00Z"  # В реальном приложении используйте datetime.now()
    }

# Обработка несуществующих маршрутов
@app.exception_handler(404)
def not_found_exception_handler(request, exc):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": "Маршрут не найден"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)