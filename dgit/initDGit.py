from dgit.provWriter import *
import os
try:
    from dulwich.repo import Repo
except ImportError:
    print "Couldn't import dulwich module."
    print "Please ensure it is installed."
    raise

def initNewRepo(path,dgitProv):
    ''' Takes current working directory (within repository)  and location of
        provenance as arguments.
        initNewRepo tries to init a git repository, add space for
        user foaf URI in local config file, and calls function to
        documents repository in .dgit/provenance.ttl
    '''

    try:
        repo = Repo.init(path)
        os.system('git config user.foaf "" ')
        print "Initiated a blank git repository."
        newRepo=True #is set to True if repository has no tracked files
    except:
        print "Failed git repository initialization."

    writeProv(path,newRepo) #calls function to write provenance
    repo.stage([dgitProv]) #stages provenance (via dulwich)
    
    print '''Repository converted to dgit repository,
please commit changes.'''


def initdGit(path):
    ''' Takes current working directory (within repository) as argument.
        initdGit builds dgit path and files, determines whether repository
        needs dgit initialization,whether directory is already a git
        repository, adds space for user foaf URI in local config file,
        and calls function to document repository in .dgit/provenance.ttl
    '''
    
    os.chdir(path)
    needsInit = False

    try: #if error is not raised, repository needs dgit init
        dgitpath = ".dgit"
        dgitProv = dgitpath + "/provenance.ttl"
        os.mkdir(dgitpath)
        os.system('touch %s'%dgitProv)
        needsInit = True 
    except:
        print '''Repository already initialized.
To reinitialize Git, please use git init command'''

    if needsInit:
    
        repoExists=False
        try: #if error is not raised, git repository alreaded inited
            repo = Repo(path)
            repoExists=True 
        except:
            initNewRepo(path,dgitProv) #calls function to initialize git
        
        if repoExists:
            os.system('git config user.foaf "" ') #create space in local config for foaf URI
            if not list(repo.open_index()): 
                newRepo=True #if no files are tracked in repo, assumes bare repository
            else:
                newRepo=False 
            writeProv(path,newRepo) #calls function to write provenance
            repo.stage([dgitProv]) #stages provenance (via dulwich)
            print '''Repository converted to dgit repository,
please commit changes.'''
