import os

try:
    from rdflib import Graph,BNode,Literal,URIRef,Namespace,RDF,RDFS
    from rdflib.namespace import FOAF
except ImportError:
    print "Couldn't import rdflib module."
    print "Please ensure it is installed."
    raise

def logdGit(path):
    ''' logdGit takes current working directory (within git repo) as arugment.
        Queries provenance for activites (commits, merges, pulls) in repository
        and outputs to screen to emulate git log with no arguments. 
    '''

    # set up graph object
    g=Graph()
    PROV = Namespace('http://www.w3.org/prov/#')
    GIT = Namespace('http://www.example.com/ns/#')
    g.bind('prov',PROV)
    g.bind('foaf',FOAF)
    g.bind('git',GIT)

    # parse provenance into graph
    g.parse(path+'/.dgit/provenance.ttl',format='turtle')

    # queries return [(URI of log object,date, author, message)] 

    #merges:
    #       for each merge URI, 3 commits will be returned
    mergelog=list(g.query('''
            SELECT DISTINCT ?mergeID ?date ?author ?msg
            WHERE {
			?repository git:hadLogMember  ?mergeID .
		       	?mergeID a git:merge .
	    		?mergeID git:hadActivityMember ?mergeCommit . 
   	    	       	?mergeCommit prov:GeneratedAtTime ?date ; 
	    	       	            prov:wasAttributedTo ?author ; 
	               	            rdfs:comment ?msg . 
                }
            ORDER BY DESC (?date) 
            '''))
    
    #pulls:
    #       for each pull URI, 3 commits will be returned
    pulllog=list(g.query('''
            SELECT DISTINCT ?pullID ?date ?author ?msg
            WHERE {
			?repository git:hadLogMember  ?pullID .
		       	?pullID a git:pull .
	    		?pullID git:hadActivityMember ?pullCommit . 
   	    	       	?pullCommit prov:GeneratedAtTime ?date ; 
	    	       	            prov:wasAttributedTo ?author ; 
	               	            rdfs:comment ?msg . 
                }
            ORDER BY DESC (?date) 
            '''))
    #commits   
    commitlog=list(g.query('''
            SELECT ?commitID ?date ?author ?msg
            WHERE {
                ?repository git:hadLogMember ?commitID .
		?commitID a git:commit ;
			  prov:GeneratedAtTime ?date ;
			  prov:wasAttributedTo ?author ;
			  rdfs:comment ?msg .
			}

            ORDER BY DESC (?date) 
            '''))

    # output log to screen:
    
    j=0 # merge index
    k=0 # pull index
    merges=[]
    pulls=[]

    # commit xxxxxxxxxx
    # Author: xxxxxx
    # Date: xxxxx
    #
    # Commit Message
    #
    
    for i in range(len(commitlog)):
        if str(commitlog[i][3]).split(':')[0]!='dgit merge' and str(commitlog[i][3]).split(':')[0]!= 'dgit pull':
            print 'commit %s'%str(commitlog[i][0]).rsplit('/',1)[1]
            print 'Author: %s'%str(commitlog[i][2])
            print 'Date: %s'%str(commitlog[i][1])
            print''
            print'\t%s'%str(commitlog[i][3])
            print''

    # merge xxxxxxxxxx
    # Author: xxxxxx
    # Date: xxxxx
    #
    # dgit merge:<xxxxxxxx>
    #
        elif str(commitlog[i][3]).split(':')[0]=='dgit merge': 
            if str(mergelog[j][0]).rsplit('/',1)[1] not in merges: # to prevent redundancy
                print 'merge %s'%str(mergelog[j][0]).rsplit('/',1)[1]
                print 'Author: %s'%str(mergelog[j][2])
                print 'Date: %s'%str(mergelog[j][1])
                print''
                print'\tdgit merge:<%s>'%str(mergelog[j][0]).rsplit('/',1)[1]
                print''
                merges+=[str(mergelog[j][0]).rsplit('/',1)[1]]
                j+=1
            else:
                j+=1

    # pull xxxxxxxxxx
    # Author: xxxxxx
    # Date: xxxxx
    #
    # dgit pull:<xxxxxxxx>
    #
        elif str(commitlog[i][3]).split(':')[0]=='dgit pull':
            if str(pulllog[j][0]).rsplit('/',1)[1] not in pulls: # to prevent redundancy
                print 'pull %s'%str(pulllog[j][0]).rsplit('/',1)[1]
                print 'Author: %s'%str(pulllog[j][2])
                print 'Date: %s'%str(pulllog[j][1])
                print''
                print'\tdgit pull:<%s>'%str(pulllog[j][0]).rsplit('/',1)[1]
                print''
                pulls+=[str(pulllog[j][0]).rsplit('/',1)[1]]
                k+=1
            else:
                k+=1
                
        
