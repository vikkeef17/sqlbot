from flask import Flask, render_template, request, jsonify, session
import os
import sys
import json
import sqlite3
import threading
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

# Абсолютные пути к базам данных. Раньше в нескольких местах использовались
# относительные пути вида 'database/sql_bot.db' — они резолвятся от текущей
# рабочей директории процесса, а не от расположения проекта. Локально
# запуск обычно происходит из корня проекта, поэтому это работало, но на
# сервере (systemd, gunicorn, Docker и т.п.) процесс часто стартует из
# другого cwd — и относительные пути ломаются ("no such table"/"unable to
# open database file"). Абсолютные пути работают независимо от того,
# откуда запущен процесс.
QA_DB_PATH = os.path.join(BASE_DIR, 'database', 'sql_bot.db')
DEMO_DB_FILE_PATH = os.path.join(BASE_DIR, 'demo_db', 'demo.db')

from core.retriever import SQLBotRetriever
from core.query_runner import build_display_payload, run_live
from demo_db.demo_database import execute_query, create_demo_database

app = Flask(__name__)
# Flask по умолчанию сортирует ключи в jsonify() по алфавиту — из-за этого
# строки sample_result (это словари "колонка: значение") показывались
# в алфавитном порядке колонок вместо реального порядка из таблицы
# (age, department, dept_id... вместо id, name, age...). Отключаем.
app.config['JSON_SORT_KEYS'] = False
try:
    app.json.sort_keys = False  # для Flask >= 2.3 с новым JSON-провайдером
except Exception:
    pass
# Секретный ключ раньше был захардкожен прямо в коде — это небезопасно,
# если код лежит в публичном репозитории/на сервере. Берём его из
# переменной окружения SECRET_KEY (её нужно задать на хостинге), а
# захардкоженное значение оставляем только как запасной вариант для
# локальной разработки.
app.secret_key = os.environ.get('SECRET_KEY', 'dev-only-insecure-key-change-me')

# Инициализация модуля поиска
bot = SQLBotRetriever()

# Проверяем наличие демо-БД (абсолютным путём — см. комментарий выше)
if not os.path.exists(DEMO_DB_FILE_PATH):
    create_demo_database()


def get_full_qa_data(qa_id, lang='ru'):
    """Получает полную информацию о вопросе из базы знаний по ID.

    Если lang='en' и для этого вопроса есть перевод в translations_en —
    вопрос/ответ/пояснение отдаются на английском (SQL, названия таблиц/
    колонок и демо-данные остаются как есть — они и так в основном на
    английском/нейтральные). Если перевода для конкретного примера ещё
    нет, тихо показываем русскую версию — переведены только основные,
    самые частые категории, чтобы не раздувать базу знаний целиком.
    """
    try:
        conn = sqlite3.connect(QA_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT question, answer, sql_example, code_explanation, table_structure, sample_result, category
            FROM qa_pairs WHERE id = ?
        """, (qa_id,))
        result = cursor.fetchone()

        question, answer, code_explanation = result[0], result[1], result[3]
        translated = False
        if result and lang == 'en':
            cursor.execute("""
                SELECT question_en, answer_en, code_explanation_en
                FROM translations_en WHERE qa_id = ?
            """, (qa_id,))
            tr = cursor.fetchone()
            if tr:
                question, answer, code_explanation = tr[0], tr[1], tr[2]
                translated = True
        conn.close()
        
        if result:
            sql_example = result[2] or ""
            stored_table_structure = json.loads(result[4]) if result[4] else []
            stored_sample_result = json.loads(result[5]) if result[5] else []

            table_structure, sample_result = stored_table_structure, stored_sample_result
            live, live_message = False, ""
            if sql_example:
                try:
                    payload = build_display_payload(
                        sql_example,
                        fallback_table_structure=stored_table_structure,
                        fallback_sample_result=stored_sample_result
                    )
                    table_structure = payload["table_structure"]
                    sample_result = payload["sample_result"]
                    live = payload["live"]
                    live_message = payload["live_message"]
                except Exception as e:
                    print(f"Ошибка живого выполнения запроса: {e}")

            return {
                "question": question,
                "answer": answer,
                "sql_example": sql_example,
                "code_explanation": code_explanation or "",
                "table_structure": table_structure,
                "sample_result": sample_result,
                "category": result[6] or "",
                "live": live,
                "live_message": live_message,
                "translated": translated
            }
        return None
    except Exception as e:
        print(f"Ошибка получения данных: {e}")
        return None


@app.route('/')
def index():
    """Главная страница с чатом"""
    return render_template('chat.html')


@app.route('/ask', methods=['POST'])
def ask():
    """
    Основной эндпоинт: обрабатывает вопрос пользователя
    Поддерживает:
    - Обычный поиск (action='search')
    - Альтернативные ответы (action='alternative')
    """
    data = request.get_json()
    user_message = data.get('message', '').strip()
    action = data.get('action', 'search')
    current_id = data.get('current_id', None)
    shown_ids = data.get('shown_ids', [])
    
    if not user_message:
        return jsonify({'error': 'Пожалуйста, введите вопрос'}), 400
    
    # === ВЕТКА 1: Альтернативные ответы ===
    if action == 'alternative' and current_id:
        alt_lang = bot.preprocessor.detect_language(user_message)
        alternatives = bot.get_alternative_answers(user_message, exclude_id=current_id, k=3)
        alternatives = [a for a in alternatives if a['id'] not in shown_ids]
        
        if alternatives:
            alt = alternatives[0]
            full_data = get_full_qa_data(alt['id'], lang=alt_lang)
            if not full_data:
                full_data = {
                    "question": alt['question'],
                    "answer": alt['answer'],
                    "sql_example": alt.get('sql_example', ''),
                    "code_explanation": "",
                    "table_structure": [],
                    "sample_result": [],
                    "category": alt.get('category', '')
                }
            
            return jsonify({
                'type': 'alternative',
                'found': True,
                'question': full_data['question'],
                'answer': full_data['answer'],
                'sql_example': full_data['sql_example'],
                'code_explanation': full_data['code_explanation'],
                'table_structure': full_data['table_structure'],
                'sample_result': full_data['sample_result'],
                'category': full_data['category'],
                'live': full_data.get('live', False),
                'live_message': full_data.get('live_message', ''),
                'current_id': alt['id'],
                'remaining_alternatives': alternatives[1:] if len(alternatives) > 1 else []
            })
        else:
            return jsonify({
                'type': 'no_more',
                'message': '😕 Больше вариантов нет. Попробуйте переформулировать вопрос.'
            })
    
    # === ВЕТКА 2: Обычный поиск ===
    result = bot.find_best_answer(user_message, use_context=False, threshold=0.35)
    
    if not result or not result.get('found'):
        suggestions = bot.get_alternative_answers(user_message, exclude_id=-1, k=5)
        suggestions = [s['question'] for s in suggestions[:3]]
        
        return jsonify({
            'type': 'answer',
            'found': False,
            'message': '😕 Извините, я не нашел подходящего ответа.',
            'suggestions': suggestions
        })
    
    full_data = get_full_qa_data(result['id'], lang=result.get('language', 'ru'))
    if not full_data:
        full_data = {
            "question": result['question'],
            "answer": result['answer'],
            "sql_example": result.get('sql_example', ''),
            "code_explanation": "",
            "table_structure": [],
            "sample_result": [],
            "category": result.get('category', '')
        }
    
    alternatives = bot.get_alternative_answers(user_message, exclude_id=result['id'], k=3)
    
    bot.add_to_history(user_message, full_data['answer'])
    
    return jsonify({
        'type': 'answer',
        'found': True,
        'question': full_data['question'],
        'answer': full_data['answer'],
        'sql_example': full_data['sql_example'],
        'code_explanation': full_data['code_explanation'],
        'table_structure': full_data['table_structure'],
        'sample_result': full_data['sample_result'],
        'category': full_data['category'],
        'live': full_data.get('live', False),
        'live_message': full_data.get('live_message', ''),
        'current_id': result['id'],
        'has_alternatives': len(alternatives) > 0,
        'alternatives_count': len(alternatives),
        'language': result.get('language', 'ru')
    })


@app.route('/reset', methods=['POST'])
def reset():
    """Сброс истории диалога"""
    bot.clear_history()
    return jsonify({'status': 'ok', 'message': 'История очищена'})


@app.route('/execute_sql', methods=['POST'])
def execute_sql_endpoint():
    data = request.get_json()
    sql_query = data.get('sql', '').strip()

    if not sql_query:
        return jsonify({'error': 'Введите SQL-запрос'}), 400

    sql_upper = sql_query.upper().strip()

    forbidden = ('ATTACH', 'DETACH', 'PRAGMA', 'VACUUM')
    if any(sql_upper.startswith(f) for f in forbidden):
        return jsonify({
            'success': False,
            'message': '⚠️ Эта команда недоступна в демо-режиме.'
        })

    if sql_upper.startswith('SELECT') or sql_upper.startswith('WITH'):
        result = execute_query(sql_query)
        return jsonify({
            'type': 'execution',
            'success': result['success'],
            'message': result.get('message', ''),
            'columns': result.get('columns', []),
            'rows': result.get('rows', []),
            'row_count': result.get('row_count', 0)
        })

    live = run_live(sql_query)
    extra_note = '' if live['executable'] else ' (запрос показан как справочный пример, SQLite-песочница не может его выполнить)'
    return jsonify({
        'type': 'execution',
        'success': live['success'],
        'message': live['message'] + extra_note,
        'columns': live.get('columns', []),
        'rows': live.get('rows', []),
        'row_count': len(live.get('rows', []))
    })


@app.route('/demo_tables', methods=['GET'])
def demo_tables():
    try:
        conn = sqlite3.connect(DEMO_DB_FILE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        conn.close()
        return jsonify({'tables': tables})
    except Exception as e:
        return jsonify({'tables': [], 'error': str(e)})


if __name__ == '__main__':
    # Переменные окружения для хостинга:
    #   PORT        — порт, который выдаёт платформа (Render/Railway/Heroku
    #                 и т.п. сами подставляют его, слушать нужно именно его,
    #                 а не жёстко зашитый 5000);
    #   HOST        — по умолчанию 0.0.0.0, чтобы сервер был доступен снаружи
    #                 контейнера/машины, а не только на localhost;
    #   FLASK_DEBUG — держим выключенным в продакшене (утечка стектрейсов,
    #                 автоперезагрузка не нужна и на прод-сервере вредна);
    #   OPEN_BROWSER — автопереход в браузер имеет смысл только на локальной
    #                 машине разработчика, на сервере это не нужно
    #                 (и там обычно просто нет браузера).
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', '0') == '1'
    open_browser_flag = os.environ.get('OPEN_BROWSER', '1' if host == '127.0.0.1' else '0') == '1'

    print("=" * 50)
    print("🚀 SQL Консультант - Чат-бот для справки по SQL")
    print("=" * 50)
    print(f"📁 База знаний: {QA_DB_PATH}")
    print(f"📊 Демо-БД: {DEMO_DB_FILE_PATH}")
    print(f"🌐 Запуск сервера: http://{host}:{port}")
    print("=" * 50)

    if open_browser_flag:
        def open_browser():
            webbrowser.open(f'http://127.0.0.1:{port}')
        threading.Timer(1, open_browser).start()

    # Встроенный сервер Flask (werkzeug) подходит только для локальной
    # разработки — сам Flask предупреждает об этом при старте. Для
    # реального хостинга приложение нужно запускать через WSGI-сервер,
    # например: gunicorn -w 2 -b 0.0.0.0:$PORT app:app (см. requirements.txt
    # и Procfile). Этот app.run(...) остаётся рабочим для локального
    # запуска (python app.py) и как аварийный вариант.
    app.run(debug=debug, host=host, port=port)