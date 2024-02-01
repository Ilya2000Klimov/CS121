import pickle
from stopwords import stopwords

if __name__ == "__main__":
    
    # Specify the path for the .pkl file where the dictionary will be saved
    pkl_file_path = 'stop_words_dict.pkl'

    # Serialize the dictionary and write it to the .pkl file
    with open(pkl_file_path, 'wb') as file:
       pickle.dump(stopwords, file)

    print(f"Dictionary has been saved to {pkl_file_path}")