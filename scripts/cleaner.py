#!/usr/bin/env python

from sys import argv, stderr

FOL = '../1_cleaned_data'

#-------------------------------------------------------------------------------

# makes gender lowercase, replaces 0 in position with '?'
def clean_characters():
    inLines = open('%s/0_movie_characters_metadata.txt' % (FOL), mode='r',
        encoding='ISO-8859-1')
    outLines = open('%s/1_characters_clean.txt' % (FOL), mode='w',
        encoding='ISO-8859-1')

    for line in inLines:
        fields = line.rsplit('\t')

        fields[4] = fields[4].lower() # gender
        fields[5] = '0\n' if fields[5] == '?\n' else fields[5] # position

        newline = '\t'.join(fields)
        outLines.write(newline)

    outLines.close()
    inLines.close()

#-------------------------------------------------------------------------------

# removes '/I' from year and removes single quotes and square brackets from
# genres
def clean_movies():
    inLines = open('%s/0_movie_titles_metadata.txt' % (FOL), mode='r',
        encoding='ISO-8859-1')
    outLines = open('%s/1_titles_clean.txt' % (FOL), mode='w',
        encoding='ISO-8859-1')

    for line in inLines:
        fields = line.rsplit('\t')

        fields[2] = fields[2].replace('/I', '') # year
        fields[5] = fields[5].replace('[', '').replace(']', '').replace('\'', '') # genres

        newline = '\t'.join(fields)
        outLines.write(newline)

    outLines.close()
    inLines.close()

#-------------------------------------------------------------------------------

# splits data by tab instead of '+++$+++'
def clean_lines():
    inLines = open('%s/0_movie_lines.txt' % (FOL), mode='r',
        encoding='ISO-8859-1')
    outLines = open('%s/1_lines_clean.txt' % (FOL), mode='w',
        encoding='ISO-8859-1')

    for line in inLines:
        fields = line.rsplit(' +++$+++ ')
        newline = '\t'.join(fields)
        outLines.write(newline)

    outLines.close()
    inLines.close()

#-------------------------------------------------------------------------------

def main():

    if len(argv) < 2:
        print('cleaner: No mode entered', file=stderr)
    if 'characters' in argv:
        clean_characters()
    if 'titles' in argv:
        clean_movies()
    if 'lines' in argv:
        clean_lines()

if __name__ == '__main__':
    main()
