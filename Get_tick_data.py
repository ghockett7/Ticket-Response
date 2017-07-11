'''
Created on Jun 19, 2017

@author: hockettr
'''

import requests
import unicodedata
import string
from nltk.corpus import stopwords
from operator import itemgetter
import pickle
from Description_Pull import get_desc
from GS_Relevant_words import maino
import time


class QUE(object):
    qid = 0
    c_year = 0
    c_month = 0
    c_day = 0
    e_year = 0
    e_month = 0
    e_day = 0
    rel_desc = []


s=set(stopwords.words('english'))

main_dict = pickle.load(open('words_dict.p', 'rb'))



bigdd = pickle.load(open('desc_dates_by_qid.p','rb'))



def strip_desc(qid):
    desc = get_desc(qid)
    unicodedata.normalize('NFKD', desc).encode('ascii','ignore')
    str_desc = desc.encode('utf-8')
    start = 'description_text'
    end = 'custom_fields'
    s_stripped = str_desc[str_desc.find(start)+19:str_desc.find(end)-3].strip()
    ns_ripped = s_stripped.translate(None, string.punctuation)
    stripped = filter(lambda w: not w in s ,ns_ripped.split())
    w_list=[]
    w_dict = dict()
    for i in stripped:
        w_list.append(i.lower())
    for word in w_list:
        if word in w_dict:
            w_dict[word]+=1
        else:
            w_dict[word]=1
    return w_dict
def dates(qid):
    info = get_desc(qid)
    unicodedata.normalize('NFKD', info).encode('ascii','ignore')
    str_info = info.encode('utf-8')
    start = 'created_at'
    end = 'updated_at'
    sd_stripped = str_info[str_info.find(start)+13:str_info.find(end)-13].strip()
    symd = sd_stripped.split('-')
    if len(symd)<3:
        return 'stop'
    else:
        sy = int(symd[0])
        sm = int(symd[1])
        sd = int(symd[2])
        #----------------------Find end dates-----------------------------------------
        the_ends = 'tags":'
        ed_stripped = str_info[str_info.find(end)+13:str_info.find(the_ends)-13].strip()
    #     print ed_stripped
        eymd = ed_stripped.split('-')
        ey = int(eymd[0])
        em = int(eymd[1])
        ed = int(eymd[2])
        start = (sy,sm,sd)
        end = (ey,em,ed)
        return start , end
def create_QUE(qid, c_year, c_month, c_day, e_year, e_month, e_day,rel_desc):
    question = QUE()
    question.qid = qid
    question.c_year = c_year
    question.c_month = c_month
    question.c_day = c_day
    question.e_year = e_year
    question.e_month = e_month
    question.e_day = e_day
    question.rel_desc = rel_desc
    return question
    


def main(start,end):
    for qid in range(start,end):
        print qid
        stripped = strip_desc(qid)
        desc = maino(stripped)
        both_dates = dates(qid)
        if both_dates == 'stop':
            that_par = create_QUE(qid, None, None, None, None, None, None, desc)
            bigdd[qid]=that_par
            continue
        cy = both_dates[0][0]
        cm = both_dates[0][1]
        cd = both_dates[0][2]
        ey = both_dates[1][0]
        em = both_dates[1][1]
        ed = both_dates[1][2]
        that_par = create_QUE(qid, cy, cm, cd, ey, em, ed, desc)
        bigdd[qid] = that_par
#         time.sleep(2)
    
    pickle.dump(bigdd,open('desc_dates_by_qid.p','wb'))
       
    
if __name__ == "__main__":
    main(0,0)
#     print pickle.load(open('desc_dates_by_qid.p','rb'))
    
# 9,400
#44
# 399
# 999
#1500
# 2500
#4000
#4600
# 5292