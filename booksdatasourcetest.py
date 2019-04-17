"""
Oliver Staten
Professor Alexander
CS 257
4/12/19
books-2
"""

import booksdatasource
import unittest

"""
As of April 12, these tests are designed to fail because the functions in the file are not implemented.
The only ones that pass are the ones that want empty lists/dictionaries returned.  
In addition, there is still more room for more tests, but I think this is a good start.
"""

class BooksDataSourceTest(unittest.TestCase):
    
    """
    SetUp
    """
    
    def setUp(self):
        self.book_checker = booksdatasource.BooksDataSource("books.csv", "authors.csv", "books_authors.csv")
        print("setUp")
        
    def tearDown(self):
        pass
    
    """
    Tests for:
    book(self, book_id)
    """
    
    def test_book_identity_true(self):
        self.assertEqual(self.book_checker.book(5), {'id': 5, 'title': 'Emma', 'publication_year': 1815})
        print("test_book_identity_true")

    def test_book_identity_false(self):
        self.assertNotEqual(self.book_checker.book(7), {'id': 5, 'title': 'Emma', 'publication_year': 1815})
        print("test_book_identity_false")

    def test_no_exist_large_book(self):
        self.assertRaises(ValueError, self.book_checker.book, -14)
        print("test_no_exist_large_book")

    def test_no_exist_large_book(self):
        self.assertRaises(ValueError, self.book_checker.book, 35)
        print("test_no_exist_large_book")
        
    """
    Tests for:
    books(self, *, author_id=None, search_text=None, start_year=None, end_year=None, sort_by='title')
    """
    
    def test_bad_author_ID(self):
        self.assertRaises(ValueError, self.book_checker.books, author_id=-14)
        print("test_bad_author_ID")

    def test_valid_author_ID(self):
        self.assertEqual(self.book_checker.books(author_id=4), [{'id': 5, 'title': 'Emma', 'publication_year': 1815}, {'id': 18, 'title': 'Pride and Prejudice', 'publication_year': 1813}, {'id': 20, 'title': 'Sense and Sensibility', 'publication_year': 1813}])
        print("test_valid_author_ID")
        
    def test_valid_search_text_books(self):
        self.assertEqual(self.book_checker.books(search_text="Pride"), [{'id': 18, 'title': 'Pride and Prejudice', 'publication_year': 1813}])
        print("test_valid_search_text_books")
    
    def test_nonexistent_search_text_books(self):
        self.assertEqual(self.book_checker.books(search_text="jive turkey"), [])
        print("test_nonexistent_search_text_books")
                             
    def test_start_year_books(self):
        self.assertEqual(self.book_checker.books(start_year=2010), [{'id': 0, 'title': 'All Clear', 'publication_year': 2010}, {'id': 3, 'title': 'Blackout', 'publication_year': 2010}])
        print("test_start_year_books")
    
    def test_end_year_books(self):
        self.assertEqual(self.book_checker.books(end_year=1813), [{'id': 18, 'title': 'Pride and Prejudice', 'publication_year': 1813}, {'id': 20, 'title': 'Sense and Sensibility', 'publication_year': 1813}, {'id': 30, 'title': 'The Life and Opinions of Tristram Shandy, Gentleman', 'publication_year': 1759}])
        print("test_end_year_books")
        
    def test_impossible_end_start_year_books(self):
        self.assertEqual(self.book_checker.books(start_year=1991, end_year=1990), [])
        print("test_impossible_end_start_year_books")
        
    def test_false_start_year_books(self):
        self.assertEqual(self.book_checker.books(start_year=2050), [])
        print("test_false_start_year_books")
        
    def test_false_end_year_books(self):
        self.assertEqual(self.book_checker.books(end_year=5), [])
        print("test_false_end_year_books")
        
    def test_sort_by_books(self):
        self.assertEqual(self.book_checker.books(author_id=4, sort_by='year'), [{'id': 18, 'title': 'Pride and Prejudice', 'publication_year': 1813}, {'id': 20, 'title': 'Sense and Sensibility', 'publication_year': 1813}, {'id': 5, 'title': 'Emma', 'publication_year': 1815}])
        print("test_sort_by_books")
        
    def test_book_combo(self):
        self.assertEqual(self.book_checker.books(author_id=4, search_text="Pride", start_year=1800, end_year=1813), [{'id': 18, 'title': 'Pride and Prejudice', 'publication_year': 1813}])
        print("test_book_combo")
    
    """
    Tests for:
    author(self, author_id)
    """
        
    def test_author_identity_true(self):
        self.assertEqual(self.book_checker.author(4), {'id': 4, 'last_name': 'Austen', 'first_name': 'Jane', 'birth_year': 1775, 'death_year': 1817})
        print("test_author_identity_true")

    def test_author_identity_false(self):
        self.assertNotEqual(self.book_checker.author(7), {'id': 5, 'title': 'Emma', 'publication_year': 1815})
        print("test_author_identity_false")

    def test_no_exist_negative_author(self):
        self.assertRaises(ValueError, self.book_checker.author, -14)
        print("test_no_exist_negative_author")

    def test_no_exist_large_author(self):
        self.assertRaises(ValueError, self.book_checker.author, 35)
        print("test_no_exist_large_author")
        
    """
    Tests for:
    authors(self, *, book_id=None, search_text=None, start_year=None, end_year=None, sort_by='birth_year')
    """
    
    def test_bad_book_ID(self):
        self.assertRaises(ValueError, self.book_checker.authors, book_id=-14)
        print("test_bad_book_ID")

    def test_valid_book_ID(self):
        self.assertEqual(self.book_checker.authors(book_id=5), [{'id': 4, 'last_name': 'Austen', 'first_name': 'Jane', 'birth_year': 1775, 'death_year': 1817}])
        print("test_valid_book_ID")
        
    def test_valid_search_text_authors(self):
        self.assertEqual(self.book_checker.authors(search_text="Austen"), [{'id': 4, 'last_name': 'Austen', 'first_name': 'Jane', 'birth_year': 1775, 'death_year': 1817}])
        print("test_valid_search_text_authors")
    
    def test_nonexistent_search_text_authors(self):
        self.assertEqual(self.book_checker.authors(search_text="jive turkey"), [])
        print("test_nonexistent_search_text_authors")
                             
    def test_start_year_end_year_authors(self):
        self.assertEqual(self.book_checker.authors(start_year=1810, end_year=1814), [{'id': 4, 'last_name': 'Austen', 'first_name': 'Jane', 'birth_year': 1775, 'death_year': 1817}, {'id': 23, 'last_name': 'Dickens', 'first_name': 'Charles', 'birth_year': 1812, 'death_year': 1870}])
        print("test_start_year_end_year_authors")
        
    def test_impossible_end_start_year_authors(self):
        self.assertEqual(self.book_checker.authors(start_year=1991, end_year=1990), [])
        print("test_impossible_end_start_year_authors")
        
    def test_false_start_year_authors(self):
        self.assertEqual(self.book_checker.authors(start_year=2050), [])
        print("test_false_start_year_authors")
        
    def test_false_end_year_authors(self):
        self.assertEqual(self.book_checker.authors(end_year=5), [])
        print("test_false_end_year_authors")
        
    def test_sort_by_authors_last_name(self):
        self.assertEqual(self.book_checker.authors(start_year=1810, end_year=1814, sort_by='last_name'), [{'id': 4, 'last_name': 'Austen', 'first_name': 'Jane', 'birth_year': 1775, 'death_year': 1817}, {'id': 23, 'last_name': 'Dickens', 'first_name': 'Charles', 'birth_year': 1812, 'death_year': 1870}])
        print("test_sort_by_authors_last_name")
        
    def test_sort_by_authors_first_name(self):
        self.assertEqual(self.book_checker.authors(start_year=1810, end_year=1814, sort_by='first_name'), [{'id': 23, 'last_name': 'Dickens', 'first_name': 'Charles', 'birth_year': 1812, 'death_year': 1870}, {'id': 4, 'last_name': 'Austen', 'first_name': 'Jane', 'birth_year': 1775, 'death_year': 1817}])
        print("test_sort_by_authors_first_name")   
        
    def test_author_combo(self):
        self.assertEqual(self.book_checker.authors(book_id=5, search_text="Austen", start_year=1810, end_year=1814), [{'id': 4, 'last_name': 'Austen', 'first_name': 'Jane', 'birth_year': 1775, 'death_year': 1817}])
        print("test_author_combo")
    
if __name__ == '__main__':
    unittest.main()
