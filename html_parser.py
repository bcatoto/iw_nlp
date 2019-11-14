#!/usr/bin/env python

from sys import argv, stderr
from in_out import read_file, write_file
import bs4
from bs4 import BeautifulSoup

SRCFOL = '2_parsed_data'
DESTFOL = '3_preprocessed_data_spacy'

#-------------------------------------------------------------------------------

def parse(doc):
    soup = BeautifulSoup(doc, 'html.parser')
    text_tag = soup.find('div', {'class': 'right-column'})

    string = ''
    for child in text_tag.children:
        if not isinstance(child, bs4.element.NavigableString):
            string = string + child.text
    write_file('data_scraping/the_program_parsed.txt', string)

#-------------------------------------------------------------------------------

def main():
    text = read_file('data_scraping/the_program.htm')
    parse(text)

if __name__ == '__main__':
    main()
