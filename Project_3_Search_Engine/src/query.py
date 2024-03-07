import math
from pymongo import MongoClient
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import pyprojroot
root = pyprojroot.here()
root = root/'Project_3_Search_Engine'
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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
        query_tokens, query_vector = self.calculate_vector(query)

        # Initialize a dictionary to hold document vectors
        doc_vectors = {}

        # Retrieve document lists and TF-IDF scores for each query token
        for token in query_tokens:
            # Find the documents containing the token
            result = self.collection.find_one({"_id": token})
            if result:
                # Iterate over the documents for the current token
                for doc in result['docs']:
                    doc_id = doc['doc_id']
                    tfidf_score = doc['tfidf']
                    # Initialize the document vector with zeros if it's new
                    if doc_id not in doc_vectors:
                        doc_vectors[doc_id] = [0] * len(query_tokens)
                    # Update the TF-IDF score in the document vector at the correct position
                    index = query_tokens.index(token)
                    doc_vectors[doc_id][index] = tfidf_score

        # Calculate cosine similarity between the query vector and each document vector
        similarities = {}
        for doc_id, doc_vector in doc_vectors.items():
            similarity = self.cosine_similarity(query_vector, doc_vector)
            similarities[doc_id] = similarity

        # Rank documents by their cosine similarity scores (higher is better)
        ranked_docs = sorted(similarities.items(), key=lambda x: x[1], reverse=True)

        return ranked_docs
    
    def cosine_similarity(query_vector, doc_vectors):

        # Convert the query vector to a 2D numpy array
        query_vector_np = np.array(query_vector).reshape(1, -1)

        # Extract document IDs and convert document vectors to a 2D numpy array
        doc_ids = list(doc_vectors.keys())
        doc_matrix = np.array(list(doc_vectors.values()))

        # Calculate cosine similarities between the query vector and document vectors
        similarities = cosine_similarity(query_vector_np, doc_matrix)

        # Create a dictionary to map document IDs to their similarity scores
        similarity_scores = {doc_id: sim[0] for doc_id, sim in zip(doc_ids, similarities)}

        # Rank documents by their cosine similarity scores (higher is better)
        ranked_docs = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)

        return ranked_docs
        

        # # Fetch all documents from the collection
        # documents = self.collection.find()

        # # Calculate the cosine similarity between each document and the query
        # results = []
        # for document in documents:
        #     document_vector = self.calculate_vector(document['content'])
        #     similarity = self.calculate_cosine_similarity(query_vector, document_vector)
        #     results.append((document['_id'], similarity))

        # # Sort the results by similarity in descending order
        # results.sort(key=lambda x: x[1], reverse=True)

        # return results

    def query_vector(self, text):
        # Split and stem the text, remove stopwords
        stop_words = set(stopwords.words('english'))
        words = self.parser.tokenize(text)
        processed_tokens = [self.parser.process_token(word) for word in words if word.isalpha() and word not in stop_words]

        # Calculate the term frequency (TF) of processed tokens
        tf = {}
        for token in processed_tokens:
            tf[token] = tf.get(token, 0) + 1

        # Normalize the TF values
        total_tokens = len(processed_tokens)
        for token in tf.keys():
            tf[token] /= total_tokens

        # Initialize lists for tokens and their TF-IDF values
        tokens_in_order = []
        tfidf_values = []

        # Calculate TF-IDF values and keep track of the token order
        for token in processed_tokens:
            if token not in tokens_in_order:
                tokens_in_order.append(token)
                idf_value = self.get_idf_value(token)  # Retrieve IDF value safely
                tfidf_values.append(tf[token] * idf_value)

        return tokens_in_order, tfidf_values

    def get_idf_value(self, token):
        # Safely retrieve the IDF value for a token from the collection
        document = self.collection.find_one({"_id": token})
        if document:
            return document.get('idf', 0)  # Return the IDF value, or 0 if not found
        else:
            return 0  # Return 0 if the token is not found in the collection



    def calculate_cosine_similarity(self, vector1, vector2):
        # Implement your logic to calculate the cosine similarity between two vectors
        # Return the cosine similarity value
        ...