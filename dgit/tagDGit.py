import os

try:
    from rdflib import Graph,BNode,Literal,URIRef,Namespace,RDF,RDFS
    from rdflib.namespace import FOAF
except ImportError:
    print "Couldn't import rdflib module."
    print "Please ensure it is installed."
    raise

def tagdGit(tag,file,path):
    '''tag--Literal to be attached to blob URI with git:hasTag
       file--filename to be tagged
       path--current working directory within repo
       tagdGit queries .dgit/provenance.ttl to find most recent blob associated with filename then attached given tag to provenance
    '''

    # set up graph object
    g=Graph()
    PROV = Namespace('http://www.w3.org/prov/#')
    GIT = Namespace('http://www.example.com/ns/#')
    g.bind('prov',PROV)
    g.bind('foaf',FOAF)
    g.bind('git',GIT)

    # parse existing provenance
    g.parse(path+'/.dgit/provenance.ttl',format='turtle')

    # query blob associated with file name
    # blobID=string with URI of most recent blob associated with filename
    blobID=str(list(g.query('SELECT ?blobID WHERE {?repository prov:hadMember ?blobID .?blobID foaf:name "%s" .}'%file))[0])
    blobID=blobID.split("'")[1]

    # add tag
    g.add((URIRef(blobID),GIT.hasTag,Literal(tag)))

    # output updated provenance
    provFile=open(path+'/.dgit/provenance.ttl','w')
    print >> provFile,(g.serialize(format='turtle'))
    provFile.close()

    # stage and commit changes
    # commit message-- dgit commit: tag [filename]
    os.system('git add .dgit/provenance.ttl')
    os.system('git commit -m "dgit commit: tag %s" '%file)
