#!/usr/bin/env python

from spacy.lang.en import English
from spacy.tokenizer import Tokenizer
from spacy.pipeline import Tagger


nlp = English()

#-------------------------------------------------------------------------------

# tokenizes text
def tokenize(text):
    tokenizer = Tokenizer(nlp.vocab)
    return tokenizer(text)

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
