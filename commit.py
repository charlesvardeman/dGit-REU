from dgit.commitDGit import *
import os

def commit():
    path=os.getcwd()
    commitdGit(raw_input('Commit message: '),path)       
commit()
