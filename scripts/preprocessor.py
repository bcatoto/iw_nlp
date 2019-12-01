#!/usr/bin/env python

from sys import argv, stderr
import re
from helper import clear_dir, read_folder_dict, write_file
import spacy

SRCFOL = '../2_parsed_data'
DESTFOL = '../3_preprocessed_data'
REMOVE_WORDS = ['yeah', 'maybe', 'huh', 'uh']

#-------------------------------------------------------------------------------

def preprocess(movie, gender):
    title = movie['title']

    regex = re.compile('([^\s\w]|_)+')
    text = regex.sub('', movie['text'].lower())
    print('%s: Finished simplifying text...' % (title))

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    print('%s: Finished processing text...' % (title))

    lemma = []
    for token in doc:
        if not token.is_stop and token.text not in REMOVE_WORDS and \
            token.lemma_ is not '-PRON-' and token.pos_ is not 'PROPN' and \
            len(token.text) > 2:
            lemma.append(token.lemma_)
    print('%s: Finished extracting lemmatized forms...' % (title))

    write_file('%s/%s/%s/%s' % (DESTFOL, gender, movie['year'], title),
        ' '.join(lemma))
    print('%s: Finished printing.' % (title))

#-------------------------------------------------------------------------------

def main():

    for year in range(1975, 2006):
        # Creates year folders if they don't exist; clears them if they do
        clear_dir(DESTFOL, 'fem', year)
        clear_dir(DESTFOL, 'male', year)

        # Preprocesses data by gender, year, and movie
        females = read_folder_dict('%s/fem/%d' % (SRCFOL, year), year)
        for movie in females:
            preprocess(movie, 'fem')

        males = read_folder_dict('%s/male/%d' % (SRCFOL, year), year)
        for movie in males:
            preprocess(movie, 'male')

if __name__ == '__main__':
    main()
