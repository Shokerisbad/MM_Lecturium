import requests
from bs4 import BeautifulSoup
import numpy as np
import os
from pyhtml2pdf import converter

class gutenberg():
    
    def __init__(self,verbose=bool(False)):
        """
         Initializes the class.

        Args:
            verbose (bool, optional): If True, functions produce output about their results. Defaults to False.
         """
        self.verbose = verbose
        self.base_url = 'https://www.gutenberg.org'
        self.bookshelf_url = self.base_url + '/ebooks/bookshelf/'
        self.search_url = self.base_url + '/ebooks/search/'
        self.search_shelves_url = self.base_url + '/ebooks/bookshelves/search/'
    
    def list_bookshelf(self, links=bool(False)):
        """
        Lists available bookshelves on Project Gutenberg.

        Args:
        links (bool, optional): If True, returns a list of dictionaries containing only the title and link for each bookshelf. Defaults to False.

        Returns:
            list: A list of bookshelves (strings) or dictionaries containing bookshelf information. False if an error occurs.
        """

        if type(links) != bool:
            raise(TypeError('The "links" parameter can only accept boolean(bool) values.'))

        response = requests.get(self.bookshelf_url)

        if response.status_code != 200:
            return False

        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')

        ebooks_div = soup.find("div", class_='bookshelves')

        shelves_a = ebooks_div.find_all('a')

        if links:
            result = []
            for shelve in shelves_a:
                result.append({'title': shelve.text, 'link': shelve['href']})
            return result

        shelves = [shelve.text for shelve in shelves_a]
        return shelves
    

    
    def bulksearch(self, search_query=str, sort_order=str(''), limit=int(0), download=bool(False)):
        """
            Bulk Search on Project Gutenberg

            Args:
                search_query (str)(list): Enter the text you want to search. This field cannot be empty. if you want to do multiple search than you must type in search_query in list type
                sort_order (str, optional): This parameter allows you to sort the search results. It can only take the values 'title', 'release_date', and 'downloads'. Defaults to empty.
                limit (int, optional): Sets the maximum number of search results to return. Defaults to 0, which returns all results.
                download (bool, optional): If set to True, all books found in the search will be automatically downloaded to the 'books' folder. Don't use with page_numbers=True. Defaults to False.

            Returns:
                list: A list search result containing book's title, author, link, image_link and extra(change with sort_order if you set release_date than extra return with book's release date, if you set downloads than extra return with number of downloads).
                if something's wrong with the page return False   
        """

        if type(search_query) != str:
            if type(search_query) != list:
                raise(TypeError('The "search_query" parameter can only accept string(str) or list values.'))
            else:
                return self.__multiple_bulk_search(search_query, sort_order, limit, download)
        else:
            if len(search_query.replace(" ","")) == 0:
                raise(ValueError('You cannot leave the "search_query" parameter blank.'))
            if len(search_query.replace(" ","")) < 3:
                raise(ValueError('The search_query must be longer than 3 characters.'))
            
        if type(sort_order) != str:
            raise(TypeError('The "sort_order" parameter can only accept string(str) values.'))
        if type(limit) != int:
            raise(TypeError('The "limit" parameter can only accept integer(int) values.'))
        if type(download) != bool:
            raise(TypeError('The "download" parameter can only accept bool values.'))

        if type(search_query) == list:
            return self.__multiple_bulk_search(search_query,sort_order,limit,download)

        parameters = {'query':search_query}
        sort_order_list = ['title', 'downloads','release_date']
        if len(sort_order.replace(" ","")) > 0:
            sort_order = sort_order.replace(" ","").lower()
            if sort_order not in sort_order_list:
                raise(ValueError("sort_order (str, optional): This parameter allows you to sort the search results. It can only take the values 'title', 'release_date', and 'downloads'."))
            parameters['sort_order'] = sort_order

        response = requests.get(self.search_url, params=parameters)

        if response.status_code != 200:
            return False
        soup = BeautifulSoup(response.content, 'html.parser')
        result = []
        number_of_data = 0
        page = 1
        while True:

            ul_tag = soup.find('ul', class_='results')
            books_li_tag = ul_tag.find_all('li',class_='booklink')

            if len(books_li_tag) == 0:
                if self.verbose:
                    print(f'scanned {page} page(s) and {number_of_data} number of result(s) founded!')
                return result
            
            for book in books_li_tag:
                if (limit > 0) and (number_of_data == limit):
                    if self.verbose:
                        print(f'scanned {page} page(s) and {number_of_data} number of result(s) founded!')
                    return result
                
                data = self.__get_book_data_from_search(book)
                self.download_book(book['link'], saveMetadata=True)
                result.append(data)

                number_of_data += 1
            next_page = soup.find('span', class_='links').find('a', {'accesskey' : '+'})

            if not next_page:
                if self.verbose:
                    print(f'scanned {page} page(s) and {number_of_data} number of result(s) founded!')
                return result
            
            response = requests.get(self.base_url + next_page['href'])
            if response.status_code != 200:
                print(f'scanned {page} page(s) and {number_of_data} number of result(s) founded!')
                return result
            soup = BeautifulSoup(response.content, 'html.parser')
            page +=1


    
    def quicksearch(self, search_query=str, sort_order=str(''), download=bool(False)):
        """
            Quick Search on Project Gutenberg

            Args:
                search_query (str)(list): Enter the text you want to search. This field cannot be empty. if you want to do multiple search than you must type in search_query in list type
                sort_order (str, optional): This parameter allows you to sort the search results. It can only take the values 'title', 'release_date', and 'downloads'. Defaults to empty.
                download (bool, optional): If set to True, all books found on the search will be automatically downloaded to the 'books' folder. Don't use with page_numbers=True. Defaults to False.

            Returns:
                list: A list search result containing book's title, author, link, image_link and extra(change with sort_order if you set release_date than extra return with book's release date, if you set downloads than extra return with number of downloads).
                if something's wrong with the page return False   
        """

        if type(search_query) != str:
            if type(search_query) != list:
                raise(TypeError('The "search_query" parameter can only accept string(str) or list values.'))
            else:
                return self.__multiple_quick_search(search_query, sort_order, download)
        else:
            if len(search_query.replace(" ","")) == 0:
                raise(ValueError('You cannot leave the "search_query" parameter blank.'))
            if len(search_query.replace(" ","")) < 3:
                raise(ValueError('The search_query must be longer than 3 characters.'))
            
        if type(sort_order) != str:
            raise(TypeError('The "sort_order" parameter can only accept string(str) values.'))
        if type(download) != bool:
            raise(TypeError('The "download" parameter can only accept bool values.'))
        
        parameters = {'query':search_query}

        sort_order_list = ['title', 'downloads','release_date']
        if len(sort_order.replace(" ","")) > 0:
            sort_order = sort_order.replace(" ","").lower()
            if sort_order not in sort_order_list:
                raise(ValueError("sort_order (str, optional): This parameter allows you to sort the search results. It can only take the values 'title', 'release_date', and 'downloads'."))
            parameters['sort_order'] = sort_order

        response = requests.get(self.search_url, params=parameters)

        if response.status_code != 200:
            return False
        soup = BeautifulSoup(response.content, 'html.parser')

        ul_tag = soup.find('ul', class_='results')
        books_li_tag = ul_tag.find_all('li',class_='booklink')
        if len(books_li_tag) == 0:
            result = []
        else:
            result = [self.__get_book_data_from_search(book) for book in books_li_tag]

        if self.verbose:
            print(f'{len(result)} book(s) founded!')
        
        if (download) and (len(result) > 0):
            for book in result:
                self.download_book(book['link'])
        return result

    


    
    def download_book(self, link=str, folder=str('books'), saveMetadata=bool(False)):
        """
            Download Book from Gutenberg

            Args:
            link(str)(list): book's link which you want to download without base url e.g. '/ebooks/73637' if you want to download multiple book than you can just type in links in list
            folder(str, optional): Download folder path. Defaults to books
            saveMetadata(bool, optional): If you want to download book's metadatas (author, language, category, etc.) set to True. Defaults to False

            Return:
                True: when process complete
        """

        if type(link) != str:
            if type(link) == list:
                return self.__bulk_download(link,folder,saveMetadata)
            else:
                raise(TypeError('The "link" parameter can only accept string(str) or list values.'))
                
        if type(folder) != str:
            raise(TypeError('The "folder" parameter can only accept string(str) values.'))

        if type(saveMetadata) != bool:
             raise(TypeError('The "saveMetadata" parameter can only accept boolean(bool) values.'))
        
        
        book_name = link.split('/')[2]
        download_link = f'{self.base_url + link}.html.images'
        
        if not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.exists(folder + '/' + book_name):
            os.makedirs(folder + '/' + book_name)

        converter.convert(download_link, f'{folder}/{book_name}/book.pdf')

        if saveMetadata:
            metadata = self.get_metadata(link)
            with open(f'{folder}/{book_name}/metadata.txt', 'wb') as f:
                f.write(str(metadata).encode('utf-8'))

        return True
        

    
    def get_metadata(self,link=str):
        """
        Get metadata of books

        Args:
        link(str)(list): You have to type in link without base url e.g. '/ebooks/64361'. If you want extract metadata of multiple books than just type in links in list

        Return:
        list
        """
        if type(link) != str:
            if type(link) != list:
                raise(TypeError('The "link" parameter can only accept string(str) or list values.'))
            else:
                return self.__get_metadata_from_list(link)
            
        response = requests.get(self.base_url + link)
        if response.status_code != 200:
            return False
        soup = BeautifulSoup(response.content, 'html.parser')
        data_table = soup.find('table', class_='bibrec')
        lines = data_table.find_all('tr')

        result = {}
        columns = []
        datas = []

        for line in lines:
            columns_lines = line.find_all('th')

            for column in columns_lines:
                columns.append(column.text.strip().lower().replace(' ','_'))

            data_lines = line.find_all('td')
            for data in data_lines:
                datas.append(data.text.strip())

        for i in range(0, len(columns)):
            if columns[i] in result:
                result[columns[i]].append(datas[i])
            else:
                if sum(col == columns[i] for col in columns) > 1:
                     result[columns[i]] = [datas[i]]
                else:
                    result[columns[i]] = datas[i]
        
            
        return result
    
    def __get_book_data_from_search(self,book):
        title = book.find('span',class_='title').text
        link = book.find('a', class_='link')['href']

        author = book.find('span', class_='subtitle')
        extra = book.find('span', class_='extra')
        image = book.find('img', class_='cover-thumb')
        
        if author:
            author = author.text
        if extra:
            extra = extra.text
        if image:
            image = image['src']
        
        return {
            'title': title,
            'author': author,
            'extra' : extra,
            'link' : link,
            'image' : image
        }


    def __multiple_bulk_search(self, query_list=list, sort_order=str, limit=int, download=bool):
        result = []
        for query in query_list:
            result.append(self.bulksearch(query, sort_order, limit, download))

        result = np.array(result)
        return result.flatten()
    
    def __multiple_quick_search(self, query_list=list, sort_order=str, download=bool):
        result = []
        for query in query_list:
            result.append(self.quicksearch(query, sort_order, download))

        result = np.array(result)
        return result.flatten()
    
    def __get_metadata_from_list(self,links):
        result = []

        for link in links:
            
            result.append(self.get_metadata(link))

        return result
    
    def __bulk_download(self, link_list, folder, saveMetadata):
        for link in link_list:
            self.download_book(link,folder,saveMetadata)
        return True