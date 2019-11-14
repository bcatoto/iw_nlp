#!/usr/bin/env python

from sys import argv, stderr

#-------------------------------------------------------------------------------

def title_genderizer(name, titles, gender):
    for title in titles:
        if (name.lower().find(title) > -1):
            return gender
    return '?'

#-------------------------------------------------------------------------------

def main():

    inLines = open('1_characters_clean.txt', mode='r', encoding='ISO-8859-1')
    outLines = open('2_characters_gendered_title.txt', mode='w',
        encoding='ISO-8859-1')

    FEMALE = ['female', 'woman', 'girl', 'mrs.', 'ms.', 'miss', 'wife', 'mom',
        'mother', 'sister']
    MALE = ['male', ' man', 'man ', 'boy', 'guy', 'mr.', 'husband', 'dad',
        'father', 'brother']

    # updates gender of characters
    for line in inLines:
        fields = line.rsplit('\t')

        name = fields[1]

        # genderize by female title
        if (fields[4] == '?'):
            fields[4] = title_genderizer(name, FEMALE, 'f')

        # genderize with male title
        if (fields[4] == '?'):
            fields[4] = title_genderizer(name, MALE, 'm')

        # print updated character metadata
        newline = '\t'.join(fields)
        outLines.write(newline)

    outLines.close()
    inLines.close()

if __name__ == '__main__':
    main()
