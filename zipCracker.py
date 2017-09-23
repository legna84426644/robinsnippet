'''
Created on Sep 23, 2017

@author: Robin
'''

import zipfile
from multiprocessing import Process

def extractFile(zfile, pw):
    try:
        zfile.extractall(pwd=pw)
        print "Found password: " + pw
    except:
        pass


if __name__ == '__main__':
    zfile = zipfile.ZipFile("testfolder.zip")

    passFile = open("pw.txt")
    process = []

    for line in passFile.readlines():
        pw = line.strip("\n") # remote the new line char
        # do extract
        p = Process(target=extractFile, args=(zfile, pw))
        p.start()
        process.append(p)

    # wait for all processes finished        
    for p in process:
        p.join()
        
    print "Done"