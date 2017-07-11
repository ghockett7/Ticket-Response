'''
Created on 19 Jun 2017

@author: hockettr
'''

import httplib
import pickle
class QUE(object):
    qid = 0
    c_year = 0
    c_month = 0
    c_day = 0
    e_year = 0
    e_month = 0
    e_day = 0
    rel_desc = []
class Question(object):
    qid = 0
    subject_cond = ""
    tags = ""
    desc_cond = ""
    email = ""
    
from Get_tags import format_tags,tags
from Change_to_Question import change_em
aall_questions = pickle.load(open('questions.p','rb'))



# payload = "{\"tags\":[\"" + g[0]  + "," + g[1] + "\"]}"

def tag_em(qid,tagss):
    print qid,tagss
    conn = httplib.HTTPSConnection("gamesparks.freshdesk.com")
    rqid = str(qid)
    g = tagss.split(',')
    finalstr = ("\",\"").join(g)
#     payload = "{\"tags\":[\"" + g[0] +"\"]}"
    payload = "{\"tags\":[\"" + finalstr + "\"]}"
    headers = {
        'authorization': "Basic T1JCeFFmdTd5MEM2TmdqcnBrRDoxMjM=",
        'content-type': "application/json",
        'cache-control': "no-cache",
        }
    
    conn.request("PUT", "/api/v2/tickets/"+rqid, payload, headers)
    
    res = conn.getresponse()
    data = res.read()

    print (data.decode("utf-8"))
    x = (data.decode("utf-8"))[2:13]
    final = x.encode("utf-8")
    if final == 'description':
        change_em(qid)
        tag_em(qid, tagss)
        
        
    
    
if __name__ == '__main__':
    not_up_count = 0
    for qid in range(3571,5293):
        if qid in aall_questions:
            if aall_questions[qid].tags == []:
                print "no tag", qid
                tgs = format_tags(tags(qid))
                print tgs
                tag_em(qid, tgs)
            else:
                not_up_count+=1
#                 print "not updated"
    print not_up_count
                
#300
#700
#1000
#1700
#2000
#2500
#3500
#4000
#4500\

# rd2
# 700