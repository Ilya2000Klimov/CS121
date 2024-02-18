from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from collections import Counter

nltk.download('stopwords')
nltk.download('wordnet')


class Parser:
    def __init__(self):
        pass


    def parse_document(self, file_path):
        # Open the file and parse it with BeautifulSoup
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            
        # Initialize stopwords set
        stop_words = set(stopwords.words('english'))
        
        # Extract text and apply tokenization, stemming/lemmatization, and stopword removal
        tokens = []
        tag_importance = {'title': 10, 'h1': 6, 'h2': 5, 'h3': 2, 'p': 2, 'b': 3, 'strong': 3}
        
        for tag, weight in tag_importance.items():
            for element in soup.find_all(tag):
                words = self.tokenize(element.get_text())
                processed_tokens = [self.process_token(word) for word in words if word.isalpha() and word not in stop_words]
                tokens.extend(processed_tokens * weight)  # Duplicate tokens based on tag importance

        # Calculate token value from frequency and tag importance
        token_frequency = Counter(tokens)

        return list(token_frequency.items())

    # Function to process tokens
    def process_token(token):
        token = token.lower()  # Convert to lowercase
        # Apply stemming and lemmatization
        stemmer = PorterStemmer()
        lemmatizer = WordNetLemmatizer()
        token = stemmer.stem(token)  # Apply stemming
        token = lemmatizer.lemmatize(token)  # Apply lemmatization
        return token

    # Tokenization function, if a word is separated by dots or slashes return the word as separate word and as a single word, such as "e-mail" returns as "e", "mail" and "e-mail"
    def tokenize(text):
        words = text.split()
        tokens = []
        for word in words:
            if '.' in word:
                tokens.extend(word.split('.'))
            elif '/' in word:
                tokens.extend(word.split('/'))
            elif '-' in word:
                tokens.extend(word.split('-'))
            elif '_' in word:
                tokens.extend(word.split('_'))
            tokens.append(word)
        return tokens