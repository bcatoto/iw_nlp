#!/usr/bin/env python

from sys import argv, stderr
import re
from pre_io import read_file, read_list, read_folder, write_file, write_word_pos
import spacy

DESTFOL = '2_preprocessed_data_spacy'

REMOVE_WORDS = ['yeah', 'maybe', 'huh', 'uh']

#-------------------------------------------------------------------------------

def preprocess(text, gender, year):
    regex = re.compile('([^\s\w]|_)+')
    text = regex.sub('', text.lower())
    print('%s: Finished simplifying text...' % (year))

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    print('%s: Finished processing text...' % (year))

    lemma = []
    for token in doc:
        if not token.is_stop and token.text not in REMOVE_WORDS and \
            token.lemma_ is not '-PRON-' and token.pos_ is not 'PROPN':
            lemma.append(token.lemma_)
    print('%s: Finished extracting lemmatized forms...' % (year))

    write_file('%s/%s/%s.txt' % (DESTFOL, gender, year), ' '.join(lemma))
    print('%s: Finished printing.' % (year))

#-------------------------------------------------------------------------------

def main():

    if 'female' in argv:
        females = read_folder('1_cleaned_data/fem_lines')
        for year, text in females.items():
            preprocess(text, 'fem', year)

    if 'male' in argv:
        males = read_folder('1_cleaned_data/male_lines')
        for year, text in males.items():
            preprocess(text, 'male', year)

if __name__ == '__main__':
    main()
