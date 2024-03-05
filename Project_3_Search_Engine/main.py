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


Index = InverseIndex(directory_path=root/'webpages/WEBPAGES_RAW')
# Index = InverseIndex(directory_path=root/'webpages/tiny_test')
# Index.calculate_TFIDF()
# Index.save_index_to_file()

Index.build_index()


# Run the GUI
# root = tk.Tk()
# app = SearchEngineGUI(root)
# root.mainloop()

# #outut url_endings to json file
# with open('url_endings.json', 'w') as file:
#     json.dump(url_endings, file, indent=4)

if __name__ == '__main__':
    # Add your code here to run when the script is executed directly
    pass
