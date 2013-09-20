import os

try:
    from rdflib import Graph,BNode,Literal,URIRef,Namespace,RDF,RDFS
    from rdflib.namespace import FOAF
except ImportError:
    print "Couldn't import rdflib module."
    print "Please ensure it is installed."
    raise

def repoWriter(graphObject,PROV,path,GIT):
    ''' Only called if repository entity has not been documented. Takes the graph object data structure,
        with its namespaces (prov and git), and path of current working directory as arguments.
    '''
    # add repository location and type triples 
    graphObject.add((URIRef('file:/%s'%path),PROV.atLocation,Literal('%s'%path)))
    graphObject.add((URIRef('file:/%s'%path),RDF.type,GIT.repository))

    # uses creation date of .dgit directory as prov:GeneratedAtTime for repository
    # fetches data by reading into a tmp file and pulling date attached to .dgit directory
    os.system('ls -Al --time-style=full-iso > /tmp/tmp.txt')
    tmp=open('/tmp/tmp.txt','r')
    line=tmp.readline() #first line in tmp.txt file 'total ##' is garbage
    for line in tmp:
        (mode,links,owner,group,size,date,time,tz,file)=line.strip().split()
        date=date+'T'+time.split('.')[0]+tz #format date
        if file=='.dgit':
            graphObject.add((URIRef('file:/%s'%path),PROV.GeneratedAtTime,Literal('%s'%date)))
    tmp.close()
    os.system('rm /tmp/tmp.txt')

def mergeWriter(graphObject,GIT,commit_hsh,merge_hsh,path):
    '''Writes provenance about merge activities. Passed graph data structure, merge hash with associated commit
       hash as arguments from provWriter
    '''

    #triples about merge
    graphObject.add((URIRef('http://example.com/object/merge/%s'%merge_hsh),RDF.type,GIT.merge))
    graphObject.add((URIRef('http://example.com/object/merge/%s'%merge_hsh),GIT.hadActivityMember,URIRef('http://example.com/object/commit/%s'%commit_hsh)))

    # repository-uri git:hadLogMemger merge-uri
    graphObject.add((URIRef('file:/%s'%path),GIT.hadLogMember,URIRef('http://example.com/object/merge/%s'%merge_hsh)))

def pullWriter(graphObject,GIT,commit_hsh,pull_hsh,path):
    '''Writes provenance about pull activities. Passed graph data structure, pull hash with associated commit
       hash as arguments from provWriter
    '''

    #triples about pull
    graphObject.add((URIRef('http://example.com/object/pull/%s'%pull_hsh),RDF.type,GIT.pull))
    graphObject.add((URIRef('http://example.com/object/pull/%s'%pull_hsh),GIT.hadActivityMember,URIRef('http://example.com/object/commit/%s'%commit_hsh)))

    # repository-uri git:hadLogMemger pull-uri
    graphObject.add((URIRef('file:/%s'%path),GIT.hadLogMember,URIRef('http://example.com/object/pull/%s'%pull_hsh)))

def provFetcher(graphObject,PROV,path,GIT):
    ''' fetches provenance information by pulling from git log and git ls-tree. adds triples about commit activities
        and blob entities to graph data structure passed from provWriter.
    '''

    # get local config info
    os.system('git config --list > /tmp/config.txt') # read local config into temp file
    config=open('/tmp/config.txt','r')
    isUserFoaf=False
    for line in config:
        if line.strip().split('=')[0]=='user.name': #pull user name
            user_name=line.strip().split('=')[1]
        if line.strip().split('=')[0]=='user.foaf': #pull user foaf (will be empty string if not added by user)
            user_foaf=line.strip().split('=')[1]
            isUserFoaf=True
    config.close()
    os.system('rm /tmp/config.txt') #remove temp file

    # read log into tmp file
    os.system('git log --pretty=format:"%H/%P/%an/%ad/%ae/%s %b" --date=iso --reverse > /tmp/tmp.txt')
    tmp=open('/tmp/tmp.txt','r') 

    for line in tmp:
        (commit_hsh,parent_hsh,author,date,email,msg)=line.strip().split('/')

        # triple about merge
        if msg.split(':')[0] == 'dgit merge':
            merge_hsh=msg.split('<')[1].split('>')[0]   # extract merge hash
            mergeWriter(graphObject,GIT,commit_hsh,merge_hsh,path) #call function to write merge prov

        # triple about pull
        if msg.split(':')[0] == 'dgit pull':
            pull_hsh=msg.split('<')[1].split('>')[0]    #extract pull hash
            pullWriter(graphObject,GIT,commit_hsh,pull_hsh,path) #call function to write pull prov
            
        # triple about commit
        if msg.split(':')[0] != 'dgit commit':
            (date,time,tz)=date.split()
            date=date+'T'+time+tz #format date
            #if commit has parents
            if parent_hsh:
                #for each parent in list of parent hashes
                for parent in parent_hsh.split():
                    # write prov: commit-hash-URI git:wasChildof parent-hash-URI
                    graphObject.add((URIRef('http://example.com/object/commit/%s'%commit_hsh),GIT.wasChildof,URIRef('http://example.com/object/commit/%s'%parent)))

            # author node            
            # add user.foaf to author triples
            
            if author==user_name:
            # if the author is the same as the local user
                if isUserFoaf:
                    if user_foaf:
                    # if the user has added a foaf URI, add commit author to prov as a URI
                        graphObject.add((URIRef('%s'%user_foaf),FOAF.mbox,Literal('%s'%email)))
                        graphObject.add((URIRef('%s'%user_foaf),RDF.type,PROV.Agent))
                        graphObject.add((URIRef('http://example.com/object/commit/%s'%commit_hsh),PROV.wasAttributedTo,URIRef('%s'%user_foaf)))
                    else:
                    # else add author to prov as a literal
                        graphObject.add((URIRef('http://example.com/object/commit/%s'%commit_hsh),PROV.wasAttributedTo,Literal('%s'%author)))
                else:
                    graphObject.add((URIRef('http://example.com/object/commit/%s'%commit_hsh),PROV.wasAttributedTo,Literal('%s'%author)))
            else:
            # if the author is not the local user, add to prov as a literal
                graphObject.add((URIRef('http://example.com/object/commit/%s'%commit_hsh),PROV.wasAttributedTo,Literal('%s'%author)))

            # triples about commit        
            graphObject.add((URIRef('http://example.com/object/commit/%s'%commit_hsh),PROV.GeneratedAtTime,Literal('%s'%date)))
            graphObject.add((URIRef('http://example.com/object/commit/%s'%commit_hsh),RDFS.comment,Literal('%s'%msg)))
            graphObject.add((URIRef('http://example.com/object/commit/%s'%commit_hsh),RDF.type,GIT.commit))

            #adding commits to repository git:hadLogMember
            if msg.split(':')[0] != 'dgit merge' or 'dgit pull': 
                graphObject.add((URIRef('file:/%s'%path),GIT.hadLogMember,URIRef('http://example.com/object/commit/%s'%commit_hsh)))
    tmp.close()
    os.system('rm /tmp/tmp.txt') #remove tmp file

    #reset repository prov:hadMember triples 
    graphObject.remove((URIRef('file:/%s'%path),PROV.hadMember,None))

    # read files tracked on current git head into tmp file
    os.system('git ls-tree --full-tree -r HEAD > /tmp/tmp.txt')
    tmp=open('/tmp/tmp.txt','r')
    for line in tmp:
        (mode,Type,hsh,file)=line.strip().split()
        (pathname,filename)=os.path.split(file)

        #if tracked file is indeed a blob
        if Type=='blob':
            
            #reset git:asOf triples about blobs (so only the most recent commit is reflected in provenance
            graphObject.remove((URIRef('http://example.com/object/blob/%s'%hsh),GIT.asOf,None))
            
            # triples about blob
            graphObject.add((URIRef('http://example.com/object/blob/%s'%hsh),RDF.type,GIT.blob))
            graphObject.add((URIRef('http://example.com/object/blob/%s'%hsh),GIT.asOf,URIRef('http://example.com/object/commit/%s'%commit_hsh)))
            graphObject.add((URIRef('http://example.com/object/blob/%s'%hsh),FOAF.name,Literal('%s'%filename)))
            graphObject.add((URIRef('http://example.com/object/blob/%s'%hsh),PROV.atLocation,Literal('%s'%(path+'/'+file))))
            graphObject.add((URIRef('http://example.com/object/blob/%s'%hsh),PROV.wasGeneratedBy,GIT.commit))

            #triple about repository blobs
            graphObject.add((URIRef('file:/%s'%path),PROV.hadMember,URIRef('http://example.com/object/blob/%s'%hsh)))
    tmp.close()
    os.system('rm /tmp/tmp.txt') #remove tmp file

def writeProv(path,newRepo=False):
    ''' takes current working directory within repo as argument. default assumes
        that repo is tracking files (i.e. is not new), but newRepo=True when
        no files are tracked by git
    '''
    # set up graph object
    g = Graph()
    PROV = Namespace('http://www.w3.org/prov/#')
    GIT = Namespace('http://www.example.com/ns/#')
    g.bind('prov',PROV)
    g.bind('foaf',FOAF)
    g.bind('git',GIT)

    # parse provenance
    g.parse(path+'/.dgit/provenance.ttl',format='turtle')

    if len(g)==0: #if provenance is empty
        repoWriter(g,PROV,path,GIT)
        
    if not newRepo: #if files are being tracked, they need documentation
        provFetcher(g,PROV,path,GIT)

    # output updated provenance to .dgit/provenance.ttl
    provFile=open(path+'/.dgit/provenance.ttl','w')
    print >> provFile,(g.serialize(format='turtle'))
    provFile.close()
