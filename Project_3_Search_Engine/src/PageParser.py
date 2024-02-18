from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from collections import Counter
import re

nltk.download('stopwords')
nltk.download('wordnet')


class Parser:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()


    def parse_document(self, file_path):
        # Open the file and parse it with BeautifulSoup
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            
        # Initialize stopwords set
        stop_words = set(stopwords.words('english'))
        
        # Extract text and apply tokenization, stemming/lemmatization, and stopword removal
        tokens = []
        tag_importance = {'title': 10, 'h1': 6, 'h2': 5, 'h3': 3, 'p': 2, 'b': 3, 'strong': 3}
        
        for tag, weight in tag_importance.items():
            for element in soup.find_all(tag):
                words = self.tokenize(element.get_text())
                processed_tokens = [self.process_token(word) for word in words if word.isalpha() and word not in stop_words]
                tokens.extend(processed_tokens * weight)  # Duplicate tokens based on tag importance

        # Calculate token value from frequency and tag importance
        token_frequency = Counter(tokens)  # Divide by 2 to avoid overvaluing the importance of tags

        return list(token_frequency.items())

    # Function to process tokens
    def process_token(self, token):
        token = token.lower()  # Convert to lowercase
        token = self.stemmer.stem(token)  # Apply stemming
        token = self.lemmatizer.lemmatize(token)  # Apply lemmatization
        return token

    # Tokenization function, if a word is separated by dots or slashes return the word as separate word and as a single word, such as "e-mail" returns as "e", "mail" and "e-mail"
    def tokenize(self, text):
        words = text.split()
        tokens = []
        for word in words:
            numberOfDelimiters = 0
            stripped_word = re.sub(r'^\W+|\W+$', '', word.lower())
            if '.' in stripped_word:
                tokens.extend(stripped_word.split('.'))
                numberOfDelimiters += 1
            if '/' in stripped_word:
                tokens.extend(stripped_word.split('/'))
                numberOfDelimiters += 1
            if '-' in stripped_word:
                tokens.extend(stripped_word.split('-'))
                numberOfDelimiters += 1
            if '_' in stripped_word:
                tokens.extend(stripped_word.split('_'))
                numberOfDelimiters += 1
            if numberOfDelimiters > 1:
                tokens.extend(re.findall(r'\b\w+\b', stripped_word))
            tokens.append(stripped_word)
        return tokens