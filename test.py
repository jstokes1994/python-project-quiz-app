import os
import re
from flask import Flask, render_template, request, redirect, url_for
from operator import itemgetter

def get_all_questions():
    questions = []
    answers = []
    with open("data/questions.txt", "r") as riddles:
        lines = riddles.read().splitlines()
    for i, text in enumerate(lines):
        if i%2 == 0:
            questions.append(text)
        else:
            answers.append(text)
            
    questions_and_answers = list(zip(questions, answers))
    
    assert len(questions_and_answers) == 8, "There should be 8"
    assert len(answers) == 8, "There are 8 answers"
    assert(lines[0]) == questions[0], "It is a question 1"
    assert(lines[3]) == answers[1], "It is the second answer"
    assert questions_and_answers[0][0] == questions[0], "First question in zipped list is question 1"
    assert questions_and_answers[4][1] == answers[4], "questions_and_answers{4][1] should be the 4th answer"
    
    return questions_and_answers
    
get_all_questions()

def checkUsernameExists(username):
    with open("data/users.txt", "r") as usernameList:
        if re.search('^{0}$'.format(re.escape(username)), usernameList.read(), flags=re.M):
            return True
        else:
            return False
            
assert checkUsernameExists("joester") == True, "joester does exist"
assert checkUsernameExists("randomname123") == False, "randomname123 does not exist"




    