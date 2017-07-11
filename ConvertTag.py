'''
Created on 3 Jul 2017

@author: hockettr
'''
# from __future__ import print_function

# f = open('newfoundTags.txt')
# g = open('allTags.txt','wb')
# for line in f.readlines():
#     print (line.split(",")[0][2:-1], file = g)

# f = open('allTags.txt')
# g = open('allTagsJSON.txt','wb')
# print ("[",file = g)
# for line in f.readlines():
#     print ("{",file = g)
#     print ('"Tag"'+": "+"\""+line.strip()+"\"",file = g)
#     print("},",file = g)
# print ("]",file = g)

class Node:
    def __init__(self,data):
        self.data = data
        self.next = None
        self.prev = None

class LinkedList:
    def __init__(self):
        self.head = None
    