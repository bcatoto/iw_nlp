#!/usr/bin/env python

from sys import argv
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# reads in text
def read_file(filename):
    inFile = open(filename, mode='r', encoding='ISO-8859-1')
    with inFile as file:
        text = file.read()
    inFile.close()
    return text

# reads in files from folder
def read_folder(name):
    list = {}
    for file in os.listdir(os.getcwd() + '/cleaned_data/%s_lines' % (name)):
        if file.endswith('.txt'):
            year = file[0:4]
            list[year] = read_file('cleaned_data/%s_lines/%s' % (name, file))
    return list

# lowers all letters and removes non-alphanumeric charactrs
def simplify(text):
    regex = re.compile('([^\s\w]|_)+')
    return regex.sub('', text.lower())

# tokenizes text
def tokenize(text):
    return nltk.word_tokenize(text)

# removes stopwords from text
def remove_stopword(text_list):
    stopwords = nltk.corpus.stopwords.words('english')
    return [word for word in text_list if word not in stopwords]

# lemmatizes text
def lemmatize(text_list):
    lemma = WordNetLemmatizer()
    return [lemma.lemmatize(word) for word in text_list]

def write_file(filename, text):
    outFile = open(filename, mode='w', encoding='ISO-8859-1')
    outFile.write(text)
    outFile.close()
    return text

#-------------------------------------------------------------------------------

def preprocess_data(text, name, print):

    textS = simplify(text)
    textT = tokenize(textS)
    textW = remove_stopword(textT)
    textL = lemmatize(textW)

    if print:
        write_file('preprocessed_data/0_%s_simple.txt' % (name), text)
        write_file('preprocessed_data/1_%s_tokenized.txt' % (name),
            ' '.join(textT))
        write_file('preprocessed_data/2_%s_stopwords.txt' % (name),
            ' '.join(textW))
        write_file('preprocessed_data/3_%s_lemmatized.txt' % (name),
            ' '.join(textL))

def preprocess_years(text, gender, year, print):

    textS = simplify(text)
    textT = tokenize(textS)
    textW = remove_stopword(textT)
    textL = lemmatize(textW)

    if print:
        write_file('preprocessed_data/%s/0_simple/%s.txt' % (gender, year), text)
        write_file('preprocessed_data/%s/1_tokenized/%s.txt' % (gender, year),
            ' '.join(textT))
        write_file('preprocessed_data/%s/2_stopwords/%s.txt' % (gender, year),
            ' '.join(textW))
        write_file('preprocessed_data/%s/3_lemmatized/%s.txt' % (gender, year),
            ' '.join(textL))

#-------------------------------------------------------------------------------

def main():
    # boolean for whether to print preprocessing steps
    print = 'print' in argv

    if 'years' in argv:
        females = read_folder('fem')
        for year, text in females.items():
            preprocess_years(text, 'fem', year, print)

        males = read_folder('male')
        for year, text in males.items():
            preprocess_years(text, 'male', year, print)

    if 'all' in argv:
        femfile = read_file('cleaned_data/fem_lines.txt')
        preprocess_data(femfile, 'fem', print)

        malefile = read_file('cleaned_data/male_lines.txt')
        preprocess_data(malefile, 'male', print)

if __name__ == '__main__':
    main()
