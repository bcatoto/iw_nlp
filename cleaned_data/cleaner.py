#!/usr/bin/env python

from sys import argv

# adds double quotations around character name and movie title
def clean_characters(inLines, outLines):
    for line in inLines:
        fields = line.rsplit('\t')

        fields[1] = '"' + fields[1] + '"' # name
        fields[3] = '"' + fields[3] + '"' # movie title
        fields[4] = fields[4].lower() # lowers gender
        fields[5] = '0\n' if fields[5] == '?\n' else fields[5]

        newline = '\t'.join(fields)
        outLines.write(newline)

# removes '/I' from year and removes single quotes and square brackets from
# genres; adds double quotations around movie title
def clean_movies(inLines, outLines):
    for line in inLines:
        fields = line.rsplit('\t')

        fields[1] = '"' + fields[1].replace(':', '') + '"' # movie title
        fields[2] = fields[2].replace('/I', '') # year
        fields[5] = fields[5].replace('[', '').replace(']', '').replace('\'', '') # genres

        newline = '\t'.join(fields)
        outLines.write(newline)

def clean_lines(inLines, outLines):
    for line in inLines:
        fields = line.rsplit(' +++$+++ ')
        newline = '\t'.join(fields)
        outLines.write(newline)

def main():

    mode = argv[1]
    inLines = open(argv[2], mode='r', encoding='ISO-8859-1')
    outLines = open(argv[3], mode='w', encoding='ISO-8859-1')

    if (mode == 'characters'):
        clean_characters(inLines, outLines)
    elif (mode == 'movies'):
        clean_movies(inLines, outLines)
    elif (mode == 'lines'):
        clean_lines(inLines, outLines)
    else:
        print('cleaner: Not a valid mode.')

    outLines.close()
    inLines.close()

if __name__ == '__main__':
    main()
