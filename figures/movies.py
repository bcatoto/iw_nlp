#!/usr/bin/env python

from sys import argv

#-------------------------------------------------------------------------------

def main():
    inFile = open('title.basics.tsv', mode='r')
    outFile = open('movies_by_year.txt', mode='w')

    years = {}

    for line in inFile:
        fields = line.split('\t')
        type = fields[1]
        year = fields[5]

        if type == 'movie':
            if year == '\\N' or int(year) > 2015:
                continue
            if year in years:
                years[year] = years[year] + 1
            else:
                years[year] = 1

    for year in sorted(years.keys()):
        outFile.write('%s\t%d\n' % (year, years[year]))

    outFile.close()
    inFile.close()

if __name__ == '__main__':
    main()
