from dgit.provWriter import *
import os

try:
    from rdflib import Graph,BNode,Literal,URIRef,Namespace,RDF,RDFS
    from rdflib.namespace import FOAF
except ImportError:
    print "Couldn't import rdflib module."
    print "Please ensure it is installed."
    raise


def mergedGit(HEAD,branch,path,pullMerge=False):
    '''HEAD is branch to merge into. branch is to be merged. path is current
       working directory within repository, pullMerge is True when function is
       called as part of a dgit pull, is False by default.
       mergedGit parses provenance from both branches and outputs  and commits
       the result to both branches to avoid merge conflicts,
       then proceeds with merge. 
    '''

    #create unique merge hash
    #(when called from pulldGit, this is the pull hash
    merge_hash=os.urandom(20).encode('hex')

    # set up graph object
    g=Graph()
    PROV = Namespace('http://www.w3.org/prov/#')
    GIT = Namespace('http://www.example.com/ns/#')
    g.bind('prov',PROV)
    g.bind('foaf',FOAF)
    g.bind('git',GIT)

    # get prov from HEAD
    g.parse(path+'/.dgit/provenance.ttl',format='turtle')

    # switch to merging branch
    os.system('git checkout %s'%branch)
    if pullMerge:
        os.system('git checkout -b fetchhead') #must name branch to prevent detached HEAD
        branch='fetchhead' #branch variable is changed from FETCH_HEAD hash

    # get prov from merging branch
    g.parse(path+'/.dgit/provenance.ttl',format='turtle')
    
    # output updated prov to branch
    provFile=open(path+'/.dgit/provenance.ttl','w')
    print >> provFile,(g.serialize(format='turtle'))
    provFile.close()

    # stage and commit to branch
    os.system('git add .dgit/provenance.ttl')
    if pullMerge:
        os.system('git commit -m "dgit pull:<%s> branch %s"'%(merge_hash,branch))
    else:
        os.system('git commit -m "dgit merge:<%s> branch %s"'%(merge_hash,branch))

    # output updated prov to HEAD
    os.system('git checkout %s'%HEAD)
    provFile=open(path+'/.dgit/provenance.ttl','w')
    print >> provFile,(g.serialize(format='turtle'))
    provFile.close()
    
    # stage and commit to HEAD
    os.system('git add .dgit/provenance.ttl')
    if pullMerge:
        os.system('git commit -m "dgit pull:<%s> branch %s"'%(merge_hash,HEAD))
    else:
        os.system('git commit -m "dgit merge:<%s> branch %s"'%(merge_hash,HEAD))

    # merge
    try:
        if pullMerge:
            notGoodMerge=os.system('git merge %s -m "dgit pull:<%s>"'%(branch,merge_hash))
        else:
            notGoodMerge=os.system('git merge %s -m "dgit merge:<%s>"'%(branch,merge_hash))
    except:
        print'Resolve merge conflicts'
        notGoodMerge=True
        
    if not notGoodMerge:
        # write provenance for merge
        writeProv(path)

        # dgit commit provenance
        os.system('git add .dgit/provenance.ttl')
        os.system('git commit -m "dgit commit: provenance merge" ')

    if pullMerge:
        os.system('git branch -d %s'%branch)

    return notGoodMerge



    

    

    
    
    
    
