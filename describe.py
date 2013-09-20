from dgit.describeDGit import *
import os

def describe():
    path=os.getcwd()
    describedGit(raw_input('graph: '),raw_input('file: '),path)
describe()
