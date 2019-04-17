"""
Oliver Staten
Professor Alexander
CS257
4/16/19
books-3
"""

import csv

"""
A BooksDataSource object provides access to data about books and authors.
The particular form in which the books and authors are stored will
depend on the context (i.e. on the particular assignment you're
working on at the time).

Most of this class's methods return Python lists, dictionaries, or
strings representing books, authors, and related information.

An author is represented as a dictionary with the keys
'id', 'last_name', 'first_name', 'birth_year', and 'death_year'.
For example, Jane Austen would be represented like this
(assuming her database-internal ID number is 72):

    {'id': 72, 'last_name': 'Austen', 'first_name': 'Jane',
     'birth_year': 1775, 'death_year': 1817}

For a living author, the death_year is represented in the author's
Python dictionary as None.

    {'id': 77, 'last_name': 'Murakami', 'first_name': 'Haruki',
     'birth_year': 1949, 'death_year': None}

Note that this is a simple-minded representation of a person in
several ways. For example, how do you represent the birth year
of Sophocles? What is the last name of Gabriel García Márquez?
Should we refer to the author of "Tom Sawyer" as Samuel Clemens or
Mark Twain? Are Voltaire and Molière first names or last names? etc.

A book is represented as a dictionary with the keys 'id', 'title',
and 'publication_year'. For example, "Pride and Prejudice"
(assuming an ID of 132) would look like this:

    {'id': 193, 'title': 'A Wild Sheep Chase', 'publication_year': 1982}

"""


class BooksDataSource: 
            
    """ 
    Initializes this data source from the three specified  CSV files, whose
    CSV fields are:

        books: ID,title,publication-year
          e.g. 6,Good Omens,1990
               41,Middlemarch,1871


        authors: ID,last-name,first-name,birth-year,death-year
          e.g. 5,Gaiman,Neil,1960,NULL
               6,Pratchett,Terry,1948,2015
               22,Eliot,George,1819,1880

        link between books and authors: book_id,author_id
          e.g. 41,22
               6,5
               6,6

          [that is, book 41 was written by author 22, while book 6
            was written by both author 5 and author 6]

    Note that NULL is used to represent a non-existent (or rather, future and
    unknown) year in the cases of living authors.

    NOTE TO STUDENTS: I have not specified how you will store the books/authors
    data in a BooksDataSource object. That will be up to you, in Phase 3.
    """


    def __init__(self, books_filename, authors_filename, books_authors_link_filename):
        """
        This function takes in the books_reader and puts the csv file into an array of arrays, in which each
        "book" is defined as an inner array, and each inner array is organized like so:
        [id, title, publication year]
        """ 
        with open(books_filename, newline='') as booksFile:
            books_reader = csv.reader(booksFile)
            try:
                bookArray = []
                newBookArray = []
                idCounter = 0
                for row in books_reader:
                    newBookArray = [idCounter, row[0], int(row[1])]
                    bookArray.append(newBookArray)
                    idCounter = idCounter + 1
                self.simpleBookArray = bookArray
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(books_filename, books_reader.line_num, e))
                
        """
        This function takes in the author_reader and puts the csv file into an array of arrays, in which
        each "author" is defined as an inner array, and each inner array is organized like so:
        [id, last name, first name, birth year, death year]
        """ 
        with open(authors_filename, newline='') as authorsFile:
            authors_reader = csv.reader(authorsFile)
            try:
                authorArray = []
                newAuthorArray = []
                for row in authors_reader:
                    if row[4] == "NULL":
                        endDate = None
                    else:
                        endDate = row[4]
                    if endDate == None:
                        newAuthorArray = [int(row[0]), row[1], row[2], int(row[3]), endDate]
                    else:
                        newAuthorArray = [int(row[0]), row[1], row[2], int(row[3]), int(row[4])]
                    authorArray.append(newAuthorArray)
                self.simpleAuthorArray = authorArray
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(authors_filename, authors_reader.line_num, e))
        
        """
        This function takes in the link_reader and puts the csv file into an array of arrays, in which each
        "book" is defined as an inner array, and each inner array is organized as the following:
        [book id, author id]
        """
        with open(books_authors_link_filename, newline='') as linkFile:
            link_reader = csv.reader(linkFile)
            try:
                linkArray = []
                newLinkArray = []
                for row in link_reader:
                    newLinkArray = [int(row[0]), int(row[1])]
                    linkArray.append(newLinkArray)
                self.simpleLinkArray = linkArray
            except csv.Error as e:
                sys.exit('file {}, line {}: {}'.format(books_authors_link_filename, link_reader.line_num, e))
        
    """
    Returns the book with the specified ID. (See the BooksDataSource comment
    for a description of how a book is represented.)
            
    Formatting is as follows:
    {'id': 193, 'title': 'A Wild Sheep Chase', 'publication_year': 1982}
    Raises ValueError if book_id is not a valid book ID.
    """
    def book(self, book_id):
        bookArray = self.simpleBookArray
        bookChecker = False
        for item in bookArray:
            if item[0] == book_id:
                bookDictionary = {'id': item[0], 'title': item[1], 'publication_year': item[2]}
                bookChecker = True
        if bookChecker == False:
            raise ValueError("book_id %d is invalid id" % (book_id)) 
        return bookDictionary
    
    """
    This function simply helps to enable our sorting method for sort_by by providing the entry
    to the publication part of the dictionary.
    """
    def takePublicationYearKey(self, bookEntry):
        return bookEntry['publication_year']

    """
    This function does a similar task to the one above in that it helps our sort_by by providing a key
    for titles.  
    """
    def takeTitleKey(self, bookEntry):
        return bookEntry['title']
    
    """
    Returns a list of all the books in this data source matching all of
    the specified non-None criteria.

        author_id - only returns books by the specified author
        search_text - only returns books whose titles contain (case-insensitively) the search text
        start_year - only returns books published during or after this year
        end_year - only returns books published during or before this year

    Note that parameters with value None do not affect the list of books returned.
    Thus, for example, calling books() with no parameters will return JSON for
    a list of all the books in the data source.

    The list of books is sorted in an order depending on the sort_by parameter:

        'year' -- sorts by publication_year, breaking ties with (case-insenstive) title
        default -- sorts by (case-insensitive) title, breaking ties with publication_year

    See the BooksDataSource comment for a description of how a book is represented.

    QUESTION: Should Python interfaces specify TypeError?
    Raises TypeError if author_id, start_year, or end_year is non-None but not an integer.
    Raises TypeError if search_text or sort_by is non-None, but not a string.
        OUR ANSWER: Not for this assignment.

    QUESTION: How about ValueError? And if so, for which parameters?
    Raises ValueError if author_id is non-None but is not a valid author ID.
        OUR ANSWER: Yes, but just for author_id.
    """
    def books(self, *, author_id=None, search_text=None, start_year=None, end_year=None, sort_by='title'):
        simpleLinkArray = self.simpleLinkArray
        simpleBookArray = self.simpleBookArray
        finalBookArray = []
        for bookEntry in simpleBookArray:
            currentBookDictionary = self.book(bookEntry[0])
            finalBookArray.append(currentBookDictionary)
            
        if author_id != None:
            author_idCounter = False
            for linkEntry in simpleLinkArray:
                if linkEntry[1] == author_id:
                    author_idCounter = True
                if linkEntry[1] != author_id:
                    for x in range(len(finalBookArray) - 1, -1, -1):
                        if finalBookArray[x]['id'] == linkEntry[0]:
                            finalBookArray.remove(finalBookArray[x])
            if author_idCounter == False:
                raise ValueError("author_id %d is invalid id" % (author_id)) 
                
        if search_text != None:
            for bookEntry in simpleBookArray:
                if search_text not in bookEntry[1]:
                    for x in range(len(finalBookArray) - 1, -1, -1):
                        if finalBookArray[x]['id'] == bookEntry[0]:
                            finalBookArray.remove(finalBookArray[x])
                            
        if start_year != None:
            for bookEntry in simpleBookArray:
                if bookEntry[2] < start_year:
                    for x in range(len(finalBookArray) - 1, -1, -1):
                        if finalBookArray[x]['id'] == bookEntry[0]:
                            finalBookArray.remove(finalBookArray[x])
                            
        if end_year != None:
            for bookEntry in simpleBookArray:
                if bookEntry[2] > end_year:
                    for x in range(len(finalBookArray) - 1, -1, -1):
                        if finalBookArray[x]['id'] == bookEntry[0]:
                            finalBookArray.remove(finalBookArray[x])
        
        if sort_by == 'year':
            finalBookArray.sort(key=self.takePublicationYearKey) 
            
        if sort_by == 'title':
            finalBookArray.sort(key=self.takeTitleKey)
            
        return finalBookArray

    """ 
    Returns the author with the specified ID. (See the BooksDataSource comment for a
    description of how an author is represented.)
    
    Formatting is as follows:
    {'id': 72, 'last_name': 'Austen', 'first_name': 'Jane', 'birth_year': 1775, 'death_year': 1817}
    death year is "None" if they aren't dead.  
    Raises ValueError if author_id is not a valid author ID.
    """
    def author(self, author_id):
        authorArray = self.simpleAuthorArray
        authorChecker = False
        for item in authorArray:
            if item[0] == author_id:
                authorDictionary = {'id': item[0], 'last_name': item[1], 'first_name': item[2], 'birth_year': item[3], 'death_year': item[4]}
                authorChecker = True
        if authorChecker == False:
            raise ValueError("author_id %d is invalid id" % (author_id)) 
        return authorDictionary
    
    """
    This function simply helps to enable our sorting method for sort_by by providing the entry
    to the publication part of the dictionary.
    """
    def takeFirstNameKey(self, authorEntry):
        return authorEntry['first_name']

    """
    This function does a similar task to the one above in that it helps our sort_by by providing a key
    for titles.  
    """
    def takeLastNameKey(self, authorEntry):
        return authorEntry['last_name']
    
    """
    This function simply helps to enable our sorting method for sort_by by providing the entry
    to the publication part of the dictionary.
    """
    def takeBirthYearKey(self, authorEntry):
        return authorEntry['birth_year']


    """ 
    Returns a list of all the authors in this data source matching all of the
    specified non-None criteria.

        book_id - only returns authors of the specified book
        search_text - only returns authors whose first or last names contain
            (case-insensitively) the search text
        start_year - only returns authors who were alive during or after
            the specified year
        end_year - only returns authors who were alive during or before
            the specified year

    Note that parameters with value None do not affect the list of authors returned.
    Thus, for example, calling authors() with no parameters will return JSON for
    a list of all the authors in the data source.

    The list of authors is sorted in an order depending on the sort_by parameter:

        'birth_year' - sorts by birth_year, breaking ties with (case-insenstive) last_name,
            then (case-insensitive) first_name
        any other value - sorts by (case-insensitive) last_name, breaking ties with
            (case-insensitive) first_name, then birth_year

    See the BooksDataSource comment for a description of how an author is represented.
    """
    def authors(self, *, book_id=None, search_text=None, start_year=None, end_year=None, sort_by='birth_year'):
        simpleLinkArray = self.simpleLinkArray
        simpleAuthorArray = self.simpleAuthorArray
        finalAuthorArray = []
        for authorEntry in simpleAuthorArray:
            currentAuthorDictionary = self.author(authorEntry[0])
            finalAuthorArray.append(currentAuthorDictionary)
        
        if book_id != None:
            book_idCounter = False
            author_exception_id = -5
            for linkEntry in simpleLinkArray:
                if linkEntry[0] == book_id:
                    author_exception_id  = linkEntry[1]
                    book_idCounter = True
                if linkEntry[0] != book_id: #if the book_id is not the desired one
                    for x in range(len(finalAuthorArray) - 1, -1, -1): #look through array of dictionaries
                        if finalAuthorArray[x]['id'] == linkEntry[1] and finalAuthorArray[x]['id'] != author_exception_id: #if the id of the dictionary is 
                            finalAuthorArray.remove(finalAuthorArray[x]) #that of the one we want to get rid 
                            #of, remove it
            if book_idCounter == False:
                raise ValueError("book_id %d is invalid id" % (book_id)) 
                
        
                
        if search_text != None:
            for authorEntry in simpleAuthorArray:
                if search_text not in authorEntry[1] and search_text not in authorEntry[2]:
                    for x in range(len(finalAuthorArray) - 1, -1, -1):
                        if finalAuthorArray[x]['id'] == authorEntry[0]:
                            finalAuthorArray.remove(finalAuthorArray[x])
                            
        if start_year != None:
            for authorEntry in simpleAuthorArray:
                tempValue = authorEntry[4]
                if authorEntry[4] == None:
                    tempValue = 2019
                if tempValue < start_year:
                    for x in range(len(finalAuthorArray) - 1, -1, -1):
                        if finalAuthorArray[x]['id'] == authorEntry[0]:
                            finalAuthorArray.remove(finalAuthorArray[x])
                            
        if end_year != None:
            for authorEntry in simpleAuthorArray:
                if authorEntry[3] > end_year:
                    for x in range(len(finalAuthorArray) - 1, -1, -1):
                        if finalAuthorArray[x]['id'] == authorEntry[0]:
                            finalAuthorArray.remove(finalAuthorArray[x])
                            
        if end_year and start_year != None:
            if end_year < start_year:
                for x in range(len(finalAuthorArray) - 1, -1, -1):
                        finalAuthorArray.remove(finalAuthorArray[x]) 
        
        if sort_by == 'birth_year':
            finalAuthorArray.sort(key=self.takeBirthYearKey) 
            
        if sort_by == 'last_name':
            finalAuthorArray.sort(key=self.takeLastNameKey)
            
        if sort_by == 'first_name':
            finalAuthorArray.sort(key=self.takeFirstNameKey)
        
        return finalAuthorArray

        
