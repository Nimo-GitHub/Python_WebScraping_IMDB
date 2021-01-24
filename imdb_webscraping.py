"""PYTHON SCRIPT FOR WEB SCRAPING IMDb "Top 1000" (Sorted by IMDb Rating Descending)"""

# Import Statements
import pandas as pd
from bs4 import BeautifulSoup as Soup
from requests import get

# Requesting IMDB Link for 1000 Top Rated Movie List
base_url = "https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc"

headers = {'Accept-Language': 'en-US,en;q=0.8'}
url = get(base_url, headers=headers).text

# Empty DataFrame Creation for Structure of the DataSet
dataset = pd.DataFrame(
    {'title': [], 'year': [], 'certificate': [], 'duration': [], 'genre': [], 'rating': [], 'metascore': [],
     'description': [], 'director': [], 'cast': []})


for pgno in range(20):
    '''Loop for accessing 20 pages of 50 Movies each'''

    print("Page Scanned : " + str(pgno + 1))

    soup = Soup(url, 'html.parser')
    movies = soup.findAll('div', {'class': 'lister-item mode-advanced'})

    for movie in movies:
        '''Loop for Accessing each movie separately and storing its contents in the DataFrame'''

        # Variables for each attribute of the movie
        title = movie.find('h3',{'class':'lister-item-header'}).a.text
        year = movie.find('span', {'class': 'lister-item-year text-muted unbold'}).text[1:-1]
        certificate = movie.find('span', {'class': 'certificate'})

        '''Some certificates are unavailable soo....'''
        if certificate is None:
            certificate = 'Not Rated'
        else:
            certificate = certificate.text

        duration = movie.find('span', {'class': 'runtime'}).text
        genre = movie.find('span', {'class': 'genre'}).text.strip()
        rating = movie.find('div', {'class': 'inline-block ratings-imdb-rating'}).strong.text

        '''Some metascores are unavailable'''
        try:
            metascore = movie.find('div', {'class': 'inline-block ratings-metascore'}).span.text.strip()
        except AttributeError:
            metascore = 'NAN'

        description = movie.find('div', {'class': 'lister-item-content'}).findAll('p')[1].text.strip()
        director = movie.find('div', {'class': 'lister-item-content'}).findAll('p')[2].a.text
        casting = movie.find('div', {'class': 'lister-item-content'}).findAll('p')[2].findAll('a')[1:]
        cast = ""

        '''Joining each actor/actress name in a single string'''
        for c in casting:
            cast += c.text + ', '
        cast = cast[:-2]

        row = pd.DataFrame(
            {'title': [title], 'year': [year], 'certificate': [certificate], 'duration': [duration], 'genre': [genre],
             'rating': [rating], 'metascore': [metascore], 'description': [description], 'director': [director],
             'cast': [cast]})

        # Appending movie details in the DataFrame
        dataset = dataset.append(row, ignore_index=True)

    '''To Ensure Halt after last page is scanned'''
    if pgno == 19:
        break

    '''To find the link extension for the next page to access the next 50 movies
       and create the url for the next page'''
    next_link = soup.find('a', {'class': 'lister-page-next next-page'})['href']
    url = get(base_url + next_link).text

# Index Correction
dataset.index += 1

#Save DataFrame in a CSV File
dataset.to_csv("imdb_top_rated_movies_dataset.csv")
