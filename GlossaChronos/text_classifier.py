from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
import joblib

class LinguisticClassifier:
    """Similar to LightSide's approach"""
    
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.classifier = MultinomialNB()
    
    def train(self, texts, labels):
        """Train classifier on historical text periods"""
        X = self.vectorizer.fit_transform(texts)
        self.classifier.fit(X, labels)
        return self
    
    def classify_period(self, text):
        """Classify text into historical period"""
        X = self.vectorizer.transform([text])
        prediction = self.classifier.predict(X)[0]
        proba = self.classifier.predict_proba(X)[0]
        return {
            'period': prediction,
            'confidence': max(proba),
            'all_probabilities': dict(zip(self.classifier.classes_, proba))
        }
    
    def save_model(self, path):
        joblib.dump((self.vectorizer, self.classifier), path)
    
    def load_model(self, path):
        self.vectorizer, self.classifier = joblib.load(path)