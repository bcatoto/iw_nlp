#!/usr/bin/env python

from sys import stderr
import re
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

#-------------------------------------------------------------------------------

# lowers all letters and removes non-alphanumeric charactrs
def simplify(text):
    regex = re.compile('([^\s\w]|_)+')
    return regex.sub('', text.lower())

# tokenizes text
def tokenize(text):
    return nltk.word_tokenize(text)

def pos_tagger(text, tokenized):
    pos_list = []
    tagged = nltk.pos_tag(text)

    for item in tagged:
        pos = item[1]

        if pos.startswith('J'):
            pos_list.append(wordnet.ADJ)
        elif pos.startswith('V'):
            pos_list.append(wordnet.VERB)
        elif pos.startswith('R'):
            pos_list.append(wordnet.ADV)
        else:
            pos_list.append(wordnet.NOUN)

    if len(pos_list) != len(tokenized):
        print('POS list and text list do not match', file=stderr)

    return pos_list

# removes stopwords from text
def remove_stopword(text_list, pos_list):
    sw = stopwords.words('english')

    new_text_list = []
    new_pos_list = []

    for word, pos in zip(text_list, pos_list):
        if word not in sw:
            new_text_list.append(word)
            new_pos_list.append(pos)

    return (new_text_list, new_pos_list)

# lemmatizes text
def lemmatize(text_list, pos_list):
    lemma = WordNetLemmatizer()
    return [lemma.lemmatize(word, pos) for word, pos in zip(text_list, pos_list)]
