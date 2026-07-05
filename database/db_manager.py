import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'sql_bot.db')


def init_db():
    """Инициализирует базу данных: создает таблицы"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Таблица вопросов-ответов
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS qa_pairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            sql_example TEXT,
            category VARCHAR(50),
            difficulty INTEGER DEFAULT 1,
            keywords TEXT
        )
    ''')
    
    # Таблица для кэша TF-IDF матрицы
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tfidf_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vector_blob BLOB,
            feature_names BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("База данных инициализирована")


def get_all_qa_pairs():
    """Возвращает все пары вопрос-ответ из базы"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, question, answer, sql_example, category FROM qa_pairs")
    results = cursor.fetchall()
    conn.close()
    return results


def insert_qa_pair(question, answer, sql_example, category, difficulty=1, keywords=''):
    """Добавляет новую пару вопрос-ответ в базу"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO qa_pairs (question, answer, sql_example, category, difficulty, keywords)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (question, answer, sql_example, category, difficulty, keywords))
    conn.commit()
    conn.close()


def clear_cache():
    """Очищает кэш TF-IDF (чтобы перестроить при следующем запуске)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tfidf_cache")
    conn.commit()
    conn.close()
    print("Кэш TF-IDF очищен")


if __name__ == '__main__':
    init_db()