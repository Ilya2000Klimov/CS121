import unittest
from collections import Counter
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

import pyprojroot

root = pyprojroot.here()
root = root/'Project_3_Search_Engine'
src = root/'src'
Test = root/'test'

import sys
sys.path.append(str(root))

from src.PageParser import Parser

class TestParser(unittest.TestCase):
    def setUp(self):
        self.parser = Parser()
        self.test_text = "Test paragraph. Some random words. Test-words/with.different_separators"

    def test_process_token(self):
        result = self.parser.process_token('Testing')
        self.assertEqual(result, 'test')

    def test_tokenize(self):
        result = self.parser.tokenize(self.test_text)
        expected_result = ['test', 'paragraph', 'some', 'random', 'words', 'test-words/with', 'different_separators', 'test-words', 'with.different_separators', 'test', 'words/with.different_separators', 'test-words/with.different', 'separators', 'test', 'words', 'with', 'different_separators', 'test-words/with.different_separators']
        self.assertEqual(result, expected_result)

    def test_parse_document(self):
        test_html = """
        <html>
            <head>
                <title>Test Title</title>
            </head>
            <body>
                <h1>Test Header 1</h1>
                <h2>Test Header 2</h2>
                <p>Test paragraph. Some random words.</p>
                <b>Test bold text</b>
                <strong>Test strong text</strong>
            </body>
        </html>
        """
        test_file_path = 'test.html'
        with open(test_file_path, 'w') as file:
            file.write(test_html)

        result = self.parser.parse_document(test_file_path)
        expected_result = [
            ('test', 10+6+5+2+3+3), 
            ('titl', 10), 
            ('header', 6+5), 
            ('paragraph', 2), 
            ('random', 2), 
            ('word', 2), 
            ('bold', 3), 
            ('text', 3+3),
            ('strong', 3),
        ]
        self.assertEqual(Counter(dict(result)), Counter(dict(expected_result)))

        import os
        os.remove(test_file_path)

if __name__ == '__main__':
    unittest.main()