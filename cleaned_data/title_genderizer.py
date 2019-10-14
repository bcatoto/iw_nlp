#!/usr/bin/env python

from sys import argv

#-------------------------------------------------------------------------------

def title_genderizer(name, titles, gender):
    for title in titles:
        if (name.lower().find(title) > -1):
            return gender
    return '?'

#-------------------------------------------------------------------------------

def main():

    inLines = open(argv[1], mode='r', encoding='ISO-8859-1')
    outLines = open(argv[2], mode='w', encoding='ISO-8859-1')

    female = ['female', 'woman', 'girl', 'mrs.', 'ms.', 'miss', 'wife', 'mom',
        'mother', 'sister']
    male = ['male', ' man', 'man ', 'boy', 'guy', 'mr.', 'husband', 'dad',
        'father', 'brother']

    test = ''

    # updates gender of characters
    for line in inLines:
        fields = line.rsplit('\t')

        name = fields[1]

        # genderize by female title
        if (fields[4] == '?'):
            fields[4] = title_genderizer(name, female, 'f')

        # genderize with male title
        if (fields[4] == '?'):
            fields[4] = title_genderizer(name, male, 'm')

        # print updated character metadata
        newline = '\t'.join(fields)
        outLines.write(newline)

    outLines.close()
    inLines.close()

if __name__ == '__main__':
    main()
