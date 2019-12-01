#!/usr/bin/env python

from urllib.request import urlopen
from bs4 import BeautifulSoup
from script_parser import parse
from helper import clear_dir, write_file
import time
import re

FOL = '../data_scraping'

def main():

    # Clears directory
    for year in range(1975, 2020):
        clear_dir(FOL, 'html', year)

    inFile = open('%s/movie_script_urls.txt' % (FOL), mode='r',
        encoding='ISO-8859-1')
    outFile = open('%s/movie_metadata.txt' % (FOL), mode='w',
        encoding='ISO-8859-1')

    counter = 0

    for line in inFile:
        fields = line.split('\t')
        title = fields[0]
        year = fields[1]
        url = fields[2]

        regex = re.compile('([^\s\w]|_)+')
        filename = regex.sub('', title.lower()).replace(' ', '_')

        try:
            page = urlopen(url)
            soup = BeautifulSoup(page, 'html.parser')
            text = soup.prettify()
            write_file('%s/html/%s/%s.html' % (FOL, year, filename), text)
        except:
            print('Could not download %s.' % (title))
            continue
            
        outFile.write('%d\t%s' % (counter, line))
        print('Finished downloading %s...' % (title))

        counter += 1

    outFile.close()
    inFile.close()
if __name__ == '__main__':
    main()
