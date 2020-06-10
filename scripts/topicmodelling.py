#!/usr/bin/env python

from sys import argv
import random
from helper import read_folder_text
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation

SRCFOL = '../3_preprocessed_data'
DESTFOL = '../4_topics'

INTRUDER = ['artist', 'singer', 'umpire', 'zoning', 'gang', 'game', 'opera',
    'siding']

#-------------------------------------------------------------------------------

def topic_model(vect, model, texts, outFile, oTopics, oTopIntr, oIntruder, year,
    gender, n_words):
    tf = vect.fit_transform(texts)
    results = model.fit(tf)
    names = vect.get_feature_names()

    outFile.write('%d, %s\n' % (year, gender))

    topics = model.components_
    for id, topic in enumerate(topics):
        if id > 9:
            break
        vocab = [names[i] for i in topic.argsort()[:-n_words - 1:-1]]
        outFile.write('Topic %d: %s\n' % (id, ' '.join(vocab)))
        oTopics.write('%s\n' % (' '.join(vocab)))

        rand = random.randrange(0, n_words)
        oIntruder.write('%d\n' % (rand + 1))
        words = []
        for i in range(0, n_words):
            if i == rand:
                top_intr = topics[random.randrange(0, len(topics))].argsort()
                intruder = names[top_intr[random.randrange(n_words, n_words + 10)]]
                words.append(intruder)
            words.append(vocab[i])
        oTopIntr.write('%s\n' % (' '.join(words)))
    outFile.write('\n')

def model(model, model_name, n_topics, n_words):
    vect = TfidfVectorizer(max_df=10, min_df=0)

    outFile = open('%s/%s/results_%dx%d.txt' % (DESTFOL, model_name, n_topics, n_words),
        mode='w', encoding='utf-8')
    oTopics = open('%s/%s/topics.txt' % (DESTFOL, model_name),
        mode='w', encoding='utf-8')
    oTopIntr = open('%s/%s/topics-with-intruder.txt' % (DESTFOL, model_name),
        mode='w', encoding='utf-8')
    oIntruder = open('%s/%s/intruder.txt' % (DESTFOL, model_name),
        mode='w', encoding='utf-8')

    for year in range(1975, 2016):
        fems = read_folder_text('%s/fem/%d' % (SRCFOL, year))
        topic_model(vect, model, fems, outFile, oTopics, oTopIntr, oIntruder,
            year, 'Female', n_words)

        males = read_folder_text('%s/male/%d' % (SRCFOL, year))
        topic_model(vect, model, males, outFile, oTopics, oTopIntr, oIntruder,
            year, 'Male', n_words)

    oTopics.close()
    oTopIntr.close()
    oIntruder.close()

#-------------------------------------------------------------------------------

def main():
    n_topics = int(argv[1])
    n_words = int(argv[2])

    lda = LatentDirichletAllocation(
        n_components=n_topics,
        learning_method='online',
        learning_offset=50.0,
    )
    nmf = NMF(n_components=n_topics)

    model(lda, 'lda', n_topics, n_words)
    model(nmf, 'nmf', n_topics, n_words)

if __name__ == '__main__':
    main()
