import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), "sql_bot.db")


def init_db():
    """Создаёт таблицы в базе данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qa_pairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            answer TEXT NOT NULL,
            sql_example TEXT,
            code_explanation TEXT,
            table_structure TEXT,
            sample_result TEXT,
            category VARCHAR(50),
            difficulty INTEGER DEFAULT 1,
            keywords TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tfidf_cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vector_blob BLOB,
            feature_names BLOB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("✅ База данных инициализирована")


def clear_cache():
    """Очищает кэш TF-IDF"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tfidf_cache")
    conn.commit()
    conn.close()
    print("🗑️ Кэш TF-IDF очищен")


def insert_qa_pair(question, answer, sql_example, code_explanation, table_structure, sample_result, category, difficulty=1, keywords=""):
    """Добавляет пару вопрос-ответ"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO qa_pairs (question, answer, sql_example, code_explanation, table_structure, sample_result, category, difficulty, keywords)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (question, answer, sql_example, code_explanation, json.dumps(table_structure), json.dumps(sample_result), category, difficulty, keywords))
    conn.commit()
    conn.close()




seed_questions = [
    {
        'question': 'Как добавить UNIQUE ограничение?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 2,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как очистить таблицу?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 3,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Что такое PRIMARY KEY целостность данных constraint?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 2,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'В чем разница DELETE и TRUNCATE удаление записей удалить?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 2,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как начать транзакцию в SQL?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 1,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как вставить данные из другой таблицы вставить добавить?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 2,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как изменить структуру таблицы добавить столбец изменить столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 2,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как удалить столбец изменить столбец удалить столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 1,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как добавить CHECK ограничение целостность данных constraint?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 3,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как удалить столбец изменить столбец изменить столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 3,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как ограничить доступ к данным запретить доступ?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 3,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как использовать RETURNING в DELETE?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 3,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как обновить все строки?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 2,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как добавить ограничение в SQL?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 1,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как использовать самообъединение сделать JOIN соединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как использовать DEFAULT в INSERT вставить добавить?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age, salary, department, position, hire_date) VALUES (\'Игорь Волков\', 26, 60000, \'IT\', \'Стажёр\', \'2024-06-01\');',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 2,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как найти строки по шаблону фильтр выбрать по условию?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как посчитать сумму по группам посчитать сгруппировать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 2,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Чем отличается LEFT JOIN от INNER JOIN сделать JOIN сделать JOIN?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e LEFT JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 3,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как объединить две таблицы объединить связать?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как использовать JOIN с дополнительными условиями соединить соединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 3,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как использовать DEFAULT в INSERT?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age, salary, department, position, hire_date) VALUES (\'Игорь Волков\', 26, 60000, \'IT\', \'Стажёр\', \'2024-06-01\');',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 2,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как выбрать данные с условием на дату извлечь извлечь?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees WHERE hire_date > \'2019-01-01\';',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 3,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как создать временную таблицу создание таблицы создать таблицу?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 1,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как изменить данные поменять изменить?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 2,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как фильтровать по дате фильтр отфильтровать?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать FULL OUTER JOIN сделать JOIN соединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e FULL OUTER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как удалить представление виртуальная таблица виртуальная таблица?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 1,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как сортировать по алфавиту по убыванию по убыванию?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 3,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как выдать привилегии пользователю права доступа запретить?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как создать таблицу с первичным ключом создать таблицу создание таблицы?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 1,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как удалить индекс?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 1,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как сортировать без учета регистра?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 2,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как использовать SELECT с условием?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 2,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать ORDER BY с позицией столбца по убыванию сортировать?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 2,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как создать хранимую процедуру?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 3,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как использовать ROLLUP?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 2,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как создать индекс?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 1,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как использовать JOIN с несколькими условиями?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как сортировать без учета регистра упорядочить по возрастанию?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 3,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как использовать RIGHT JOIN объединить связать?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e RIGHT JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Для чего нужны триггеры trigger trigger?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 2,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как добавить строку в базу данных новая запись создать запись?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 1,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как использовать NATURAL JOIN связать связать?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как обновить данные из другой таблицы поменять обновление данных?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 3,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как фильтровать по дате?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Что такое JOIN простыми словами?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как использовать FULL OUTER JOIN объединить сделать JOIN?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e FULL OUTER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как выбрать конкретные столбцы из таблицы?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как вставить с RETURNING?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 3,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как работает JOIN в SQL объединить связать?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'В чем разница DELETE и TRUNCATE убрать убрать?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 2,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как работает триггер в SQL триггер триггер?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 2,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как удалить все строки удаление записей удалить?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 1,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как использовать SELECT с подзапросом извлечь выбрать?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT name, salary, (SELECT AVG(salary) FROM employees) AS avg_salary FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как отменить изменения в SQL transaction commit?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 3,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как создать таблицу?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 2,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как работает JOIN в SQL?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 3,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как выбрать все данные из таблицы?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 2,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как начать транзакцию в SQL commit transaction?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 2,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как использовать RETURNING в UPDATE обновить обновить?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 1,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как выбрать данные с сортировкой?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 3,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать BETWEEN для диапазона фильтр отфильтровать?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE salary BETWEEN 70000 AND 90000;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать WHERE с подзапросом выбрать по условию отфильтровать?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как дать доступ к таблице запретить разрешить?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как использовать DEFAULT в INSERT добавить вставить?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age, salary, department, position, hire_date) VALUES (\'Игорь Волков\', 26, 60000, \'IT\', \'Стажёр\', \'2024-06-01\');',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 3,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Что такое JOIN простыми словами связать сделать JOIN?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'В чем разница DELETE и TRUNCATE?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 1,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Когда срабатывает триггер триггер триггер?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 1,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как использовать WHERE с подзапросом?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Зачем нужны процедуры?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 2,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как использовать SELECT с вычисляемыми полями запросить получить?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать CUBE группировка группа?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как удалить записи убрать удалить?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 1,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Когда срабатывает триггер автоматическое выполнение триггер?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 1,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как использовать EXISTS с коррелированным подзапросом?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees e WHERE EXISTS (SELECT 1 FROM orders o WHERE o.employee_id = e.id);',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как выдать роль в SQL?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как использовать COMMIT и ROLLBACK transaction transaction?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 3,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как использовать LIKE для поиска условие фильтр?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE name LIKE \'%ов%\';',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как добавить NOT NULL ограничение?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 3,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как работает триггер в SQL?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 1,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как использовать GROUPING SETS?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как обновить несколько столбцов обновить обновление данных?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 3,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как использовать ANY и ALL отфильтровать выбрать по условию?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как обновить данные из другой таблицы поменять поменять?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 3,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как ускорить поиск в таблице?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 3,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как использовать несколько условий в WHERE?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать REGEXP в SQL отфильтровать выбрать по условию?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как добавить ограничение в SQL ограничение внешний ключ?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 1,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как выбрать данные с группировкой?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать GRANT доступ разрешить?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 3,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как ускорить поиск в таблице ускорить поиск create index?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 1,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как очистить таблицу удаление записей удаление записей?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 2,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как переименовать столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 1,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как использовать SELECT с условием извлечь извлечь?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 2,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать IN для списка значений фильтр фильтр?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать COMMIT и ROLLBACK?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 2,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как использовать EXISTS с коррелированным подзапросом отфильтровать фильтр?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees e WHERE EXISTS (SELECT 1 FROM orders o WHERE o.employee_id = e.id);',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как ограничить доступ к данным права доступа запретить?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Что такое составной индекс?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 1,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как добавить столбец добавить столбец добавить столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 2,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как вставить данные из другой таблицы?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 3,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как использовать FULL OUTER JOIN?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e FULL OUTER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как удалить индекс create index create index?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 2,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как использовать ANY и ALL?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как выдать привилегии пользователю разрешить права доступа?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как добавить UNIQUE ограничение целостность данных внешний ключ?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 2,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как удалить записи?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 1,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как использовать JOIN с подзапросом связать соединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.avg_salary FROM employees e JOIN (SELECT dept_id, AVG(salary) AS avg_salary FROM employees GROUP BY dept_id) d ON e.dept_id = d.dept_id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 3,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как использовать BETWEEN для диапазона выбрать по условию условие?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE salary BETWEEN 70000 AND 90000;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как разрешить пользователю SELECT права доступа привилегии?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 3,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как использовать JOIN с подзапросом?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.avg_salary FROM employees e JOIN (SELECT dept_id, AVG(salary) AS avg_salary FROM employees GROUP BY dept_id) d ON e.dept_id = d.dept_id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Чем DROP отличается от DELETE удаление таблицы удалить таблицу?',
        'answer': 'DROP TABLE удаляет таблицу из базы данных вместе со всеми данными. Операция необратима.',
        'sql_example': 'DROP TABLE employees;',
        'code_explanation': 'Строка: `DROP` — удаление объекта из базы данных (необратимо!); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица удалена"}],
        'category': 'DROP',
        'difficulty': 3,
        'keywords': 'удалить таблицу drop удаление таблицы'
    }
,
    {
        'question': 'Как использовать CROSS JOIN соединить объединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как использовать SELECT с псевдонимами извлечь запросить?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 2,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как создать представление представление view?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 2,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как использовать SELECT с подзапросом?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT name, salary, (SELECT AVG(salary) FROM employees) AS avg_salary FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать REGEXP в SQL?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать несколько условий в WHERE выбрать по условию условие?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как отфильтровать данные с условием выбрать по условию отфильтровать?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Что такое транзакция транзакция commit?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 3,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как использовать IN для списка значений отфильтровать условие?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как изменить значения в таблице?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 1,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как изменить тип столбца?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 3,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как создать индекс create index create index?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 1,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как фильтровать по дате выбрать по условию фильтр?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать ORDER BY с NULL значениями по убыванию по убыванию?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 2,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как выдать права доступа доступ права доступа?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 2,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как изменить данные поменять обновить?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 2,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как использовать DROP TABLE удалить таблицу drop?',
        'answer': 'DROP TABLE удаляет таблицу из базы данных вместе со всеми данными. Операция необратима.',
        'sql_example': 'DROP TABLE employees;',
        'code_explanation': 'Строка: `DROP` — удаление объекта из базы данных (необратимо!); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица удалена"}],
        'category': 'DROP',
        'difficulty': 1,
        'keywords': 'удалить таблицу drop удаление таблицы'
    }
,
    {
        'question': 'Как выбрать данные с сортировкой получить запросить?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как отсортировать результаты по возрастанию сортировать?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 2,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как посчитать количество записей в группе?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 3,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Что такое VIEW в SQL view виртуальная таблица?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 1,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как выбрать данные с условием на дату получить выбрать?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees WHERE hire_date > \'2019-01-01\';',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как отфильтровать данные с условием?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать SELECT с псевдонимами?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как обновить запись в SQL изменить поменять?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 3,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Чем процедура отличается от функции?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 3,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как отфильтровать данные с условием условие условие?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать DROP TABLE drop удалить таблицу?',
        'answer': 'DROP TABLE удаляет таблицу из базы данных вместе со всеми данными. Операция необратима.',
        'sql_example': 'DROP TABLE employees;',
        'code_explanation': 'Строка: `DROP` — удаление объекта из базы данных (необратимо!); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица удалена"}],
        'category': 'DROP',
        'difficulty': 1,
        'keywords': 'удалить таблицу drop удаление таблицы'
    }
,
    {
        'question': 'Как создать триггер?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 2,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как использовать WHERE с подзапросом выбрать по условию выбрать по условию?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как удалить таблицу навсегда удаление таблицы drop?',
        'answer': 'DROP TABLE удаляет таблицу из базы данных вместе со всеми данными. Операция необратима.',
        'sql_example': 'DROP TABLE employees;',
        'code_explanation': 'Строка: `DROP` — удаление объекта из базы данных (необратимо!); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица удалена"}],
        'category': 'DROP',
        'difficulty': 1,
        'keywords': 'удалить таблицу drop удаление таблицы'
    }
,
    {
        'question': 'Как использовать LIKE с несколькими шаблонами?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE name LIKE \'И%\' OR name LIKE \'А%\';',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как объединить три таблицы объединить объединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как объединить две таблицы?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Что такое уровни изоляции транзакция commit?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 3,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как дать доступ к таблице привилегии запретить?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как удалить с подзапросом?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE dept_id IN (SELECT id FROM departments WHERE budget < 250000);',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 3,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как использовать CROSS JOIN?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как использовать LIKE с несколькими шаблонами условие условие?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE name LIKE \'И%\' OR name LIKE \'А%\';',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать CUBE?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 2,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Когда срабатывает триггер?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 3,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как использовать представление?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 2,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Что такое PRIMARY KEY constraint целостность данных?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 1,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Для чего нужны представления?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 3,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как добавить несколько записей сразу?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 2,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как использовать ORDER BY с NULL значениями отсортировать упорядочить?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 1,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как использовать RIGHT JOIN?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e RIGHT JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как изменить тип столбца добавить столбец добавить столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 2,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как использовать CROSS JOIN соединить связать?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как добавить новую запись добавить новая запись?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 3,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как ограничить количество строк запросить выбрать?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 3,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как очистить таблицу убрать стереть?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 2,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как выбрать данные с условием на дату?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees WHERE hire_date > \'2019-01-01\';',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 2,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как сортировать без учета регистра по возрастанию по возрастанию?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 2,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Чем отличается LEFT JOIN от INNER JOIN объединить связать?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e LEFT JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 3,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Что такое уникальный индекс?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 3,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Зачем нужны процедуры stored procedure хранимая процедура?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 3,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как использовать ROLLUP группа посчитать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как добавить строку в базу данных новая запись новая запись?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 2,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как использовать COMMIT и ROLLBACK commit rollback?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 1,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как найти максимум и минимум в группе сгруппировать группа?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 3,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как добавить строку в базу данных?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 1,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как выдать права доступа?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как удалить таблицу из базы удаление таблицы удаление таблицы?',
        'answer': 'DROP TABLE удаляет таблицу из базы данных вместе со всеми данными. Операция необратима.',
        'sql_example': 'DROP TABLE employees;',
        'code_explanation': 'Строка: `DROP` — удаление объекта из базы данных (необратимо!); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица удалена"}],
        'category': 'DROP',
        'difficulty': 3,
        'keywords': 'удалить таблицу drop удаление таблицы'
    }
,
    {
        'question': 'Как создать хранимую процедуру процедура процедура?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 2,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как использовать SELECT с псевдонимами выбрать извлечь?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как удалить представление?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 3,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как отменить изменения в SQL commit rollback?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 1,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как найти строки по шаблону фильтр условие?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как удалить таблицу навсегда удалить таблицу drop?',
        'answer': 'DROP TABLE удаляет таблицу из базы данных вместе со всеми данными. Операция необратима.',
        'sql_example': 'DROP TABLE employees;',
        'code_explanation': 'Строка: `DROP` — удаление объекта из базы данных (необратимо!); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица удалена"}],
        'category': 'DROP',
        'difficulty': 1,
        'keywords': 'удалить таблицу drop удаление таблицы'
    }
,
    {
        'question': 'Для чего нужны представления view виртуальная таблица?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 3,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как проверить NULL в SQL фильтр условие?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать самообъединение?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 3,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как сортировать по нескольким столбцам отсортировать по убыванию?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 3,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Чем процедура отличается от функции хранимая процедура процедура?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 2,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как выбрать уникальные значения выбрать запросить?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 3,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как вызвать процедуру в SQL?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 1,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как вставить данные в таблицу новая запись вставить?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 2,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как создать таблицу с первичным ключом?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 1,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как использовать RETURNING в DELETE удаление записей стереть?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 3,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как изменить значения в таблице поменять изменить?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 1,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Зачем нужны индексы в SQL create index индекс?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 2,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как переименовать столбец изменить столбец удалить столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 3,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как объединить три таблицы сделать JOIN объединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как ускорить поиск в таблице create index индекс?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 1,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как использовать RETURNING в DELETE удалить убрать?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 3,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как ограничить количество строк?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 3,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать ORDER BY с вычисляемым полем по убыванию по убыванию?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 2,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как добавить новую запись создать запись создать запись?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 1,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как обновить запись в SQL обновление данных изменить?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 3,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Что такое VIEW в SQL view view?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 1,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как использовать ORDER BY с вычисляемым полем?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 2,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как ограничить доступ к данным?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 3,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как использовать JOIN с несколькими условиями связать соединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 3,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как использовать HAVING для фильтрации групп группировка сгруппировать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) > 1;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 2,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как обновить все строки изменить поменять?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 2,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как зафиксировать изменения в SQL commit транзакция?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 1,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как добавить столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 2,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как использовать SELECT с условием выбрать выбрать?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать REVOKE?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 3,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как использовать GROUP BY по нескольким столбцам сгруппировать группа?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 2,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как найти максимум и минимум в группе?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 3,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как использовать WHERE и HAVING вместе?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees WHERE age > 25 GROUP BY department HAVING COUNT(*) > 1;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 2,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как проверить NULL в SQL фильтр отфильтровать?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать ORDER BY с вычисляемым полем сортировать по возрастанию?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 1,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как использовать SELECT с подзапросом выбрать выбрать?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT name, salary, (SELECT AVG(salary) FROM employees) AS avg_salary FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 2,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как переименовать столбец удалить столбец добавить столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 2,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как отсортировать результаты?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 3,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как вставить с RETURNING вставить создать запись?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 3,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Что такое транзакция?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 3,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как выбрать данные с группировкой извлечь получить?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать GROUPING SETS посчитать посчитать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 3,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как создать временную таблицу?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 3,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как удалить таблицу из базы удаление таблицы удалить таблицу?',
        'answer': 'DROP TABLE удаляет таблицу из базы данных вместе со всеми данными. Операция необратима.',
        'sql_example': 'DROP TABLE employees;',
        'code_explanation': 'Строка: `DROP` — удаление объекта из базы данных (необратимо!); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица удалена"}],
        'category': 'DROP',
        'difficulty': 3,
        'keywords': 'удалить таблицу drop удаление таблицы'
    }
,
    {
        'question': 'Как использовать ORDER BY с NULL значениями?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 2,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как проверить NULL в SQL?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как создать индекс create index ускорить поиск?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 3,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как создать таблицу на основе существующей создать таблицу создание таблицы?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 1,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как использовать WHERE и HAVING вместе сгруппировать посчитать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees WHERE age > 25 GROUP BY department HAVING COUNT(*) > 1;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 3,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Что такое уровни изоляции?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 1,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как удалить представление представление view?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 3,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как создать таблицу на основе существующей создание таблицы создать таблицу?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 2,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как отозвать права доступа разрешить доступ?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 3,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как отсортировать результаты по убыванию по убыванию?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 2,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Что такое транзакция rollback транзакция?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 3,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как выдать права доступа запретить привилегии?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как создать представление?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 1,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как обновить данные из другой таблицы?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 2,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как создать FOREIGN KEY ограничение внешний ключ?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 2,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как сортировать по алфавиту по возрастанию по убыванию?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 1,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как посчитать количество записей в группе группа группа?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как объединить три таблицы?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как создать новую таблицу в SQL?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 1,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как использовать JOIN с дополнительными условиями?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как посчитать сумму по группам сгруппировать группа?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как использовать агрегатные функции с DISTINCT посчитать посчитать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT COUNT(DISTINCT department) FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как использовать ORDER BY с позицией столбца по убыванию отсортировать?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 1,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как соединить таблицы без JOIN?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 3,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как зафиксировать изменения в SQL rollback transaction?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 2,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как отменить изменения в SQL?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 2,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как использовать самообъединение соединить соединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 3,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Чем отличается LEFT JOIN от INNER JOIN?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e LEFT JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 3,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Зачем нужны процедуры хранимая процедура stored procedure?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 2,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как работает хранимая процедура хранимая процедура процедура?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 1,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как сортировать по нескольким столбцам по убыванию упорядочить?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 2,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как создать таблицу на основе существующей?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 2,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как изменить значения в таблице изменить обновление данных?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 1,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как использовать CUBE посчитать группа?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 2,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как добавить новую запись?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 2,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как найти максимум и минимум в группе группа сгруппировать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 3,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как обновить несколько столбцов изменить поменять?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 1,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как добавить NOT NULL ограничение внешний ключ constraint?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 2,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как вызвать процедуру в SQL процедура хранимая процедура?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 2,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как использовать JOIN с дополнительными условиями объединить объединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как выдать роль в SQL привилегии разрешить?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как выбрать данные с сортировкой извлечь выбрать?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 3,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как вставить данные в таблицу?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 2,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как выбрать данные с группировкой запросить получить?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 3,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как изменить данные?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 1,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как соединить таблицы без JOIN связать соединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как начать транзакцию в SQL rollback rollback?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 2,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как использовать триггер для автоматического обновления даты?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 3,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как сортировать по алфавиту?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 1,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как удалить все строки?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 3,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Чем DROP отличается от DELETE?',
        'answer': 'DROP TABLE удаляет таблицу из базы данных вместе со всеми данными. Операция необратима.',
        'sql_example': 'DROP TABLE employees;',
        'code_explanation': 'Строка: `DROP` — удаление объекта из базы данных (необратимо!); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица удалена"}],
        'category': 'DROP',
        'difficulty': 3,
        'keywords': 'удалить таблицу drop удаление таблицы'
    }
,
    {
        'question': 'Что такое процедура в SQL процедура процедура?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 2,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как использовать SELECT с вычисляемыми полями запросить запросить?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 2,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как удалить индекс ускорить поиск create index?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 3,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как удалить таблицу навсегда?',
        'answer': 'DROP TABLE удаляет таблицу из базы данных вместе со всеми данными. Операция необратима.',
        'sql_example': 'DROP TABLE employees;',
        'code_explanation': 'Строка: `DROP` — удаление объекта из базы данных (необратимо!); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица удалена"}],
        'category': 'DROP',
        'difficulty': 2,
        'keywords': 'удалить таблицу drop удаление таблицы'
    }
,
    {
        'question': 'Как использовать HAVING для фильтрации групп группировка посчитать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) > 1;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как добавить несколько записей сразу вставить добавить?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 3,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как запретить доступ к таблице права доступа доступ?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как использовать триггер для автоматического обновления даты автоматическое выполнение trigger?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 1,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как посчитать среднее значение по группам группа посчитать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как удалить таблицу из базы?',
        'answer': 'DROP TABLE удаляет таблицу из базы данных вместе со всеми данными. Операция необратима.',
        'sql_example': 'DROP TABLE employees;',
        'code_explanation': 'Строка: `DROP` — удаление объекта из базы данных (необратимо!); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица удалена"}],
        'category': 'DROP',
        'difficulty': 3,
        'keywords': 'удалить таблицу drop удаление таблицы'
    }
,
    {
        'question': 'Чем процедура отличается от функции хранимая процедура stored procedure?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 1,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как посчитать количество записей в группе группировка сгруппировать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 2,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как создать таблицу с первичным ключом создать таблицу создать таблицу?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 2,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Для чего нужны представления view представление?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 2,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как посчитать среднее значение по группам?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 2,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Зачем нужны индексы в SQL?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 2,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как обновить запись в SQL?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 1,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как использовать GROUP BY по нескольким столбцам?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 2,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Что такое триггер триггер триггер?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 2,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Что такое уникальный индекс create index индекс?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 1,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как использовать REGEXP в SQL фильтр отфильтровать?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Что такое VIEW в SQL?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 3,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как зафиксировать изменения в SQL?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 3,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Как отозвать права доступа разрешить привилегии?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 2,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как выбрать уникальные значения извлечь извлечь?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как сгруппировать строки группа посчитать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 2,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как работает хранимая процедура хранимая процедура stored procedure?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 3,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как сортировать по нескольким столбцам?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 2,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как вставить данные в таблицу создать запись создать запись?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 1,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как использовать NOT для отрицания?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как обновить несколько столбцов?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 1,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как использовать REVOKE права доступа права доступа?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 2,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как объединить две таблицы соединить соединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как использовать LIKE для поиска?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE name LIKE \'%ов%\';',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать SELECT с вычисляемыми полями?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 2,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как вызвать процедуру в SQL хранимая процедура stored procedure?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 2,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как добавить несколько записей сразу добавить новая запись?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 1,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как использовать WHERE и HAVING вместе группировка группировка?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees WHERE age > 25 GROUP BY department HAVING COUNT(*) > 1;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как использовать RETURNING в UPDATE обновить поменять?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 2,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как выдать роль в SQL разрешить разрешить?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как добавить столбец удалить столбец удалить столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 1,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как разрешить пользователю SELECT?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 3,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Что такое PRIMARY KEY?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 1,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как использовать ANY и ALL условие условие?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как создать новую таблицу в SQL создание таблицы новая таблица?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 3,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как использовать GRANT запретить привилегии?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 3,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Что такое уникальный индекс ускорить поиск индекс?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 1,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как использовать ROLLUP посчитать группировка?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 3,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как создать триггер trigger trigger?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 2,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как создать новую таблицу в SQL создать таблицу новая таблица?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 2,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как использовать IN для списка значений?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как работает хранимая процедура?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 1,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как удалить все строки удаление записей стереть?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 1,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как создать FOREIGN KEY?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 1,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как использовать LIKE с несколькими шаблонами фильтр отфильтровать?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE name LIKE \'И%\' OR name LIKE \'А%\';',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Что такое процедура в SQL?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 1,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как использовать JOIN с подзапросом соединить соединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.avg_salary FROM employees e JOIN (SELECT dept_id, AVG(salary) AS avg_salary FROM employees GROUP BY dept_id) d ON e.dept_id = d.dept_id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как использовать JOIN с несколькими условиями связать связать?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как добавить CHECK ограничение?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 3,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как вставить с RETURNING создать запись создать запись?',
        'answer': 'INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.',
        'sql_example': 'INSERT INTO employees (name, age) VALUES (\'Иван\', 30);',
        'code_explanation': 'Строка: `INSERT` — вставка новой строки в таблицу; `INTO` — указывает целевую таблицу для INSERT (вставка); `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'; `age` — столбец \'age\' из таблицы \'employees\'; `VALUES` — перечисление значений для вставки; `\'Иван\'` — строковое значение; `30` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка добавлена"}],
        'category': 'INSERT',
        'difficulty': 1,
        'keywords': 'добавить вставить создать запись'
    }
,
    {
        'question': 'Как работает триггер в SQL автоматическое выполнение триггер?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 3,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как работает JOIN в SQL объединить объединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как сгруппировать строки?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как посчитать среднее значение по группам группировка группа?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 3,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как удалить данные из таблицы?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 1,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Что такое триггер автоматическое выполнение trigger?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 3,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Что такое уровни изоляции commit rollback?',
        'answer': 'Транзакция — группа операций, выполняемых как единое целое. BEGIN, COMMIT, ROLLBACK.',
        'sql_example': 'BEGIN TRANSACTION; UPDATE accounts SET balance = balance - 100 WHERE id = 1; UPDATE accounts SET balance = balance + 100 WHERE id = 2; COMMIT;',
        'code_explanation': 'Строка: `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `TRANSACTION` — транзакция — группа операций, которые выполняются как единое целое; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число; `UPDATE` — обновление существующих данных в таблице; `accounts` — идентификатор (имя столбца, таблицы или переменной); `SET` — указывает, какие столбцы обновить и на какие значения; `balance` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `balance` — идентификатор (имя столбца, таблицы или переменной); `+` — математический оператор; `100` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `2` — число; `COMMIT` — подтверждение транзакции (сохранение всех изменений в базе данных)',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRANSACTION',
        'difficulty': 2,
        'keywords': 'транзакция transaction commit'
    }
,
    {
        'question': 'Чем DROP отличается от DELETE удаление таблицы удаление таблицы?',
        'answer': 'DROP TABLE удаляет таблицу из базы данных вместе со всеми данными. Операция необратима.',
        'sql_example': 'DROP TABLE employees;',
        'code_explanation': 'Строка: `DROP` — удаление объекта из базы данных (необратимо!); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица удалена"}],
        'category': 'DROP',
        'difficulty': 1,
        'keywords': 'удалить таблицу drop удаление таблицы'
    }
,
    {
        'question': 'Как добавить UNIQUE ограничение constraint внешний ключ?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 1,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как использовать несколько условий в WHERE условие отфильтровать?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как использовать GRANT?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Для чего нужны триггеры?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 3,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как использовать NOT для отрицания выбрать по условию отфильтровать?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как запретить доступ к таблице?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 2,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как создать таблицу новая таблица новая таблица?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 3,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как создать временную таблицу создать таблицу создание таблицы?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 2,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как использовать NATURAL JOIN объединить соединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 1,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как удалить записи убрать убрать?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 2,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как использовать ORDER BY с позицией столбца?',
        'answer': 'ORDER BY сортирует результаты запроса по одному или нескольким столбцам. ASC — по возрастанию, DESC — по убыванию.',
        'sql_example': 'SELECT * FROM employees ORDER BY salary DESC;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `ORDER` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `salary` — столбец \'salary\' из таблицы \'employees\'; `DESC` — сортировка по убыванию (от большего к меньшему)',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"name": "Сергей Павлов", "salary": 95000}, {"name": "Алексей Иванов", "salary": 90000}, {"name": "Дмитрий Козлов", "salary": 85000}],
        'category': 'ORDER BY',
        'difficulty': 3,
        'keywords': 'сортировать упорядочить отсортировать'
    }
,
    {
        'question': 'Как разрешить пользователю SELECT права доступа доступ?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 2,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как использовать агрегатные функции с DISTINCT?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT COUNT(DISTINCT department) FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 3,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как использовать представление представление представление?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 2,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как посчитать сумму по группам?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 3,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как использовать EXISTS с коррелированным подзапросом условие отфильтровать?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees e WHERE EXISTS (SELECT 1 FROM orders o WHERE o.employee_id = e.id);',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Что такое JOIN простыми словами сделать JOIN сделать JOIN?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 3,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как добавить NOT NULL ограничение constraint внешний ключ?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 2,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как удалить данные из таблицы убрать убрать?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 1,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как удалить столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 3,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как изменить тип столбца изменить столбец добавить столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 3,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как использовать агрегатные функции с DISTINCT посчитать сгруппировать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT COUNT(DISTINCT department) FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 3,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как создать FOREIGN KEY целостность данных ограничение?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 2,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как дать доступ к таблице?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как изменить структуру таблицы изменить столбец изменить столбец?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 3,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Как создать таблицу новая таблица создание таблицы?',
        'answer': 'CREATE TABLE создаёт новую таблицу. Нужно указать имя таблицы, столбцы и их типы данных.',
        'sql_example': 'CREATE TABLE employees (id INT, name TEXT, salary DECIMAL);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `id` — столбец \'id\' из таблицы \'employees\'; `INT` — целое число (сокращение от INTEGER); `name` — столбец \'name\' из таблицы \'employees\'; `TEXT` — текстовая строка переменной длины; `salary` — столбец \'salary\' из таблицы \'employees\'; `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица создана"}],
        'category': 'CREATE',
        'difficulty': 2,
        'keywords': 'создать таблицу создание таблицы новая таблица'
    }
,
    {
        'question': 'Как использовать триггер для автоматического обновления даты триггер trigger?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 2,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как использовать LIKE для поиска отфильтровать выбрать по условию?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE name LIKE \'%ов%\';',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 2,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как выбрать уникальные значения?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 3,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать GROUPING SETS группа сгруппировать?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как отозвать права доступа?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 1,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как ограничить количество строк получить выбрать?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 2,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать BETWEEN для диапазона?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE salary BETWEEN 70000 AND 90000;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 1,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как создать триггер автоматическое выполнение триггер?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 1,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как удалить с подзапросом стереть удалить?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE dept_id IN (SELECT id FROM departments WHERE budget < 250000);',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 3,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Зачем нужны индексы в SQL ускорить поиск индекс?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 3,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как соединить таблицы без JOIN объединить объединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как создать хранимую процедуру stored procedure хранимая процедура?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 2,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Что такое триггер?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 3,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как выбрать все данные из таблицы получить извлечь?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 3,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать представление view представление?',
        'answer': 'VIEW — виртуальная таблица, создаваемая на основе запроса. Упрощает доступ к данным.',
        'sql_example': 'CREATE VIEW high_salary AS SELECT * FROM employees WHERE salary > 70000;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `VIEW` — представление — виртуальная таблица на основе запроса (не хранит данные, только показывает); `high_salary` — идентификатор (имя столбца, таблицы или переменной); `AS` — задаёт псевдоним (алиас) для столбца или таблицы (удобно для сокращения имён); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `salary` — столбец \'salary\' из таблицы \'employees\'; `>` — оператор сравнения; `70000` — число',
        'table_structure': [],
        'sample_result': [],
        'category': 'VIEW',
        'difficulty': 3,
        'keywords': 'представление view виртуальная таблица'
    }
,
    {
        'question': 'Как использовать RIGHT JOIN соединить объединить?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e RIGHT JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Как использовать NATURAL JOIN?',
        'answer': 'JOIN объединяет строки из двух таблиц по условию. INNER JOIN возвращает совпадающие строки, LEFT JOIN — все строки из левой таблицы, RIGHT JOIN — все строки из правой таблицы.',
        'sql_example': 'SELECT e.name, d.dept_name FROM employees e INNER JOIN departments d ON e.dept_id = d.id;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `e.name` — столбец \'name\'; `d.dept_name` — столбец \'dept_name\'; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `e` — идентификатор (имя столбца, таблицы или переменной); `INNER` — идентификатор (имя столбца, таблицы или переменной); `JOIN` — объединение двух таблиц по условию; `departments` — таблица departments — содержит данные о departments; `d` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `e.dept_id` — столбец \'dept_id\'; `=` — оператор сравнения; `d.id` — столбец \'id\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}, {"name": "departments", "columns": ["id", "dept_name", "manager_id", "budget"], "sample_rows": [[1, "IT", 3, 500000], [2, "HR", 4, 200000], [3, "Sales", 9, 350000], [4, "Marketing", 6, 300000], [5, "Finance", None, 400000]]}],
        'sample_result': [{"name": "Иван Петров", "dept_name": "IT"}, {"name": "Мария Сидорова", "dept_name": "IT"}, {"name": "Алексей Иванов", "dept_name": "HR"}, {"name": "Дмитрий Козлов", "dept_name": "Sales"}, {"name": "Ольга Новикова", "dept_name": "Marketing"}],
        'category': 'JOIN',
        'difficulty': 2,
        'keywords': 'объединить соединить связать'
    }
,
    {
        'question': 'Для чего нужны триггеры trigger автоматическое выполнение?',
        'answer': 'Триггер — процедура, которая автоматически выполняется при вставке, обновлении или удалении данных.',
        'sql_example': 'CREATE TRIGGER update_timestamp AFTER UPDATE ON employees FOR EACH ROW BEGIN UPDATE employees SET updated_at = NOW() WHERE id = NEW.id; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `TRIGGER` — триггер — процедура, которая автоматически выполняется при INSERT, UPDATE или DELETE; `update_timestamp` — идентификатор (имя столбца, таблицы или переменной); `AFTER` — триггер срабатывает ПОСЛЕ выполнения операции (INSERT/UPDATE/DELETE); `UPDATE` — обновление существующих данных в таблице; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `FOR` — идентификатор (имя столбца, таблицы или переменной); `EACH` — идентификатор (имя столбца, таблицы или переменной); `ROW` — строка — одна запись в таблице, содержащая значения всех столбцов; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `updated_at` — идентификатор (имя столбца, таблицы или переменной); `=` — оператор сравнения; `NOW` — идентификатор (имя столбца, таблицы или переменной); `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `NEW.id` — столбец \'id\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'TRIGGER',
        'difficulty': 1,
        'keywords': 'триггер trigger автоматическое выполнение'
    }
,
    {
        'question': 'Как сгруппировать строки сгруппировать группировка?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Что такое составной индекс индекс ускорить поиск?',
        'answer': 'Индекс ускоряет поиск данных в таблице. Создаётся на одном или нескольких столбцах.',
        'sql_example': 'CREATE INDEX idx_name ON employees(name);',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `INDEX` — индекс — структура данных для ускорения поиска и сортировки в таблице; `idx_name` — идентификатор (имя столбца, таблицы или переменной); `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `name` — столбец \'name\' из таблицы \'employees\'',
        'table_structure': [],
        'sample_result': [],
        'category': 'INDEX',
        'difficulty': 1,
        'keywords': 'индекс ускорить поиск create index'
    }
,
    {
        'question': 'Как добавить ограничение в SQL внешний ключ ограничение?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 3,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как использовать RETURNING в UPDATE?',
        'answer': 'UPDATE изменяет существующие строки. Всегда используйте WHERE, чтобы не обновить все строки.',
        'sql_example': 'UPDATE employees SET salary = 50000 WHERE name = \'Иван\';',
        'code_explanation': 'Строка: `UPDATE` — обновление существующих данных в таблице; `employees` — таблица employees — содержит данные о employees; `SET` — указывает, какие столбцы обновить и на какие значения; `salary` — столбец \'salary\' из таблицы \'employees\'; `=` — оператор сравнения; `50000` — число; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `name` — столбец \'name\' из таблицы \'employees\'; `=` — оператор сравнения; `\'Иван\'` — строковое значение',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка обновлена"}],
        'category': 'UPDATE',
        'difficulty': 3,
        'keywords': 'обновить изменить поменять'
    }
,
    {
        'question': 'Как использовать HAVING для фильтрации групп?',
        'answer': 'GROUP BY группирует строки с одинаковыми значениями. Агрегатные функции (COUNT, SUM, AVG, MAX, MIN) применяются к каждой группе.',
        'sql_example': 'SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) > 1;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `department` — столбец \'department\' из таблицы \'employees\'; `COUNT` — подсчёт количества строк в группе (COUNT(*) — все строки, COUNT(column) — непустые значения); `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `GROUP` — идентификатор (имя столбца, таблицы или переменной); `BY` — идентификатор (имя столбца, таблицы или переменной); `department` — столбец \'department\' из таблицы \'employees\'',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"department": "IT", "count": 3}, {"department": "HR", "count": 2}, {"department": "Sales", "count": 2}, {"department": "Marketing", "count": 2}],
        'category': 'GROUP BY',
        'difficulty': 1,
        'keywords': 'сгруппировать группировка группа'
    }
,
    {
        'question': 'Как использовать REVOKE привилегии права доступа?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 2,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как удалить данные из таблицы удаление записей удаление записей?',
        'answer': 'DELETE удаляет строки по условию. Без WHERE удаляются все строки. Используйте с осторожностью.',
        'sql_example': 'DELETE FROM employees WHERE id = 1;',
        'code_explanation': 'Строка: `DELETE` — удаление строк из таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `id` — столбец \'id\' из таблицы \'employees\'; `=` — оператор сравнения; `1` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ 1 строка удалена"}],
        'category': 'DELETE',
        'difficulty': 3,
        'keywords': 'удалить убрать стереть'
    }
,
    {
        'question': 'Как изменить структуру таблицы?',
        'answer': 'ALTER TABLE изменяет структуру существующей таблицы: добавляет, удаляет или изменяет столбцы.',
        'sql_example': 'ALTER TABLE employees ADD COLUMN bonus DECIMAL;',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `COLUMN` — столбец — поле в таблице, содержащее данные одного типа; `bonus` — идентификатор (имя столбца, таблицы или переменной); `DECIMAL` — число с фиксированной точностью (для денежных значений, например DECIMAL(10,2))',
        'table_structure': [],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'ALTER',
        'difficulty': 2,
        'keywords': 'добавить столбец удалить столбец изменить столбец'
    }
,
    {
        'question': 'Что такое процедура в SQL хранимая процедура хранимая процедура?',
        'answer': 'Хранимая процедура — это блок SQL-кода, который сохраняется на сервере и вызывается по имени. Может принимать параметры.',
        'sql_example': 'CREATE PROCEDURE GetEmployeesByDept(IN dept_name VARCHAR(50)) BEGIN SELECT * FROM employees WHERE department = dept_name; END;',
        'code_explanation': 'Строка: `CREATE` — создание нового объекта (таблицы, индекса, триггера, процедуры, представления); `PROCEDURE` — хранимая процедура — блок кода, который сохраняется на сервере и вызывается по имени; `GetEmployeesByDept` — идентификатор (имя столбца, таблицы или переменной); `IN` — проверка, входит ли значение в список (например, column IN (1,2,3)); `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `VARCHAR` — текстовая строка переменной длины с максимальной длиной; `50` — число; `BEGIN` — начало транзакции (группа операций, выполняемых как единое целое); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `department` — столбец \'department\' из таблицы \'employees\'; `=` — оператор сравнения; `dept_name` — столбец \'dept_name\' из таблицы \'departments\'; `END` — конец конструкции CASE или блока кода',
        'table_structure': [],
        'sample_result': [{"message": "✅ Хранимая процедура создана"}],
        'category': 'PROCEDURE',
        'difficulty': 1,
        'keywords': 'процедура хранимая процедура stored procedure'
    }
,
    {
        'question': 'Как добавить CHECK ограничение constraint ограничение?',
        'answer': 'Ограничения (constraints) обеспечивают целостность данных: PRIMARY KEY, FOREIGN KEY, UNIQUE, CHECK, NOT NULL.',
        'sql_example': 'ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);',
        'code_explanation': 'Строка: `ALTER` — изменение структуры существующего объекта (таблицы, индекса и т.д.); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees; `ADD` — идентификатор (имя столбца, таблицы или переменной); `CONSTRAINT` — идентификатор (имя столбца, таблицы или переменной); `check_age` — идентификатор (имя столбца, таблицы или переменной); `CHECK` — проверка условия для каждой строки (например, CHECK (age >= 18)); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `=` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [{"message": "✅ Структура таблицы изменена"}],
        'category': 'CONSTRAINT',
        'difficulty': 1,
        'keywords': 'ограничение constraint целостность данных'
    }
,
    {
        'question': 'Как найти строки по шаблону?',
        'answer': 'WHERE фильтрует строки по заданному условию. Возвращаются только строки, для которых условие истинно.',
        'sql_example': 'SELECT * FROM employees WHERE age > 18;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees; `WHERE` — условие фильтрации строк (остаются только те, для которых условие истинно); `age` — столбец \'age\' из таблицы \'employees\'; `>` — оператор сравнения; `18` — число',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'WHERE',
        'difficulty': 3,
        'keywords': 'фильтр условие отфильтровать'
    }
,
    {
        'question': 'Как выдать привилегии пользователю?',
        'answer': 'GRANT выдаёт привилегии пользователям. REVOKE отзывает привилегии.',
        'sql_example': 'GRANT SELECT ON employees TO \'user\'@\'localhost\';',
        'code_explanation': 'Строка: `GRANT` — выдача прав доступа пользователю или роли (команда безопасности); `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `ON` — условие, по которому соединяются таблицы в JOIN; `employees` — таблица employees — содержит данные о employees; `TO` — указывает, кому выдаются или отзываются права доступа; `\'user\'` — строковое значение; `\'localhost\'` — строковое значение',
        'table_structure': [],
        'sample_result': [{"message": "✅ Права выданы"}],
        'category': 'GRANT',
        'difficulty': 3,
        'keywords': 'права доступа привилегии доступ'
    }
,
    {
        'question': 'Как выбрать конкретные столбцы из таблицы получить запросить?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 2,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как выбрать все данные из таблицы запросить запросить?',
        'answer': 'SELECT используется для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные, добавлять условия, сортировку и группировку.',
        'sql_example': 'SELECT * FROM employees;',
        'code_explanation': 'Строка: `SELECT` — команда для выборки данных из таблицы. Можно выбирать все столбцы (*) или конкретные; `*` — звёздочка — означает \'все столбцы\' таблицы; `FROM` — указывает таблицу, из которой берутся данные; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [{"name": "employees", "columns": ["id", "name", "age", "salary", "department", "position", "hire_date"], "sample_rows": [[1, "Иван Петров", 30, 75000, "IT", "Разработчик", "2020-01-15"], [2, "Мария Сидорова", 28, 80000, "IT", "Старший разработчик", "2019-03-10"], [3, "Алексей Иванов", 35, 90000, "IT", "Team Lead", "2018-06-20"], [4, "Елена Смирнова", 25, 65000, "HR", "HR-менеджер", "2021-02-01"], [5, "Дмитрий Козлов", 40, 85000, "Sales", "Менеджер по продажам", "2017-11-11"]]}],
        'sample_result': [],
        'category': 'SELECT',
        'difficulty': 1,
        'keywords': 'выбрать получить извлечь'
    }
,
    {
        'question': 'Как использовать DROP TABLE?',
        'answer': 'DROP TABLE удаляет таблицу из базы данных вместе со всеми данными. Операция необратима.',
        'sql_example': 'DROP TABLE employees;',
        'code_explanation': 'Строка: `DROP` — удаление объекта из базы данных (необратимо!); `TABLE` — таблица — основная структура для хранения данных в реляционной БД; `employees` — таблица employees — содержит данные о employees',
        'table_structure': [],
        'sample_result': [{"message": "✅ Таблица удалена"}],
        'category': 'DROP',
        'difficulty': 3,
        'keywords': 'удалить таблицу drop удаление таблицы'
    }
,

    # ============================================================
    # INSERT (дополнительно - 20 вопросов)
    # ============================================================
    {
        "question": "Как вставить данные в таблицу в SQL?",
        "answer": "INSERT INTO добавляет новую строку в таблицу. Можно указать столбцы или вставить значения для всех столбцов.",
        "sql_example": "INSERT INTO employees (name, age) VALUES ('Иван', 30);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 1,
        "keywords": "insert добавить вставить данные"
    },
    {
        "question": "Как вставить несколько строк в таблицу за один запрос?",
        "answer": "Можно добавить несколько строк за один INSERT, перечислив несколько наборов значений через запятую после VALUES.",
        "sql_example": "INSERT INTO employees (name, age) VALUES ('Иван', 30), ('Мария', 28), ('Алексей', 35);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 3 строки добавлены"}],
        "category": "INSERT",
        "difficulty": 2,
        "keywords": "insert несколько строк массовый"
    },
    {
        "question": "Как вставить данные из одной таблицы в другую?",
        "answer": "INSERT INTO SELECT копирует данные из одной таблицы в другую. Структура столбцов должна совпадать.",
        "sql_example": "INSERT INTO employees_backup (name, age) SELECT name, age FROM employees WHERE department = 'IT';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 3 строки скопированы"}],
        "category": "INSERT",
        "difficulty": 2,
        "keywords": "insert select копирование"
    },
    {
        "question": "Как использовать INSERT с RETURNING в PostgreSQL?",
        "answer": "RETURNING возвращает вставленные данные. Полезно для получения сгенерированного ID.",
        "sql_example": "INSERT INTO employees (name, age) VALUES ('Иван', 30) RETURNING id;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"id": 11, "message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 3,
        "keywords": "insert returning получить id"
    },
    {
        "question": "Как использовать DEFAULT в INSERT?",
        "answer": "DEFAULT вставляет значение по умолчанию для столбца (если оно задано в структуре таблицы).",
        "sql_example": "INSERT INTO employees (name, salary) VALUES ('Иван', DEFAULT);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 2,
        "keywords": "insert default значение по умолчанию"
    },
    {
        "question": "Как вставить данные в конкретные столбцы таблицы?",
        "answer": "Перечислите нужные столбцы в INSERT INTO. Значения подставляются в том же порядке.",
        "sql_example": "INSERT INTO employees (name, department) VALUES ('Иван', 'IT');",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 1,
        "keywords": "insert конкретные столбцы"
    },
    {
        "question": "Как вставить данные без указания столбцов?",
        "answer": "Можно не перечислять столбцы, но тогда значения должны соответствовать ВСЕМ столбцам таблицы по порядку.",
        "sql_example": "INSERT INTO employees VALUES (11, 'Иван', 30, 75000, 'IT', 'Разработчик', '2024-01-01');",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 1,
        "keywords": "insert все столбцы без указания"
    },
    {
        "question": "Как добавить запись в таблицу с автоматически увеличивающимся ID?",
        "answer": "Просто не указывайте поле ID (первичный ключ с AUTO_INCREMENT) — база данных подставит следующее значение.",
        "sql_example": "INSERT INTO employees (name, age) VALUES ('Иван', 30);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 1,
        "keywords": "insert auto_increment id"
    },
    {
        "question": "Как вставить данные с ON CONFLICT (UPSERT) в PostgreSQL?",
        "answer": "ON CONFLICT позволяет обновить запись, если она уже существует, или вставить новую.",
        "sql_example": "INSERT INTO employees (id, name) VALUES (1, 'Иван') ON CONFLICT (id) DO UPDATE SET name = 'Иван';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена или обновлена"}],
        "category": "INSERT",
        "difficulty": 3,
        "keywords": "insert on conflict upsert"
    },
    {
        "question": "Как вставить данные с игнорированием дубликатов в MySQL?",
        "answer": "INSERT IGNORE пропускает строки, которые нарушают уникальность (например, дубликат первичного ключа).",
        "sql_example": "INSERT IGNORE INTO employees (id, name) VALUES (1, 'Иван');",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена или пропущена"}],
        "category": "INSERT",
        "difficulty": 3,
        "keywords": "insert ignore дубликаты"
    },
    {
        "question": "Как вставить данные с использованием подзапроса?",
        "answer": "В VALUES можно использовать подзапрос, возвращающий одно значение.",
        "sql_example": "INSERT INTO employees (name, department) VALUES ((SELECT name FROM temp WHERE id = 1), 'IT');",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 3,
        "keywords": "insert подзапрос values"
    },
    {
        "question": "Как вставить NULL в столбец?",
        "answer": "Просто укажите NULL в VALUES. Убедитесь, что столбец допускает NULL (нет ограничения NOT NULL).",
        "sql_example": "INSERT INTO employees (name, department) VALUES ('Иван', NULL);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 1,
        "keywords": "insert null пустое значение"
    },
    {
        "question": "Как добавить запись с текущей датой?",
        "answer": "Используйте функцию NOW() или CURRENT_DATE для вставки текущей даты и времени.",
        "sql_example": "INSERT INTO employees (name, hire_date) VALUES ('Иван', NOW());",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 2,
        "keywords": "insert now дата текущая"
    },
    {
        "question": "Как вставить данные в таблицу из CSV?",
        "answer": "В большинстве СУБД есть команда LOAD DATA INFILE для импорта из CSV. В SQLite используется .import.",
        "sql_example": "LOAD DATA INFILE 'data.csv' INTO TABLE employees FIELDS TERMINATED BY ',';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Данные импортированы"}],
        "category": "INSERT",
        "difficulty": 3,
        "keywords": "insert csv импорт load data"
    },
    {
        "question": "Как вставить данные с использованием переменных?",
        "answer": "В SQL можно использовать переменные (например, SET @name = 'Иван') и подставлять их в INSERT.",
        "sql_example": "SET @name = 'Иван'; INSERT INTO employees (name) VALUES (@name);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 2,
        "keywords": "insert переменные set"
    },
    {
        "question": "Как добавить запись с вычисляемым значением?",
        "answer": "В VALUES можно использовать арифметические выражения и функции.",
        "sql_example": "INSERT INTO employees (name, salary) VALUES ('Иван', 50000 + 10000);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 2,
        "keywords": "insert вычисляемое значение"
    },
    {
        "question": "Как добавить запись с данными из другой БД?",
        "answer": "Используйте полное имя таблицы: БД.Таблица. Например: INSERT INTO local_table SELECT * FROM remote_db.remote_table;",
        "sql_example": "INSERT INTO employees SELECT * FROM backup_db.employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Данные скопированы"}],
        "category": "INSERT",
        "difficulty": 3,
        "keywords": "insert другая база данных"
    },
    {
        "question": "Как вставить данные с проверкой условий?",
        "answer": "Можно использовать INSERT ... WHERE с подзапросом для проверки условий перед вставкой.",
        "sql_example": "INSERT INTO employees (name, department) SELECT 'Иван', 'IT' WHERE NOT EXISTS (SELECT 1 FROM employees WHERE name = 'Иван');",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 3,
        "keywords": "insert where условие"
    },
    {
        "question": "Как добавить запись с использованием VALUES и SELECT одновременно?",
        "answer": "В INSERT можно комбинировать VALUES и SELECT через UNION.",
        "sql_example": "INSERT INTO employees (name) SELECT 'Иван' UNION SELECT 'Мария' UNION SELECT 'Алексей';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 3 строки добавлены"}],
        "category": "INSERT",
        "difficulty": 2,
        "keywords": "insert values select union"
    },
    {
        "question": "Как вставить данные с кавычками внутри строки?",
        "answer": "Экранируйте кавычки двойной кавычкой (''). Например: 'Иван''s'.",
        "sql_example": "INSERT INTO employees (name) VALUES ('Иван''s');",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 2,
        "keywords": "insert кавычки экранирование"
    },
    {
        "question": "Как вставить данные с CONCAT для объединения строк?",
        "answer": "Используйте CONCAT для объединения нескольких строк в одно значение.",
        "sql_example": "INSERT INTO employees (name) VALUES (CONCAT('Иван', ' ', 'Петров'));",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка добавлена"}],
        "category": "INSERT",
        "difficulty": 2,
        "keywords": "insert concat объединить строки"
    },

    # ============================================================
    # SELECT (дополнительно - 20 вопросов)
    # ============================================================
    {
        "question": "Как выбрать данные с условием LIKE в SQL?",
        "answer": "LIKE используется для поиска по шаблону. % — любое количество символов, _ — ровно один символ.",
        "sql_example": "SELECT * FROM employees WHERE name LIKE 'И%';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров"}, {"name": "Иван Иванов"}],
        "category": "SELECT",
        "difficulty": 2,
        "keywords": "select like поиск шаблон"
    },
    {
        "question": "Как выбрать данные с условием BETWEEN?",
        "answer": "BETWEEN выбирает значения в указанном диапазоне (включая границы).",
        "sql_example": "SELECT * FROM employees WHERE salary BETWEEN 50000 AND 80000;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "salary": 75000}],
        "category": "SELECT",
        "difficulty": 2,
        "keywords": "select between диапазон"
    },
    {
        "question": "Как выбрать данные с условием IN?",
        "answer": "IN проверяет, входит ли значение в список. Это сокращение для нескольких условий OR.",
        "sql_example": "SELECT * FROM employees WHERE department IN ('IT', 'Sales');",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "department": "IT"}],
        "category": "SELECT",
        "difficulty": 2,
        "keywords": "select in список значений"
    },
    {
        "question": "Как выбрать данные с условием IS NULL?",
        "answer": "IS NULL проверяет, что значение отсутствует (NULL).",
        "sql_example": "SELECT * FROM employees WHERE department IS NULL;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сотрудник без отдела"}],
        "category": "SELECT",
        "difficulty": 2,
        "keywords": "select is null"
    },
    {
        "question": "Как выбрать данные с условием IS NOT NULL?",
        "answer": "IS NOT NULL проверяет, что значение присутствует (не NULL).",
        "sql_example": "SELECT * FROM employees WHERE department IS NOT NULL;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "department": "IT"}],
        "category": "SELECT",
        "difficulty": 2,
        "keywords": "select is not null"
    },
    {
        "question": "Как выбрать данные с псевдонимом столбца?",
        "answer": "Используйте AS для задания псевдонима (алиаса) столбцу в результате запроса.",
        "sql_example": "SELECT name AS 'Имя сотрудника', salary AS 'Зарплата' FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"Имя сотрудника": "Иван Петров", "Зарплата": 75000}],
        "category": "SELECT",
        "difficulty": 1,
        "keywords": "select as псевдоним алиас"
    },
    {
        "question": "Как выбрать данные с псевдонимом таблицы?",
        "answer": "Используйте сокращённое имя таблицы (алиас) для упрощения запроса.",
        "sql_example": "SELECT e.name FROM employees e WHERE e.department = 'IT';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров"}],
        "category": "SELECT",
        "difficulty": 1,
        "keywords": "select псевдоним таблицы алиас"
    },
    {
        "question": "Как выбрать данные с функцией COALESCE?",
        "answer": "COALESCE возвращает первое не-NULL значение из списка. Полезно для замены NULL на значение по умолчанию.",
        "sql_example": "SELECT name, COALESCE(department, 'Без отдела') AS department FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "department": "IT"}],
        "category": "SELECT",
        "difficulty": 2,
        "keywords": "select coalesce null замена"
    },
    {
        "question": "Как выбрать данные с функцией NULLIF?",
        "answer": "NULLIF возвращает NULL, если два аргумента равны. Используется для избежания деления на ноль.",
        "sql_example": "SELECT name, salary / NULLIF(experience, 0) AS salary_per_year FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "salary_per_year": 75000}],
        "category": "SELECT",
        "difficulty": 3,
        "keywords": "select nullif деление на ноль"
    },
    {
        "question": "Как выбрать данные с функцией CONCAT?",
        "answer": "CONCAT объединяет несколько строк в одну.",
        "sql_example": "SELECT CONCAT(name, ' (', department, ')') AS employee_info FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"employee_info": "Иван Петров (IT)"}],
        "category": "SELECT",
        "difficulty": 2,
        "keywords": "select concat объединить строки"
    },
    {
        "question": "Как выбрать данные с функцией SUBSTRING?",
        "answer": "SUBSTRING извлекает подстроку из строки (указывается начальная позиция и длина).",
        "sql_example": "SELECT name, SUBSTRING(name, 1, 1) AS first_letter FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "first_letter": "И"}],
        "category": "SELECT",
        "difficulty": 2,
        "keywords": "select substring подстрока"
    },
    {
        "question": "Как выбрать данные с функцией LENGTH?",
        "answer": "LENGTH возвращает длину строки в символах.",
        "sql_example": "SELECT name, LENGTH(name) AS name_length FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "name_length": 11}],
        "category": "SELECT",
        "difficulty": 2,
        "keywords": "select length длина строки"
    },
    {
        "question": "Как выбрать данные с функцией UPPER или LOWER?",
        "answer": "UPPER преобразует строку в верхний регистр, LOWER — в нижний.",
        "sql_example": "SELECT name, UPPER(name) AS name_upper FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "name_upper": "ИВАН ПЕТРОВ"}],
        "category": "SELECT",
        "difficulty": 1,
        "keywords": "select upper lower регистр"
    },
    {
        "question": "Как выбрать данные с функцией TRIM?",
        "answer": "TRIM удаляет пробелы в начале и конце строки.",
        "sql_example": "SELECT TRIM('  Иван Петров  ') AS name_trimmed;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name_trimmed": "Иван Петров"}],
        "category": "SELECT",
        "difficulty": 1,
        "keywords": "select trim пробелы"
    },
    {
        "question": "Как выбрать данные с функцией ROUND?",
        "answer": "ROUND округляет число до указанного количества знаков после запятой.",
        "sql_example": "SELECT name, ROUND(salary, 0) AS rounded_salary FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "rounded_salary": 75000}],
        "category": "SELECT",
        "difficulty": 2,
        "keywords": "select round округление"
    },
    {
        "question": "Как выбрать данные с использованием CASE?",
        "answer": "CASE позволяет создавать условные столбцы (как IF-THEN-ELSE).",
        "sql_example": "SELECT name, salary, CASE WHEN salary > 80000 THEN 'High' WHEN salary > 50000 THEN 'Medium' ELSE 'Low' END AS salary_level FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "salary_level": "Medium"}],
        "category": "SELECT",
        "difficulty": 3,
        "keywords": "select case условие if"
    },
    {
        "question": "Как выбрать данные с использованием подзапроса в SELECT?",
        "answer": "Подзапрос в SELECT возвращает одно значение для каждой строки.",
        "sql_example": "SELECT name, (SELECT AVG(salary) FROM employees) AS avg_salary FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "avg_salary": 80000}],
        "category": "SELECT",
        "difficulty": 3,
        "keywords": "select подзапрос скалярный"
    },
    {
        "question": "Как выбрать данные с использованием EXISTS?",
        "answer": "EXISTS проверяет, существует ли хотя бы одна строка в подзапросе.",
        "sql_example": "SELECT * FROM departments d WHERE EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"id": 1, "dept_name": "IT"}],
        "category": "SELECT",
        "difficulty": 3,
        "keywords": "select exists подзапрос"
    },
    {
        "question": "Как выбрать данные с использованием ANY?",
        "answer": "ANY — истина, если условие выполняется хотя бы для одного значения в списке.",
        "sql_example": "SELECT name, salary FROM employees WHERE salary > ANY (SELECT salary FROM employees WHERE department = 'IT');",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "salary": 75000}],
        "category": "SELECT",
        "difficulty": 3,
        "keywords": "select any подзапрос"
    },
    {
        "question": "Как выбрать данные с использованием ALL?",
        "answer": "ALL — истина, если условие выполняется для всех значений в списке.",
        "sql_example": "SELECT name, salary FROM employees WHERE salary > ALL (SELECT salary FROM employees WHERE department = 'IT');",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "salary": 95000}],
        "category": "SELECT",
        "difficulty": 3,
        "keywords": "select all подзапрос"
    },

    # ============================================================
    # UPDATE (дополнительно - 10 вопросов)
    # ============================================================
    {
        "question": "Как обновить данные в таблице SQL?",
        "answer": "UPDATE изменяет существующие строки. ВСЕГДА используйте WHERE, чтобы не обновить все строки!",
        "sql_example": "UPDATE employees SET salary = 50000 WHERE name = 'Иван';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка обновлена"}],
        "category": "UPDATE",
        "difficulty": 2,
        "keywords": "update обновить изменить"
    },
    {
        "question": "Как обновить несколько столбцов в таблице?",
        "answer": "Перечислите столбцы через запятую после SET.",
        "sql_example": "UPDATE employees SET salary = 80000, position = 'Senior Developer' WHERE name = 'Иван';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка обновлена"}],
        "category": "UPDATE",
        "difficulty": 2,
        "keywords": "update несколько столбцов"
    },
    {
        "question": "Как обновить данные с использованием данных из другой таблицы?",
        "answer": "Используйте UPDATE с JOIN или подзапрос для обновления на основе значений из другой таблицы.",
        "sql_example": "UPDATE employees SET salary = salary * 1.1 WHERE department IN (SELECT dept_name FROM departments WHERE budget > 300000);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 3 строки обновлены"}],
        "category": "UPDATE",
        "difficulty": 3,
        "keywords": "update join подзапрос"
    },
    {
        "question": "Как обновить все строки в таблице?",
        "answer": "Без WHERE обновляются все строки. Используйте с осторожностью!",
        "sql_example": "UPDATE employees SET bonus = 0;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Все строки обновлены"}],
        "category": "UPDATE",
        "difficulty": 1,
        "keywords": "update все строки"
    },
    {
        "question": "Как обновить данные с ограничением количества строк?",
        "answer": "В некоторых СУБД можно использовать LIMIT для ограничения количества обновляемых строк.",
        "sql_example": "UPDATE employees SET salary = 50000 WHERE department = 'IT' LIMIT 5;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 5 строк обновлены"}],
        "category": "UPDATE",
        "difficulty": 3,
        "keywords": "update limit ограничить"
    },
    {
        "question": "Как обновить данные с использованием вычисляемого значения?",
        "answer": "В SET можно использовать арифметические выражения.",
        "sql_example": "UPDATE employees SET salary = salary * 1.1 WHERE department = 'IT';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 3 строки обновлены"}],
        "category": "UPDATE",
        "difficulty": 2,
        "keywords": "update вычисляемое значение"
    },
    {
        "question": "Как обновить данные с использованием текущей даты?",
        "answer": "Используйте NOW() или CURRENT_DATE для установки текущей даты.",
        "sql_example": "UPDATE employees SET hire_date = NOW() WHERE name = 'Иван';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка обновлена"}],
        "category": "UPDATE",
        "difficulty": 2,
        "keywords": "update now дата"
    },
    {
        "question": "Как обновить данные с проверкой условий?",
        "answer": "Используйте WHERE с несколькими условиями для точного обновления.",
        "sql_example": "UPDATE employees SET salary = 70000 WHERE department = 'IT' AND age > 30;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка обновлена"}],
        "category": "UPDATE",
        "difficulty": 2,
        "keywords": "update where условия"
    },
    {
        "question": "Как обновить данные с использованием подзапроса в SET?",
        "answer": "В SET можно использовать подзапрос, возвращающий одно значение.",
        "sql_example": "UPDATE employees SET salary = (SELECT AVG(salary) FROM employees) WHERE department = 'IT';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 3 строки обновлены"}],
        "category": "UPDATE",
        "difficulty": 3,
        "keywords": "update подзапрос set"
    },
    {
        "question": "Как обновить данные с использованием DEFAULT?",
        "answer": "Установите столбец в значение по умолчанию с помощью DEFAULT.",
        "sql_example": "UPDATE employees SET department = DEFAULT WHERE name = 'Иван';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка обновлена"}],
        "category": "UPDATE",
        "difficulty": 2,
        "keywords": "update default значение по умолчанию"
    },

    # ============================================================
    # DELETE (дополнительно - 10 вопросов)
    # ============================================================
    {
        "question": "Как удалить данные из таблицы в SQL?",
        "answer": "DELETE FROM удаляет строки по условию. Без WHERE удаляются все строки!",
        "sql_example": "DELETE FROM employees WHERE name = 'Иван';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка удалена"}],
        "category": "DELETE",
        "difficulty": 2,
        "keywords": "delete удалить данные"
    },
    {
        "question": "Как удалить все строки из таблицы?",
        "answer": "DELETE FROM без WHERE удаляет все строки. Для быстрого удаления используйте TRUNCATE.",
        "sql_example": "DELETE FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Все строки удалены"}],
        "category": "DELETE",
        "difficulty": 1,
        "keywords": "delete все строки"
    },
    {
        "question": "Как удалить строки с использованием подзапроса?",
        "answer": "DELETE с подзапросом позволяет удалять строки на основе условий из другой таблицы.",
        "sql_example": "DELETE FROM employees WHERE department IN (SELECT dept_name FROM departments WHERE budget < 200000);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 2 строки удалены"}],
        "category": "DELETE",
        "difficulty": 3,
        "keywords": "delete подзапрос"
    },
    {
        "question": "Как удалить строки с ограничением количества?",
        "answer": "В некоторых СУБД можно использовать LIMIT для ограничения количества удаляемых строк.",
        "sql_example": "DELETE FROM employees WHERE department = 'IT' LIMIT 2;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 2 строки удалены"}],
        "category": "DELETE",
        "difficulty": 3,
        "keywords": "delete limit ограничить"
    },
    {
        "question": "Как удалить строки с условием на дату?",
        "answer": "Используйте WHERE с условием на дату для удаления старых записей.",
        "sql_example": "DELETE FROM employees WHERE hire_date < '2020-01-01';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 2 строки удалены"}],
        "category": "DELETE",
        "difficulty": 2,
        "keywords": "delete дата условие"
    },
    {
        "question": "Как удалить строки с несколькими условиями?",
        "answer": "Используйте AND и OR для комбинирования условий в WHERE.",
        "sql_example": "DELETE FROM employees WHERE department = 'IT' AND age > 30;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 1 строка удалена"}],
        "category": "DELETE",
        "difficulty": 2,
        "keywords": "delete условия and or"
    },
    {
        "question": "Как удалить строки с использованием EXISTS?",
        "answer": "EXISTS проверяет наличие связанных записей в другой таблице.",
        "sql_example": "DELETE FROM employees e WHERE EXISTS (SELECT 1 FROM departments d WHERE d.id = e.dept_id AND d.budget < 200000);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 2 строки удалены"}],
        "category": "DELETE",
        "difficulty": 3,
        "keywords": "delete exists"
    },
    {
        "question": "Как удалить данные с каскадным удалением?",
        "answer": "При создании FOREIGN KEY можно указать ON DELETE CASCADE — тогда при удалении записи удалятся связанные.",
        "sql_example": "-- Создание таблицы с каскадным удалением\nCREATE TABLE orders (id INT, employee_id INT, FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Связанные записи удалены"}],
        "category": "DELETE",
        "difficulty": 3,
        "keywords": "delete cascade каскадное удаление"
    },
    {
        "question": "В чем разница между DELETE и TRUNCATE?",
        "answer": "DELETE удаляет строки по условию (можно откатить через ROLLBACK). TRUNCATE удаляет все строки, быстрее, но не может быть откачен в некоторых СУБД.",
        "sql_example": "TRUNCATE TABLE employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Таблица очищена"}],
        "category": "DELETE",
        "difficulty": 2,
        "keywords": "delete truncate отличие"
    },
    {
        "question": "Как удалить дубликаты из таблицы?",
        "answer": "Используйте DELETE с подзапросом для удаления дубликатов, оставляя одну запись.",
        "sql_example": "DELETE FROM employees WHERE id NOT IN (SELECT MIN(id) FROM employees GROUP BY name);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Дубликаты удалены"}],
        "category": "DELETE",
        "difficulty": 3,
        "keywords": "delete дубликаты уникальные"
    },

    # ============================================================
    # SUBQUERY (подзапросы) - 20 вопросов
    # ============================================================
    {
        "question": "Что такое подзапрос в SQL?",
        "answer": "Подзапрос (subquery) — это запрос внутри другого запроса. Может возвращать одно значение, список или таблицу.",
        "sql_example": "SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Алексей Иванов", "salary": 90000}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "подзапрос subquery вложенный"
    },
    {
        "question": "Как использовать подзапрос в WHERE?",
        "answer": "Подзапрос в WHERE используется для фильтрации строк на основе результата подзапроса.",
        "sql_example": "SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Алексей Иванов", "salary": 90000}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "подзапрос where фильтрация"
    },
    {
        "question": "Как использовать подзапрос в FROM?",
        "answer": "Подзапрос в FROM используется как производная таблица (derived table).",
        "sql_example": "SELECT * FROM (SELECT * FROM employees WHERE department = 'IT') AS it_employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "department": "IT"}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "подзапрос from производная таблица"
    },
    {
        "question": "Как использовать подзапрос в SELECT?",
        "answer": "Подзапрос в SELECT возвращает одно значение для каждой строки (скалярный подзапрос).",
        "sql_example": "SELECT name, (SELECT AVG(salary) FROM employees) AS avg_salary FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "avg_salary": 80000}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "подзапрос select скалярный"
    },
    {
        "question": "Как использовать коррелированный подзапрос?",
        "answer": "Коррелированный подзапрос ссылается на столбец из внешнего запроса и выполняется для каждой строки.",
        "sql_example": "SELECT name, (SELECT dept_name FROM departments WHERE id = e.dept_id) FROM employees e;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "dept_name": "IT"}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "коррелированный подзапрос"
    },
    {
        "question": "Как использовать EXISTS с подзапросом?",
        "answer": "EXISTS проверяет, существует ли хотя бы одна строка в подзапросе. Возвращает TRUE или FALSE.",
        "sql_example": "SELECT * FROM departments d WHERE EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"id": 1, "dept_name": "IT"}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "exists подзапрос существует"
    },
    {
        "question": "Как использовать NOT EXISTS с подзапросом?",
        "answer": "NOT EXISTS проверяет, что в подзапросе нет ни одной строки.",
        "sql_example": "SELECT * FROM departments d WHERE NOT EXISTS (SELECT 1 FROM employees e WHERE e.dept_id = d.id);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"id": 5, "dept_name": "Finance"}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "not exists отсутствие"
    },
    {
        "question": "Как использовать подзапрос с IN?",
        "answer": "IN с подзапросом проверяет, входит ли значение в результат подзапроса.",
        "sql_example": "SELECT * FROM employees WHERE department IN (SELECT dept_name FROM departments WHERE budget > 300000);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "department": "IT"}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "in подзапрос список"
    },
    {
        "question": "Как использовать подзапрос с ANY?",
        "answer": "ANY — истина, если условие выполняется хотя бы для одного значения из подзапроса.",
        "sql_example": "SELECT * FROM employees WHERE salary > ANY (SELECT salary FROM employees WHERE department = 'IT');",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "salary": 95000}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "any подзапрос"
    },
    {
        "question": "Как использовать подзапрос с ALL?",
        "answer": "ALL — истина, если условие выполняется для всех значений из подзапроса.",
        "sql_example": "SELECT * FROM employees WHERE salary > ALL (SELECT salary FROM employees WHERE department = 'IT');",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "salary": 95000}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "all подзапрос"
    },
    {
        "question": "Как использовать подзапрос в HAVING?",
        "answer": "Подзапрос в HAVING фильтрует группы после GROUP BY.",
        "sql_example": "SELECT department, AVG(salary) FROM employees GROUP BY department HAVING AVG(salary) > (SELECT AVG(salary) FROM employees);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"department": "Sales", "avg_salary": 90000}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "having подзапрос"
    },
    {
        "question": "Как использовать скалярный подзапрос?",
        "answer": "Скалярный подзапрос возвращает одно значение (одну строку и один столбец).",
        "sql_example": "SELECT name, (SELECT COUNT(*) FROM employees) AS total_employees FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "total_employees": 10}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "скалярный подзапрос одно значение"
    },
    {
        "question": "Как использовать подзапрос с UNION?",
        "answer": "Подзапрос может возвращать результаты для UNION с другим запросом.",
        "sql_example": "SELECT name FROM employees UNION SELECT dept_name FROM departments;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров"}, {"name": "IT"}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "union подзапрос"
    },
    {
        "question": "Как использовать подзапрос с агрегатной функцией?",
        "answer": "Подзапросы часто используются с агрегатными функциями для сравнения с итоговыми значениями.",
        "sql_example": "SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Алексей Иванов", "salary": 90000}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "подзапрос агрегатная функция"
    },
    {
        "question": "Как использовать подзапрос с CASE?",
        "answer": "Подзапрос может использоваться внутри CASE для условной логики.",
        "sql_example": "SELECT name, CASE WHEN salary > (SELECT AVG(salary) FROM employees) THEN 'High' ELSE 'Low' END AS salary_level FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "salary_level": "Low"}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "case подзапрос условие"
    },
    {
        "question": "Как использовать подзапрос в ORDER BY?",
        "answer": "Подзапрос в ORDER BY позволяет сортировать по вычисляемому значению.",
        "sql_example": "SELECT * FROM employees ORDER BY (SELECT AVG(salary) FROM employees) - salary;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "salary": 95000}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "order by подзапрос"
    },
    {
        "question": "Как использовать подзапрос с LIMIT?",
        "answer": "Подзапрос с LIMIT позволяет получить ограниченное количество значений.",
        "sql_example": "SELECT * FROM employees WHERE salary IN (SELECT salary FROM employees ORDER BY salary DESC LIMIT 3);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "salary": 95000}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "limit подзапрос"
    },
    {
        "question": "Как использовать вложенные подзапросы?",
        "answer": "Подзапросы могут быть вложенными друг в друга (подзапрос внутри подзапроса).",
        "sql_example": "SELECT * FROM employees WHERE salary > (SELECT AVG(salary) FROM employees WHERE department IN (SELECT dept_name FROM departments WHERE budget > 300000));",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "salary": 95000}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "вложенный подзапрос"
    },
    {
        "question": "Как использовать подзапрос с GROUP BY?",
        "answer": "Подзапрос может быть частью GROUP BY для группировки по вычисляемому значению.",
        "sql_example": "SELECT department, COUNT(*) FROM employees GROUP BY department HAVING COUNT(*) > (SELECT AVG(cnt) FROM (SELECT COUNT(*) AS cnt FROM employees GROUP BY department) AS dept_counts);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"department": "IT", "count": 3}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "group by подзапрос"
    },
    {
        "question": "Как использовать подзапрос с DISTINCT?",
        "answer": "Подзапрос с DISTINCT возвращает уникальные значения для внешнего запроса.",
        "sql_example": "SELECT * FROM employees WHERE department IN (SELECT DISTINCT department FROM employees);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "department": "IT"}],
        "category": "SUBQUERY",
        "difficulty": 3,
        "keywords": "distinct подзапрос"
    },

    # ============================================================
    # CREATE (создание) - 10 вопросов
    # ============================================================
    {
        "question": "Как создать таблицу с первичным ключом?",
        "answer": "PRIMARY KEY задаёт уникальный идентификатор для каждой строки. Не может быть NULL.",
        "sql_example": "CREATE TABLE employees (id INT PRIMARY KEY, name TEXT, salary DECIMAL);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Таблица создана"}],
        "category": "CREATE",
        "difficulty": 2,
        "keywords": "create table primary key"
    },
    {
        "question": "Как создать таблицу с внешним ключом?",
        "answer": "FOREIGN KEY создаёт связь с другой таблицей. Обеспечивает целостность данных.",
        "sql_example": "CREATE TABLE orders (id INT, employee_id INT, FOREIGN KEY (employee_id) REFERENCES employees(id));",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Таблица создана"}],
        "category": "CREATE",
        "difficulty": 2,
        "keywords": "create table foreign key"
    },
    {
        "question": "Как создать таблицу с UNIQUE ограничением?",
        "answer": "UNIQUE гарантирует, что все значения в столбце уникальны (не могут повторяться).",
        "sql_example": "CREATE TABLE employees (id INT, email TEXT UNIQUE);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Таблица создана"}],
        "category": "CREATE",
        "difficulty": 2,
        "keywords": "create table unique"
    },
    {
        "question": "Как создать таблицу с NOT NULL ограничением?",
        "answer": "NOT NULL запрещает NULL значения в столбце — значение обязательно должно быть заполнено.",
        "sql_example": "CREATE TABLE employees (id INT, name TEXT NOT NULL);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Таблица создана"}],
        "category": "CREATE",
        "difficulty": 1,
        "keywords": "create table not null"
    },
    {
        "question": "Как создать таблицу с DEFAULT значением?",
        "answer": "DEFAULT задаёт значение по умолчанию для столбца, если оно не указано при вставке.",
        "sql_example": "CREATE TABLE employees (id INT, salary DECIMAL DEFAULT 0);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Таблица создана"}],
        "category": "CREATE",
        "difficulty": 1,
        "keywords": "create table default"
    },
    {
        "question": "Как создать таблицу с CHECK ограничением?",
        "answer": "CHECK проверяет условие для каждой строки. Например, возраст не может быть меньше 18.",
        "sql_example": "CREATE TABLE employees (id INT, age INT CHECK (age >= 18));",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Таблица создана"}],
        "category": "CREATE",
        "difficulty": 2,
        "keywords": "create table check"
    },
    {
        "question": "Как создать временную таблицу?",
        "answer": "CREATE TEMP TABLE создаёт таблицу, которая существует только в течение сессии.",
        "sql_example": "CREATE TEMP TABLE temp_employees AS SELECT * FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Временная таблица создана"}],
        "category": "CREATE",
        "difficulty": 2,
        "keywords": "create temp table временная"
    },
    {
        "question": "Как создать таблицу из результата запроса?",
        "answer": "CREATE TABLE ... AS SELECT ... копирует структуру и данные из результата запроса.",
        "sql_example": "CREATE TABLE it_employees AS SELECT * FROM employees WHERE department = 'IT';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Таблица создана"}],
        "category": "CREATE",
        "difficulty": 2,
        "keywords": "create table as select"
    },
    {
        "question": "Как создать таблицу с составным первичным ключом?",
        "answer": "Составной PRIMARY KEY состоит из нескольких столбцов. Их комбинация должна быть уникальной.",
        "sql_example": "CREATE TABLE orders (employee_id INT, product_id INT, PRIMARY KEY (employee_id, product_id));",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Таблица создана"}],
        "category": "CREATE",
        "difficulty": 2,
        "keywords": "create table составной primary key"
    },
    {
        "question": "Как создать таблицу с AUTO_INCREMENT?",
        "answer": "AUTO_INCREMENT автоматически увеличивает значение столбца при вставке новых строк.",
        "sql_example": "CREATE TABLE employees (id INT AUTO_INCREMENT PRIMARY KEY, name TEXT);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Таблица создана"}],
        "category": "CREATE",
        "difficulty": 2,
        "keywords": "create table auto_increment"
    },

    # ============================================================
    # ALTER TABLE - 10 вопросов
    # ============================================================
    {
        "question": "Как добавить новый столбец в таблицу?",
        "answer": "ALTER TABLE ADD COLUMN добавляет новый столбец в существующую таблицу.",
        "sql_example": "ALTER TABLE employees ADD COLUMN bonus DECIMAL;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Столбец добавлен"}],
        "category": "ALTER",
        "difficulty": 2,
        "keywords": "alter add column добавить столбец"
    },
    {
        "question": "Как удалить столбец из таблицы?",
        "answer": "ALTER TABLE DROP COLUMN удаляет столбец из таблицы. Данные безвозвратно теряются.",
        "sql_example": "ALTER TABLE employees DROP COLUMN bonus;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Столбец удалён"}],
        "category": "ALTER",
        "difficulty": 2,
        "keywords": "alter drop column удалить столбец"
    },
    {
        "question": "Как изменить тип данных столбца?",
        "answer": "ALTER TABLE ALTER COLUMN изменяет тип данных столбца.",
        "sql_example": "ALTER TABLE employees ALTER COLUMN salary TYPE DECIMAL(10,2);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Тип столбца изменён"}],
        "category": "ALTER",
        "difficulty": 2,
        "keywords": "alter type изменить тип"
    },
    {
        "question": "Как переименовать столбец в таблице?",
        "answer": "ALTER TABLE RENAME COLUMN переименовывает столбец.",
        "sql_example": "ALTER TABLE employees RENAME COLUMN position TO job_title;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Столбец переименован"}],
        "category": "ALTER",
        "difficulty": 2,
        "keywords": "alter rename column переименовать"
    },
    {
        "question": "Как добавить ограничение NOT NULL?",
        "answer": "ALTER TABLE ALTER COLUMN SET NOT NULL добавляет ограничение NOT NULL.",
        "sql_example": "ALTER TABLE employees ALTER COLUMN name SET NOT NULL;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Ограничение добавлено"}],
        "category": "ALTER",
        "difficulty": 2,
        "keywords": "alter not null ограничение"
    },
    {
        "question": "Как удалить ограничение NOT NULL?",
        "answer": "ALTER TABLE ALTER COLUMN DROP NOT NULL убирает ограничение NOT NULL.",
        "sql_example": "ALTER TABLE employees ALTER COLUMN name DROP NOT NULL;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Ограничение удалено"}],
        "category": "ALTER",
        "difficulty": 2,
        "keywords": "alter drop not null"
    },
    {
        "question": "Как добавить UNIQUE ограничение?",
        "answer": "ALTER TABLE ADD CONSTRAINT UNIQUE добавляет ограничение уникальности.",
        "sql_example": "ALTER TABLE employees ADD CONSTRAINT unique_email UNIQUE (email);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Ограничение добавлено"}],
        "category": "ALTER",
        "difficulty": 2,
        "keywords": "alter unique ограничение"
    },
    {
        "question": "Как добавить CHECK ограничение?",
        "answer": "ALTER TABLE ADD CONSTRAINT CHECK добавляет проверочное ограничение.",
        "sql_example": "ALTER TABLE employees ADD CONSTRAINT check_age CHECK (age >= 18);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Ограничение добавлено"}],
        "category": "ALTER",
        "difficulty": 2,
        "keywords": "alter check ограничение"
    },
    {
        "question": "Как добавить FOREIGN KEY ограничение?",
        "answer": "ALTER TABLE ADD CONSTRAINT FOREIGN KEY добавляет внешний ключ.",
        "sql_example": "ALTER TABLE orders ADD CONSTRAINT fk_employee FOREIGN KEY (employee_id) REFERENCES employees(id);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Внешний ключ добавлен"}],
        "category": "ALTER",
        "difficulty": 2,
        "keywords": "alter foreign key внешний ключ"
    },
    {
        "question": "Как переименовать таблицу?",
        "answer": "ALTER TABLE RENAME переименовывает таблицу.",
        "sql_example": "ALTER TABLE employees RENAME TO staff;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Таблица переименована"}],
        "category": "ALTER",
        "difficulty": 2,
        "keywords": "alter rename таблица переименовать"
    },

    # ============================================================
    # WINDOW FUNCTIONS - 10 вопросов
    # ============================================================
    {
        "question": "Что такое оконные функции в SQL?",
        "answer": "Оконные функции выполняют вычисления по набору строк, связанных с текущей строкой, не сводя результат в одну группу.",
        "sql_example": "SELECT name, department, salary, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank_in_dept FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Алексей Иванов", "rank_in_dept": 1}],
        "category": "WINDOW",
        "difficulty": 3,
        "keywords": "оконная функция window over"
    },
    {
        "question": "Как использовать ROW_NUMBER() в SQL?",
        "answer": "ROW_NUMBER() присваивает уникальный номер каждой строке в пределах раздела.",
        "sql_example": "SELECT name, ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "row_num": 1}],
        "category": "WINDOW",
        "difficulty": 3,
        "keywords": "row_number нумерация оконная"
    },
    {
        "question": "Как использовать RANK() в SQL?",
        "answer": "RANK() присваивает ранг с пропусками при одинаковых значениях (1,2,2,4).",
        "sql_example": "SELECT name, salary, RANK() OVER (ORDER BY salary DESC) as rank FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "rank": 1}],
        "category": "WINDOW",
        "difficulty": 3,
        "keywords": "rank ранг оконная"
    },
    {
        "question": "Как использовать DENSE_RANK() в SQL?",
        "answer": "DENSE_RANK() присваивает ранг без пропусков (1,2,2,3).",
        "sql_example": "SELECT name, salary, DENSE_RANK() OVER (ORDER BY salary DESC) as dense_rank FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "dense_rank": 1}],
        "category": "WINDOW",
        "difficulty": 3,
        "keywords": "dense_rank ранг оконная"
    },
    {
        "question": "Как использовать LAG() в SQL?",
        "answer": "LAG() возвращает значение из предыдущей строки в окне.",
        "sql_example": "SELECT name, salary, LAG(salary, 1) OVER (ORDER BY salary) as prev_salary FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "prev_salary": None}],
        "category": "WINDOW",
        "difficulty": 3,
        "keywords": "lag предыдущая строка оконная"
    },
    {
        "question": "Как использовать LEAD() в SQL?",
        "answer": "LEAD() возвращает значение из следующей строки в окне.",
        "sql_example": "SELECT name, salary, LEAD(salary, 1) OVER (ORDER BY salary) as next_salary FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "next_salary": 80000}],
        "category": "WINDOW",
        "difficulty": 3,
        "keywords": "lead следующая строка оконная"
    },
    {
        "question": "Как использовать FIRST_VALUE() в SQL?",
        "answer": "FIRST_VALUE() возвращает первое значение в окне.",
        "sql_example": "SELECT name, salary, FIRST_VALUE(salary) OVER (ORDER BY salary) as first_salary FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Елена Смирнова", "first_salary": 65000}],
        "category": "WINDOW",
        "difficulty": 3,
        "keywords": "first_value первое значение оконная"
    },
    {
        "question": "Как использовать LAST_VALUE() в SQL?",
        "answer": "LAST_VALUE() возвращает последнее значение в окне (с учётом фрейма).",
        "sql_example": "SELECT name, salary, LAST_VALUE(salary) OVER (ORDER BY salary ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) as last_salary FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "last_salary": 95000}],
        "category": "WINDOW",
        "difficulty": 3,
        "keywords": "last_value последнее значение оконная"
    },
    {
        "question": "Как использовать NTILE() в SQL?",
        "answer": "NTILE(n) разбивает строки на n приблизительно равных групп (квантилей).",
        "sql_example": "SELECT name, salary, NTILE(4) OVER (ORDER BY salary DESC) as quartile FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "quartile": 1}],
        "category": "WINDOW",
        "difficulty": 3,
        "keywords": "ntile квантиль групповая оконная"
    },
    {
        "question": "Как использовать PARTITION BY в оконных функциях?",
        "answer": "PARTITION BY разбивает окно на группы — оконная функция применяется к каждой группе отдельно.",
        "sql_example": "SELECT name, department, salary, ROW_NUMBER() OVER (PARTITION BY department ORDER BY salary DESC) as rank_in_dept FROM employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Алексей Иванов", "rank_in_dept": 1}],
        "category": "WINDOW",
        "difficulty": 3,
        "keywords": "partition by разделение групп оконная"
    },

    # ============================================================
    # CTE (WITH) - 10 вопросов
    # ============================================================
    {
        "question": "Что такое CTE (Common Table Expression) в SQL?",
        "answer": "CTE — это временное именованное выражение, которое существует только в рамках одного запроса. Упрощает сложные запросы.",
        "sql_example": "WITH dept_stats AS (SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department) SELECT e.name, e.salary, ds.avg_salary FROM employees e JOIN dept_stats ds ON e.department = ds.department;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "avg_salary": 81666.67}],
        "category": "CTE",
        "difficulty": 3,
        "keywords": "cte with общее табличное выражение"
    },
    {
        "question": "Как использовать рекурсивный CTE в SQL?",
        "answer": "Рекурсивный CTE позволяет выполнять итеративные запросы, например, для обхода иерархических структур (деревьев).",
        "sql_example": "WITH RECURSIVE org_tree AS (SELECT id, name, manager_id, 0 as level FROM employees WHERE manager_id IS NULL UNION ALL SELECT e.id, e.name, e.manager_id, ot.level + 1 FROM employees e JOIN org_tree ot ON e.manager_id = ot.id) SELECT * FROM org_tree;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Алексей Иванов", "level": 0}],
        "category": "CTE",
        "difficulty": 3,
        "keywords": "recursive рекурсия иерархия"
    },
    {
        "question": "Как использовать несколько CTE в одном запросе?",
        "answer": "Можно перечислить несколько CTE через запятую после WITH.",
        "sql_example": "WITH dept_avg AS (SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department), dept_count AS (SELECT department, COUNT(*) as emp_count FROM employees GROUP BY department) SELECT * FROM dept_avg JOIN dept_count ON dept_avg.department = dept_count.department;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"department": "IT", "avg_salary": 81666.67, "emp_count": 3}],
        "category": "CTE",
        "difficulty": 3,
        "keywords": "несколько cte with"
    },
    {
        "question": "Как использовать CTE с INSERT?",
        "answer": "CTE можно использовать в INSERT для подготовки данных перед вставкой.",
        "sql_example": "WITH it_employees AS (SELECT * FROM employees WHERE department = 'IT') INSERT INTO employees_backup SELECT * FROM it_employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 3 строки скопированы"}],
        "category": "CTE",
        "difficulty": 3,
        "keywords": "cte insert вставка"
    },
    {
        "question": "Как использовать CTE с UPDATE?",
        "answer": "CTE можно использовать в UPDATE для обновления на основе вычисленных данных.",
        "sql_example": "WITH dept_avg AS (SELECT department, AVG(salary) as avg_salary FROM employees GROUP BY department) UPDATE employees SET salary = dept_avg.avg_salary FROM dept_avg WHERE employees.department = dept_avg.department;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Все строки обновлены"}],
        "category": "CTE",
        "difficulty": 3,
        "keywords": "cte update обновление"
    },
    {
        "question": "Как использовать CTE с DELETE?",
        "answer": "CTE можно использовать в DELETE для удаления на основе вычисленных данных.",
        "sql_example": "WITH dept_to_delete AS (SELECT department FROM departments WHERE budget < 200000) DELETE FROM employees WHERE department IN (SELECT department FROM dept_to_delete);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ 2 строки удалены"}],
        "category": "CTE",
        "difficulty": 3,
        "keywords": "cte delete удаление"
    },
    {
        "question": "Как использовать CTE с UNION?",
        "answer": "CTE можно использовать в UNION для подготовки данных для объединения.",
        "sql_example": "WITH it_employees AS (SELECT name, department FROM employees WHERE department = 'IT'), hr_employees AS (SELECT name, department FROM employees WHERE department = 'HR') SELECT * FROM it_employees UNION SELECT * FROM hr_employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "department": "IT"}],
        "category": "CTE",
        "difficulty": 3,
        "keywords": "cte union объединение"
    },
    {
        "question": "Как использовать CTE с оконными функциями?",
        "answer": "CTE часто используется для подготовки данных перед применением оконных функций.",
        "sql_example": "WITH ranked AS (SELECT name, salary, ROW_NUMBER() OVER (ORDER BY salary DESC) as row_num FROM employees) SELECT * FROM ranked WHERE row_num <= 3;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "row_num": 1}],
        "category": "CTE",
        "difficulty": 3,
        "keywords": "cte оконная функция"
    },
    {
        "question": "Как использовать CTE с агрегатными функциями?",
        "answer": "CTE можно использовать для вычисления агрегатов, которые затем используются в основном запросе.",
        "sql_example": "WITH dept_stats AS (SELECT department, AVG(salary) as avg_salary, MAX(salary) as max_salary FROM employees GROUP BY department) SELECT e.name, e.salary, ds.avg_salary, ds.max_salary FROM employees e JOIN dept_stats ds ON e.department = ds.department;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Иван Петров", "avg_salary": 81666.67}],
        "category": "CTE",
        "difficulty": 3,
        "keywords": "cte агрегатные функции"
    },
    {
        "question": "Как использовать CTE с подзапросами?",
        "answer": "CTE может содержать подзапросы и использоваться как временная таблица для основного запроса.",
        "sql_example": "WITH dept_data AS (SELECT department, (SELECT COUNT(*) FROM employees e WHERE e.department = d.dept_name) as emp_count FROM departments d) SELECT * FROM dept_data WHERE emp_count > 0;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"department": "IT", "emp_count": 3}],
        "category": "CTE",
        "difficulty": 3,
        "keywords": "cte подзапрос"
    },

    # ============================================================
    # GRANT/REVOKE - 5 вопросов
    # ============================================================
    {
        "question": "Как выдать права на SELECT пользователю?",
        "answer": "GRANT SELECT позволяет пользователю читать данные из таблицы.",
        "sql_example": "GRANT SELECT ON employees TO 'user'@'localhost';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Права выданы"}],
        "category": "GRANT",
        "difficulty": 2,
        "keywords": "grant select права"
    },
    {
        "question": "Как выдать права на INSERT пользователю?",
        "answer": "GRANT INSERT позволяет пользователю добавлять данные в таблицу.",
        "sql_example": "GRANT INSERT ON employees TO 'user'@'localhost';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Права выданы"}],
        "category": "GRANT",
        "difficulty": 2,
        "keywords": "grant insert права"
    },
    {
        "question": "Как выдать права на UPDATE пользователю?",
        "answer": "GRANT UPDATE позволяет пользователю обновлять данные в таблице.",
        "sql_example": "GRANT UPDATE ON employees TO 'user'@'localhost';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Права выданы"}],
        "category": "GRANT",
        "difficulty": 2,
        "keywords": "grant update права"
    },
    {
        "question": "Как выдать все права пользователю?",
        "answer": "GRANT ALL PRIVILEGES даёт пользователю все разрешения на таблицу.",
        "sql_example": "GRANT ALL PRIVILEGES ON employees TO 'user'@'localhost';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Все права выданы"}],
        "category": "GRANT",
        "difficulty": 2,
        "keywords": "grant all privileges все права"
    },
    {
        "question": "Как отозвать права пользователя?",
        "answer": "REVOKE отзывает ранее выданные привилегии.",
        "sql_example": "REVOKE INSERT ON employees FROM 'user'@'localhost';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Права отозваны"}],
        "category": "GRANT",
        "difficulty": 2,
        "keywords": "revoke отозвать права"
    },

    # ============================================================
    # TRANSACTION - 5 вопросов
    # ============================================================
    {
        "question": "Как начать транзакцию в SQL?",
        "answer": "BEGIN TRANSACTION или START TRANSACTION начинает новую транзакцию.",
        "sql_example": "BEGIN TRANSACTION;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Транзакция начата"}],
        "category": "TRANSACTION",
        "difficulty": 2,
        "keywords": "begin transaction начать"
    },
    {
        "question": "Как сохранить изменения в транзакции?",
        "answer": "COMMIT сохраняет все изменения, сделанные в транзакции.",
        "sql_example": "BEGIN TRANSACTION; UPDATE employees SET salary = 50000 WHERE id = 1; COMMIT;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Транзакция выполнена"}],
        "category": "TRANSACTION",
        "difficulty": 2,
        "keywords": "commit сохранить транзакция"
    },
    {
        "question": "Как отменить изменения в транзакции?",
        "answer": "ROLLBACK отменяет все изменения, сделанные в текущей транзакции.",
        "sql_example": "BEGIN TRANSACTION; UPDATE employees SET salary = 50000 WHERE id = 1; ROLLBACK;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Транзакция отменена"}],
        "category": "TRANSACTION",
        "difficulty": 2,
        "keywords": "rollback отменить транзакция"
    },
    {
        "question": "Что такое уровни изоляции транзакций?",
        "answer": "Уровни изоляции определяют видимость изменений между транзакциями: READ UNCOMMITTED, READ COMMITTED, REPEATABLE READ, SERIALIZABLE.",
        "sql_example": "SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Уровень изоляции установлен"}],
        "category": "TRANSACTION",
        "difficulty": 3,
        "keywords": "изоляция isolation level"
    },
    {
        "question": "Как использовать SAVEPOINT в транзакции?",
        "answer": "SAVEPOINT создаёт точку сохранения внутри транзакции, к которой можно откатиться с помощью ROLLBACK TO.",
        "sql_example": "BEGIN TRANSACTION; UPDATE employees SET salary = 50000 WHERE id = 1; SAVEPOINT before_update; UPDATE employees SET salary = 60000 WHERE id = 2; ROLLBACK TO before_update; COMMIT;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Транзакция выполнена"}],
        "category": "TRANSACTION",
        "difficulty": 3,
        "keywords": "savepoint точка сохранения"
    },

    # ============================================================
    # TRIGGER (дополнительно) - 5 вопросов
    # ============================================================
    {
        "question": "Как создать триггер BEFORE UPDATE?",
        "answer": "BEFORE UPDATE триггер срабатывает ДО обновления строки.",
        "sql_example": "CREATE TRIGGER before_update_salary BEFORE UPDATE ON employees FOR EACH ROW BEGIN IF NEW.salary < 0 THEN SET NEW.salary = 0; END IF; END;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Триггер создан"}],
        "category": "TRIGGER",
        "difficulty": 3,
        "keywords": "trigger before update"
    },
    {
        "question": "Как создать триггер AFTER INSERT?",
        "answer": "AFTER INSERT триггер срабатывает ПОСЛЕ вставки новой строки.",
        "sql_example": "CREATE TRIGGER after_insert_employee AFTER INSERT ON employees FOR EACH ROW BEGIN INSERT INTO logs (action, employee_id) VALUES ('INSERT', NEW.id); END;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Триггер создан"}],
        "category": "TRIGGER",
        "difficulty": 3,
        "keywords": "trigger after insert"
    },
    {
        "question": "Как создать триггер BEFORE DELETE?",
        "answer": "BEFORE DELETE триггер срабатывает ДО удаления строки.",
        "sql_example": "CREATE TRIGGER before_delete_employee BEFORE DELETE ON employees FOR EACH ROW BEGIN INSERT INTO deleted_employees SELECT * FROM employees WHERE id = OLD.id; END;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Триггер создан"}],
        "category": "TRIGGER",
        "difficulty": 3,
        "keywords": "trigger before delete"
    },
    {
        "question": "Как удалить триггер?",
        "answer": "DROP TRIGGER удаляет существующий триггер.",
        "sql_example": "DROP TRIGGER update_timestamp;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Триггер удалён"}],
        "category": "TRIGGER",
        "difficulty": 2,
        "keywords": "drop trigger удалить"
    },
    {
        "question": "Как создать триггер на несколько операций?",
        "answer": "Можно создать триггер, который срабатывает на INSERT, UPDATE и DELETE одновременно.",
        "sql_example": "CREATE TRIGGER log_changes AFTER INSERT OR UPDATE OR DELETE ON employees FOR EACH ROW BEGIN INSERT INTO logs (action, employee_id) VALUES (CASE WHEN INSERTING THEN 'INSERT' WHEN UPDATING THEN 'UPDATE' WHEN DELETING THEN 'DELETE' END, NEW.id); END;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Триггер создан"}],
        "category": "TRIGGER",
        "difficulty": 3,
        "keywords": "trigger insert update delete"
    },

    # ============================================================
    # VIEW - 5 вопросов
    # ============================================================
    {
        "question": "Как создать представление (VIEW) в SQL?",
        "answer": "CREATE VIEW создаёт виртуальную таблицу на основе запроса. Упрощает сложные запросы.",
        "sql_example": "CREATE VIEW high_salary_employees AS SELECT name, salary FROM employees WHERE salary > 70000;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Представление создано"}],
        "category": "VIEW",
        "difficulty": 2,
        "keywords": "create view представление"
    },
    {
        "question": "Как удалить представление?",
        "answer": "DROP VIEW удаляет представление из базы данных. Исходные таблицы не затрагиваются.",
        "sql_example": "DROP VIEW high_salary_employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Представление удалено"}],
        "category": "VIEW",
        "difficulty": 2,
        "keywords": "drop view удалить представление"
    },
    {
        "question": "Как использовать представление в запросе?",
        "answer": "Представление используется как обычная таблица в SELECT, JOIN и других запросах.",
        "sql_example": "SELECT * FROM high_salary_employees WHERE salary > 80000;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"name": "Сергей Павлов", "salary": 95000}],
        "category": "VIEW",
        "difficulty": 2,
        "keywords": "view select использование"
    },
    {
        "question": "Как создать представление с JOIN?",
        "answer": "Представление может содержать JOIN для объединения данных из нескольких таблиц.",
        "sql_example": "CREATE VIEW employee_dept AS SELECT e.name, d.dept_name FROM employees e JOIN departments d ON e.dept_id = d.id;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Представление создано"}],
        "category": "VIEW",
        "difficulty": 2,
        "keywords": "view join представление"
    },
    {
        "question": "Как создать представление с агрегатными функциями?",
        "answer": "Представление может содержать GROUP BY и агрегатные функции.",
        "sql_example": "CREATE VIEW dept_stats AS SELECT department, COUNT(*) as emp_count, AVG(salary) as avg_salary FROM employees GROUP BY department;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Представление создано"}],
        "category": "VIEW",
        "difficulty": 2,
        "keywords": "view агрегатные функции"
    },

    # ============================================================
    # INDEX - 5 вопросов
    # ============================================================
    {
        "question": "Как создать индекс для ускорения поиска?",
        "answer": "CREATE INDEX создаёт индекс на столбце, ускоряя поиск и сортировку.",
        "sql_example": "CREATE INDEX idx_employees_name ON employees(name);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Индекс создан"}],
        "category": "INDEX",
        "difficulty": 2,
        "keywords": "create index ускорение"
    },
    {
        "question": "Как удалить индекс?",
        "answer": "DROP INDEX удаляет индекс из базы данных.",
        "sql_example": "DROP INDEX idx_employees_name;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Индекс удалён"}],
        "category": "INDEX",
        "difficulty": 2,
        "keywords": "drop index удалить"
    },
    {
        "question": "Как создать составной индекс?",
        "answer": "Составной индекс создаётся на нескольких столбцах и ускоряет запросы по комбинации этих столбцов.",
        "sql_example": "CREATE INDEX idx_emp_dept_salary ON employees(department, salary);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Индекс создан"}],
        "category": "INDEX",
        "difficulty": 2,
        "keywords": "составной индекс несколько столбцов"
    },
    {
        "question": "Как создать уникальный индекс?",
        "answer": "Уникальный индекс гарантирует, что все значения в столбце уникальны.",
        "sql_example": "CREATE UNIQUE INDEX idx_employees_email ON employees(email);",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Индекс создан"}],
        "category": "INDEX",
        "difficulty": 2,
        "keywords": "unique индекс уникальность"
    },
    {
        "question": "Как проверить, используется ли индекс?",
        "answer": "EXPLAIN показывает, используется ли индекс при выполнении запроса.",
        "sql_example": "EXPLAIN SELECT * FROM employees WHERE name = 'Иван';",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ План выполнения"}],
        "category": "INDEX",
        "difficulty": 3,
        "keywords": "explain индекс план"
    },

    # ============================================================
    # DROP - 5 вопросов
    # ============================================================
    {
        "question": "Как удалить таблицу из базы данных?",
        "answer": "DROP TABLE удаляет таблицу и все её данные. Операция необратима!",
        "sql_example": "DROP TABLE employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Таблица удалена"}],
        "category": "DROP",
        "difficulty": 1,
        "keywords": "drop table удалить"
    },
    {
        "question": "Как удалить базу данных?",
        "answer": "DROP DATABASE удаляет всю базу данных со всеми таблицами. Операция необратима!",
        "sql_example": "DROP DATABASE company;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ База данных удалена"}],
        "category": "DROP",
        "difficulty": 2,
        "keywords": "drop database удалить"
    },
    {
        "question": "Чем отличается DROP от DELETE?",
        "answer": "DROP удаляет структуру объекта (таблицы, базы). DELETE удаляет данные, но структура остаётся.",
        "sql_example": "-- DELETE: удаляет строки, таблица остаётся\nDELETE FROM employees;\n-- DROP: удаляет таблицу полностью\nDROP TABLE employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Объект удалён"}],
        "category": "DROP",
        "difficulty": 2,
        "keywords": "drop delete отличие"
    },
    {
        "question": "Как удалить столбец из таблицы?",
        "answer": "ALTER TABLE DROP COLUMN удаляет столбец из таблицы.",
        "sql_example": "ALTER TABLE employees DROP COLUMN bonus;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Столбец удалён"}],
        "category": "ALTER",
        "difficulty": 2,
        "keywords": "drop column удалить столбец"
    },
    {
        "question": "Как удалить представление?",
        "answer": "DROP VIEW удаляет представление из базы данных.",
        "sql_example": "DROP VIEW high_salary_employees;",
        "code_explanation": "",
        "table_structure": [],
        "sample_result": [{"message": "✅ Представление удалено"}],
        "category": "VIEW",
        "difficulty": 2,
        "keywords": "drop view представление удалить"
    },
]



def seed_database():
    """Наполняет базу данных"""
    init_db()
    clear_cache()

    for qa in seed_questions:
        insert_qa_pair(
            question=qa["question"],
            answer=qa["answer"],
            sql_example=qa["sql_example"],
            code_explanation=qa.get("code_explanation", ""),
            table_structure=qa.get("table_structure", []),
            sample_result=qa.get("sample_result", []),
            category=qa["category"],
            difficulty=qa["difficulty"],
            keywords=qa["keywords"]
        )

    print(f"✅ Добавлено 405 вопросов в базу данных")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM qa_pairs")
    count = cursor.fetchone()[0]
    print(f"📊 В базе {count} записей")

    cursor.execute("SELECT category, COUNT(*) FROM qa_pairs GROUP BY category ORDER BY category")
    stats = cursor.fetchall()
    print("\n📈 Статистика по категориям:")
    for cat, cnt in stats:
        print(f"   {cat}: {cnt} вопросов")

    conn.close()


if __name__ == "__main__":
    seed_database()