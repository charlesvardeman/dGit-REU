from dgit.tagDGit import *
import os

def tag():
    path=os.getcwd()
    tagdGit(raw_input('tag: '),raw_input('file: '),path)
tag()
