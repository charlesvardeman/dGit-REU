import os

try:
    from rdflib import Graph,BNode,Literal,URIRef,Namespace,RDF,RDFS
    from rdflib.namespace import FOAF
except ImportError:
    print "Couldn't import rdflib module."
    print "Please ensure it is installed."
    raise

def describedGit(graph,file,path):
    '''
        describedGit takes three arguments: graph--turtle file containing descriptive triples,
                                            file--filename in repository to be described,
                                            path--current working directory (within repository)
        Assumes that the graph describes only the file, i.e. the subject of all the triples
        refers to the most current blob associated with the filename
    '''

    # set up graph objects
    g=Graph()   #g: provenance graph
    h=Graph()   #h: user graph
    PROV = Namespace('http://www.w3.org/prov/#')
    GIT = Namespace('http://www.example.com/ns/#')
    g.bind('prov',PROV)
    g.bind('foaf',FOAF)
    g.bind('git',GIT)
    h.bind('prov',PROV)
    h.bind('foaf',FOAF)
    h.bind('git',GIT)

    # parse existing provenance
    g.parse(path+'/.dgit/provenance.ttl',format='turtle')

    # query blob associated with file name
    blobID=str(list(g.query('SELECT ?blobID WHERE {?repository prov:hadMember ?blobID .?blobID foaf:name "%s" .}'%file))[0])
    blobID=blobID.split("'")[1]

    # parse user graph
    h.parse(graph,format='turtle')
    
    # add predictes and objects from user graph into provenance, attached to subject blob URI
    for _,p,o in h.triples((None,None,None)):
        g.add((URIRef(blobID),p,o))

    # output updated provenance
    provFile=open(path+'/.dgit/provenance.ttl','w')
    print >> provFile,(g.serialize(format='turtle'))
    provFile.close()

    # commit changes to provenace
    os.system('git add .dgit/provenance.ttl')
    os.system('git commit -m "dgit commit: describe %s" '%file)

    
