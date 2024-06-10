from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class MessageAnalyzer:
    def __init__(self):
        self.nlp = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self.vectorizer = TfidfVectorizer()

    def analyze_commit_message(self, commit_message, diff_stat):
        diff_keywords = self._extract_keywords(diff_stat)
        return self._compare_message_with_diff(commit_message, diff_keywords)

    def _extract_keywords(self, diff_stat):
        keywords = set()
        for line in diff_stat.split('\n'):
            if '|' in line:
                file_name = line.split('|')[0].strip()
                keywords.add(file_name)
            if 'insertions(+)' in line or 'deletions(-)' in line:
                keywords.update(re.findall(r'\b\w+\b', line))
        print(' '.join(keywords))
        return ' '.join(keywords)

    def _compare_message_with_diff(self, message, diff_keywords):
        documents = [message, diff_keywords]
        tfidf_matrix = self.vectorizer.fit_transform(documents)
        cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return cosine_sim[0][0]
