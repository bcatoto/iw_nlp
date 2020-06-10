#!/usr/bin/env python

from sys import argv, stderr
import re
from helper import clear_dir, read_folder_dict, write_file
import spacy

SRCFOL = '../2_parsed_data'
DESTFOL = '../3_preprocessed_data'
REMOVE_WORDS = ['yeah', 'maybe', 'huh', 'uh', 'okay']

#-------------------------------------------------------------------------------

def preprocess(movie, gender):
    title = movie['title']

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(movie['text'])
    print('%s: Finished processing text...' % (title))

    lemma = []
    for token in doc:
        if not token.is_stop and token.lemma_ not in REMOVE_WORDS and \
            token.lemma_ != '-PRON-' and token.pos_ != 'PROPN' and \
            len(token.text) > 2:
            lemma.append(token.lemma_)
    print('%s: Finished extracting lemmatized forms...' % (title))

    regex = re.compile('([^\s\w]|_)+')
    text = regex.sub('', ' '.join(lemma).lower())
    print('%s: Finished simplifying text...' % (title))

    write_file('%s/%s/%s/%s' % (DESTFOL, gender, movie['year'], title), text)
    print('%s: Finished printing.' % (title))

    return len(lemma)

#-------------------------------------------------------------------------------

def main():
    fem = 0
    male = 0

    for year in range(1975, 2016):
        print('Parsing movies in %d...' % (year))

        # Creates year folders if they don't exist; clears them if they do
        clear_dir('%s/fem/%d' % (DESTFOL, year))
        clear_dir('%s/male/%d' % (DESTFOL, year))

        # Preprocesses data by gender, year, and movie
        females = read_folder_dict('%s/fem/%d' % (SRCFOL, year), year)
        for movie in females:
            fem += preprocess(movie, 'fem')

        males = read_folder_dict('%s/male/%d' % (SRCFOL, year), year)
        for movie in males:
            male += preprocess(movie, 'male')

        print('-----------------------------')

    print('NUMBER OF WORDS SPOKEN')
    print('\tMale:\t\t%d' % (male))
    print('\tFemale:\t\t%d' % (fem))

if __name__ == '__main__':
    main()
