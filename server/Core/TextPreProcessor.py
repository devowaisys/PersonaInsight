from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

class TextPreprocessor:
    def __init__(self):
        self.lemmatizerlemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))

    def preprocess_text(self, text):
        try:
            text = str(text).lower()
            text = re.sub(r'http\S+|www\S+|https\S+|@\w+|#\w+|\d+|[^\w\s]', ' ', text)
            tokens = text.split()
            cleaned_tokens = [
                self.lemmatizer.lemmatize(token)
                for token in tokens
                if token not in self.stop_words
            ]
            return ' '.join(cleaned_tokens)
        except Exception as e:
            print(f"Error preprocessing text: {str(e)}")
            return text