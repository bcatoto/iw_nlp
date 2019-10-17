#!/usr/bin/env python

import os

#-------------------------------------------------------------------------------

# reads in text
def read_file(filename):
    inFile = open(filename, mode='r', encoding='ISO-8859-1')
    with inFile as file:
        text = file.read()
    inFile.close()
    return text

def read_list(filename):
    return read_file(filename).split(' ')

# reads in files from folder
def read_folder(directory):
    list = {}
    for file in os.listdir(os.getcwd() + '/%s' % (directory)):
        if file.endswith('.txt'):
            year = file[0:4]
            list[year] = read_file('%s/%s' % (directory, file))
    return list

def write_file(filename, text):
    outFile = open(filename, mode='w', encoding='ISO-8859-1')
    outFile.write(text)
    outFile.close()
    return text

def write_word_pos(filename, text_list, pos_list):
    outFile = open(filename, mode='w', encoding='ISO-8859-1')
    for word, pos in zip(text_list, pos_list):
        outFile.write('%s %s ' % (word, pos))
    outFile.close()
