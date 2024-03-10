from pymongo import MongoClient
import math
import tqdm

# Connect to the MongoDB server
client = MongoClient()

# Access the "searchEngine" database
db = client["searchEngine"]

# Access the "Documents" collection
documents_collection = db["Documents"]

# Access the "Index" collection
index_collection = db["Index"]

# Iterate over each document in the Documents collection
for document in documents_collection.find():
    # Extract the document length
    doc_length = document.get("doc_length", 1)  # Default to 1 to avoid division by zero

    # Initialize a list to store the updated token frequencies and their TF-IDF values
    updated_token_frequencies = []
    total_squared_sum = 0

    # Iterate over each term and its frequency in the document
    for token, frequency in document.get("token_frequency", []):
        # Calculate the updated term frequency (as a frequency by dividing by doc_length)
        updated_term_frequency = frequency / doc_length
        
        # Retrieve the corresponding IDF value for the term from the Index collection
        index_entry = index_collection.find_one({"_id": token})
        if index_entry:
            idf = index_entry.get("idf", 0)
            
            # Calculate the TF-IDF value for the term
            tfidf = (math.log(1 + updated_term_frequency)) * idf
            
            # Add the term and its TF-IDF value to the updated list
            updated_token_frequencies.append([token, tfidf])
            
            # Add the square of the TF-IDF value to the total sum for magnitude calculation
            total_squared_sum += math.pow(tfidf, 2)
        else:
            # If the term is not found in the Index collection, you might want to handle this case.
            # For now, we'll skip it.
            pass

    # Calculate the square root of the sum to get the magnitude
    magnitude = math.sqrt(total_squared_sum)

    # Update the document with the updated token frequencies (TF-IDF values) and the calculated magnitude
    documents_collection.update_one({'_id': document['_id']}, {'$set': {'token_frequency_tfidf': updated_token_frequencies, 'magnitude': magnitude}})

    # Print the magnitude for the current document
    print(f"Document ID: {document['_id']}, Magnitude: {magnitude}")
    
if __name__ == '__main__':
    # Add your code here to run when the script is executed directly
    pass