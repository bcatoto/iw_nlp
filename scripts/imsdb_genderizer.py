#!/usr/bin/env python

from sys import argv, stderr
import config
from helper import clear_dir, read_folder_dict
from title_genderizer import title_genderizer
from genderize import Genderize
from gender_genderizer import gender_genderizer

SRCFOL = '../0_scraped_data/parsed_txt'
DESTFOL = '../1_cleaned_data/imsdb'

#-------------------------------------------------------------------------------

def getGender(name, characters, genderize):
    if name in characters:
        return characters[name]

    gender = '?'
    if gender == '?' and title_genderizer(name, 'f') == 'f':
        gender = 'f'
    if gender == '?' and title_genderizer(name, 'm') == 'm':
        gender = 'm'
    if gender == '?':
        result = gender_genderizer(genderize, name)
        if result['probability'] > 0.6:
            gender = result['gender'][0:1]
        else:
            gender = '?'

    characters[name] = gender
    return gender

#-------------------------------------------------------------------------------

def main():
    # Creates year folders if they don't exist; clears them if they do
    for year in range(1975, 2016):
        clear_dir('%s/%d' % (DESTFOL, year))

    genderize = Genderize(
        user_agent='GenderizeDocs/0.0',
        api_key=config.api_key,
        timeout=60)

    femCount = 0
    maleCount = 0
    unkCount = 0

    for year in range(1975, 2016):

        print('Gendering movies in %d...' % (year))

        movies = read_folder_dict('%s/%d' % (SRCFOL, year), year)

        for movie in movies:
            characters = {}
            title = movie['title']
            lines = movie['text'].split('\n')

            outFile = open('%s/%d/%s' % (DESTFOL, year, title), mode='w',
                encoding='ISO-8859-1')

            for i in range(2, len(lines)):
                fields = lines[i].split('\t')

                if len(fields) < 2:
                    continue

                name = fields.pop(0)
                gender = getGender(name, characters, genderize)
                outFile.write('%s\t%s\t%s\n' % (name, gender, ' '.join(fields)))

            for gender in characters.values():
                if gender == '?':
                    unkCount += 1
                elif gender == 'f':
                    femCount += 1
                elif gender == 'm':
                    maleCount += 1

            outFile.close()
            print('Finished %s...' % (title))

        print('----------------------------------------')

    print('NUMBER OF CHARACTERS')
    print('\tMale:\t\t%d' % (maleCount))
    print('\tFemale:\t\t%d' % (femCount))
    print('\tUnknown:\t%d' % (unkCount))

if __name__ == '__main__':
    main()
