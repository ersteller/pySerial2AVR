'''
Created on 10.08.2012

@author: Thomas
'''

import time 
import os


def getRawFiles(data_path):
    # returns all files found in "raw" subfolders of data_path
    file_list = list()
    for root, dirs, files in os.walk(data_path):
        if "raw" in root:
            for e in files:
                file_list.append(root + "\\" + e) 
    return file_list

def isFileNewerThan(path, time):
    # is path newer than time(since the epoch) --> True or False
    t = os.path.getmtime(path)
    if t > time:
        return True
    else: 
        return False 

filename = "d00146_20120810230115"

files = getRawFiles(os.getcwd())
for e in files:
    print e
    print "last acces:    " + time.asctime(time.localtime(os.path.getatime(e)))
    print "last modified: " + time.asctime(time.localtime(os.path.getmtime(e)))
    print "creation:      " + time.asctime(time.localtime(os.path.getctime(e)))
    

# converting g2d to raw
"""
proc = subprocess.Popen('c:\\GP5W_Shell\\GP5wSHELL.exe' +  ' "c:\\gp5w_shell\\data\\D00146\\raw\\' + filename + '.g2d"')
time.sleep(5)
proc.kill()
"""

#F = open("C:\\GP5W_Shell\\export\\" + filename + ".csv")
F = open(filename + ".csv")

header = F.readline()
zeilekey = F.readline()
zeilewert = F.readline()




pass



    
