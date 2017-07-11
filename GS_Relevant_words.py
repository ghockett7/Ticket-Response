'''
Created on Jun 15, 2017

@author: hockettr
'''
import enchant
import pickle
from operator import itemgetter

d = enchant.Dict("en_US")

main_dict = pickle.load(open('words_dict.p','rb'))

def sort_dict(dic):
    ls2=[]
    for k in dic:
        ls2.append((k,dic[k]))
    return sorted(ls2, key = itemgetter(1), reverse = True)[:500]

main_ls=[]
def common_dubs():
    f = open('common_words.txt','r')
    for line in f:
        main_ls.append(line[:-1].lower())

#Cuts list down based on word length, commonality and whether or not it is english
def cut_it(ls):
    clist=ls[:]
    for item in ls:
        word = item[0]
        if len(word)<3:
            clist.remove(item)
            continue
        if len(word)>20:
            clist.remove(item)
            continue
        if word in main_ls:
            clist.remove(item)
            continue
#         if not d.check(word):
#                 if word == 'sdk' or 'spark' in word: #this could be refined
#                     continue
#                 else: 
#                     clist.remove(item)
    return clist

def maino(dic):
    common_dubs()
    sorted_ls = sort_dict(dic)
#     v = 1
    return cut_it(sorted_ls)
#         print v
#         v+=1
#         print i
#         print (float(i[1])/5292.00)*100, '%'

if __name__ == "__main__":
    print maino(main_dict)


