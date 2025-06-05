import re
import math
from collections import Counter, defaultdict
from typing import List, Tuple, Dict
import string


class KeywordExtractor:
    def __init__(self):
        self.russian_stopwords = {
            'а', 'без', 'более', 'будет', 'будто', 'бы', 'был', 'была', 'были', 'было',
            'быть', 'в', 'вам', 'вас', 'весь', 'во', 'вот', 'все', 'всего', 'всех',
            'вы', 'где', 'да', 'даже', 'для', 'до', 'его', 'ее', 'если', 'есть',
            'еще', 'же', 'за', 'здесь', 'и', 'из', 'или', 'им', 'их', 'к', 'как',
            'ко', 'когда', 'кто', 'ли', 'либо', 'мне', 'может', 'мы', 'на', 'надо',
            'наш', 'не', 'него', 'нее', 'нет', 'ни', 'них', 'но', 'ну', 'о', 'об',
            'однако', 'он', 'она', 'они', 'оно', 'от', 'очень', 'по', 'под', 'при',
            'с', 'со', 'та', 'так', 'также', 'такой', 'там', 'те', 'тем', 'то',
            'того', 'тоже', 'той', 'только', 'том', 'ты', 'у', 'уже', 'хотя',
            'чего', 'чем', 'что', 'чтобы', 'чье', 'эта', 'эти', 'это', 'я'
        }

        self.english_stopwords = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from', 'has',
            'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the', 'to', 'was',
            'will', 'with', 'would', 'have', 'had', 'been', 'this', 'these', 'they',
            'were', 'said', 'each', 'which', 'their', 'time', 'but', 'or', 'if',
            'can', 'could', 'should', 'would', 'his', 'her', 'him', 'she', 'we',
            'you', 'your', 'me', 'my', 'i', 'am', 'do', 'did', 'does', 'done'
        }

        self.stopwords = self.russian_stopwords.union(self.english_stopwords)

    def preprocess_text(self, text: str) -> List[str]:
        """Предобработка текста: очистка и токенизация"""
        # Приведение к нижнему регистру
        text = text.lower()

        # Удаление знаков препинания
        text = re.sub(r'[^\w\s]', ' ', text)

        # Разбиение на слова
        words = text.split()

        # Удаление стоп-слов и коротких слов
        words = [word for word in words if word not in self.stopwords and len(word) > 2]

        return words

    def extract_sentences(self, text: str) -> List[str]:
        """Извлечение предложений из текста"""
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]

    def tf_idf_keywords(self, text: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Извлечение ключевых слов методом TF-IDF"""
        sentences = self.extract_sentences(text)
        if not sentences:
            return []

        # Создание документов (предложений)
        documents = [self.preprocess_text(sentence) for sentence in sentences]
        documents = [doc for doc in documents if doc]  # Удаление пустых документов

        if not documents:
            return []

        # Подсчет TF (Term Frequency)
        tf_scores = {}
        for doc in documents:
            doc_length = len(doc)
            word_count = Counter(doc)
            for word, count in word_count.items():
                if word not in tf_scores:
                    tf_scores[word] = []
                tf_scores[word].append(count / doc_length)

        # Подсчет IDF (Inverse Document Frequency)
        doc_count = len(documents)
        idf_scores = {}

        for word in tf_scores:
            containing_docs = sum(1 for doc in documents if word in doc)
            idf_scores[word] = math.log(doc_count / containing_docs)

        # Подсчет TF-IDF
        tfidf_scores = {}
        for word in tf_scores:
            avg_tf = sum(tf_scores[word]) / len(tf_scores[word])
            tfidf_scores[word] = avg_tf * idf_scores[word]

        # Сортировка по убыванию значимости
        sorted_keywords = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_keywords[:top_k]

    def rake_keywords(self, text: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Извлечение ключевых фраз методом RAKE"""
        # Разбиение текста на предложения
        sentences = self.extract_sentences(text)

        # Извлечение фраз-кандидатов
        phrase_candidates = []

        for sentence in sentences:
            # Удаление знаков препинания и приведение к нижнему регистру
            sentence = re.sub(r'[^\w\s]', ' ', sentence.lower())
            words = sentence.split()

            # Разбиение на фразы по стоп-словам
            current_phrase = []
            for word in words:
                if word in self.stopwords or len(word) <= 2:
                    if current_phrase:
                        phrase_candidates.append(' '.join(current_phrase))
                        current_phrase = []
                else:
                    current_phrase.append(word)

            if current_phrase:
                phrase_candidates.append(' '.join(current_phrase))

        # Подсчет характеристик слов
        word_degree = defaultdict(int)
        word_frequency = defaultdict(int)

        for phrase in phrase_candidates:
            words = phrase.split()
            phrase_length = len(words)

            for word in words:
                word_frequency[word] += 1
                word_degree[word] += phrase_length - 1

        # Подсчет RAKE-оценки для каждой фразы
        phrase_scores = {}
        for phrase in phrase_candidates:
            words = phrase.split()
            score = 0
            for word in words:
                if word_frequency[word] > 0:
                    word_score = word_degree[word] / word_frequency[word]
                    score += word_score
            phrase_scores[phrase] = score

        # Сортировка по убыванию значимости
        sorted_phrases = sorted(phrase_scores.items(), key=lambda x: x[1], reverse=True)

        return sorted_phrases[:top_k]

    def word_frequency_keywords(self, text: str, top_k: int = 10) -> List[Tuple[str, int]]:
        """Извлечение ключевых слов по частоте встречаемости"""
        words = self.preprocess_text(text)
        word_freq = Counter(words)

        return word_freq.most_common(top_k)

    def analyze_text(self, text: str, top_k: int = 10) -> Dict:
        """Комплексный анализ текста с применением всех методов"""
        if not text.strip():
            return {"error": "Пустой текст"}

        results = {
            "text_stats": {
                "total_chars": len(text),
                "total_words": len(text.split()),
                "unique_words": len(set(self.preprocess_text(text)))
            },
            "tf_idf_keywords": self.tf_idf_keywords(text, top_k),
            "rake_phrases": self.rake_keywords(text, top_k),
            "frequency_keywords": self.word_frequency_keywords(text, top_k)
        }

        return results

    def print_results(self, results: Dict):
        """Красивый вывод результатов анализа"""
        if "error" in results:
            print(f"Ошибка: {results['error']}")
            return

        stats = results["text_stats"]
        print(f"\n СТАТИСТИКА ТЕКСТА:")
        print(f"   Всего символов: {stats['total_chars']}")
        print(f"   Всего слов: {stats['total_words']}")
        print(f"   Уникальных слов: {stats['unique_words']}")

        print(f"\n ТОП КЛЮЧЕВЫХ СЛОВ (TF-IDF):")
        print(f"{'Ранг':<4} {'Слово':<20} {'TF-IDF Оценка':<15}")
        print("-" * 40)
        for i, (word, score) in enumerate(results["tf_idf_keywords"], 1):
            print(f"{i:<4} {word:<20} {score:.4f}")

        print(f"\n ТОП КЛЮЧЕВЫХ ФРАЗ (RAKE):")
        print(f"{'Ранг':<4} {'Фраза':<30} {'RAKE Оценка':<15}")
        print("-" * 50)
        for i, (phrase, score) in enumerate(results["rake_phrases"], 1):
            print(f"{i:<4} {phrase:<30} {score:.4f}")

        print(f"\n ТОП СЛОВ ПО ЧАСТОТЕ:")
        print(f"{'Ранг':<4} {'Слово':<20} {'Частота':<10}")
        print("-" * 35)
        for i, (word, freq) in enumerate(results["frequency_keywords"], 1):
            print(f"{i:<4} {word:<20} {freq}")


def main():
    extractor = KeywordExtractor()

    try:
        with open("input_text.txt", "r", encoding="utf-8") as file:
            file_text = file.read()
            print("Анализ текста из файла input_text.txt:")
    except FileNotFoundError:
        file_text = """
            Искусственный интеллект и машинное обучение стремительно развиваются в современном мире.
            Нейронные сети и глубокое обучение открывают новые возможности для автоматизации и анализа данных.
            Алгоритмы машинного обучения применяются в различных областях: от медицины до финансов.
            Обработка естественного языка позволяет компьютерам понимать и генерировать человеческую речь.
            Компьютерное зрение и распознавание образов революционизируют многие индустрии.
            Большие данные и их анализ становятся ключевыми факторами успеха в бизнесе.
            """
        print("Файл input_text.txt не найден. Пожалуйста, создайте файл с текстом для анализа.")

    results = extractor.analyze_text(file_text)
    extractor.print_results(results)


if __name__ == "__main__":
    main()
