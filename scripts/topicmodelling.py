#!/usr/bin/env python

from sys import argv
from helper import read_folder_text
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

# number of topics and top words
n_topics = 3
n_words = 5

SRCFOL = '../3_preprocessed_data'

#-------------------------------------------------------------------------------

def display(model, feature_names, gender, model_name, year):
    print('%s, %s, %d' % (gender, model_name, year))

    for id, topic in enumerate(model.components_):
        topics = ' '.join([feature_names[i] for i in topic.argsort()[:-n_words - 1:-1]])
        print('Topic %d: %s' % (id, topics))

    print()

def lda(texts, gender, year):
    vect = CountVectorizer(max_df=0.95, min_df=2)
    tf = vect.fit_transform(texts)
    names = vect.get_feature_names()

    model = LatentDirichletAllocation(n_components=n_topics, max_iter=5,
        learning_method='online', learning_offset=50.,random_state=0).fit(tf)

    display(model, names, gender, 'LDA', year)

def nmf(texts, gender, year):
    vect = TfidfVectorizer(max_df=0.95, min_df=2)
    tf = vect.fit_transform(texts)
    names = vect.get_feature_names()

    model = NMF(n_components=n_topics, max_iter=5, random_state=0).fit(tf)

    display(model, names, gender, 'NMF', year)

#-------------------------------------------------------------------------------

def main():

    for year in range(1975, 2006):
        females = read_folder_text('%s/fem/%d' % (SRCFOL, year))
        lda(females, 'Female', year)
        nmf(females, 'Female', year)

        males = read_folder_text('%s/male/%d' % (SRCFOL, year))
        lda(males, 'Male', year)
        nmf(males, 'Male', year)

if __name__ == '__main__':
    main()
