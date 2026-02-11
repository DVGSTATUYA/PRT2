import sqlite3
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
import logging

logger = logging.getLogger(__name__)

DATABASE_NAME = "integration.db"

@contextmanager
def get_db_connection():
    """Контекстный менеджер для подключения к базе данных"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Для доступа к колонкам по имени
    try:
        yield conn
    finally:
        conn.close()

def init_db():
    """Инициализация базы данных и создание таблиц"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Создание таблицы items
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL,
                quantity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Создание триггера для автоматического обновления updated_at
        cursor.execute('''
            CREATE TRIGGER IF NOT EXISTS update_items_timestamp
            AFTER UPDATE ON items
            FOR EACH ROW
            BEGIN
                UPDATE items SET updated_at = CURRENT_TIMESTAMP
                WHERE id = OLD.id;
            END
        ''')
        
        conn.commit()
        logger.info("Таблица items создана или уже существует")

def get_all_items() -> List[Dict[str, Any]]:
    """Получение всех записей из таблицы items"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items ORDER BY id")
        items = cursor.fetchall()
        return [dict(item) for item in items]

def get_item_by_id(item_id: int) -> Optional[Dict[str, Any]]:
    """Получение записи по ID"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM items WHERE id = ?", (item_id,))
        item = cursor.fetchone()
        return dict(item) if item else None

def create_item(item_data: dict) -> Dict[str, Any]:
    """Создание новой записи"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO items (name, description, price, quantity)
            VALUES (?, ?, ?, ?)
        ''', (
            item_data.name,
            item_data.description,
            item_data.price,
            item_data.quantity
        ))
        conn.commit()
        
        # Получаем созданную запись
        item_id = cursor.lastrowid
        return get_item_by_id(item_id)

def update_item(item_id: int, item_data: dict) -> Optional[Dict[str, Any]]:
    """Обновление существующей записи"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # Формируем SQL запрос динамически на основе переданных полей
        updates = []
        values = []
        
        if item_data.name is not None:
            updates.append("name = ?")
            values.append(item_data.name)
        
        if item_data.description is not None:
            updates.append("description = ?")
            values.append(item_data.description)
        
        if item_data.price is not None:
            updates.append("price = ?")
            values.append(item_data.price)
        
        if item_data.quantity is not None:
            updates.append("quantity = ?")
            values.append(item_data.quantity)
        
        if not updates:
            return get_item_by_id(item_id)
        
        values.append(item_id)
        sql = f"UPDATE items SET {', '.join(updates)} WHERE id = ?"
        
        cursor.execute(sql, values)
        conn.commit()
        
        return get_item_by_id(item_id)

def delete_item(item_id: int) -> bool:
    """Удаление записи"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        return cursor.rowcount > 0