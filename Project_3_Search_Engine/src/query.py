import math
from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import pyprojroot
root = pyprojroot.here()
root = root/'Project_3_Search_Engine'


from src.PageParser import PageParser


class MongoDBSearch:
    def __init__(self, db_name='searchEngine', collection_name='Index'):
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.documents = self.db['Documents']
        self.parser = PageParser()

    def search(self, query):
        # Calculate the query vector
        query_vector = self.calculate_vector(query)

        # Fetch all documents from the collection
        documents = self.collection.find()

        # Calculate the cosine similarity between each document and the query
        results = []
        for document in documents:
            document_vector = self.calculate_vector(document['content'])
            similarity = self.calculate_cosine_similarity(query_vector, document_vector)
            results.append((document['_id'], similarity))

        # Sort the results by similarity in descending order
        results.sort(key=lambda x: x[1], reverse=True)

        return results

    def query_vector(self, text):
        # Implement your logic to calculate the query vector
        # split and stem the text
        stop_words = set(stopwords.words('english'))
        words = self.parser.tokenize(text)
        processed_tokens = (self.parser.process_token(word) for word in words if word.isalpha() and word not in stop_words)
        
        # Calculate the term frequency (tf) of processed tokens
        tf = {}
        for token in processed_tokens:
            tf[token] = tf.get(token, 0) + 1

        # Normalize the tf values
        total_tokens = len(processed_tokens)
        for token in tf:
            tf[token] /= total_tokens

        # Convert the tf dictionary to a vector
        vector = [tf.get(token, 0) for token in processed_tokens]
        # Return the query vector
        return vector

    def calculate_cosine_similarity(self, vector1, vector2):
        # Implement your logic to calculate the cosine similarity between two vectors
        # Return the cosine similarity value
        ...

# Example usage
search_engine = MongoDBSearch('mydb', 'mycollection')
results = search_engine.search('python programming')
for result in results:
    print(result)