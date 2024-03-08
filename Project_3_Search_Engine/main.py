import pyprojroot
from pymongo import MongoClient

root = pyprojroot.here()
root = root/'Project_3_Search_Engine'
src = root/'src'
Test = root/'test'

import sys
sys.path.append(str(root))

from src.Index import InverseIndex
from urllib.parse import urlparse
import tkinter as tk
from src.gui import SearchEngineGUI
from src.query import MongoDBSearch
import json
import os


Index = InverseIndex(directory_path=root/'webpages/WEBPAGES_RAW')

with open(os.path.join(Index.directory_path, "bookkeeping.json"), 'r', encoding='utf-8') as file:
    data = json.load(file)
# Index = InverseIndex(directory_path=root/'webpages/tiny_test')
# Index.calculate_TFIDF()
# Index.save_index_to_file()

# Index.build_index()
# Index.collection.create_index([("_id.documents.document_id", 1)]) 
# Sort the database alphabetically _id
# Index.collection.create_index([("_id", 1)])


# Run the GUI
# root = tk.Tk()
# app = SearchEngineGUI(root)
# root.mainloop()

# Runn the search
search = MongoDBSearch()
#print (search.query_vector("hello world"))
ranked_docs = search.search("machine learning")  # Assuming search_instance is an instance of your MongoDBSearch class

# Check if there are at least 20 documents, if not, take the length of ranked_docs
top_n = 20 if len(ranked_docs) >= 20 else len(ranked_docs)

print(f"Top {top_n} Documents:")
for i in range(top_n):
    doc_id, similarity_score = ranked_docs[i]  # Unpack the tuple
    print(f"{i+1}. Document ID: {doc_id}, Document URL {data[doc_id]}, Similarity Score: {similarity_score}")
    
    
# Print the bottom 5 documents
print(f"\nBottom 5 Documents:")
for i in range(-5, 0):
    doc_id, similarity_score = ranked_docs[i]  # Unpack the tuple
    print(f"{i+1}. Document ID: {doc_id}, Similarity Score: {similarity_score}")
    

# #outut url_endings to json file
# with open('url_endings.json', 'w') as file:
#     json.dump(url_endings, file, indent=4)

if __name__ == '__main__':
    # Add your code here to run when the script is executed directly
    pass
