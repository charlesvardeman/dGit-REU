from dgit.mergeDGit import *
import os

def merge():
    path=os.getcwd()
    
    # find name of HEAD
    head=open('.git/HEAD','r')
    HEAD=head.readline().rsplit('/',1)[1]
    head.close()
    
    mergedGit(HEAD,raw_input('Branch to be merged: '),path)
    
merge()
    
