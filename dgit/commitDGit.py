import os
from dgit.provWriter import *

def commitdGit(commit_msg,path):
    ''' commitdGit takes two arguments: commit message and the path to the current working directory
        (within git directory). Staged changes are committed with given commit message.
        Provenance metadata is written to .dgit/provenance.ttl and this change is staged and committed as
        "dgit commit: [original commit message]"
    '''
    os.chdir(path)
    os.system('git commit -m "%s"'%commit_msg) #git commit from command line
    
    writeProv(path)     #call functions from provWriter to generate provenance

    os.system('git add .dgit/provenance.ttl') #stage change from command line

    os.system('git commit -m "dgit commit: %s"'%commit_msg) #dgit commit from command line
