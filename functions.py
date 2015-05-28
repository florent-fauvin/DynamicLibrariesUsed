# -*-coding:utf-8 -*


"""
Module containing various functions for the dynamicLibrariesUsed.py script
"""


import os
import subprocess
import sys
import json


def isReachable(f):
    """
    This function return True if f exists and is readable
    :param f: file, folder or link
    :return: boolean
    """
    if os.access(f, os.F_OK):
        if os.access(f, os.R_OK) :
            return True
    return False


def isFolder(folder):
    if os.path.isdir(folder):
        return True
    return False


def isFile(file):
    if os.path.isfile(file):
        return True
    return False


def isLink(link):
    if os.path.islink(link):
        return True
    return False


def appendFoldersFromEnvironmentVariable(folders,envVar):
    """
    This function appends to the folders list, the folders included in PATH.
    May be it is useful for another environment variable.
    :param folders: list
    :param envVar: environment variable
    """
    try:
        envPath= os.environ[envVar]
    except KeyError:
        print "Be careful : the {} environment variable doesn't exist !".format(envVar)
    else:
        if(envPath):
            envPathFolders = envPath.split(":")
            folders.extend(envPathFolders)


def getDynamicLibraries(file):
    """
    This function returns the dynamic libraries of a executable file
    :param file: executable file
    :return: a list or None
    """

    cmd = "ldd {}".format(file)

    try:
        ret = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        # https://docs.python.org/2/library/subprocess.html?highlight=subprocess.calledprocesserror#subprocess.CalledProcessError
        # print "{} : CalledProcessError ({})".format(e.cmd, e.returncode)
        # print "continue..."
        # NO : if ldd concludes the file is "not a dynamic executable", a error is raised, and we don't want.
        return None
    except :
        return None
    else:
        if ret :
            l1 = ret.split("\n\t")
            if l1:
                l2=[]
                for str1 in l1:
                    if "=>" in str1:
                        l2.append(str1.split("=>", 1)[1])
                    else:
                        l2.append(str1)
                if l2 :
                    l3=[]
                    for str2 in l2:
                        str3 = str2.split("(", 1)[0]
                        str3 = str3.replace(" ","")
                        if str3:
                            l3.append(str3)
                    if l3:
                        return l3
        return None


def append (d,l,f):
    if l :
        for s in l:
            if not s in d:
                d[s]=[]
                d[s].append(1)
                d[s].append([f])
            else:
                d[s][0]+=1
                d[s][1].append(f)

def save(filename,obj):
    if obj:
        s = json.dumps(obj)
        try:
            with open(filename,'w') as f:
                f.write(s)
        except IOError as e:
            print "{} : IOError ({}) : {}".format(e.filename, e.errno, e.strerror)
            return False
        except:
            print "Unexpected error : {}\nThis script stopped.".format(sys.exc_info()[0])
            return False
        else:
            return True


def display(sortedLibraries):
    print "Number of dynamic libraries found : {}\n".format(len(sortedLibraries))
    print "The most used dynamic libraries are (extract) :"
    for t in range(0, min(5,len(sortedLibraries))):
        print "{}\t: {} executable(s)".format(sortedLibraries[t][0],sortedLibraries[t][1][0])


def main(libraries,f,parsedFolders):
    """
    The main function. It is a recursive function.
    :param f: a folder or a file
    :param libraries: the dictionary with the name of the libraries
    """


    f=f.replace("//","/")


    if not isReachable(f):
        if isFolder(f):
            print "Be careful : the {} folder is not reachable !".format(f)
            print "continue..."
        elif isFile(f):
            print "Be careful : the {} file is not reachable !".format(f)
            print "continue..."
        else:
            pass


    elif isLink(f):
        pass
        # Links are ignored.
        # A rustic way to avoid infinite loop, because this function is recursive.


    elif isFolder(f):

        if f in parsedFolders:
            pass
        else:
            parsedFolders.append(f)

            try:
                list = os.listdir(f)
            except OSError as e:
                print "{} : OSError ({}) : {}".format(e.filename, e.errno, e.strerror)
                print "continue..."
            except :
                print "Unexpected error : {}".format(sys.exc_info()[0])
                print "continue..."
            else:
                print "The {} folder is parsing. Wait please...".format(f)
                for subf in list:
                    path="{}/{}".format(f, subf)
                    main(libraries,path,parsedFolders)  # The recursive call


    elif isFile(f): # The fact this file is executable or not, is not checked here.

        libs = getDynamicLibraries(f)
        if libs:
            append(libraries, libs, f)


    else:
        pass
        # If f is neither a folder nor a file

