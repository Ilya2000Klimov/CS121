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
from pathlib import Path
from pymongo import MongoClient, UpdateOne
import json

class InverseIndex:
    def __init__(self, db_uri='localhost', db_port=27017, db_name='searchEngine', collection_name='Index', directory_path=root/'webpages/WEBPAGES_RAW'):
        self.client = MongoClient(db_uri, db_port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        self.documents = self.db['Documents']
        #self.collection.create_index([("terms"), ("document_id")])
        self.collection.create_index("_id")
        self.collection.create_index("documents.document_id")
        self.documents.create_index("_id")
        self.total_docs = 0
        self.directory_path = directory_path

    def calculate_tf(self, term_freq, doc_length):
        # Calculate Term Frequency (TF)
        return term_freq / doc_length



    def index_document(self, file_path, doc_id):
        # Parse the document, calculate metrics, and update the index for each term in the document
        parser = PageParser(self.directory_path)
        document_data = parser.parse_document(file_path, doc_id)
        doc_length = document_data['doc_size']
        
        # Convert dict_items to dictionary
        token_frequency = dict(document_data['token_frequency'])
        
        # Push document_data to document collection
        document_data = {
            'doc_term_weight': sum(token_frequency.values()),
            'doc_length': doc_length,
            'token_frequency': list(token_frequency.items()),
            'is_html': document_data["is_html"],
            'url': document_data["url"],
            'hrefs': document_data["hrefs"]
        }
        self.documents.update_one(
            {'_id': doc_id},
            {'$set': document_data},
            upsert=True
        )
        
        
        # Prepare a list for bulk operations
        bulk_operations = []

        for term, term_freq in document_data['token_frequency']:
            tf = term_freq #self.calculate_tf(term_freq, doc_length)
            doc_ref = {"document_id": doc_id, "tf": tf, "tfidf": 0}

            # Prepare the update operation
            update_operation = UpdateOne(
                {"_id": term},
                {
                    "$push": {"documents": doc_ref}
                },
                upsert=True  # This ensures that if the term does not exist, it will be inserted
            )

            # Add the operation to the list
            bulk_operations.append(update_operation)

        # Execute all the operations in bulk
        if bulk_operations:
            self.collection.bulk_write(bulk_operations)
        
        

    
    # Implement the logic to build the index for all documents in a directory
    def build_index(self):
        directory_path = Path(self.directory_path)
        #for each subdirectory in the passed in directory directory in the 
        for dir in directory_path.iterdir(): #, desc=f"Indexing documents"):
            # Iterate over each file in the directory
            if dir.is_dir():
                parent_directory_path = Path(directory_path).parent
                # print(f"Indexing files in {os.path.relpath(dir, parent_directory_path)}")
                for file in tqdm(dir.iterdir(), desc=f"Indexing files in {os.path.relpath(dir, parent_directory_path)}"):
                    file_path = file
                    # print(f"[{file_path.name}]", end="")
                    doc_id = os.path.relpath(file_path, directory_path)
                    self.index_document(file_path, doc_id)
                    self.total_docs += 1
        
        # directory_path = Path(self.directory_path)
        # for file_path in directory_path.rglob('*/*'): #, desc=f"Indexing documents"):
        #     print(f"Indexing file: {file_path}") 
        #     # print(f"[Indexing files in {dir}]", end="")
        #     # Iterate over each file in the directory
        #     for file in file_path.parent.iterdir(): #, desc=f"Indexing {dir}"):
        #         file_path = file
        #         doc_id = os.path.relpath(file_path, directory_path)  # Use relative path as a unique identifier
        #         self.index_document(file_path, doc_id)
        #         self.total_docs += 1
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
                
        docs=self.documents
        # Open the file in write mode
        with open('docs.json', 'w', encoding='utf-8') as file:
            # Iterate over all documents in the collection
            for document in docs.find():
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
        

    def calculate_TFIDF(self, batch_size=100):
        # Calculate the TF-IDF score for each term-document pair in the collection
        
        #Print the number of terma in the collection
        print(f"Number of terms in the collection: {self.collection.count_documents({})}")
        # Calculate IDF for each term
        for term_entry in tqdm(self.collection.find(), desc="Calculating IDF"):
            # Calculate IDF for the term
            doc_freq = len(term_entry['documents'])
            idf = math.log(self.total_docs / doc_freq + 1)
            # Update the term's IDF in the collection
            self.collection.update_one({"_id": term_entry['_id']}, {"$set": {"idf": idf}})
        
        
        
        # Determine the total number of terms to process
        total_terms = self.collection.count_documents({})
        
        # Calculate the number of batches needed
        num_batches = (total_terms + batch_size - 1) // batch_size
        
        
        for batch_num in range(num_batches):
            # Calculate the skip and limit for the current batch
            skip = batch_num * batch_size
            limit = batch_size
            
            # Fetch the batch of term entries
            batch_term_entries = self.collection.find({}).skip(skip).limit(limit)
            
            updates = []  # List to store the updates for the current batch
            for term_entry in tqdm(batch_term_entries, desc=f"Processing batch {batch_num + 1}/{num_batches}"):
                
                for doc in term_entry['documents']:
                    # Calculate the TF-IDF score
                    tfidf = (1 + math.log(doc['tf'])) * term_entry['idf']
                    
                    # Prepare the update operation
                    update = UpdateOne(
                        {"_id": term_entry['_id'], "documents.document_id": doc['document_id']},
                        {"$set": {"documents.$.tfidf": tfidf}}
                    )
                    updates.append(update)
                
            # Execute the bulk update for the current batch
            print(f"Bulk write", end="")
            if updates:
                self.collection.bulk_write(updates)
                # empty updates list
                updates = []
            print(" complete")
    
    def process_term_entry(self, term_entry):
        updates = []
        for doc in term_entry['documents']:
            tfidf = (1 + math.log(doc['tf'])) * term_entry['idf']
            update = UpdateOne(
                {"_id": term_entry['_id'], "documents.document_id": doc['document_id']},
                {"$set": {"documents.$.tfidf": tfidf}}
            )
            updates.append(update)
        return updates