import sqlite3
import os

DB_DEMO_PATH = os.path.join(os.path.dirname(__file__), 'demo.db')


def create_demo_database():
    """Создаёт тестовую БД с данными для демонстрации SQL-запросов"""

    if os.path.exists(DB_DEMO_PATH):
        os.remove(DB_DEMO_PATH)

    conn = sqlite3.connect(DB_DEMO_PATH)
    cursor = conn.cursor()

    # Таблица отделов (создаём раньше employees, т.к. на неё есть ссылка)
    cursor.execute('''
        CREATE TABLE departments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dept_name TEXT NOT NULL,
            manager_id INTEGER,
            budget REAL
        )
    ''')

    # Таблица сотрудников.
    # dept_id и manager_id добавлены, т.к. база знаний бота использует
    # JOIN/рекурсивные CTE по этим колонкам (e.dept_id, e.manager_id) —
    # раньше их не было в схеме, из-за чего запросы падали с ошибкой
    # "no such column: e.dept_id".
    cursor.execute('''
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            salary REAL,
            department TEXT,
            position TEXT,
            hire_date TEXT,
            dept_id INTEGER,
            manager_id INTEGER,
            experience INTEGER DEFAULT 0,
            FOREIGN KEY (dept_id) REFERENCES departments(id),
            FOREIGN KEY (manager_id) REFERENCES employees(id)
        )
    ''')

    # Таблица продуктов
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            price REAL,
            stock INTEGER,
            category TEXT
        )
    ''')

    # Таблица заказов
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            order_date TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    ''')

    # Таблица счетов — нужна для примеров из категории TRANSACTION
    # (BEGIN TRANSACTION; UPDATE accounts SET balance ...). Раньше такой
    # таблицы не было вообще, поэтому все примеры транзакций падали
    # с ошибкой "no such table: accounts".
    cursor.execute('''
        CREATE TABLE accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner TEXT NOT NULL,
            balance REAL NOT NULL
        )
    ''')

    # --- Отделы (сначала, т.к. employees.dept_id на них ссылается) ---
    departments_data = [
        ('IT', None, 500000),
        ('HR', None, 200000),
        ('Sales', None, 350000),
        ('Marketing', None, 300000),
        ('Finance', None, 400000),
    ]
    cursor.executemany(
        'INSERT INTO departments (dept_name, manager_id, budget) VALUES (?, ?, ?)',
        departments_data
    )
    conn.commit()

    dept_ids = {row[0]: row[1] for row in cursor.execute(
        "SELECT dept_name, id FROM departments"
    ).fetchall()}

    # --- Сотрудники ---
    # Формат: name, age, salary, department, position, hire_date, dept_key, manager_key, experience
    # manager_key — временный индекс сотрудника-руководителя в этом же списке (1-based), None если топ-уровень
    employees_data = [
        ('Иван Петров',       30, 75000, 'IT',        'Разработчик',            '2020-01-15', 'IT',        3, 4),
        ('Мария Сидорова',    28, 80000, 'IT',        'Старший разработчик',    '2019-03-10', 'IT',        3, 6),
        ('Алексей Иванов',    35, 90000, 'IT',        'Team Lead',              '2018-06-20', 'IT',        None, 12),
        ('Елена Смирнова',    25, 65000, 'HR',        'HR-менеджер',            '2021-02-01', 'HR',        None, 3),
        ('Дмитрий Козлов',    40, 85000, 'Sales',     'Менеджер по продажам',   '2017-11-11', 'Sales',     9, 15),
        ('Ольга Новикова',    32, 70000, 'Marketing', 'Маркетолог',             '2019-09-15', 'Marketing', None, 8),
        ('Павел Морозов',     29, 72000, 'IT',        'Разработчик',            '2020-07-22', 'IT',        3, 4),
        ('Анна Васильева',    27, 68000, 'HR',        'Рекрутер',               '2021-05-10', 'HR',        4, 2),
        ('Сергей Павлов',     38, 95000, 'Sales',     'Руководитель отдела',    '2016-08-01', 'Sales',     None, 18),
        ('Татьяна Егорова',   33, 78000, 'Marketing', 'PR-менеджер',            '2019-12-03', 'Marketing', 6, 7),
    ]

    # Сначала вставляем всех без manager_id, чтобы узнать реальные id
    inserted_ids = []
    for row in employees_data:
        name, age, salary, dept, position, hire_date, dept_key, _mgr_key, experience = row
        cursor.execute(
            'INSERT INTO employees (name, age, salary, department, position, hire_date, dept_id, experience) '
            'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (name, age, salary, dept, position, hire_date, dept_ids[dept_key], experience)
        )
        inserted_ids.append(cursor.lastrowid)

    # Теперь проставляем manager_id, ссылаясь на реальные id по позиции в списке
    for idx, row in enumerate(employees_data):
        mgr_key = row[7]
        if mgr_key is not None:
            manager_real_id = inserted_ids[mgr_key - 1]
            cursor.execute(
                'UPDATE employees SET manager_id = ? WHERE id = ?',
                (manager_real_id, inserted_ids[idx])
            )
    conn.commit()

    # Проставляем manager_id отделов реальными id руководителей
    dept_manager = {
        'IT': inserted_ids[2],        # Алексей Иванов
        'HR': inserted_ids[3],        # Елена Смирнова
        'Sales': inserted_ids[8],     # Сергей Павлов
        'Marketing': inserted_ids[5], # Ольга Новикова
    }
    for dept_name, manager_id in dept_manager.items():
        cursor.execute(
            'UPDATE departments SET manager_id = ? WHERE dept_name = ?',
            (manager_id, dept_name)
        )

    # --- Продукты ---
    products_data = [
        ('Ноутбук', 120000, 15, 'Электроника'),
        ('Мышь', 2500, 50, 'Электроника'),
        ('Клавиатура', 5000, 30, 'Электроника'),
        ('Монитор', 35000, 10, 'Электроника'),
        ('Стул офисный', 15000, 25, 'Мебель'),
        ('Стол', 25000, 12, 'Мебель'),
        ('Лицензия ПО', 30000, 100, 'ПО'),
    ]
    cursor.executemany(
        'INSERT INTO products (product_name, price, stock, category) VALUES (?, ?, ?, ?)',
        products_data
    )

    # --- Заказы ---
    orders_data = [
        (inserted_ids[0], 1, 1, '2024-01-15'),
        (inserted_ids[0], 2, 2, '2024-01-15'),
        (inserted_ids[1], 1, 1, '2024-01-16'),
        (inserted_ids[1], 4, 1, '2024-01-16'),
        (inserted_ids[4], 5, 3, '2024-01-17'),
        (inserted_ids[5], 6, 1, '2024-01-18'),
        (inserted_ids[2], 1, 1, '2024-01-20'),
        (inserted_ids[6], 3, 2, '2024-01-21'),
        (inserted_ids[8], 7, 5, '2024-01-22'),
    ]
    cursor.executemany(
        'INSERT INTO orders (employee_id, product_id, quantity, order_date) VALUES (?, ?, ?, ?)',
        orders_data
    )

    # --- Счета (для примеров TRANSACTION) ---
    accounts_data = [
        ('Иван Петров', 10000.0),
        ('Мария Сидорова', 5000.0),
    ]
    cursor.executemany(
        'INSERT INTO accounts (owner, balance) VALUES (?, ?)',
        accounts_data
    )

    conn.commit()
    conn.close()

    print(f"✅ Демонстрационная БД создана: {DB_DEMO_PATH}")
    print("📊 Таблицы: employees, departments, products, orders, accounts")
    print("📈 Данные добавлены: 10 сотрудников, 5 отделов, 7 продуктов, 9 заказов, 2 счёта")


def execute_query(sql_query: str, limit: int = 10) -> dict:
    """
    Выполняет SQL-запрос к демонстрационной БД.
    Возвращает результат или ошибку.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_DEMO_PATH)
        cursor = conn.cursor()

        sql_upper = sql_query.upper().strip()
        if sql_upper.startswith('SELECT') and 'LIMIT' not in sql_upper:
            sql_query = f"{sql_query.rstrip(';')} LIMIT {limit};"

        cursor.execute(sql_query)

        if sql_upper.startswith('SELECT'):
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []

            return {
                'success': True,
                'columns': columns,
                'rows': rows,
                'row_count': len(rows),
                'message': f'✅ Запрос выполнен. Получено {len(rows)} строк.'
            }
        else:
            conn.commit()
            return {
                'success': True,
                'message': f'✅ Запрос выполнен. Изменено строк: {cursor.rowcount}'
            }

    except sqlite3.Error as e:
        return {
            'success': False,
            'message': f'❌ Ошибка выполнения: {str(e)}',
            'error': str(e)
        }
    finally:
        if conn:
            conn.close()


def get_table_info(table_name: str) -> dict:
    """Возвращает информацию о структуре таблицы"""
    conn = None
    try:
        conn = sqlite3.connect(DB_DEMO_PATH)
        cursor = conn.cursor()

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]

        return {
            'success': True,
            'columns': columns,
            'row_count': row_count,
            'table_name': table_name
        }
    except sqlite3.Error as e:
        return {
            'success': False,
            'message': f'Таблица {table_name} не найдена'
        }
    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    create_demo_database()

    print("\n--- Тестовый запрос ---")
    result = execute_query("SELECT * FROM employees")
    if result['success']:
        print(result['message'])
        print(f"Колонки: {result['columns']}")
        print(f"Первые строки: {result['rows'][:3]}")
