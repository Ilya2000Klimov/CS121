import unittest
from pymongo import MongoClient

import pyprojroot

root = pyprojroot.here()
root = root/'Project_3_Search_Engine'
src = root/'src'
Test = root/'test'

import sys
sys.path.append(str(root))

from src.Index import InverseIndex

class TestInverseIndex(unittest.TestCase):
    def setUp(self):
        # Create a test instance of InverseIndex with a test database and collection
        self.index = InverseIndex(db_name='testDB', collection_name='testCollection', directory_path=root/'webpages'/'test_webpages')
        
        #Clear the collection
        #self.index.collection.delete_many({})

    def test_calculate_tf(self):
        # Test the calculate_tf method with some example inputs
        self.assertEqual(self.index.calculate_tf(5, 10), 0.5)
        self.assertEqual(self.index.calculate_tf(0, 10), 0.0)
        self.assertEqual(self.index.calculate_tf(10, 10), 1.0)

    def test_update_index(self):
        # Test the update_index method with a new term
        self.index.update_index('testTerm', 'testDoc', 0.5)
        term_entry = self.index.collection.find_one({"term": 'testTerm'})
        self.assertIsNotNone(term_entry)
        self.assertEqual(term_entry['documents'][0]['document_id'], 'testDoc')
        self.assertEqual(term_entry['documents'][0]['tf'], 0.5)

        # Test the update_index method with an existing term
        self.index.update_index('testTerm', 'testDoc2', 0.6)
        term_entry = self.index.collection.find_one({"term": 'testTerm'})
        self.assertEqual(len(term_entry['documents']), 2)
        self.assertEqual(term_entry['documents'][1]['document_id'], 'testDoc2')
        self.assertEqual(term_entry['documents'][1]['tf'], 0.6)
        
    # def test_save_index_to_file(self):
    #     # Test the save_index_to_file method
    #     self.index.save_index_to_file(Test/'test_index.json')
    #     self.assertTrue((Test/'test_index.json').exists())

    # def test_load_index_from_file(self):
    #     # Test the load_index_from_file method
    #     self.index.save_index_to_file(Test/'test_index.json')
    #     self.index.collection.delete_many({})
    #     self.index.load_index_from_file(Test/'test_index.json')
    #     self.assertTrue(self.index.collection.count_documents({}) > 0)
        
        
    def test_index_document(self):
        # Test the index_document method
        self.index.index_document(root/'webpages'/'test_webpages'/'1'/'1', '1')
        term_entry = self.index.collection.find_one({"term": 'bren'})
        self.assertIsNotNone(term_entry)
        
    def test_build_index(self):
        # Test the build_index method
        self.index.build_index()
        self.assertTrue(self.index.total_docs > 0)
        self.assertTrue(self.index.collection.count_documents({}) > 0)

    # Test calculate_TFIDF method
    def test_calculate_TFIDF(self):
        # Test the calculate_TFIDF method
        self.index.update_index('testTerm', 'testDoc', 0.5)
        self.index.calculate_TFIDF()
        term_entry = self.index.collection.find_one({"term": 'testTerm'})
        self.assertEqual(term_entry['documents'][0]['tfidf'], 0.5)
           
    # def test_update_index(self):
    #     # Test the update_index method
    #     self.index.update_index('testTerm', 'testDoc', 0.5)
    #     term_entry = self.index.collection.find_one({"term": 'testTerm'})
    #     self.assertIsNotNone(term_entry)
    #     self.assertEqual(term_entry['documents'][0]['document_id'], 'testDoc')
    #     self.assertEqual(term_entry['documents'][0]['tf'], 0.5)

    #     self.index.update_index('testTerm', 'testDoc2', 0.6)
    #     term_entry = self.index.collection.find_one({"term": 'testTerm'})
    #     self.assertEqual(len(term_entry['documents']), 2)
    #     self.assertEqual(term_entry['documents'][1]['document_id'], 'testDoc2')
    #     self.assertEqual(term_entry['documents'][1]['tf'], 0.6)

    # Add more tests as needed for the other methods in your class

if __name__ == '__main__':
    unittest.main()