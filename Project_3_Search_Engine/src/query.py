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
from tqdm import tqdm


class MongoDBSearch:
    def __init__(self, db_name='searchEngine', collection_name='Index'):
        self.client = MongoClient()
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.documents = self.db['Documents']
        self.parser = PageParser()

    def search(self, query):
        # Calculate the query vector using the query_vector method
        query_tokens, query_vector = self.query_vector(query)
        


        # Initialize a dictionary to hold document vectors
        doc_vectors = {}

        # Retrieve document lists and TF-IDF scores for each query token
        for token in query_tokens:
            result = self.collection.find_one({"_id": token})
            if result:
                for doc in result['documents']:
                    doc_id = doc['document_id']
                    tfidf_score = doc['tfidf']
                    if doc_id not in doc_vectors:
                        doc_vectors[doc_id] = [0] * len(query_tokens)
                    index = query_tokens.index(token)
                    doc_vectors[doc_id][index] = tfidf_score
            
        #from self.documents load all the documents doc_vector[doc_id] at onece into a dictoinary
        
            
        query_tokens.append("others")
        query_vector.append(0) 

        # Rank documents by their cosine similarity scores
        # print(doc_vectors)
        # print(len(doc_vectors))
        ranked_docs = self.cosine_similarity(query_vector, doc_vectors)

        return ranked_docs

    def cosine_similarity(self, query_vector, doc_vectors):
        ranked_docs = []
        
        # Convert query vector to numpy array for efficient computation
        query_vector_np = np.array(query_vector)

        for doc_id, doc_vector in doc_vectors.items():
            # Convert document vector to numpy array
            doc_vector_np = np.array(doc_vector)

            # Calculate dot product between query vector and document vector
            dot_product = np.dot(query_vector_np, doc_vector_np)

            # Calculate magnitude (norm) of query vector and document vector
            query_norm = np.linalg.norm(query_vector_np)
            doc_norm = self.documents.find_one({"_id": doc_id})['magnitude']

            # Avoid division by zero
            if query_norm == 0 or doc_norm == 0:
                similarity = 0
            else:
                # Calculate cosine similarity
                similarity = dot_product / (query_norm * doc_norm)
                #similarity *= (doc_norm/query_norm)

            # Append doc_id and similarity score to ranked_docs
            ranked_docs.append((doc_id, similarity))
        
        # doc_ids = list(doc_vectors.keys())
        # # print(query_vector)
        # # print(query_vector_np)
        # doc_matrix = np.array(list(doc_vectors.values()))
        # # print(doc_matrix)
        # similarities = cosine_similarity(query_vector_np, doc_matrix)
        # print(similarities)
        # similarity_scores = {doc_id: score for doc_id, score in zip(doc_ids, similarities[0])}
        # # print(f"similarity scores {similarity_scores}")
        # ranked_docs = sorted(ranked_docs.items(), key=lambda x: x[1], reverse=True)
        
        ranked_docs.sort(key=lambda x: x[1], reverse=True)
        return ranked_docs

    def query_vector(self, text):
        stop_words = set(stopwords.words('english'))
        words = self.parser.tokenize(text)
        processed_tokens = [self.parser.process_token(word) for word in words if word.isalpha() and word not in stop_words]

        tf = {}
        for token in processed_tokens:
            tf[token] = tf.get(token, 0) + 1

        total_tokens = len(processed_tokens)
        for token in tf.keys():
            tf[token] /= total_tokens

        tokens_in_order = []
        tfidf_values = []
        for token in processed_tokens:
            if token not in tokens_in_order:
                tokens_in_order.append(token)
                idf_value = self.get_idf_value(token)
                tfidf_values.append(tf[token] * idf_value)

        return tokens_in_order, tfidf_values

    def get_idf_value(self, token):
        document = self.collection.find_one({"_id": token})
        return document.get('idf', 0) if document else 0