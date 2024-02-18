from pymongo import MongoClient
from bs4 import BeautifulSoup
import os
import json
from PageParser import Parser

class InverseIndex:
    def __init__(self, db_uri='localhost', db_port=27017, db_name='searchEngine', collection_name='Index'):
        self.client = MongoClient(db_uri, db_port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.total_docs = 0 
        
    def calculate_tf(self, term_freq, doc_length):
        # Calculate Term Frequency (TF)
        return term_freq / doc_length

    def calculate_tfidf(self, term, doc_id, term_freq, doc_freq, total_docs):
        ... # Implement TF-IDF calculation here

    def update_index(self, term, doc_id, tf, tag_importance):
        # Check if the term already exists in the collection
        term_entry = self.collection.find_one({"term": term})

        # Document reference structure
        doc_ref = {"document_id": doc_id, "tf": tf, "tag_importance": tag_importance}

        if term_entry:
            # If the term exists, update it with the new document reference
            self.collection.update_one({"term": term}, {"$push": {"documents": doc_ref}})
        else:
            # If the term doesn't exist, create a new entry for it
            self.collection.insert_one({"term": term, "documents": [doc_ref]})

    def index_document(self, file_path, doc_id):
        # Parse the document, calculate metrics, and update the index for each term in the document
        Parser.parse_document(file_path)
        

    
    # Implement the logic to build the index for all documents in a directory
    def build_index(self, directory_path):
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                doc_id = os.path.relpath(file_path, directory_path)  # Use relative path as a unique identifier
                self.index_document(file_path, doc_id)
    


    def save_index_to_file(self, collection=self.collection, file_path = 'index.json'):
        """
        Save the contents of the MongoDB collection to a JSON file.

        Args:
        - collection: The MongoDB collection to be saved.
        - file_path: The path to the file where the index will be saved.
        """
        # Open the file in write mode
        with open(file_path, 'w', encoding='utf-8') as file:
            # Iterate over all documents in the collection
            for document in collection.find():
                # Convert the MongoDB document to a JSON string
                json_str = json.dumps(document, default=str)
                # Write the JSON string to the file, followed by a newline character
                file.write(json_str + '\n')
    
    def load_index_from_file(self, file_path = 'index.json'):
        """
        Load the contents of a JSON file into a MongoDB collection.

        Args:
        - file_path: The path to the file containing the index.
        """
        # Open the file in read mode
        with open(file_path, 'r', encoding='utf-8') as file:
            # Iterate over each line in the file
            for line in file:
                # Parse the JSON string to create a Python dictionary
                document = json.loads(line)
                # Insert the document into the collection
                self.collection.insert_one(document)
        

    # Add more methods as needed, e.g., for querying the index, handling updates, etc.