#!/usr/bin/env python

import os

#-------------------------------------------------------------------------------

# Returns all files in folder
def get_files(folder):
    files = []
    for file in os.listdir(folder):
        if file.endswith('.txt') or file.endswith('.html'):
            files.append(file)
    return files

#-------------------------------------------------------------------------------

# Reads in text
def read_file(filename):
    inFile = open(filename, mode='r', encoding='ISO-8859-1')
    with inFile as file:
        text = file.read()
    inFile.close()
    return text

# Reads in text from folders and returns dictionary object with movie title,
# year, and text of each file
def read_folder_dict(folder, year):
    list = []
    files = get_files(folder)
    for file in files:
        list.append({
            'title' : file,
            'year' : year,
            'text' : read_file('%s/%s' % (folder, file))
        })
    return list

# Reads in text from folders and returns list of scripts
def read_folder_text(folder):
    list = []
    files = get_files(folder)
    for file in files:
        list.append(read_file('%s/%s' % (folder, file)))
    return list

#-------------------------------------------------------------------------------

# Writes given text to given filename
def write_file(filename, text):
    outFile = open(filename, mode='w', encoding='ISO-8859-1')
    outFile.write(text)
    outFile.close()

#-------------------------------------------------------------------------------

# Removes all .txt files in given folder
def remove_files(folder):
    files = get_files(folder)
    for file in files:
        os.remove(os.path.join(folder, file))

# Creates year directory in dest and name folders if it does not exist and
# clears directory of .txt files if it does exist
def clear_dir(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
    else:
        remove_files(dir)
