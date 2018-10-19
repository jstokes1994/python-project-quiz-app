# RiddleMeThis

This is a game that combines Python and Flask to produce a quiz game. The game
asks 8 different riddles which a user can work through before reaching the end.

The game includes a leaderboard in which it shows the high scores of users that 
have taken part in the game (includes those who didn't make it to the end).

Since the learning had not taken us through sessions, I made the presumption
they were not supposed to be used. Through research for the project I did
note that sessions would be useful certain areas but decided to provide
a solution without.

## UX

My project is very simplistic in design. Considering the lack of features
expected it felt necessary to produce a clean and simple design to the user.

The homepage very briefly introduces the game and the box to provide a username
is self explanatory. It also provides a button to view the leaderboard.

Each page thereafter follows a consistent CSS style which offers no surprise
or distraction from the project's purpose.

One potential user frustration would potentially come from when incorrect on an
answer or when attempting to choose a unique username. For both, the game is
redirected to a URL which is solely built to inform the user they are correct/
incorrect or that the username has been taken. It seems like an unnecessary step
to have these extra pages but it seemed like the only way possible with the
technologies expected.

## Features

### Riddles:

Here the riddle.html template contains a variable 'question_number'. As the
questions and answers are stored in a list of tuples it allowed iteration
through the list after each correct answer ([question_number][0]).

When a question was answered correctly, the question_number variable had 1 added
to it. The success page would then allow the riddle.html template to be reloaded
with the new question_number variable in place.

The ask_questions() function also facilitated the checking of the answer in
which the questions_and_answers list of tuples again became useful in which
the index could be found as follows: [question_number][1].

### Incorrect answers:

Within the ask_questions() function every time an answer did not match the
answer found in the list of tuples it was appended to a incorrect_answer list.
The html page contains a for loop that adds the incorrect answer every time the
failure page redirects back to the riddle html page.

### Features left to implement:

I would like to add the ability for slightly incorrect answers to be accepted.
For example if an answer is 'apple', and the user types 'an apple', this should
be accepted and would cause frustration. This is also the case with capitalised
answers.

I would like to add the ability for the page to update dynamically and inform
the user they were incorrect or correct without the need for the success/failure
pages. I believe this could be achieved through sessions.

Again sessions should allow the riddles to be shuffled so that it is not the 
same 8 questions each time and selected by a larger pool of riddles.

### Leaderboard:

My solution to the leaderboard was everytime a correct answer was found, the
username of the user would be written to a new line in a specially made 
"leaderboard.txt" file. Then using the leaderboard() function the sum of each
unique username is counted and then presented in a table on the leaderboard.html
template.

## Technologies Used

- Python 3.4.3
- Flask (Python Microframework)
- BootStrap 3
- Google Fonts
- CSS
- HTML

## Testing:

# Automated:

I tried to use automated tests and follow the TDD principle where I could.
The tests can be found in the test.py file

# Manual tests:

To test the index() function on the homepage, simply type in a username and
check the users.txt file to make sure it is being appended.

To test the start_game(username, question_number) function, I made sure that
the URL was being filled with the requested username and with 0 as the 
question_number. It was crucual the question number was 0 to start at the 0
index in the questions_and_answers list of tuples.

For the ask_questions() function, it was simple to test the answer functionality.
When typing in correct answer it should redirect to success page and when wrong,
to the failure page. Could also see the username being printed to the 
leaderboard.txt file when correct. If incorrect, the answer is seen printed
below the answer box - so clearly working.

For testing the leaderboard() function, I used the automated tests shown in 
test.py but also made sure the data was being passed to the HTML file properly.
I tried new users with random names answering varying numbers of questions and
was satisfied it was being displayed correctly.
