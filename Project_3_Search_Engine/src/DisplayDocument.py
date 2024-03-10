from bs4 import BeautifulSoup
from bs4 import MarkupResemblesLocatorWarning
import re
import json
import os
import warnings
import sys
from pymongo import MongoClient, UpdateOne
import tqdm

import pyprojroot
root = pyprojroot.here()
root = root/'Project_3_Search_Engine'


        
class DisplayDocument:
    def __init__(self, db_uri='localhost', db_port=27017, db_name='searchEngine', collection_name='DisplayDocuments', directory_path=root/'webpages/WEBPAGES_RAW'):
        self.directory_path = directory_path
        with open(os.path.join(directory_path, "bookkeeping.json"), 'r', encoding='utf-8') as file:
            self.data = json.load(file)
        self.client = MongoClient(db_uri, db_port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def upload_documents(self):
        operations = []
        for doc_id, url in tqdm.tqdm(self.data.items(), desc="Uploading Documents"):
            file_path = os.path.join(self.directory_path, doc_id)
            doc_info = self.extract_info(file_path, doc_id, url)
            operations.append(UpdateOne({'_id': doc_id}, {'$set': doc_info}, upsert=True))

            if len(operations) >= 1000:  # Perform the bulk operation in batches of 1000
                self.collection.bulk_write(operations)
                operations = []

        if operations:  # Ensure any remaining operations are executed
            self.collection.bulk_write(operations)

    def extract_info(self, file_path, doc_id, url):
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()

        soup = BeautifulSoup(file_content, 'html.parser' if '<html' in file_content.lower() else 'xml')
        text = ' '.join(soup.stripped_strings)
        summary = ' '.join(text.split()[:30])  # Get the first 30 words

        # Check if title exists and has a non-empty string, otherwise use the first 10 words of text
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        else:
            title = ' '.join(text.split()[:10])

        return {'_id': doc_id, 'title': title, 'url': url, 'summary': summary}



if __name__ == '__main__':
    display_doc = DisplayDocument()
    display_doc.upload_documents()