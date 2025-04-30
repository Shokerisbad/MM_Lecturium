# Gutenberg
 This Python script allows you to scrape and download books from the Gutenberg Project website.

## Installation
The script requires the following Python libraries:

## Requirements:
* requests
* beautifulsoup4
* numpy
* os
* pyhtml2pdf

### You can install them using pip:
```python
pip install -r requirements.txt
```
# Usage:

### Import the library:
```python
from gutenberg import gutenberg
```
### Create an instance of the Gutenberg class:
```python
project = gutenberg()
```
### List available bookshelves:
```python
print(bookshelves)
```
### Get a list of dictionaries containing titles and links for each bookshelf:
```python
bookshelves_info = project.list_bookshelf(links=True)
print(bookshelves_info)
```
## Bulk Search for Books:

### Search for a book by title:
```python
search_result = project.bulksearch(search_query="Moby Dick", download=True)
```
### Search for books with limit and sort by title:
```python
search_result = project.bulksearch(search_query=["A Tale of Two Cities", "Pride and Prejudice"], sort_order="title", limit=2)
```
### Print details of each book found in the search:
```python
if search_result:
  for book in search_result:
    print(f"Title: {book['title']}, Author: {book.get('author')}, Link: {book['link']}")
```

### Download all search results (without using download parameter sets download=True by default):
```python
project.bulksearch(search_query="The Adventures of Sherlock Holmes")
```
### Quick Search for Books:
```python
search_result = project.quicksearch(search_query="The Metamorphosis")
```
### Quick search with sorting by downloads:
```python
search_result = project.quicksearch(search_query="Frankenstein", sort_order="downloads")
```
### Print details of the first book found in the search:
```python
if search_result:
  print(search_result[0])
```
### Download a Single Book:
```python
project.download_book("/ebooks/1632") 
project.download_book("/ebooks/1632", folder="my_downloads") #Download book by relative URL, specifying download folder
project.download_book("/ebooks/1632", saveMetadata) #Download book with metadata
project.download_book(["/ebooks/1632", "/ebooks/1932"]) #Download multiple book
```
