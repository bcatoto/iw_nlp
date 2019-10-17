#!/usr/bin/env python

from sys import argv, stderr
import re
from pre_io import read_file, read_list, read_folder, write_file, write_word_pos
from pre_nltk import simplify, tokenize, pos_tagger, remove_stopword, lemmatize

# from preprocess_spacy import tokenize, pos_tagger, remove_stopword, lemmatize

DESTFOL = '2_preprocessed_data_nltk'

#-------------------------------------------------------------------------------

def preprocess_gender(name):

    text = read_file('1_cleaned_data/%s_lines.txt' % (name))
    print('Finished reading in file...')

    textS = simplify(text)
    print('Finished simplifying...')

    textT = tokenize(textS)
    print('Finished tokenizing...')

    pos_list = pos_tagger(textS, textT)
    print('Finished finished tagging...')

    textW = remove_stopword(textT, pos_list)
    print('Finished removing stopwords...')

    textL = lemmatize(textW, pos_list)
    print('Finished lemmatizing...')

    if 'print' in argv:
        write_file('%s/0_%s_simple.txt' % (DESTFOL, name), textS)
        write_file('%s/1_%s_tokenized.txt' % (DESTFOL, name), ' '.join(textT))
        write_file('%s/2_%s_pos.txt' % (DESTFOL, name), ' '.join(pos_list))
        write_word_pos('%s/2.5_%s_pos.txt' % (DESTFOL, name), textT, pos_list)
        write_file('%s/3_%s_stopwords.txt' % (name), ' '.join(textW))
        write_file('%s/%s/4_lemmatized/%s.txt' % (DESTFOL, name),
            ' '.join(textL))
    print('Finished printing.')

def preprocess_years(text, gender, year):

    textS = simplify(text)
    textT = tokenize(textS)
    pos_list = pos_tagger(textS, textT)
    textW = remove_stopword(textT, pos_list)
    textL = lemmatize(textW, pos_list)

    if 'print' in argv:
        write_file('%s/%s/0_simple/%s.txt' % (DESTFOL, gender, year), textS)
        write_file('%s/%s/1_tokenized/%s.txt' % (DESTFOL, gender, year),
            ' '.join(textT))
        write_file('%s/%s/2_stopwords/%s.txt' % (DESTFOL, gender, year),
            ' '.join(textW))
        write_file('%s/%s/3_lemmatized/%s.txt' % (DESTFOL, gender, year),
            ' '.join(textL))

    print('Finished processing %s.' % (year))

#-------------------------------------------------------------------------------

def main():

    if 'gender' in argv:
        if ('female' in argv):
            preprocess_gender('fem')

        if ('male' in argv):
            preprocess_gender('male')

    if 'years' in argv:
        if ('female' in argv):
            females = read_folder('fem')
            for year, text in females.items():
                preprocess_years(text, 'fem', year)

        if ('male' in argv):
            males = read_folder('male')
            for year, text in males.items():
                preprocess_years(text, 'male', year)

if __name__ == '__main__':
    main()
