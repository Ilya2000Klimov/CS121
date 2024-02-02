#import libraries
import pickle
from urllib.parse import urlparse
import re
from collections import Counter


def analytics_analysis():
    # Load analytics from pickle files
    with open("frontier_state/url_patterns.pkl", "rb") as file:
        url_patterns = pickle.load(file)
    with open("frontier_state/word_freq.pkl", "rb") as file:
        words_freq = pickle.load(file)
    with open("frontier_state/trap_urls.pkl", "rb") as file:
        trap_urls = pickle.load(file)
    with open("frontier_state/subdomains.pkl", "rb") as file:
        subdomains = pickle.load(file)
    with open("frontier_state/visited_pages.pkl", "rb") as file:
        visited_pages = pickle.load(file)

    #visited pages
    # 'http://archive.ics.uci.edu/ml/datasets.html?format=mat&task=clu&att=&area=&numAtt=greater100&numIns=&type=&sort=dateUp&view=table': {'word_count': 0, 'total_valid_out_links': 0, 'valid_out_links': []}

    # Identify the page with the most valid outlinks
    #max_outlinks_page, max_outlinks_count = max(visited_pages.items(), key=lambda item: item[1]['outlinks_count']) if visited_pages else (None, 0)

    # Identify the longest page in terms of word count
    #longest_page, longest_page_word_count = max(visited_pages.items(), key=lambda item: item[1]['word_count']) if visited_pages else (None, 0)

    # Opening the output file
    with open('analysis.txt', 'w') as f:

        max_outlinks_page = get_page_with_most_outlinks(visited_pages)
        max_outlinks_count = visited_pages[max_outlinks_page]['total_valid_out_links']

        # Page with the most valid outlinks
        f.write(f"\nPage with the most valid outlinks: {max_outlinks_page} ({max_outlinks_count} links)\n")

        longest_page = get_longest_page(visited_pages)
        longest_page_word_count = visited_pages[longest_page]['word_count']

        # Longest page in terms of word count
        f.write(f"\nLongest page by word count: {longest_page} ({longest_page_word_count} words)\n")


        # Write 50 most common words
        f.write("\n50 most common words:\n")
        for i, (word, count) in enumerate(sorted(words_freq.items(), key=lambda item: item[1], reverse=True)[:50]):
            f.write(f"{word}: {count}\t\t")
            if (i+1) % 5 == 0:
                f.write("\n")


        # Write 50 most common subdomains in descending order
        f.write("\n50 most common subdomains and URL count in descending order:\n")
        for subdomain, count in sorted(subdomains.items(), key=lambda item: item[1], reverse=True)[:50]:
            f.write(f"{subdomain}: {count}\n")

        #Write ten longest urls
        f.write("\nTen longest URLs by word count:\n")
        for url, data in get_10_longest_urls(visited_pages):
            f.write(f"{url}: {data['word_count']}\n")

        # Write trap urls by type 
        f.write("\nTrap URLs by type:\n")
        # Create a list of tuples and sort it by trap types
        sorted_trap_urls = sorted(trap_urls.items(), key=lambda item: item[1])

        for url, trap_types in sorted_trap_urls:
            f.write(f"{url}: {', '.join(trap_types)}\n")

def get_page_with_most_outlinks(visited_pages):
    max_outlinks = 0
    page_with_most_outlinks = None

    for page, data in visited_pages.items():
        if data['total_valid_out_links'] > max_outlinks:
            max_outlinks = data['total_valid_out_links']
            page_with_most_outlinks = page

    return page_with_most_outlinks

def get_longest_page(visited_pages):
    max_word_count = 0
    longest_page = None

    for page, data in visited_pages.items():
        if data['word_count'] > max_word_count:
            max_word_count = data['word_count']
            longest_page = page

    return longest_page

def get_10_longest_urls(visited_pages):
    # Sort the pages by the length of the URL and return 10 longest URLs
    return sorted(visited_pages.items(), key=lambda item: len(item[0]), reverse=True)[:10]


if __name__ == "__main__":
    analytics_analysis()



    