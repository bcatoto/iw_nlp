#!/usr/bin/env python

from urllib.request import urlopen
from bs4 import BeautifulSoup

FOL = '../1_scraped_data'

#-------------------------------------------------------------------------------

def getYear(title):
    try:
        url = 'https://www.imsdb.com/Movie%20Scripts/' +
            title.replace(':', '').replace(' ', '%20')
        page = urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
    except:
        print('Could not get script URL of %s' % (title))
        return None

    movie = soup.find(text='Movie Release Date')
    script = soup.find(text='Script Date')

    if movie != None:
        date = movie.parent.next_sibling.string
    elif script != None:
        date = script.parent.next_sibling.string
    else:
        return None

    year = date[-4:len(date)]

    try:
        year = int(year)
    except ValueError:
        print('%s: %s is not a year' % (title, year))
        return None

    return year

#-------------------------------------------------------------------------------

def main():

    url = 'https://www.imsdb.com/all%20scripts/'
    page = urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    td = soup.find_all('h1')[1].parent
    links = td.find_all('p')

    outFile = open('%s/movie_script_urls.txt' % (FOL), mode='w',
        encoding='ISO-8859-1')

    for link in links:
        title = link.find('a').get('title').replace(' Script', '')
        script = title.replace(' ', '-')
        year = getYear(title)

        if year == None or year < 1975:
            continue

        outFile.write('%s\t%s\thttps://www.imsdb.com/scripts/%s.html\n' % \
            (title, year, script))
        print('Finished %s...' % (title))

    outFile.close()
if __name__ == '__main__':
    main()
