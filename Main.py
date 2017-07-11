'''
Created on Jun 7, 2017

@author: hockettr
'''

'''
This program is intended to read in a csv file which represents customer questions 
it established a searchable database in the form of a nested dictionary. When a new set of questions is inputted
the program finds questions similar to the new questions and outputs those questions. In a perfect state, the program
would output a suitable answer to each question.
'''


'''
Identified problems: 

Doesn't seem to properly read the first row of the csv file
'''



import numpy
import matplotlib
import pandas
import scipy
import sklearn
import csv
import re
import string
from operator import itemgetter
from User_Interaction import usr_inp, man_yn, new_config
import pickle
import timeit


all_questions = dict()

tags_d = dict()

#another question class that is rendered from a direct fresh desk call
class QUE(object):
    qid = 0
    c_year = 0
    c_month = 0
    c_day = 0
    e_year = 0
    e_month = 0
    e_day = 0
    rel_desc = []
#dictionary of ids and questions objects with desc and date attributes
description_dict = pickle.load(open('desc_dates_by_qid.p','rb'))

main_csv = 'All_tickets.csv' #Enter the filepath of the main csv data file

New_csv = 'new_tickets.csv'  # Enter the name of the new csv file here



# class that establishes object question
class Question(object):
    qid = 0
    subject_cond = ""
    tags = []
    desc_cond = ""
    email = ""
#function which helps to remove filler words from subjects and reduce the number of false matches


# all_questions = pickle.load(open('questions.p','rb'))

# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Uncomment this line if you want to load from file 

def condense_subj(subj):
    if type(subj) == str:
        cond = re.sub('(\s)+(a|an|and|the|for|on|from)(\s+)', '\2', subj)
        no_punc = cond.translate(None, string.punctuation)
        all_lower = no_punc.lower()
        return all_lower
    else:
        return ""
#makes tag lowercase

def l_tag(tag):
    if type(tag) == float:
        return []
    tags = tag.split(',')
    l_tags = []
    for t in tags:
        l_tags.append(t.lower())
    return l_tags
        
#creates a new question
def make_question(qid, subject, status, email, tags):
    question = Question()
    question.qid = qid
    question.subject_cond = condense_subj(subject)
    question.tags = l_tag(tags)
    question.email = email
#     question.desc_cond = description_dict[qid].rel_desc
    if qid not in all_questions:
        all_questions[qid] = question
    return question

# def get_all_subjects():
#     sub_list = []
#     for key in loaded_questions.keys():
#         sub_list.append(key.subject_cond)
#     return sub_list
# proper column order is: qid, subject, status, email,tags

#reads in csv file row by row into a series of tuples, each tuple represents a row
def read_csv(csv_file):
    df = pandas.read_csv(csv_file, delimiter=',')
    tuples = [tuple(x) for x in df.values]
    return tuples


#Each row is now converted into an object of type question
def create_questions(csv_tuples):
    question_list = []
    for quest in csv_tuples:
        question_list.append(make_question(*quest))
    return question_list


#renders new csv input into list of question objects
def new_input(new_csv):
    tupes = read_csv(new_csv)
    return create_questions(tupes)

#creates a new object question to test against database
def new_man_inp(qid, subject,status,email,tags):
    ls = []
    ls.append(make_question(qid, subject, status, email, tags))
    return ls
# not used right now
def calc_weights(quest_ls):
    tag_weights = dict()
    for quest in quest_ls:
        for tag in quest.tags:
            if tag in tag_weights:
                tag_weights[tag] += 1
            else:
                tag_weights[tag] = 1
    return tag_weights


#both of these functions update a dictionary of tags which map to the subjects that are linked to these tags
#initial organization of tags_d. Only used when implementing from new CSV data file
def subj_org(tag, q, dc):
    subj = q.subject_cond
    if subj in dc[tag]:
        dc[tag][subj].append(q.qid)
    else:
        dc[tag][subj] = []
        dc[tag][subj].append(q.qid)

def organize(qlist,dc):
    for q in qlist:
        for tag in q.tags:
            if tag in dc:
                subj_org(tag, q, dc)
            else:
                dc[tag] = {}
                subj_org(tag, q, dc)

#this number represents the degree of similarity between two subjects that you are requiring
similarity_threshold = 0

#this function determines similarity possible subjects using set intersection               
def most_similar(subjects, q_sub):
    subj_matches = []
    for subj in subjects:
        common_score = len(set(subj.split(" ")).intersection(set(q_sub.split(" "))))
        if common_score >= similarity_threshold:
            subj_matches.append((subj, common_score)) 
#     print 'q', q_sub
#     print subj_matches   
    return sorted(subj_matches, key = itemgetter(1), reverse = True)

# def exact_comparison(subject, s_score):
#     if len(subject) == s_score:
#         return '(Exact)'
#     else: return ''
                 
#this function compares your new inputs to the full database                                       
def test_new_input(tdict, questions):
    match_dict=dict()
    for question in questions:
        matches = []
        subjects = []
        tags = question.tags
        for tag  in tags:
            if tag in tdict:
                subjects = tdict[tag].keys()
    
#             else:
#                 subjects = get_all_subjects()   
#             print subjects
#             print "try subjs: ", tag, subjects
            sorted_subjs = most_similar(subjects, question.subject_cond)
            for subj in sorted_subjs:
                act_subj = subj[0]
                qids = tdict[tag][act_subj]
                s_qids = set(qids)
                matches.append((s_qids,subj[1]))
        match_dict[question.qid]=matches
    return match_dict
        
# recon = False

def output_config(m_dict):
    aqs = pickle.load(open('questions.p','rb'))
    print '\r'
    for k in m_dict.keys():
        q = aqs[k]
        print k, q.subject_cond
        for v in m_dict[k]:
            e_match=''
            ind = 0
            for i in v[0]:
                ind = int(i)
            v_s = aqs[ind]
            v_ss = v_s.subject_cond
            if len(v_ss.split(' ')) == v[1]: e_match='(exact)'
            print '\t'+str(ind)+':', (v_ss)+', score:', str(v[1]), e_match
            print '\t\t'+ 'https://gamesparks.freshdesk.com/api/v2/tickets/1'+str(ind)
        print '\r'
#     print aqs
#     print m_dict

def main():
    
    #loads tags dictionary from file
    n_tags_d = pickle.load(open('file.p','rb'))
    #these steps configure the database...Shouldn't be necessary once stored properly
    #should be run once
    dct = dict()
    if new_config():
        dct = tags_d
        cs = read_csv(main_csv)
        qls = create_questions(cs)
        organize(qls,dct)
        pickle.dump(tags_d, open('file.p','wb'))
        x = pickle.load(open('file.p','rb'))
        pickle.dump(all_questions,open('questions.p','wb'))
        c = pickle.load(open('questions.p','rb'))
        
    else:
        dct = n_tags_d
    #--------------------------------------------------------------------------------
    if man_yn():
        #manual entry
        man = new_man_inp(*usr_inp())
        o_dict = test_new_input(dct, man)
        output_config(o_dict)
        organize(man,dct)
        
    else:
        #entry from csv
        start = timeit.default_timer()
        quests = new_input(New_csv)
        o_dict = test_new_input(dct, quests)
        pickle.dump(all_questions,open('questions.p','wb'))
        output_config(o_dict)
        organize(quests,dct)
        stop = timeit.default_timer()
        print stop-start
    pickle.dump(dct, open('file.p','wb'))   
    pickle.dump(all_questions,open('questions.p','wb'))
if __name__ == "__main__":
    main()
    
