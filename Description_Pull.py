'''
Created on Jun 15, 2017

@author: hockettr
'''
import requests
import unicodedata
import string
from nltk.corpus import stopwords
from operator import itemgetter
import pickle
import time

#Don't touch this please lol

s=set(stopwords.words('english'))

w_dict = pickle.load(open('words_dict.p', 'rb'))

def get_desc(qid):
#imports data from freshdesk directly, last digits of the url is the only variable
    url = "https://gamesparks.freshdesk.com/api/v2/tickets/"+str(qid)
    headers = {
        'authorization': "Basic T1JCeFFmdTd5MEM2TmdqcnBrRDoxMjM=",
        'cache-control': "no-cache",
        'postman-token': "73e79a00-8a09-e4c7-bd7e-5b20920a9a84"
        }
    response = requests.request("GET", url, headers=headers)
    print response.text
#///////////////////////////////////////////////////////////////////////////////////
#     no_punc = cond.translate(None, string.punctuation)
def strip_desc(qid):
    desc = get_desc(qid)
    unicodedata.normalize('NFKD', desc).encode('ascii','ignore')
    str_desc = desc.encode('utf-8')
    start = 'description_text'
    end = 'custom_fields'
    s_stripped = str_desc[str_desc.find(start)+19:str_desc.find(end)-3].strip()
    ns_ripped = s_stripped.translate(None, string.punctuation)
    stripped = filter(lambda w: not w in s ,ns_ripped.split()) 
    w_list = []
    for i in stripped:
        w_list.append(i.lower())
    for word in w_list:
        if word in w_dict:
            w_dict[word]+=1
        else:
            w_dict[word]=1
            
def get_all_desc(start,stop):
    for i in range(start,stop):
        print i
        strip_desc(i)
    pickle.dump(w_dict, open('words_dict.p','wb'))


get_all_desc(14, 15)
#9,50
#50,140
#140,200
#200,250
#250,280
#280.350
#350,400
#400,450
#450,500
# 500,550
# 550,620
# 620, 690
# 690, 750
# 750,870
# 870,950
# 950,1040
# 1040,1100
# 1100,1200
#1200,1300
# 1300,1400
# 1400,1500
# 1500,1600
# 1600,1700
# 1700.1800
# 1800,1900
# 1900,2000
# 2000,2100
# 2100,2200
# 2200,2300
# 2300,2400
# 2400,2500
# 2700
# 2800
# 2900
# 3000
3100
3200
3300
3600
3700
3800
3900
4000
4100
4200
4300
4400
4500
4600
4700
4800
5100