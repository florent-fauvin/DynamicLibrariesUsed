# -*-coding:utf-8 -*


"""
Usage : python readOutputFile.py filename
"""


import sys
import json


# Arguments tests
script = sys.argv[0]
if len(sys.argv) != 2 or not sys.argv[1]:
    print "Usage : python {} filename".format(script)

else:
    # Arguments
    filename = sys.argv[1]

    try:
        f = open(filename,'r')
    except IOError as e:
        print "{} : IOError ({}) : {}".format(e.filename, e.errno, e.strerror)
    except:
        print "Unexpected error : {}\nThis script stopped.".format(sys.exc_info()[0])
    else:
        js = f.read()
        l = json.loads(js)

        print "****************************************************************"
        print "Reading from the {} file.\nThe most used dynamic libraries are (extract) :".format(filename)
        for t in range(0, min(10,len(l))):
            # print t
            print "{}\t: {} executable(s)".format(l[t][0],l[t][1][0])
        print "****************************************************************"
