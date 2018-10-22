import os
import re
from flask import Flask, render_template, request, redirect, url_for
from fuzzywuzzy import fuzz, process

app = Flask(__name__)

incorrect_answers = [] # Global variable used for the list of incorrect answers found on the riddle.html page.

def get_all_questions():
# This function takes each line in questions.txt file (questions and answers) and puts them into individual lists before 
# zipping into a list of tuples
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
    
def checkUsernameExists(username):
# This function reads each line in users.txt and returns true if the name input already exists
# The user input username is the parameter of the function
    with open("data/users.txt", "r") as usernameList:
        if re.search('^{0}$'.format(re.escape(username)), usernameList.read(), flags=re.M):
            return True
        else:
            return False
    
@app.route('/', methods=["GET", "POST"])
# Home Page where user chooses a username
# The checkUsernameExists() function is invoked and user is redirected based on availability of the username in the txt file.
def index():
    if request.method == "POST":
        username = request.form["username"]
        if checkUsernameExists(username):
            return redirect(url_for('usernameExists', username=username))
        else:
            with open("data/users.txt", "a") as user_list:
                user_list.writelines(request.form["username"] + "\n")
        return redirect(request.form["username"])
    return render_template("index.html")

@app.route('/<username>', methods=['GET', 'POST'])
# Page that invites the user to start the quiz
def start_game(username):
    question_number = 0 # This is where the question_number variable starts before incremeting up after each correct answer
    if request.method == "POST":
        return redirect(url_for('ask_questions', username=username, question_number=question_number))
    return render_template("startgame.html", username=username)
    
@app.route('/<username>/exists', methods=['GET', 'POST'])
# Page that informs the user that the page exists - simply redirect back to index page on button click
def usernameExists(username):
    if request.method == "POST":
        return redirect(url_for('index'))
    return render_template("username_exists.html", username=username)

@app.route('/<username>/<question_number>', methods=['GET', 'POST'])
# Ask a question dependent on which question_number the user is on
# Checks the user's answer's fuzz.ratio (likeness) to the actual answer and redirects to success/failure page
# If incorrect the answer is stored in a list and sent to the HTML template to be shown on the page
# Starts the scoreboard functionality by simply writing the username to a newline in leaderboard.txt when correct
def ask_questions(username, question_number):
    questions = get_all_questions()
    question = questions[int(question_number)][0]
    if request.method == "POST":
        user_answer = request.get_data() # How to handle the user data from form
        convert_to_str = user_answer.decode() # Necessary with Python3 (bytes>str)
        raw_answer = convert_to_str.split("=")[1] # split user answer from the 'guess=' found in the URL
        answer = raw_answer.replace("+", " ") #replaces the + from URL with a space
        if fuzz.ratio(answer, questions[int(question_number)][1]) >= 80: # module fuzzywuzzy allows string matching for similar answers (more in readME)
            question_number = int(question_number) + 1
            with open("data/leaderboard.txt", "a") as scoreboard:
                scoreboard.writelines(username + "\n")
            incorrect_answers.clear() # Empty the incorrect answers list when the user answers correctly, ready for next question
            return redirect(url_for('success_page', username=username, question_number=question_number, answer=answer))
        else:
            incorrect_answers.append(answer)
            return redirect(url_for('failure_page', username=username, question_number=question_number, answer=answer))
    return render_template("riddle.html", question=question, username=username, incorrect_answers=incorrect_answers)
    
@app.route('/<username>/<question_number>/<answer>/correct', methods=['GET', 'POST'])
# Page appears if user got the correct answer
# If the question_number is more than 7, there are no more questions and user has finished the game so redirects to quiz_complete page.
def success_page(username, question_number, answer):
    if request.method == "POST" and int(question_number) <= 7:
        return redirect(url_for('ask_questions', username=username, question_number=question_number))
    elif int(question_number) > 7:
        return redirect(url_for('quiz_complete', username=username))
    return render_template("success.html", username=username)
    
@app.route('/<username>/<question_number>/<answer>/incorrect', methods=['GET', 'POST']) 
# Page appears if user got the question wrong
def failure_page(username, question_number, answer):
    if request.method == "POST":
        return redirect(url_for('ask_questions', username=username, question_number=question_number))
    return render_template("failure.html", username=username, incorrect_answer=answer)
    
@app.route('/<username>/complete', methods=['GET', 'POST'])
# Page to inform the user they have completed the quiz
# Invites user to look at the leaderboard
def quiz_complete(username):
    if request.method == "POST":
        return redirect(url_for('leaderboard'))
    return render_template("completed.html", username=username)
    
@app.route('/leaderboard', methods=['GET', 'POST'])
# Page to show the leaderboard for all users - How many questions they got through before completing/quitting (check readMe for more)
def leaderboard():
    count = {}
    usernames = []
    score = []
    for w in open('data/leaderboard.txt').read().split():
        if w in count:
            count[w] += 1
        else:
            count[w] = 1
    for word, times in count.items():
        score.append(times)
        usernames.append(word)
        username_and_score = list(zip(score, usernames)) # Zip the two lists so username and score are together
        sorted_username_and_score = sorted(username_and_score, reverse=True) # Display the username/score in order of score (reversed for descending)
    return render_template("leaderboard.html", username_and_score=sorted_username_and_score)

app.run(host=os.getenv('IP'), port=int(os.getenv('PORT')), debug=True) 
