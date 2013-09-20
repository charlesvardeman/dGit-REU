import os
from dgit.mergeDGit import *

try:
    from rdflib import Graph,BNode,Literal,URIRef,Namespace,RDF,RDFS
    from rdflib.namespace import FOAF
except ImportError:
    print "Couldn't import rdflib module."
    print "Please ensure it is installed."
    raise

def pulldGit(HEAD,path):
    '''HEAD is branch user is currently on. Path is current working directory
       within repository.
       A git pull fetches the current commit of the remote repository and does
       a merge. 
    '''

    # added file .git/FETCH_HEAD containing commit hash of current remote repo
    os.system('git fetch origin')

    # parse contents for desired commit hash to merge with to complete pull
    fetch=open('.git/FETCH_HEAD','r')
    for line in fetch:
        line=line.strip().split()
        if line[1]!='not-for-merge': #filter commit hashes marked 'not-for-merge'
            fetchID=line[0] #fetchID=commit hash of remote repo
            notGoodMerge=mergedGit(HEAD,fetchID,path,pullMerge=True)
        if notGoodMerge:
            break
    fetch.close()
        
