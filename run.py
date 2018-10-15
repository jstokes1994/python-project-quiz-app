import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

incorrect_answers = []
score = 0

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
    return questions_and_answers
    
@app.route('/', methods=["GET", "POST"])
def index():
    """Home Page where user chooses a username"""
    if request.method == "POST":
        with open("data/users.txt", "a") as user_list:
            user_list.writelines(request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")

@app.route('/<username>', methods=['GET', 'POST'])
def start_game(username):
    question_number = 0
    if request.method == "POST":
        return redirect(url_for('ask_questions', username=username, question_number=question_number))
    return render_template("startgame.html", username=username)
    
@app.route('/<username>/<question_number>', methods=['GET', 'POST'])
def ask_questions(username, question_number):
    questions = get_all_questions()
    question = questions[int(question_number)][0]
    if request.method == "POST":
        user_answer = request.get_data()
        convert_to_str = user_answer.decode() #Necessary with Python3
        answer = convert_to_str.split("=")[1]
        if answer == questions[int(question_number)][1]:
            question_number = int(question_number) + 1
            incorrect_answers.clear()
            return redirect(url_for('success_page', username=username, question_number=question_number, answer=answer))
        else:
            incorrect_answers.append(answer)
            print(incorrect_answers)
            return redirect(url_for('failure_page', username=username, question_number=question_number, answer=answer))
    return render_template("riddle1.html", question=question, username=username, incorrect_answers=incorrect_answers)
    
@app.route('/<username>/<question_number>/<answer>/correct', methods=['GET', 'POST'])
def success_page(username, question_number, answer):
    if request.method == "POST" and int(question_number) <= 7:
        return redirect(url_for('ask_questions', username=username, question_number=question_number))
    elif int(question_number) > 7:
        return redirect(url_for('quiz_complete', username=username))
    return render_template("success.html", username=username)
    
@app.route('/<username>/<question_number>/<answer>/incorrect', methods=['GET', 'POST'])    
def failure_page(username, question_number, answer):
    if request.method == "POST":
        return redirect(url_for('ask_questions', username=username, question_number=question_number))
    return render_template("failure.html", username=username, incorrect_answer=answer)
    
@app.route('/<username>/complete', methods=['GET', 'POST'])
def quiz_complete(username):
    return render_template("completed.html")

#Add a finishing page
#Can we figure out the + thing?
#Scoreboard
#Style it

#README - under impression we were not to use sessions
# request.get_data() as this is putting in a multidict

    #if question[question_number][0] == question[question_number][1]:
     #   question_number += 1

        
    

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True) 
