#!/usr/bin/env python

from sys import argv
import re
from helper import clear_dir, read_folder_dict, write_file
from bs4 import BeautifulSoup

TABS = False
NUM_NAME = 29
NUM_LINE = 16

FOL = '../0_scraped_data'
REMOVE_NAME = ['(V.O.)', '(VO)', '(O.S.)', '(OS)', '(CONT\'D)', '(CONT)']
NOT_NAME = [':', '--', 'TO:', 'CUT TO', 'JUMP TO', 'GO TO', 'FADE', 'DISSOLVE',
    'THE END', 'WIPE TO', 'VOICE OVER']

#-------------------------------------------------------------------------------

def isName(name):
    if name == None:
        return False

    if len(name) < NUM_NAME + 1:
        return False

    if re.search(r'[0-9]+\.', name):
        return False

    for word in NOT_NAME:
        if name.find(word) != -1:
            return False

    if TABS:
        for i in range(0, NUM_NAME):
            if name[i] != '\t':
                return False
    else:
        for i in range(0, NUM_NAME):
            if name[i] != ' ':
                return False

    return True

def isLine(line):
    if len(line) < NUM_LINE + 1:
        return False

    if TABS:
        if line[NUM_LINE] == '\T':
            return False

        for i in range(0, NUM_LINE):
            if line[i] != '\t':
                return False
    else:
        if line[NUM_LINE] == ' ':
            return False

        for i in range(0, NUM_LINE):
            if line[i] != ' ':
                return False

    return True

#-------------------------------------------------------------------------------

def clean_title(string):
    return string.replace('\t', '').replace('\n', '')

def clean_name(string):
    string = string.replace('\t', '').replace('\n', '')

    for word in REMOVE_NAME:
        string = string.replace(word, '')

    start = string.find('(')
    end = string.find(')')

    while start != -1 and end != -1:
        substring = string[start:end + 1]
        string = string.replace(substring, '')
        start = string.find('(')
        end = string.find(')')

    if TABS:
        return string
    else:
        return string[NUM_NAME:len(string)]

def clean_dialog(string):
    string = string.replace('\t', '').replace('\n', ' ')

    if TABS:
        return string
    else:
        return string[NUM_LINE:len(string)]

def parse(info):
    outFile = open('%s/txt/%s/%s.txt' % (FOL, info['year'], info['title'][0:-5]),
        mode='w', encoding='ISO-8859-1')

    soup = BeautifulSoup(info['text'], 'html.parser')

    # Gets and prints title
    title = soup.find_all('title')

    if title:
        title = clean_title(title[0].string.replace(' Script at IMSDb.', ''))[3:-2]
        outFile.write('%s\n\n' % (title))

    # Gets script contents
    try:
        script = soup.find_all('pre')[0]
    except:
        print('Could not parse %s' % (info['title']))
        return

    # Gets all names in script
    # - Names of places and speaking characters are bolded
    names = script.find_all('b')

    # Iterates over names to get dialog
    for name in names:
        if isName(name.string):
            if name.next_sibling == None:
                continue

            # Writes name
            outFile.write('%s\t' % (clean_name(name.string)))

            # Gets character's dialog
            lines = name.next_sibling.string
            if not lines:
                continue
            lines = name.next_sibling.string.split('\n')

            # Writes character's lines
            for line in lines:
                if isLine(line):
                    outFile.write('%s ' % (clean_dialog(line)))
            outFile.write('\n')
    print('Finished %s...' % (title))
    outFile.close()

#-------------------------------------------------------------------------------

def main():
    for year in range(1975, 2016):
        # Creates year folders if they don't exist; clears them if they do
        clear_dir('%s/txt/%d' % (FOL, year))

        print('Parsing movies in %d...' % (year))

        # Preprocesses data by gender, year, and movie
        movies = read_folder_dict('%s/html/%d' % (FOL, year), year)
        for movie in movies:
            parse(movie)

        print('-----------------------------')

if __name__ == '__main__':
    main()
