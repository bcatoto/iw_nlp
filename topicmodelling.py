#!/usr/bin/env python

from sys import argv
from pre_io import read_folder
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

# number of topics and top words
n_topics = 5
n_words = 5

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
    if 'female' in argv:
        females = read_folder('2_preprocessed_data_spacy/fem')
        texts = [*females.values()]

        if 'lda' in argv:
            lda(texts, 'Female')
        if 'nmf' in argv:
            nmf(texts, 'Female')

    if 'male' in argv:
        males = read_folder('2_preprocessed_data_spacy/male')
        texts = [*males.values()]

        if 'lda' in argv:
            lda(texts, 'Male')
        if 'nmf' in argv:
            nmf(texts, 'Male')


if __name__ == '__main__':
    main()
