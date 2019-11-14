#!/usr/bin/env python

from sys import argv
from classes import Movie, Character

SRCFOL = '../1_cleaned_data'

#-------------------------------------------------------------------------------

def read_data(movies, characters, females, males, unknowns):

    inMovies = open('%s/1_titles_clean.txt' % (SRCFOL), mode='r',
        encoding='ISO-8859-1')
    inChars = open('%s/3_characters_gendered_genderize.txt' % (SRCFOL),
        mode='r', encoding='ISO-8859-1')
    inLines = open('%s/1_lines_clean.txt' % (SRCFOL), mode='r',
        encoding='ISO-8859-1')

    # stores movie metadata
    for line in inMovies:
        fields = line.replace('\n', '').rsplit('\t')

        id = int(fields[0][1:])
        title = fields[1]
        year = int(fields[2])
        rating = float(fields[3])
        votes = int(fields[4])
        genres = None if len(fields) < 6 else fields[5].rsplit(', ')

        movie = Movie(id, title, year, rating, votes, genres)
        movies.append(movie)
    print('Finished reading in movies...')

    # stores character metadata
    for line in inChars:
        fields = line.replace('\n', '').rsplit('\t')

        id = int(fields[0][1:])
        name = fields[1]
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
        else:
            unknowns.append(character)
    print('Finished reading in characters...')

    # stores lines with corresponding character
    for line in inLines:
        fields = line.replace('\n', '').rsplit('\t')

        # if no line is spoken
        if (len(fields) < 5):
            continue

        id = int(fields[0][1:])
        charID = int(fields[1][1:])
        movieID = int(fields[2][1:])
        text = fields[4]

        characters[charID].add_line(text)
    print('Finished reading in lines...')

    inMovies.close()
    inChars.close()
    inLines.close()

#-------------------------------------------------------------------------------

def main():

    movies = []
    characters = []
    females = []
    males = []
    unknowns = []

    # reads in movies, characters, and lines data
    read_data(movies, characters, females, males, unknowns)

    # prints all movie lines separated by gender and year
    for movie in movies:
        if movie.year() < 1975 or movie.year() > 2005:
            continue

        filename = str(movie.year())
        outFem = open('fem/%s.txt' % (filename), mode='a+',
            encoding='ISO-8859-1')
        outMale = open('male/%s.txt' % (filename), mode='a+',
            encoding='ISO-8859-1')

        for char in movie.characters():
            if char.is_fem():
                outFem.write(char.lines())
            elif char.is_male():
                outMale.write(char.lines())

        outFem.close()
        outMale.close()
        print('Finished parsing %s...' % (movie.title()))

    # counts
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

    print('----------------------------------------')
    print('NUMBER OF CHARACTERS')
    print('\tMale:\t\t%d' % (len(males)))
    print('\tFemale:\t\t%d' % (len(females)))
    print('\tUnknown:\t%d' % (len(unknowns)))

    print('----------------------------------------')
    print('NUMBER OF LINES SPOKEN')
    print('\tMale:\t\t%d' % (maleLines))
    print('\tFemale:\t\t%d' % (femLines))
    print('\tUnknown:\t%d' % (unkLines))

    print('----------------------------------------')
    print('NUMBER OF WORDS SPOKEN')
    print('\tMale:\t\t%d' % (maleWords))
    print('\tFemale:\t\t%d' % (femWords))
    print('\tUnknown:\t%d' % (unkWords))

if __name__ == '__main__':
    main()
