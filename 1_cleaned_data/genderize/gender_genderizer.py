#!/usr/bin/env python

from sys import argv, stderr
from genderize import Genderize
import config

#-------------------------------------------------------------------------------

def getGender(genderize, name):
    results = genderize.get(name)
    if len(name) > 1:
        for result in results:
            if result['gender'] is not 'None' and result['probability'] > 0.6:
                return result
    return results[0]

#-------------------------------------------------------------------------------

def main():

    inFile = '../2_characters_gendered_title.txt'
    inLines = open(inFile, mode='r', encoding='ISO-8859-1')

    unknown = []

    # create array of unknown gender characters
    for line in inLines:
        fields = line.rsplit('\t')
        if fields[4] == '?':
            name = fields[4].split(' ')
            unknown.append(fields[1])

    # creates Genderize and gets genders
    genderize = Genderize(
        user_agent='GenderizeDocs/0.0',
        api_key=config.api_key,
        timeout=60)

    results = []
    for name in unknown:
        results.append(getGender(genderize, name.split(' ')))

    # sets pointer to beginning of file
    inLines.seek(0)

    outLines = open('../3_characters_gendered_genderize.txt', mode='w',
        encoding='ISO-8859-1')

    # counts
    changed = 0
    unchanged = 0
    i = 0

    for line in inLines:
        fields = line.rsplit('\t')
        name = fields[1]

        if fields[4] == '?':
            prob = results[i]['probability']
            if prob > 0.6:
                gender = results[i]['gender'][0:1]
                print('CHANGED:\t%s -> %s, %.2f' % (name, gender, prob))
                fields[4] = gender
                changed += 1
            else:
                print('UNCHANGED:\t%s' % (name))
                unchanged += 1
            i += 1

        # print updated character metadata
        newline = '\t'.join(fields)
        outLines.write(newline)

    print('--------------------')
    print('TOTAL UNKNOWN:\t\t%d' % (len(unknown)))
    print('TOTAL CHANGED:\t\t%d' % (changed))
    print('TOTAL UNCHANGED:\t%d' % (unchanged))

    outLines.close()
    inLines.close()

#-------------------------------------------------------------------------------

if __name__ == '__main__':
    main()