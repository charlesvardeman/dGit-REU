import os
import time

def software_prov_generator():
    '''intended to generate a turtle description of a software entity.
       this version is being converted to python 2 and modified for use
       with cluster modules'''

    doap_name=raw_input('Name of software: ')
    filename=doap_name.replace(' ','_')+'.ttl'
    out=open(filename,'a')
    tmp=open('temp.txt','w')
    tmp=open('temp.txt','r')
    
    os.system('which %s > temp.txt'%doap_name)
    location=tmp.readline().strip()

    print >> out,'''@prefix foaf: <http://xmlns.com/foaf/0.1/#> .
@prefix doap: <http://usefulinc.com/ns/doap#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'''

    print >> out ,'<'+location+'>'

    os.system('%s --version | grep %s >> temp.txt'%(doap_name,doap_name))
    doap_version=tmp.readline().strip().split()[2]

    os.system('%s --version | grep Copyright >> temp.txt'%doap_name)
    doap_vendor=tmp.readline().strip().split(None,3)[3]

    print >> out,'\tdoap:version "%s" ;'%doap_version
    print >> out,'\tdoap:vendor "%s" ;'%doap_vendor

    print('Feel free to leave some of the following blank.')

    str_dict={'doap:audience':'Description of target user base: ',
              'doap:shortdesc':'Short (8 or 9 words) plain text description of a project: ',
              'doap:description':'Plain text description of a project, of 2-4 sentences in length: ',
              'doap:browse':'Web browser interface to repository: ',
              'doap:wiki':'URL of Wiki for collaborative discussion of project: ',
              'doap:created':'Date of software release (YYYY-MM-DD): ',
              'doap:programming-language':'Programming language software is implemented in or intended for use with: '}

    uri_dict={'doap:homepage':'URL of software homepage, associated with exactly one project: ',
              'doap:old-homepage':"URL of software's past homepage, associated with exactly one project: ",
              'doap:tester':'FOAF identifier of a tester or other quality control contributor: ',
              'doap:maintainer':'FOAF identifier of a maintainer of the software, a project leader: ',
              'doap:documenter':'FOAF identifier of a contributor of the documentation of the software: ',
              'doap:developer':'FOAF identifier of a developer of the software: ',
              'doap:helper':'FOAF identifier of a contributor: '}

    for i in str_dict.keys():
        j=raw_input(str_dict[i])
        if j:
            ttl='\t%s "%s" ;'%(i,j)
            print >> out,ttl

    for i in uri_dict.keys():
        j=raw_input(uri_dict[i])
        if j:
            ttl='\t%s <%s> ;'%(i,j)
            print >> out,ttl

    print >> out,'\tdoap:os "%s" ;'%os.uname()[0]

    stats=os.stat(location)
    generated_time='%s-%s-%sT%s:%s:%s'%(time.localtime(stats.st_ctime).tm_year,
                                                    time.localtime(stats.st_ctime).tm_mon,
                                                    time.localtime(stats.st_ctime).tm_mday,
                                                    time.localtime(stats.st_ctime).tm_hour,
                                                    time.localtime(stats.st_ctime).tm_min,
                                                    time.localtime(stats.st_ctime).tm_sec)

    print >> out,'\tprov:generatedAtTime "%s" ;'%generated_time

    passwd=open('/etc/passwd','r')

    isMatch=False
    while isMatch==False:
        userid=passwd.readline().split(':')
        if stats.st_uid==int(userid[2]):
            isMatch=True
            print >> out,'\tprov:wasAttributedTo "{0}" ;'.format(userid[4])
    passwd.close()

    print >> out,'\tdoap:name "%s" ;\n\ta prov:Entity .'%doap_name

    out.close()
    tmp.close()
    os.system('rm temp.txt')

software_prov_generator()

