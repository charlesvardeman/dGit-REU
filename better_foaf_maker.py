import os

def better_foaf_maker():
    '''Creates FOAF in turtle format about a person from user input.
    Output file is Firstname_foaf.ttl'''
    
    print('''Fill in the following information.
          Feel free to leave any blank.''')

    givenName=input('First name: ').lower().capitalize()
    filename=givenName+'_foaf.ttl'
    out=open(filename,'w')

    print('@prefix : <http://xmls.com/foaf/0.1/> .',file=out)
    print('@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .',file=out)
    print('',file=out)
    print('<',os.path.abspath(filename),'>',sep='',file=out)

    print('\t:givenName "{0}" ;'.format(givenName),file=out)
    
    str_dict={'lastName':'Last name: ','gender':'Gender: ',
              'topic_interest':'A thing of interest to you: ',
              'status':'A string expressing your current status/activity: ',
              'title':'Your title (Dr.,Ms.,etc.): ',
              'myersBriggs':'Your 4 letter Myers-Briggs classification: ',
              'age':'Your age: ','phone':'Your phone number: ',
              'mbox':'Your email address: ','nick':'Your nickname: ',
              'birthday':'Your birthdate (mm-dd): '}

    str_dict_keys=list(str_dict.keys())

    uri_dict={'interest':'Link to page about a topic of interest: ',
              'member':'Link to group you are a member of: ',
              'thumbnail':'Link to a thumbnail of you: ',
              'pastProject':"Link to a project you've previously worked on: ",
              'publications':'Link to your publications: ',
              'workInfoHomepage':'Link to a page about your work: ',
              'fundedBy':'Link to organization funding you: ',
              'workplaceHomepage':'Link to the homepage of your workplace: ',
              'schoolHomepage':"Link to homepage of a school you've attended: ",
              'currentProject':'Link to a current project you are working on: '}

    uri_dict_keys=list(uri_dict.keys())
    
    for i in str_dict_keys:
        j=input(str_dict[i])
        if j:
            ttl='\t:{0} "{1}" ;'.format(i,j)
            print(ttl,file=out)

    for i in uri_dict_keys:
        j=input(uri_dict[i])
        if j:
            ttl='\t:{0} <{1}> ;'.format(i,j)
            print(ttl,file=out)

    knows=input('Name of person you know, with whom you share reciprocated interaction: ')
    ttl='\t:knows <{0}> ;'.format(knows)
    print(ttl,file=out)
    knows=input('If you would like to add another person, type their name, otherwise hit Enter again: ')
    while knows:
        ttl='\t:knows <{0}> ;'.format(knows)
        print(ttl,file=out)
        knows=input('If you would like to add another person, type their name, otherwise hit Enter again: ')
        
    
    print('\ta :Person .',file=out)

    out.close()

better_foaf_maker()
