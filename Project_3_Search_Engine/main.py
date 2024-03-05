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


Index = InverseIndex(directory_path=root/'webpages/WEBPAGES_RAW')
# Index = InverseIndex(directory_path=root/'webpages/tiny_test')
# Index.calculate_TFIDF()
# Index.save_index_to_file()

Index.build_index()

# connect to the mongodb
client = MongoClient('localhost', 27017)
from nltk.stem import PorterStemmer, WordNetLemmatizer

db = client['searchEngine']
collection = db['Index']

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

#Find the 20 documents with the highest TFIDF score for term irvine
term = 'irvine'
term = lemmatizer.lemmatize(stemmer.stem(term.lower()))

print(term)

# Find the irvine term in the index
pipeline = [
    {"$match": {"term": term}},  # Replace "yourTerm" with the actual term you're interested in
    {"$unwind": "$documents"},
    {"$sort": {"documents.tf": -1}},
    {"$limit": 20},
    {"$group": {
        "_id": "$_id",
        "term": {"$first": "$term"},
        "documents": {"$push": "$documents"}
    }}
]

# Execute the query
results = collection.aggregate(pipeline)

# Print the results
for result in results:
    print(result)

# # Open /home/ilya2k/Documents/CS121/Project_3_Search_Engine/webpages/WEBPAGES_RAW/bookkeeping.json and output all url endings
# import json
# import os

# with open(root/'webpages/WEBPAGES_RAW/bookkeeping.json', 'r', encoding='utf-8') as file:
#     data = json.load(file)
# url_endings = [] # list of touples (url_ending, count)

# for key, url in data.items():
#     # print url endings
#     parsed_url = urlparse(url)
#     path = parsed_url.path
#     # Get the ending part of the path
#     ending = path.split('/')[-1]
#     #if ending not in url_endings: add it to the list with a count of one
#     if ending not in [x[0] for x in url_endings]:
#         url_endings.append((ending, 1))
#     else: # if ending in url_endings: increment the count
#         for i in range(len(url_endings)):
#             if url_endings[i][0] == ending:
#                 url_endings[i] = (url_endings[i][0], url_endings[i][1] + 1)
# #outut url_endings to json file
# with open('url_endings.json', 'w') as file:
#     json.dump(url_endings, file, indent=4)

if __name__ == '__main__':
    # Add your code here to run when the script is executed directly
    pass
