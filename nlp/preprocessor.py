import re
from langdetect import detect, DetectorFactory
import nltk

DetectorFactory.seed = 0

# Скачиваем стоп-слова (один раз)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords


class SimpleStemmer:
    """Простой стеммер для русского языка"""
    
    def __init__(self):
        self.endings = [
            'ться', 'тся', 'ую', 'юю', 'ая', 'яя', 'ое', 'ее',
            'ые', 'ие', 'ой', 'ей', 'ым', 'им', 'ого', 'его',
            'ому', 'ему', 'ом', 'ем', 'ать', 'ять', 'ить', 'еть',
            'ал', 'ял', 'ил', 'ел', 'али', 'яли', 'или', 'ели',
            'ова', 'ева', 'ива', 'ыва', 'ов', 'ев', 'ив', 'ыв'
        ]
    
    def stem(self, word: str) -> str:
        word = word.lower()
        if len(word) <= 3:
            return word
        for ending in self.endings:
            if word.endswith(ending):
                return word[:-len(ending)]
        if len(word) > 5 and word[-1] in 'аеиоуыэюя':
            return word[:-1]
        return word


class TextPreprocessor:
    def __init__(self):
        self.stemmer_ru = SimpleStemmer()
        self.stop_words_ru = set(stopwords.words('russian'))
        self.stop_words_en = set(stopwords.words('english'))
        
        self.sql_keywords = {
            'select', 'from', 'where', 'join', 'inner', 'left', 'right', 'full',
            'group', 'order', 'by', 'having', 'insert', 'into', 'update', 'set',
            'delete', 'create', 'drop', 'alter', 'table', 'index', 'view',
            'and', 'or', 'not', 'null', 'is', 'like', 'in', 'between', 'as',
            'count', 'sum', 'avg', 'min', 'max', 'distinct', 'limit', 'offset'
        }
    
    def detect_language(self, text: str) -> str:
        try:
            lang = detect(text)
            return lang if lang in ['ru', 'en'] else 'ru'
        except:
            return 'ru'
    
    def clean_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', '', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def stem_russian(self, text: str) -> str:
        words = text.split()
        result = []
        for word in words:
            if word in self.sql_keywords:
                result.append(word)
            else:
                result.append(self.stemmer_ru.stem(word))
        return ' '.join(result)
    
    def stem_english(self, text: str) -> str:
        words = text.split()
        result = []
        for word in words:
            if word in self.sql_keywords:
                result.append(word)
            else:
                if len(word) > 3 and word.endswith('ing'):
                    word = word[:-3]
                elif len(word) > 2 and word.endswith('ed'):
                    word = word[:-2]
                elif len(word) > 1 and word.endswith('s') and not word.endswith('ss'):
                    word = word[:-1]
                result.append(word)
        return ' '.join(result)
    
    def remove_stopwords(self, text: str, lang: str) -> str:
        words = text.split()
        stop_words = self.stop_words_ru if lang == 'ru' else self.stop_words_en
        filtered = [w for w in words if w in self.sql_keywords or w not in stop_words]
        return ' '.join(filtered)
    
    def preprocess(self, text: str) -> tuple:
        lang = self.detect_language(text)
        text = self.clean_text(text)
        if lang == 'ru':
            text = self.stem_russian(text)
        else:
            text = self.stem_english(text)
        text = self.remove_stopwords(text, lang)
        return text, lang


if __name__ == '__main__':
    p = TextPreprocessor()
    print(p.preprocess("Как объединить две таблицы?"))