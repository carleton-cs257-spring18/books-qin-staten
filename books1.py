"""
Oliver Staten
Professor Alexander
CS257
4/8/19
books-1
"""

import csv
import sys

"""
Note that in this particular file, the format should be the following:
python3 books1.py input-file action [sort-direction]
python3: constant
books1.py: constant for our purposes
input-file: name of csv file (books.csv)
action: command, like to type "books" would print the books
in case-sensitive lexicographic order
[sort direction]: the brackets indicate this is an optional command,
and if the command was missing, we can expect the order would be normal.
However, we could type "reverse", and the sorting would happen in
reverse case-sensitive lexicographic order.  
"""

"""
Error statement for if the line contains the incorrect number of inputs;
if it doesn't, exit from the program.
"""
if len(sys.argv) < 3 or  len(sys.argv) > 4:
    print('Usage: must have 3 or 4 inputs', file=sys.stderr) 
    exit()

"""
Small function that returns the first item of the list so that it can be used in a sorting key.
"""    
def takeFirst(list):
    return list[0]
    
""" 
Prints books in case-sensitive lexicographic order.
"""            
def orderBooks(reverseOrNormal):
    #list of books, soon to be ordered
    bookList = [] 
    #go through each row of file, appending on the new entry each time
    for row in reader:
        bookList.append(row[0])
        bookList.sort(reverse = reverseOrNormal) #sort based on reverse variable
    for i in range(len(bookList)):
        print("", bookList[i] ,"")
        
"""
Prints authors in case-sensitive lexicographic order by last name.
"""
def orderAuthors(reverseOrNormal):
    authorList = [] #the full list of authors
    #go through each row of file, appending on the new entry each time
    for row in reader:
        authorName = row[2].split(" ") #create parts of author names 
        for i in range(len(authorName) - 1, 0, -1): #integrate backwards to not index out of range
            if "(" in authorName[i]: #get rid of the dates
                authorName.remove(authorName[i])
        lastNameIndex = len(authorName) - 1;
        for i in range(len(authorName) - 1, 0, -1): 
            if authorName[i] == "and": #deal with special 'and' author case
                lastNameIndex = i - 1
        lastName = authorName[lastNameIndex] #save the last name
        finalAuthorName = " "
        finalAuthorName = finalAuthorName.join(authorName) #rejoin items so it is one string
        innerList = [lastName, finalAuthorName] #add to the list in correct order
        authorList.append(innerList) #add to list
    authorList.sort(key = takeFirst, reverse = reverseOrNormal) #sort based on reverse variable
    for i in range(len(authorList)):
        print("", authorList[i][1] ,"") #print only the whole name
    
""" 
Orders the content based on the command line inputs; redirects most of the
actual logic to one of two helper functions that either sorts books or authors.
"""         
def order():
    #if the command line didn't specify a command, assume normal order
    reverse = False
    #if the command line specified a command
    if len(sys.argv) == 4:
        if sys.argv[3] == "reverse":
            reverse = True
    if sys.argv[2] == "books":
        orderBooks(reverse)
    if sys.argv[2] == "authors":
        orderAuthors(reverse)

"""
The "beginning" of the program, and the first implementation of csv.
csv creates a new file variable called csvFile, then reads it using
csv reader.  Then, it tries to order, unless the file is in a bad format.
"""
filename = sys.argv[1]
with open(filename, newline='') as csvFile:
    reader = csv.reader(csvFile)
    try:
        order()
    except csv.Error as e:
        sys.exit('file {}, line {}: {}'.format(filename, reader.line_num, e))

        
