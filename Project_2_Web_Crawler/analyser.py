#import libraries
import pickle
from urllib.parse import urlparse
import re
from collections import Counter



def analitics_analysis():
    # Load analitics from pkl files
    with open("frontier_state/url_patterns.pkl", "rb") as file:
        url_patterns = pickle.load(file)
    with open("frontier_state/words_freq.pkl", "rb") as file:
        words_freq = pickle.load(file)
    with open("frontier_state/trap_urls.pkl", "rb") as file:
        trap_urls = pickle.load(file)
    with open("frontier_state/subdomains.pkl", "rb") as file:
        subdomains = pickle.load(file)
    with open("frontier_state/word_freq.pkl", "rb") as file:
        visited_pages = pickle.load(file)

        # Open the output file
        with open('analysis.txt', 'w') as f:
            # Write 50 most common words
            f.write("50 most common words:\n")
            f.write(str(words_freq.most_common(50)))
            f.write("\n\n")

            # Write subdomains in descending order
            f.write("Subdomains in descending order:\n")
            # Sort subdomains
            subdomains = dict(sorted(subdomains.items(), key=lambda item: item[1], reverse=True))
            f.write(str(subdomains))
            f.write("\n\n")

            # Write trap urls by type
            f.write("Trap urls by type:\n")
            # Sort trap urls by type
            trap_urls = sorted(trap_urls.items(), key=lambda x: x[1], reverse=True)
            f.write(str(trap_urls))
            f.write("\n\n")

if __name__ == "__main__":
    analitics_analysis()


    