'''
Created on Jun 15, 2017

@author: hockettr
'''

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

desc_dict = pickle.load(open('desc_dates_by_qid.p','rb'))
# all_quests = pickle.load(open('questions.p','rb'))
totalqs= 0
totalDItems = 0
for qid in desc_dict:
    totalqs = totalqs + 1
    desc = desc_dict[qid].rel_desc
    
    final_desc = []
    for word in desc:
        if word[0] in open('gs_words_2.txt').read():
            for i in range(word[1]):
                final_desc.append(word)
    totalDItems = totalDItems + len(final_desc)
print float(totalDItems)/totalqs
# pickle.dump(desc_dict, open('desc_dates_by_qid.p','wb'))
# x = pickle.load(open('desc_dates_by_qid.p','rb'))
# 
# for q in x:
#     print x[q].rel_desc            