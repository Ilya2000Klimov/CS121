from bs4 import BeautifulSoup
from bs4 import MarkupResemblesLocatorWarning
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from collections import Counter
import re
import json
import os
import warnings
import sys

nltk.download('stopwords')
nltk.download('wordnet')



def handle_warning(message, category, filename, lineno, file=None, line=None):
    # Prinrt the warning to the alternate stream
    print(f"Warning: {message}", file=sys.stderr)
        
class PageParser:
    def __init__(self, directory_path):
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        self.directory_path = directory_path
        with open(os.path.join(directory_path, "bookkeeping.json"), 'r', encoding='utf-8') as file:
            self.data = json.load(file)
    
    
    def parse_document(self, file_path):
        # Open the file and parse it with BeautifulSoup
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        
        if '<html' in file_content.lower():
            soup = BeautifulSoup(file_content, 'html.parser')
            is_html = True
        else:
            soup = BeautifulSoup(file_content, 'xml')
            is_html = False


            
        # Initialize stopwords set
        stop_words = set(stopwords.words('english'))
        
        # Extract text and apply tokenization, stemming/lemmatization, and stopword removal
        tokens = []
        if is_html:
            tag_importance = {'title': 10, 'h1': 6, 'h2': 5, 'h3': 3, 'p': 2, 'b': 3, 'strong': 3}
        else:
            # For XML, you might want to adjust how you handle tag importance
            tag_importance = {tag.name: 1 for tag in soup.find_all()}
        
        processed_tokens = []
        for tag, weight in tag_importance.items():
            for element in soup.find_all(tag):
                words = self.tokenize(element.get_text())
                processed_tokens += [self.process_token(word) for word in words if word.isalpha() and word not in stop_words]
                tokens.extend(processed_tokens * weight)  # Duplicate tokens based on tag importance

        # For each token Calculate token value from frequency and tag importance
        token_frequency = Counter(tokens)

        return dict(doc_size=len(processed_tokens), token_frequency=token_frequency.items())

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