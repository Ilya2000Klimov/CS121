import unittest
from frontier import Frontier
from crawler import check_similar_url_different_number

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

if __name__ == '__main__':
    unittest.main()