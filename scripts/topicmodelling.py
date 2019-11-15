#!/usr/bin/env python

from sys import argv
from in_out import read_folder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

# number of topics and top words
n_topics = 5
n_words = 5

SRCFOL = '../3_preprocessed_data'

#-------------------------------------------------------------------------------

def display(model, feature_names, gender, model_name):
    print('%s, %s' % (gender, model_name))

    for id, topic in enumerate(model.components_):
        topics = ' '.join([feature_names[i] for i in topic.argsort()[:-n_words - 1:-1]])
        print('Topic %d: %s' % (id, topics))

    print()

def lda(texts, gender):
    vect = CountVectorizer(max_df=0.95, min_df=2)
    tf = vect.fit_transform(texts)
    names = vect.get_feature_names()

    model = LatentDirichletAllocation(n_components=n_topics, max_iter=5,
        learning_method='online', learning_offset=50.,random_state=0).fit(tf)

    display(model, names, gender, 'LDA')

def nmf(texts, gender):
    vect = TfidfVectorizer(max_df=0.95, min_df=2)
    tf = vect.fit_transform(texts)
    names = vect.get_feature_names()

    model = NMF(n_components=n_topics, max_iter=5, random_state=0).fit(tf)

    display(model, names, gender, 'NMF')

#-------------------------------------------------------------------------------

def main():

    females = read_folder('%s/fem' % (SRCFOL))
    texts = [*females.values()]
    lda(texts, 'Female')
    nmf(texts, 'Female')

    males = read_folder('%s/male' % (SRCFOL))
    texts = [*males.values()]
    lda(texts, 'Male')
    nmf(texts, 'Male')

if __name__ == '__main__':
    main()
