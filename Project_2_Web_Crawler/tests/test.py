import unittest
from unittest.mock import Mock
import sys
sys.path.append("..")

from crawler import check_similar_url_different_number
from frontier import *
from unittest.mock import Mock
import unittest

class TestCheckSimilarUrlDifferentNumber(unittest.TestCase):
    def setUp(self):
        self.frontier = Frontier()

    def test_no_numeric_segments(self):
        url = "http://www.ics.uci.edu/test.html"
        self.assertFalse(check_similar_url_different_number(url, self.frontier))

    def test_single_numeric_segment(self):
        url = "http://www.ics.uci.edu/test/123.html"
        self.assertFalse(check_similar_url_different_number(url, self.frontier))

    def test_multiple_numeric_segments(self):
        url = "http://www.ics.uci.edu/test/123/456.html"
        self.assertFalse(check_similar_url_different_number(url, self.frontier))

    def test_repeated_url_pattern(self):
        url1 = "http://www.ics.uci.edu/test/123.html"
        url2 = "http://www.ics.uci.edu/test/456.html"
        check_similar_url_different_number(url1, self.frontier)
        self.assertTrue(check_similar_url_different_number(url2, self.frontier))

    def test_different_url_pattern(self):
        url1 = "https://wics.ics.uci.edu/events/2019-02-01/ "
        url2 = "https://wics.ics.uci.edu/events/2020-06-03/ "
        url3 = "https://wics.ics.uci.edu/events/2022-637-033/ "
        url4 = "https://wics.ics.uci.edu/events/2220-543-03453/ "
        check_similar_url_different_number(url1, self.frontier)
        check_similar_url_different_number(url3, self.frontier)
        check_similar_url_different_number(url4, self.frontier)
        check = check_similar_url_different_number(url2, self.frontier)
        #write pattern to a file
        # with open('patterns.txt', 'w') as f:
        #     for pattern in self.frontier.url_patterns:
        #         f.write(f"{pattern}\n")
        print(self.frontier.url_patterns)
                
        self.assertTrue(check)

class test_check_same_url_different_dinamic_parameter(unittest.TestCase):
    def setUp(self):
        self.frontier = Frontier()

    def test_no_dynamic_parameters(self):
        url = "http://www.ics.uci.edu/test.html"
        self.assertFalse(check_similar_url_different_number(url, self.frontier))

    def test_single_dynamic_parameter(self):
        url = "http://www.ics.uci.edu/test.html?param1=1"
        self.assertFalse(check_similar_url_different_number(url, self.frontier))

    def test_multiple_dynamic_parameters(self):
        url = "http://www.ics.uci.edu/test.html?param1=1&param2=2"
        self.assertFalse(check_similar_url_different_number(url, self.frontier))

    def test_repeated_url_pattern(self):
        url1 = "http://www.ics.uci.edu/test.html?param1=1"
        url2 = "http://www.ics.uci.edu/test.html?param2=2"
        check_similar_url_different_number(url1, self.frontier)
        self.assertTrue(check_similar_url_different_number(url2, self.frontier))

    def test_different_url_pattern(self):
        url1 = "https://wics.ics.uci.edu/events?date=2019-02-01 "
        url2 = "https://wics.ics.uci.edu/events?date=2020-06-03 "
        url3 = "https://wics.ics.uci.edu/events?date=2022-637-033 "
        url4 = "https://wics.ics.uci.edu/events?date=2220-543-03453 "
        check_similar_url_different_number(url1, self.frontier)
        check_similar_url_different_number(url3, self.frontier)
        check_similar_url_different_number(url4, self.frontier)
        check = check_similar_url_different_number(url2, self.frontier)
        #write pattern to a file
        # with open('patterns.txt', 'w') as f:
        #     for pattern in self.frontier.url_patterns:
        #         f.write(f"{pattern}\n")
        print(self.frontier.url_patterns)
                
        self.assertTrue(check)
if __name__ == '__main__':
    unittest.main()