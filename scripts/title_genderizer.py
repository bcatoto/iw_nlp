#!/usr/bin/env python

from sys import argv, stderr

FOL = '../1_cleaned_data/cornell'

#-------------------------------------------------------------------------------

def title_genderizer(name, gender):
    # Female titles
    titles = ['female', 'woman', 'girl', 'mrs.', 'ms.', 'miss', 'wife', 'mom',
        'mother', 'sister']

    # Male titles
    if gender == 'm':
        titles = ['male', ' man', 'man ', 'boy', 'guy', 'mr.', 'husband', 'dad',
            'father', 'brother']

    for title in titles:
        if (name.lower().find(title) > -1):
            return gender
    return '?'

#-------------------------------------------------------------------------------

def main():

    inLines = open('%s/1_characters_clean.txt' % (FOL), mode='r',
        encoding='ISO-8859-1')
    outLines = open('%s/2_characters_gendered_title.txt' % (FOL), mode='w',
        encoding='ISO-8859-1')

    # updates gender of characters
    for line in inLines:
        fields = line.rsplit('\t')

        name = fields[1]

        # genderize by female title
        if (fields[4] == '?'):
            fields[4] = title_genderizer(name, 'f')

        # genderize with male title
        if (fields[4] == '?'):
            fields[4] = title_genderizer(name, 'm')

        # print updated character metadata
        newline = '\t'.join(fields)
        outLines.write(newline)

    outLines.close()
    inLines.close()

if __name__ == '__main__':
    main()
