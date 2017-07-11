
'''
Created on Jun 13, 2017

@author: hockettr
'''
def new_config():
    ncon = raw_input('Would you like to configure a new Database from CSV? Y|N: ')
    if ncon == 'Y' or 'y': return True
    else: return False
def man_yn():
    man_inp = raw_input('Would like to use manual input? Y/N: ')
    if man_inp == 'Y':
        return True
    else:
        return False
#qid, subject,status,email
def usr_inp():
    qid = raw_input('Input Qid: ')
    subject = raw_input('Input subject: ')
    status = raw_input('Input status (Open|Closed):')
    email = raw_input('Input email of customer: ')
    tags = raw_input('Input tags: ')
    return (qid,subject,status,email,tags)
    
        
        
        
        
    

