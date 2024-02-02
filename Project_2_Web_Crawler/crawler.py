import logging
import re
from urllib.parse import urlparse, urlunparse
from urllib.parse import urldefrag, urljoin
import urllib.request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import pickle
from collections import Counter

logger = logging.getLogger(__name__)

class Crawler:
    """
    This class is responsible for scraping urls from the next available link in frontier and adding the scraped links to
    the frontier
    """

    def __init__(self, frontier, corpus):
        # Initialize the Crawler with a frontier
        self.frontier = frontier
        # Initialize the Crawler with a corpus
        self.corpus = corpus
        # Initialize the Crawler with a boolean to check if the URL is a trap
        self.is_trap = False
        # Initialise a dictionary of comon stop words to skip for the analitics of the website content from the pkl file
        with open('stop_words_dict.pkl', 'rb') as file:
            self.stopwords = pickle.load(file)


# add the words in the coment above into a dictionary to check if the word is a stop word

        

    def start_crawling(self):
        """
        This method starts the crawling process which is scraping urls from the next available link in frontier and adding
        the scraped links to the frontier
        """
        while self.frontier.has_next_url():
            url = self.frontier.get_next_url()
            if url not in self.frontier.visited_pages:
                self.frontier.visited_pages[url] = {
                    'word_count': 0,
                    'total_valid_out_links': 0,
                    'valid_out_links': [],
                }
            logger.info("Fetching URL %s ... Fetched: %s, Queue size: %s", url, self.frontier.fetched, len(self.frontier))
            url_data = self.corpus.fetch_url(url)

            for next_link in self.extract_next_links(url_data):
                if self.is_valid(next_link):
                    if self.corpus.get_file_name(next_link) is not None:
                        self.frontier.visited_pages[url]['total_valid_out_links'] += 1
                        self.frontier.visited_pages[url]['valid_out_links'].append(next_link)
                        self.frontier.add_url(next_link)

    def extract_next_links(self, url_data):
        """
        The url_data coming from the fetch_url method will be given as a parameter to this method. url_data contains the
        fetched url, the url content in binary format, and the size of the content in bytes. This method should return a
        list of urls in their absolute form (some links in the content are relative and needs to be converted to the
        absolute form). Validation of links is done later via is_valid method. It is not required to remove duplicates
        that have already been fetched. The frontier takes care of that.

        Suggested library: lxml
        
        url: the requested url to be downloaded
        content: the content of the downloaded url in binary format. None if url does not exist in the corpus
        size: the size of the downloaded content in bytes. 0 if url does not exist in the corpus
        content_type: Content-Type from the response http headers. None if the url does not exist in the corpus
or content-type wasn't provided
        http_code: the response http status code. 404 if the url does not exist in the corpus
        is_redirected: a boolean indicating if redirection has happened to get the final response
        final_url: the final url after all of the redirections. None if there was no redirection.
        
        """
        outputLinks = []  # Initialize empty list for URLs

        url = url_data['url']  # Extract the URL from url_data
        content = url_data['content']  # Extract the HTML content from url_data
        http_code = url_data['http_code']  # Extract the HTTP status code
        content_type = url_data.get('content_type', '')  # The Content-Type of the response
        is_redirected = url_data.get('is_redirected', False)  # Flag for redirection
        final_url = url_data.get('final_url', url)  # The final URL after redirection

        # Initialize soup as None to handle the case when it's not set
        soup = None

        if http_code == 200 and content:  # Check if the HTTP status code is OK and content is not empty
            # Check if content_type is not None and contains 'html'
            if content_type and 'html' in content_type:
                # Parse the content using BeautifulSoup
                soup = BeautifulSoup(content, "html.parser")

                # Determine the base URL for resolving relative URLs
                base_url = final_url if is_redirected else url


            # Proceed only if soup has been successfully created
        if soup:
            for link_tag in soup.find_all('a', href=True):
                href = link_tag.get('href')  # Extract the href attribute
                href, _ = urldefrag(href)  # Remove fragment from URL if any

                # Parse the href to check if it's relative or absolute
                parsed_href = urlparse(href)
                # If href is relative, make it absolute
                if not parsed_href.netloc:
                    href = urljoin(base_url, parsed_href.geturl())
                # If href lacks a scheme, use the scheme from the base URL
                elif not parsed_href.scheme:
                    parsed_href = parsed_href._replace(scheme=urlparse(base_url).scheme)
                    href = parsed_href.geturl()

                # Add the absolute URL to the set of output links

                outputLinks.append(href)  # Add the absolute URL to the list
            
            # Extract the text from the HTML content
            text = soup.get_text()
            text = re.sub(r'\s+', ' ', text)
            text = re.sub(r'\W', ' ', text)
            text = text.lower()
            text = text.split()
            #Count the words in the text
            self.frontier.visited_pages[url]['word_count'] = len(text)
            for word in text:
                if word not in self.stopwords:
                    self.frontier.words_freq[word] = self.frontier.words_freq.get(word, 0) + 1
            


        return outputLinks  # Return the list of unique URLs, but first removes duplicates

    def is_valid(self, url):
        """
        Function returns True or False based on whether the url has to be fetched or not. This is a great place to
        filter out crawler traps. Duplicated urls will be taken care of by frontier. You don't need to check for duplication
        in this method
        
        
        Filter out crawler traps (e.g. the ICS calendar, dynamic URL’s, etc.), Additionally crawler traps include history based
        trap detection where based on your practice runs you will determine if there are sites that you have crawled that
        are traps, continuously repeating sub-directories and very long URLs. You will need to do some research online but
        you will provide information on the type of trap detection you implemented and why you implemented it that
        way.(DO NOT HARD CODE URLS YOU THINK ARE TRAPS, ie regex urls, YOU SHOULD USE LOGIC TO FILTER THEM
        OUT)
        """
        # Initialize the Crawler with a boolean to check if the URL is a trap
        self.is_trap = False
        
        trap_types = []
        
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        try:
            if ".ics.uci.edu" not in parsed.hostname \
                or \
                re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
                + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
                + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
                + "|thmx|mso|arff|rtf|jar|csv" \
                + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower()):
                return False
            
            
            # return ".ics.uci.edu" in parsed.hostname \
            #        and not re.match(".*\.(css|js|bmp|gif|jpe?g|ico" + "|png|tiff?|mid|mp2|mp3|mp4" \
            #                         + "|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf" \
            #                         + "|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso|epub|dll|cnf|tgz|sha1" \
            #                         + "|thmx|mso|arff|rtf|jar|csv" \
            #                         + "|rm|smil|wmv|swf|wma|zip|rar|gz|pdf)$", parsed.path.lower())

        except TypeError:
            print("TypeError for ", parsed)
            return False
        
        
        #Use fetch corpus.fetch_url(url) to get try to get robots.txt file and check if the url is allowed to be crawled
        
        # robots = self.corpus.fetch_url(urlparse(url).scheme + "://" + urlparse(url).netloc + "/robots.txt")
        # if robots['http_code'] != 404:
        #     with open('robots.txt', 'w') as f:
        #         f.write(str(robots)) #NO ROBOT FILE???
        
        
        # History traps detection implemented
        # Checking long urls implemented
        if len(url) > 500:  # Check if the URL is too long
            self.is_trap = True
            trap_types.append('long_url')

        # Check for repeating subdirectories
        matches = re.findall(r'(/[^/]+)', parsed.path)
        counter = Counter(matches)
        repeats = [key for key, value in counter.items() if value > 1]

        if repeats:
            self.is_trap = True
            trap_types.append('repeating_subdirectories')


        # Split the path into segments
        #segments = parsed.path.split('/')
        segments = re.split(r'[/.-_]', parsed.path)  
        # Check for a similar URL with a different number
        
        # Create a copy of segments for manipulation
        segments_copy = segments.copy()
        numeric_segments = set()

        # Replace all numeric segments of size 2 or more with a placeholder
        for i, segment in enumerate(segments_copy):
            if segment.isdigit() and len(segment) >= 2:
                segments_copy[i] = '{}'
                numeric_segments.add(segment)

        # Create a URL pattern from the modified segments
        url_pattern = '/'.join(segments_copy)

        # If the URL pattern has been encountered before
        if url_pattern in self.frontier.url_patterns:
            self.is_trap = True
            trap_types.append('similar_url_different_number')
        elif numeric_segments:
            #Join the numeric segments
            numeric_segment = '/'.join(numeric_segments)
            # Add the original URL pattern to the set of encountered patterns
            if url_pattern not in self.frontier.url_patterns:
                self.frontier.url_patterns[url_pattern] = []
            self.frontier.url_patterns[url_pattern].append(numeric_segment)

        # Checking for dynamic urls implemented query 
        # URLs with query parameters (containing a ? and/or a &) 
        # Session IDs
        if re.search(r'[?&%](utm\_source|sessionid|sid|phpsessid|jsessionid|st|v|m|vl|ti|z|version|id)=', url):
            self.is_trap = True
            trap_types.append('session_id')

        


        # If the URL is a trap, add it to the list of traps
        if self.is_trap:
            self.frontier.trap_urls[url] = trap_types
            return False
        
        return True
    

def normalize_url(url):
    # Parse URL and remove query string and fragment
    parsed_url = urlparse(url)
    normalized_url = parsed_url._replace(query="", fragment="").geturl()
    # Standardize casing and remove trailing slash if present
    normalized_url = normalized_url.lower().rstrip('/')
    return normalized_url
