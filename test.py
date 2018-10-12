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
    print (questions_and_answers[1][1])
    return questions_and_answers
    
get_all_questions()
    

