#!/usr/bin/env python

from sys import argv
import numpy as np
import pandas as pd

#-------------------------------------------------------------------------------

def remove(string, sub):
    return string.replace(sub, '')

def txt_title(title):
    title = remove(title, ':')
    title = remove(title, '\'')
    title = remove(title, ',')
    title = remove(title, '.')
    return '_'.join(title.rsplit(' '))

def print_list(list):
    for item in list:
        print(item)

def read_data(movies, characters, females, males, unknowns):

    # stores movie metadata
    for line in inMovies:
        fields = remove(line, '\n').rsplit('\t')

        id = int(fields[0][1:])
        title = remove(fields[1], '"')
        year = int(fields[2])
        rating = float(fields[3])
        votes = int(fields[4])
        genres = fields[5].rsplit(', ')

        movie = Movie(id, title, year, rating, votes, genres)
        movies.append(movie)

    # stores character metadata
    for line in inChars:
        fields = remove(line, '\n').rsplit('\t')

        id = int(fields[0][1:])
        name = remove(fields[1], '"')
        movieID = int(fields[2][1:])
        movie = movies[movieID]
        gender = fields[4]
        pos = int(fields[5])

        character = Character(id, name, movie, gender, pos)
        movie.add_character(character)
        characters.append(character)

        # adds character to Characters object corresponding to gender
        if (character.gender() == 'f'):
            females.append(character)
        elif (character.gender() == 'm'):
            males.append(character)
        # elif (character.gender() == "mf"):
            # mf.append(character)
        # elif (character.gender() == "mm"):
            # mm.append(character)
        else:
            unknowns.append(character)

    # stores lines with corresponding character
    for line in inLines:
        fields = remove(line, '\n').rsplit('\t')

        # if no line is spoken
        if (len(fields) < 5):
            continue

        id = int(fields[0][1:])
        charID = int(fields[1][1:])
        movieID = int(fields[2][1:])
        text = fields[4]

        characters[charID].add_line(text)

    inMovies.close()
    inChars.close()
    inLines.close()

#-------------------------------------------------------------------------------

def main():

    movies = pd.read_table('cleaned_data/1_movie_titles_metadata_clean.txt',
        sep = '\t',
        names = ['id', 'title', 'year', 'rating', 'votes', 'genres'])
    movies.set_index('id', inplace = True)

    characters = pd.read_table('cleaned_data/2_movie_titles_metadata_gendered_title.txt',
        sep = '\t',
        names = ['id', 'name', 'movieid', 'title', 'gender', 'position'])
    characters.set_index('id', inplace = True)

    # reads in movies, characters, and lines data
    # read_data(movies, characters, females, males, unknowns)

    if (argv[1] == 'folder'):
        for movie in movies:
            title = txt_title(movie.title())
            outFem = open('cleaned_data/fem_lines/%s.txt' % (title), mode='w',
                encoding='ISO-8859-1')
            outMale = open('cleaned_data/male_lines/%s.txt' % (title), mode='w',
                encoding='ISO-8859-1')

            for char in movie.characters():
                if (char.is_fem()):
                    outFem.write(char.lines())
                elif (char.is_male()):
                    outMale.write(char.lines())

            outFem.close()
            outMale.close()

    elif (argv[1] == 'file'):
        outFem = open('cleaned_data/fem_line.txt', mode='w',
            encoding='ISO-8859-1')
        outMale = open('cleaned_data/male_lines.txt', mode='w',
            encoding='ISO-8859-1')

        for fem in females:
            outFem.write(fem.lines())

        for male in males:
            outMale.write(male.lines())

        outFem.close()
        outMale.close()

    else:
        print('dataparser: Not a valid mode')

    maleLines = 0
    femLines = 0
    unkLines = 0
    maleWords = 0
    femWords = 0
    unkWords = 0

    for male in males:
        maleLines += male.line_count()
        maleWords += male.word_count()

    for fem in females:
        femLines += fem.line_count()
        femWords += fem.word_count()

    for unk in unknowns:
        unkLines += unk.line_count()
        unkWords += unk.word_count()

    print('# of characters: %d %d %d' % \
        (len(males), len(females), len(unknowns)))
    print('# of lines: %d %d %d' % (maleLines, femLines, unkLines))
    print('# of words: %d %d %d' % (maleWords, femWords, unkWords))



if __name__ == '__main__':
    main()
