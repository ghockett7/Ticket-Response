'''
Created on 19 Jun 2017

@author: hockettr
'''
import pickle
from GS_Relevant_words import maino
from operator import itemgetter
import operator
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
    tags = []
    desc_cond = ""
    email = ""
    
all_quests = pickle.load(open('questions.p','rb'))

desc_dict = pickle.load(open('desc_dates_by_qid.p','rb'))

main_dict = pickle.load(open('words_dict.p', 'rb'))

rel_words = maino(main_dict)
# for word in rel_words:
#     print word[0]
word_set = set()

n_tags_d = pickle.load(open('file.p','rb'))

existing_tags = set(n_tags_d.keys())

with open('newfoundTags.txt') as f:
    for line in f.readlines():
        x = line.split(',')
        existing_tags.add(x[0][1:])    

possible_tags = dict()

with open('gs_words') as f:
    for line in f.readlines():
        word_set.add(line.strip())
def tags(qid):
    question = desc_dict[qid]
    desc = question.rel_desc
    d_set = set()
#     print desc
    for i in desc:
        d_set.add(i[0])
    inter = word_set.intersection(d_set)
    #assures that the tags already exist
    new_ts = inter.difference(existing_tags)
#     if qid not in possible_tags["keys"]:
    for t in new_ts:
        if t in possible_tags:
            possible_tags[t]+=1
        else:
            possible_tags[t]=1
#     possible_tags["keys"].add(qid)
    inter2 = inter.intersection(existing_tags)
    final_ls = []
    for word in inter2:
        for x in desc:
            if word == x[0]:
                final_ls.append((word,x[1]))
    pickle.dump(possible_tags,open('possible_tags.p','wb'))
#     print possible_tags
    return sorted(final_ls,key=itemgetter(1),reverse=True)

def format_tags(tags_list):
#     final  = and 
    final = []
    if tags_list == []:
        return ""
    for tag in tags_list:
        final.append(tag[0])
    return ','.join(final)
         
if __name__ == '__main__':
#     for i in  n_tags_d.keys():
#         print i
    
    for i in range(295,298):
        tags(i)
        print i , tags(i)
    sorted_tags = sorted(possible_tags.items(), key = operator.itemgetter(1),reverse = True)
#     for i in sorted_tags[1:100]:
#         print i 