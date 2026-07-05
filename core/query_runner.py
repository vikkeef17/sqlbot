"""
Модуль живого выполнения SQL-примеров из базы знаний.

Проблема, которую он решает:
раньше table_structure и sample_result для каждой пары вопрос-ответ
были захардкожены вручную в seed_data.py и не всегда совпадали с тем,
что реально вернёт demo.db при выполнении sql_example (несуществующие
колонки, устаревшие данные и т.д.).

Вместо того чтобы вручную подгонять 400+ текстовых примеров под базу,
этот модуль на каждый ответ бота:
  1) определяет, какие таблицы использует запрос;
  2) подставляет их РЕАЛЬНУЮ структуру (колонки + несколько строк) —
     table_structure строится не вручную, а через PRAGMA/интроспекцию demo.db;
  3) пытается реально выполнить запрос в изолированной временной копии
     demo.db (чтобы DDL/DML-примеры не портили общую демо-базу и не
     конфликтовали друг с другом при повторных запусках);
  4) если запрос выполнился — sample_result строится из настоящих
     данных, которые вернула база;
  5) если выполнить нельзя (например, GRANT/PROCEDURE — конструкции,
     которых в SQLite нет в принципе), честно возвращает пометку
     об этом, и бот показывает статический иллюстративный пример.
"""

import os
import re
import shutil
import sqlite3
import tempfile

DEMO_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'demo_db', 'demo.db')

KNOWN_TABLES = ['employees', 'departments', 'products', 'orders', 'accounts']

# Конструкции, которых не существует в SQLite в принципе (это нормальные
# части стандартного SQL / MySQL, которые бот показывает как справочный
# материал, но выполнить их в SQLite-песочнице невозможно).
NOT_SUPPORTED_BY_SQLITE = (
    r'\bGRANT\b', r'\bREVOKE\b', r'\bCREATE\s+PROCEDURE\b', r'\bCALL\b',
    r'\bLOAD\s+DATA\b', r'\bADD\s+CONSTRAINT\b', r'\bDELIMITER\b',
    r'\bALTER\s+COLUMN\b', r'\bTRUNCATE\b', r'\bDROP\s+DATABASE\b',
    r'\bSET\s+TRANSACTION\b', r'\bINSERT\s+IGNORE\b',
    r'[<>]\s*ANY\s*\(', r'[<>]\s*ALL\s*\(',
    r'=\s*DEFAULT\b', r',\s*DEFAULT\s*[,)]',
    r'\bSET\s+@\w+', r'\bFOR\s+EACH\s+ROW\b',
    r'\bINSERTING\b', r'\bUPDATING\b', r'\bDELETING\b',
    r'\bIF\s+NEW\.', r'\bSET\s+NEW\.', r'backup_db\.',
)

# Функции/конструкции других СУБД, которые можно безопасно подменить
# для целей живой демонстрации, не меняя сам обучающий текст примера.
LIVE_DEMO_SUBSTITUTIONS = [
    (re.compile(r'\bNOW\(\)', re.IGNORECASE), "datetime('now')"),
]


def _table_names_in_query(sql: str) -> list:
    found = []
    for t in KNOWN_TABLES:
        if re.search(rf'\b{t}\b', sql, re.IGNORECASE):
            found.append(t)
    return found


def get_real_table_structure(table_names: list, sql: str = "") -> list:
    """
    Строит table_structure из РЕАЛЬНОЙ схемы demo.db.

    Раньше показывались ВСЕ колонки таблицы, из-за чего, например, в примере
    JOIN по employees.dept_id = departments.id в превью всё равно светился
    текстовый employees.department — визуально дублирующий то, что и так
    достаётся через JOIN, хотя запрос его не использует. Теперь показываем
    только колонки, которые реально фигурируют в конкретном запросе
    (плюс 'id' — он всегда полезен для контекста), остальные скрываем.
    """
    structure = []
    if not table_names:
        return structure

    conn = sqlite3.connect(DEMO_DB_PATH)
    cursor = conn.cursor()
    try:
        for table in table_names:
            cursor.execute(f"PRAGMA table_info({table})")
            cols_info = cursor.fetchall()
            if not cols_info:
                continue
            all_columns = [c[1] for c in cols_info]

            if sql:
                relevant_columns = [
                    col for col in all_columns
                    if col == 'id' or re.search(rf'\b{re.escape(col)}\b', sql, re.IGNORECASE)
                ]
                # На случай, если ни одна колонка не распозналась (например,
                # SELECT *) — показываем схему целиком, а не пустую таблицу.
                if len(relevant_columns) <= 1:
                    relevant_columns = all_columns
            else:
                relevant_columns = all_columns

            col_indexes = [all_columns.index(c) for c in relevant_columns]

            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            total_rows = cursor.fetchone()[0]

            cursor.execute(f"SELECT * FROM {table} LIMIT 20")
            full_rows = cursor.fetchall()
            sample_rows = [[row[i] for i in col_indexes] for row in full_rows]

            structure.append({
                "name": table,
                "columns": relevant_columns,
                "sample_rows": sample_rows,
                "total_rows": total_rows,
                "truncated": total_rows > len(sample_rows)
            })
    finally:
        conn.close()

    return structure


def is_unsupported_by_sqlite(sql: str) -> bool:
    return any(re.search(pattern, sql, re.IGNORECASE) for pattern in NOT_SUPPORTED_BY_SQLITE)


def _apply_live_substitutions(sql: str) -> str:
    for pattern, replacement in LIVE_DEMO_SUBSTITUTIONS:
        sql = pattern.sub(replacement, sql)
    return sql


def run_live(sql_example: str) -> dict:
    """
    Пытается реально выполнить sql_example в изолированной временной
    копии demo.db (изменения никогда не попадают в основную demo.db,
    поэтому запросы можно выполнять сколько угодно раз подряд).

    Возвращает:
      {
        'executable': bool,      # можно ли вообще выполнить в SQLite
        'success': bool,         # выполнился ли успешно в этот раз
        'columns': [...],
        'rows': [...],
        'message': str,
        'table_structure': [...]  # реальная структура задействованных таблиц
      }
    """
    tables = _table_names_in_query(sql_example)
    table_structure = get_real_table_structure(tables, sql_example)

    if is_unsupported_by_sqlite(sql_example):
        return {
            'executable': False,
            'success': False,
            'columns': [],
            'rows': [],
            'message': 'ℹ️ Эта конструкция — часть стандартного SQL/специфики других СУБД '
                       '(например, MySQL) и не поддерживается движком SQLite, '
                       'на котором работает демо-база. Показан справочный пример.',
            'table_structure': table_structure
        }

    demo_sql = _apply_live_substitutions(sql_example)
    statements = [s.strip() for s in demo_sql.split(';') if s.strip()]
    if not statements:
        return {
            'executable': False, 'success': False, 'columns': [], 'rows': [],
            'message': 'Пустой запрос', 'table_structure': table_structure
        }

    tmp_fd, tmp_path = tempfile.mkstemp(suffix='.db')
    os.close(tmp_fd)
    try:
        shutil.copy(DEMO_DB_PATH, tmp_path)
        conn = sqlite3.connect(tmp_path)
        cursor = conn.cursor()

        columns, rows = [], []
        try:
            for stmt in statements:
                cursor.execute(stmt)

            first_upper = statements[0].upper()
            if first_upper.startswith('SELECT') or first_upper.startswith('WITH'):
                rows = [list(r) for r in cursor.fetchall()]
                columns = [d[0] for d in cursor.description] if cursor.description else []
                message = f'✅ Запрос выполнен. Получено {len(rows)} строк.'
            else:
                conn.commit()
                message = f'✅ Запрос выполнен. Изменено строк: {cursor.rowcount if cursor.rowcount != -1 else 0}'
                if tables:
                    try:
                        # Раньше здесь стоял LIMIT 10, из-за чего у демо-таблиц
                        # (например employees с 10 строками) только что вставленная
                        # 11-я строка "срезалась" и не попадала в показанный результат.
                        # Показываем весь текущий объём маленькой демо-таблицы.
                        cursor.execute(f"SELECT * FROM {tables[0]} LIMIT 50")
                        rows = [list(r) for r in cursor.fetchall()]
                        columns = [d[0] for d in cursor.description] if cursor.description else []
                    except sqlite3.Error:
                        pass

            return {
                'executable': True,
                'success': True,
                'columns': columns,
                'rows': rows,
                'message': message,
                'table_structure': table_structure or get_real_table_structure(tables, sql_example)
            }
        except sqlite3.Error as e:
            return {
                'executable': True,
                'success': False,
                'columns': [],
                'rows': [],
                'message': f'❌ Ошибка выполнения: {e}',
                'table_structure': table_structure
            }
        finally:
            conn.close()
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def build_display_payload(sql_example: str, fallback_table_structure=None, fallback_sample_result=None) -> dict:
    """
    Главная функция для app.py: возвращает то, что реально нужно
    показать пользователю под конкретный sql_example — либо настоящий
    результат выполнения, либо (если выполнить нельзя в SQLite)
    аккуратный статический пример с честной пометкой.
    """
    result = run_live(sql_example)

    if result['executable'] and result['success']:
        if result['columns'] and result['rows']:
            # Формат, который ожидает фронтенд (chat.html -> formatSampleResult):
            # список словарей "строка -> {колонка: значение}", а не отдельно
            # columns/rows. Раньше эти строки писались в seed_data.py вручную
            # и расходились с реальной demo.db — теперь собираются из
            # настоящего результата выполнения запроса.
            sample_result = [dict(zip(result['columns'], row)) for row in result['rows']]
        else:
            sample_result = [{"message": result['message']}]
        return {
            "table_structure": result['table_structure'] or fallback_table_structure or [],
            "sample_result": sample_result,
            "live": True,
            "live_message": result['message']
        }

    # Не выполнилось (или в принципе не поддерживается SQLite) —
    # используем структуру таблиц из реальной demo.db, если удалось её
    # определить, иначе откатываемся на сохранённый в базе знаний вариант.
    return {
        "table_structure": result['table_structure'] or fallback_table_structure or [],
        "sample_result": fallback_sample_result or [{"message": result['message']}],
        "live": False,
        "live_message": result['message']
    }
