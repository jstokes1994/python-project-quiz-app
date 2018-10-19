import os
import re
from flask import Flask, render_template, request, redirect, url_for

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

def ask_questions(username, question_number):
    incorrect_answers = []
    questions = get_all_questions()
    question = questions[int(question_number)][0]
    assert question == questions[1][0], "When 1 passed in as the question number it should find right question" 
    if request.method == "POST":
        user_answer = request.get_data()
        convert_to_str = user_answer.decode() #Necessary with Python3
        raw_answer = convert_to_str.split("=")[1]
        answer = raw_answer.replace("+", " ") #replaces the + from URL with a space
        if answer == questions[int(question_number)][1]:
            question_number = int(question_number) + 1
            with open("data/leaderboard.txt", "a") as scoreboard:
                scoreboard.writelines(username + "\n")
            incorrect_answers.clear()
            return redirect(url_for('success_page', username=username, question_number=question_number, answer=answer))
        else:
            incorrect_answers.append(answer)
            return redirect(url_for('failure_page', username=username, question_number=question_number, answer=answer))
    return render_template("riddle.html", question=question, username=username, incorrect_answers=incorrect_answers)

#ask_questions("joe", 1)

def leaderboard():
    count = {}
    usernames = []
    score = []
    for w in open('data/leaderboard.txt').read().split():
        if w in count:
            count[w] += 1
        else:
            count[w] = 1
    assert count["joester"] == 8, "joester appears 8 times in leaderboard.txt" 
    assert count ["Harry"] == 3, "Harry appears 3 times"
    for word, times in count.items():
        score.append(times)
        usernames.append(word)
        username_and_score = list(zip(score, usernames))
        sorted_username_and_score = sorted(username_and_score, reverse=True)

leaderboard()