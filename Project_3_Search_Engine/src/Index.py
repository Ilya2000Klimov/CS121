from pymongo import MongoClient, UpdateOne
from bs4 import BeautifulSoup
import os
import json
import math

import pyprojroot
root = pyprojroot.here()
root = root/'Project_3_Search_Engine'

import sys
sys.path.append(str(root))

from src.PageParser import PageParser
from tqdm import tqdm

class InverseIndex:
    def __init__(self, db_uri='localhost', db_port=27017, db_name='searchEngine', collection_name='Index', directory_path=root/'webpages/WEBPAGES_RAW'):
        self.client = MongoClient(db_uri, db_port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.total_docs = 0
        self.directory_path = directory_path
        
    def calculate_tf(self, term_freq, doc_length):
        # Calculate Term Frequency (TF)
        return term_freq / doc_length

    def update_index(self, term, doc_id, tf):
        # Check if the term already exists in the collection
        term_entry = self.collection.find_one({"term": term})

        # Document reference structure
        doc_ref = {"document_id": doc_id, "tf": tf, "tfidf": 0}

        if term_entry:
            # If the term exists, update it with the new document reference
            self.collection.update_one({"term": term}, {"$push": {"documents": doc_ref}})
        else:
            # If the term doesn't exist, create a new entry for it
            self.collection.insert_one({"term": term, "documents": [doc_ref]})

    def index_document(self, file_path, doc_id):
        # Parse the document, calculate metrics, and update the index for each term in the document
        parser = PageParser()
        documant_data = parser.parse_document(file_path)
        doc_length = documant_data['doc_size']
        
        # for each term in the document_data['token_frequency'] calculate the term frequency and update the index
        for term, term_freq in documant_data['token_frequency']:
            #print(f"Indexing term: {term} in document: {doc_id},  document length: {doc_length}")
            tf = self.calculate_tf(term_freq, doc_length)
            self.update_index(term, doc_id, tf)
        
        

    
    # Implement the logic to build the index for all documents in a directory
    def build_index(self):
        directory_path = self.directory_path
        for root, dirs, files in os.walk(directory_path):
            # Print directory path
            print(f"Indexing files in {root}[", end="")
            for file in files:
                # Print file name
                print(f"| {file} ", end="")
                file_path = os.path.join(root, file)
                doc_id = os.path.relpath(file_path, directory_path)  # Use relative path as a unique identifier
                self.index_document(file_path, doc_id)
                self.total_docs += 1
            print("]")
        self.calculate_TFIDF()
        self.save_index_to_file()
    


    def save_index_to_file(self, file_path = 'index.json'):
        """
        Save the contents of the MongoDB collection to a JSON file.

        Args:
        - collection: The MongoDB collection to be saved.
        - file_path: The path to the file where the index will be saved.
        """
        collection=self.collection
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
        

    def calculate_TFIDF(self):
        # Calculate the TF-IDF score for each term-document pair in the collection
        
        #Print the number of terma in the collection
        print(f"Number of terms in the collection: {self.collection.count_documents({})}")
        # Calculate IDF for each term
        for term_entry in tqdm(self.collection.find(), desc="Calculating IDF"):
            # Calculate IDF for the term
            doc_freq = len(term_entry['documents'])
            idf = math.log(self.total_docs / (1 + doc_freq))
            # Update the term's IDF in the collection
            self.collection.update_one({"term": term_entry['term']}, {"$set": {"idf": idf}})
        
        # For each term in the collection
        for term_entry in tqdm(self.collection.find(), desc="Calculating TF-IDF scores"):
            # Create a list to store the updates for the term
            updates = []
            # For each document in the term's document list
            for doc in term_entry['documents']:
                # Calculate the TF-IDF score for the term in the document
                tfidf = (1 + math.log(doc['tf'])) * term_entry['idf']
                # Create an update dictionary for the document
                update = UpdateOne(
                {"term": term_entry['term'], "documents.document_id": doc['document_id']},
                {"$set": {"documents.$.tfidf": tfidf}}
                )
                # Append the update dictionary to the list of updates
                updates.append(update)
            # Update all documents for the term at once
            if updates:  # Ensure there are operations to execute
                self.collection.bulk_write(updates)
        if updates:  # Ensure there are operations to execute
                self.collection.bulk_write(updates)
        
        # for term_entry in self.collection.find():
        #     # Iterate over each document in the term's document list
        #     for doc in term_entry['documents']:
        #         # Calculate the TF-IDF score for the term in the document
        #         tfidf = doc['tf'] * term_entry['idf']
        #         # Update the document's TF-IDF score in the collection
        #         self.collection.update_one({"term": term_entry['term'], "documents.document_id": doc['document_id']}, {"$set": {"documents.$.tfidf": tfidf}})
    # Add more methods as needed, e.g., for querying the index, handling updates, etc.