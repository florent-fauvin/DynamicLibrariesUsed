# -*-coding:utf-8 -*


"""
Usage : python dynamicLibrariesUsed.py filename
"""


from functions import *
import operator
import sys


# Arguments tests
script = sys.argv[0]
if len(sys.argv) != 2 or not sys.argv[1]:
    print "Usage : python {} filename".format(script)
else:


    # Arguments
    filename = sys.argv[1]


    # The libraries with their number of occurrences.
    libraries={}
    # The folders where the files will be read.
    folders=[]
    # The folders ever parsed.
    parsedFolders=[]
    # folders is filled with the folders of the PATH environment variable.
    appendFoldersFromEnvironmentVariable(folders,'PATH')
    # To append new folders to the PATH folders list.
    # Usage : otherFolders["folder1", "folder2", "folderN"]
    otherFolders=[]
    folders.extend(otherFolders)


    if not folders:
        print "No folder to analyze !"
    else:


        # Print folders that will be parsed
        print "****************************************************************"
        print "The parsed folders are : {}".format(folders)
        print "Don't worry, the inclusion of folders is managed !"
        print "****************************************************************"


        # The folders parsing
        for folder in folders:
            main(libraries, folder, parsedFolders)
        # To sort the libraries dictionary by value
        sortedLibraries = sorted(libraries.items(), key=operator.itemgetter(1), reverse=True)


        if sortedLibraries:
            # The display of results
            print "****************************************************************"
            display(sortedLibraries)
            # The save of results
            print "****************************************************************"
            if save(filename,sortedLibraries):
                print "This result is saved as a json string in the file : {}".format(filename)
            else:
                print "This result is saved in none file. Is the provided file reachable ?".format(script)
            print "****************************************************************"
