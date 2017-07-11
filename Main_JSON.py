from __future__ import print_function
# from nltk.corpus import stopwords
# s=set(stopwords.words('english'))
# 
# txt="a long string of text about him and her"
# print filter(lambda w: not w in s,txt.split())
import pickle
import csv
import json
import unicodedata

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

desc_dict = pickle.load(open('desc_dates_by_qid.p','rb'))
all_quests = pickle.load(open('questions.p','rb'))
temp_dict = dict()


f = open('outshput.txt','wb')
def quotify(strang): return "\"" + strang + "\""
print ("[", file = f)
for b in range(15,5293):
    if b in all_quests and b in desc_dict:
        i = all_quests[b]
        c = desc_dict[b]
        ls = [i.subject_cond,c.rel_desc,i.tags,c.c_year,c.c_month,c.c_day,c.e_year,c.e_month,c.e_day]
        subject = str(i.subject_cond)
        sub_list = i.subject_cond.split(' ')
        fin_sub = " ".join(sub_list)
        print (sub_list)
        print ("{", file = f)
        print ('"ticketID"'+": "+str(i.qid)+',',file = f)
        print ('"Subject"'+": " + quotify(str(fin_sub))+',',file = f)
        print ('"Description"'+": [",file = f)
        last = len(c.rel_desc)-1
        for k in range(len(c.rel_desc)):
            if k != last:
                print ("{",file = f)
                print ('"word"'+": "+quotify(str(c.rel_desc[k][0]))+',',file=f)
                print ('"score"'+": "+str(c.rel_desc[k][1]),file=f)
                print ("},",file = f)
            else:
                print ("{",file = f)
                print ('"tag"'+": "+quotify(str(c.rel_desc[k][0]))+',',file=f)
                print ('"score"'+": "+str(c.rel_desc[k][1]),file=f)
                print ("}", file = f)
        print ("],",file = f)
#         quoted_list = [quotify(x) for x in i.tags]
        quoted_list = []
        for l in i.tags:
#                 print(quotify(l))
                quoted_list.append(quotify(l))
        p = (','.join(quoted_list))
        print ('"Tags"'+": "+'['+str(p)+']',file = f)
        print ("},",file = f)
        
print ("]", file = f)
# keys = sorted(temp_dict.keys())
# with open("output.csv", "wb") as outfile:
#     writer = csv.writer(outfile, delimiter = "\t")
#     writer.writerow(keys)
#     writer.writerows(zip(*[temp_dict[key] for key in keys])) 
   
# jsonarray = json.dumps(temp_dict)
# print temp_dict
# print jsonarray
# with open('outshput.txt', 'wb') as outfile:
#     json.dump(temp_dict, outfile)
# with open("output.text",'wb'):
#     
#     print jsonarray
# with open('output.csv','wb') as f:
#     w = csv.writer(f)
#     w.writerows()