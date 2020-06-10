#!/usr/bin/env python

from sys import argv
import os
import config
from classes import Movie, Character
from helper import clear_dir, read_folder_dict

CORNELL_SRCFOL = '../1_cleaned_data/cornell'
IMSDB_SRCFOL = '../1_cleaned_data/imsdb'
DESTFOL = '../2_parsed_data'

#-------------------------------------------------------------------------------

def read_data(movies, characters, females, males, unknowns):

    inMovies = open('%s/1_titles_clean.txt' % (CORNELL_SRCFOL), mode='r',
        encoding='ISO-8859-1')
    inChars = open('%s/3_characters_gendered_genderize.txt' % (CORNELL_SRCFOL),
        mode='r', encoding='ISO-8859-1')
    inLines = open('%s/1_lines_clean.txt' % (CORNELL_SRCFOL), mode='r',
        encoding='ISO-8859-1')

    # Stores movie metadata
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

    # Stores character metadata
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

        # Adds character to Characters object corresponding to gender
        if (character.gender() == 'f'):
            females.append(character)
        elif (character.gender() == 'm'):
            males.append(character)
        else:
            unknowns.append(character)

    # Stores lines with corresponding character
    for line in inLines:
        fields = line.replace('\n', '').rsplit('\t')

        # Continue if no line is spoken
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

def cornell():
    movies = []
    characters = []
    females = []
    males = []
    unknowns = []

    # Reads in movies, characters, and lines data
    read_data(movies, characters, females, males, unknowns)

    # Parses all movie lines by gender, year, and movie
    for movie in movies:
        if movie.year() < 1975 or movie.year() > 2005:
            continue

        year = str(movie.year())
        title = movie.title()
        outFem = open('%s/fem/%s/%s.txt' % (DESTFOL, year, title), mode='a+',
            encoding='ISO-8859-1')
        outMale = open('%s/male/%s/%s.txt' % (DESTFOL, year, title), mode='a+',
            encoding='ISO-8859-1')

        for char in movie.characters():
            if char.is_fem():
                outFem.write(char.lines())
            elif char.is_male():
                outMale.write(char.lines())

        outFem.close()
        outMale.close()

    # Counts
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

    print('CORNELL MOVIE DIALOG DATABASE:')
    print('NUMBER OF CHARACTERS')
    print('\tMale:\t\t\t%d' % (len(males)))
    print('\tFemale:\t\t%d' % (len(females)))
    print('\tUnknown:\t%d' % (len(unknowns)))
    print()

    print('NUMBER OF LINES SPOKEN')
    print('\tMale:\t\t\t%d' % (maleLines))
    print('\tFemale:\t\t%d' % (femLines))
    print('\tUnknown:\t%d' % (unkLines))
    print()

    print('NUMBER OF WORDS SPOKEN')
    print('\tMale:\t\t\t%d' % (maleWords))
    print('\tFemale:\t\t%d' % (femWords))
    print('\tUnknown:\t%d' % (unkWords))
    print('----------------------------------------')

#-------------------------------------------------------------------------------

def imsdb():
    fem = 0
    male = 0
    unk = 0

    maleLines = 0
    femLines = 0
    unkLines = 0

    maleWords = 0
    femWords = 0
    unkWords = 0

    for year in range(1975, 2016):
        movies = read_folder_dict('%s/%d' % (IMSDB_SRCFOL, year), year)

        for movie in movies:
            characters = []
            title = movie['title']
            lines = movie['text'].split('\n')

            outFem = open('%s/fem/%d/%s' % (DESTFOL, year, title),
                mode='w', encoding='ISO-8859-1')
            outMale = open('%s/male/%d/%s' % (DESTFOL, year, title),
                mode='w', encoding='ISO-8859-1')

            for line in lines:
                fields = line.split('\t')

                if len(fields) < 3:
                    continue

                name = fields[0]
                gender = fields[1]
                line = fields[2]

                if gender == 'f':
                    outFem.write(line + ' ')
                    femLines += 1
                    femWords += len(line.split(' '))
                elif gender == 'm':
                    outMale.write(fields[2] + ' ')
                    maleLines += 1
                    maleWords += len(line.split(' '))
                else:
                    unkLines += 1
                    unkWords += len(line.split(' '))

                if name not in characters:
                    characters.append(name)
                    if gender == 'f':
                        fem += 1
                    elif gender == 'm':
                        male += 1
                    else:
                        unk += 1

            outFem.close()
            outMale.close()

    print('INTERNET MOVIE SCRIPT DATABASE:')
    print('NUMBER OF CHARACTERS')
    print('\tMale:\t\t\t%d' % (male))
    print('\tFemale:\t\t%d' % (fem))
    print('\tUnknown:\t%d' % (unk))
    print()

    print('NUMBER OF LINES SPOKEN')
    print('\tMale:\t\t\t%d' % (maleLines))
    print('\tFemale:\t\t%d' % (femLines))
    print('\tUnknown:\t%d' % (unkLines))
    print()

    print('NUMBER OF WORDS SPOKEN')
    print('\tMale:\t\t\t%d' % (maleWords))
    print('\tFemale:\t\t%d' % (femWords))
    print('\tUnknown:\t%d' % (unkWords))

#-------------------------------------------------------------------------------

def main():
    # Creates year folders if they don't exist; clears them if they do
    for year in range(1975, 2016):
        clear_dir('%s/fem/%d' % (DESTFOL, year))
        clear_dir('%s/male/%d' % (DESTFOL, year))

    cornell()
    imsdb()

if __name__ == '__main__':
    main()
