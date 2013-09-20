import os
from dgit.pullDGit import *

def pull():
    path=os.getcwd()

    # find name of HEAD
    head=open('.git/HEAD','r')
    try:
        HEAD=head.readline().rsplit('/',1)[1]
    except:
        HEAD=head.readline()
    head.close()
    
    pulldGit(HEAD,path)  

pull()
