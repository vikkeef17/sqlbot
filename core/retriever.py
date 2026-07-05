import pickle
import sqlite3
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.preprocessor import TextPreprocessor

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'sql_bot.db')


class SQLBotRetriever:
    def __init__(self):#загружает или строит TF-IDF индекс
        self.preprocessor = TextPreprocessor()
        self.vectorizer = None
        self.tfidf_matrix = None
        self.questions = []
        self.processed_questions = []
        self.qa_pairs = []
        self.history = []
        
        self.load_or_build_index()
    
    def load_or_build_index(self):
        """Загружает готовый индекс из кэша или строит новый"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Загружаем все вопросы и ответы
        cursor.execute("SELECT id, question, answer, sql_example, category FROM qa_pairs")
        self.qa_pairs = cursor.fetchall()
        
        if not self.qa_pairs:
            print("⚠️ База знаний пуста! Сначала запустите python database/seed_data.py")
            conn.close()
            return
        
        self.questions = [q[1] for q in self.qa_pairs]
        
        # Обрабатываем каждый вопрос
        self.processed_questions = []
        for q in self.questions:
            processed, _ = self.preprocessor.preprocess(q)
            self.processed_questions.append(processed)
        
        # Пытаемся загрузить кэшированную матрицу
        cursor.execute("SELECT vector_blob, feature_names FROM tfidf_cache ORDER BY id DESC LIMIT 1")
        cache = cursor.fetchone()
        
        if cache:
            try:
                # Загружаем матрицу из кэша
                self.tfidf_matrix = pickle.loads(cache[0])
                feature_names = pickle.loads(cache[1])
                
                # СОЗДАЁМ И ОБУЧАЕМ vectorizer заново на тех же данных
                self.vectorizer = TfidfVectorizer(
                    ngram_range=(1, 2),
                    max_features=5000,
                    min_df=1,
                    max_df=0.95
                )
                # Обучаем vectorizer на обработанных вопросах
                self.vectorizer.fit(self.processed_questions)
                
                # Проверяем, что матрица совпадает с новой
                new_matrix = self.vectorizer.transform(self.processed_questions)
                if new_matrix.shape != self.tfidf_matrix.shape:
                    # Если размерности не совпадают, перестраиваем
                    print("⚠️ Кэш не совпадает, перестраиваем индекс...")
                    self._build_index(conn, cursor)
                else:
                    print(f"✅ Загружен кэш TF-IDF: {len(self.questions)} вопросов")
                    
            except Exception as e:
                print(f"⚠️ Ошибка загрузки кэша: {e}. Перестраиваем индекс...")
                self._build_index(conn, cursor)
        else:
            self._build_index(conn, cursor)
        
        conn.close()
        print(f"📊 Индекс готов. Размерность матрицы: {self.tfidf_matrix.shape}")
    
    def _build_index(self, conn, cursor):
        """Строит TF-IDF матрицу и сохраняет в кэш"""
        print("🔨 Строим TF-IDF индекс...")
        
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            max_features=5000,
            min_df=1,
            max_df=0.95
        )
        
        # Обучаем и трансформируем
        self.tfidf_matrix = self.vectorizer.fit_transform(self.processed_questions)
        
        # Сохраняем в кэш
        vector_blob = pickle.dumps(self.tfidf_matrix)
        features_blob = pickle.dumps(self.vectorizer.get_feature_names_out())
        
        # Очищаем старый кэш
        cursor.execute("DELETE FROM tfidf_cache")
        cursor.execute(
            "INSERT INTO tfidf_cache (vector_blob, feature_names) VALUES (?, ?)",
            (vector_blob, features_blob)
        )
        conn.commit()
        print("✅ Индекс построен и сохранен в кэш")
    
    def add_to_history(self, question, answer):
        """Добавляет сообщение в историю диалога"""
        self.history.append({"question": question, "answer": answer})
        if len(self.history) > 5:
            self.history.pop(0)
    
    def get_context_query(self, current_query: str) -> str:
        """Добавляет контекст из истории к текущему запросу"""
        if not self.history:
            return current_query
        
        recent_questions = [h["question"] for h in self.history[-3:]]
        context = " ".join(recent_questions)
        return f"{context} {current_query}"
    
    def find_best_answer(self, user_query: str, use_context=True, threshold=0.15):
        """
        принимает вопрос, Находит лучший ответ на запрос пользователя
        """
        if not self.qa_pairs or self.vectorizer is None:
            return {"found": False, "confidence": 0, "suggestions": []}
        
        # Добавляем контекст
        query_to_use = self.get_context_query(user_query) if use_context else user_query
        
        # Предобработка запроса
        processed_query, lang = self.preprocessor.preprocess(query_to_use)
        
        # Векторизация запроса
        query_vector = self.vectorizer.transform([processed_query])
        
        # Вычисление косинусного сходства
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Находим лучший результат
        best_idx = np.argmax(similarities)
        best_score = similarities[best_idx]
        
        if best_score < threshold:
            top_indices = np.argsort(similarities)[::-1][:3]
            suggestions = []
            for idx in top_indices:
                if similarities[idx] >= threshold * 0.5:
                    suggestions.append(self.qa_pairs[idx][1])
            
            return {
                "found": False,
                "confidence": float(best_score),
                "suggestions": suggestions
            }
        
        best_pair = self.qa_pairs[best_idx]
        
        return {
            "found": True,
            "id": best_pair[0],
            "question": best_pair[1],
            "answer": best_pair[2],
            "sql_example": best_pair[3],
            "category": best_pair[4],
            "confidence": float(best_score),
            "language": lang
        }
    


    def clear_history(self):
        """Очищает историю диалога"""
        self.history = []

    def get_alternative_answers(self, user_query: str, exclude_id: int, k: int = 3) -> list:
        """
        Возвращает альтернативные ответы, исключая один по ID.
        """
        if not self.qa_pairs or self.vectorizer is None:
            return []
        
        processed_query, lang = self.preprocessor.preprocess(user_query)
        query_vector = self.vectorizer.transform([processed_query])
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        sorted_indices = np.argsort(similarities)[::-1]
        
        alternatives = []
        for idx in sorted_indices:
            qa = self.qa_pairs[idx]
            if qa[0] != exclude_id and similarities[idx] > 0.15:
                try:
                    import sqlite3
                    conn = sqlite3.connect(DB_PATH)
                    cursor = conn.cursor()
                    cursor.execute("""
                        SELECT sql_example, category 
                        FROM qa_pairs WHERE id = ?
                    """, (qa[0],))
                    extra = cursor.fetchone()
                    conn.close()
                    
                    alternatives.append({
                        'id': qa[0],
                        'question': qa[1],
                        'answer': qa[2],
                        'sql_example': extra[0] if extra else '',
                        'category': extra[1] if extra else '',
                        'confidence': float(similarities[idx])
                    })
                except Exception as e:
                    print(f"Ошибка получения данных для альтернативы {qa[0]}: {e}")
                    continue
                    
                if len(alternatives) >= k:
                    break
        
        return alternatives

# Тестирование
if __name__ == '__main__':
    bot = SQLBotRetriever()
    
    test_questions = [
        "как объединить две таблицы",
        "как удалить записи",
        "select"
    ]
    
    for q in test_questions:
        result = bot.find_best_answer(q)
        if result and result.get("found"):
            print(f"\n✅ Вопрос: {q}")
            print(f"   Ответ: {result['answer'][:80]}...")
        else:
            print(f"\n❌ Вопрос: {q} - не найден")