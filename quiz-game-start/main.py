from question_model import Question
from data import question_data
from quiz_brain import QuizBrain
question_bank = []
for i in range(0, len(question_data)):
    new_question = Question(question=question_data[i]["question"], correct_answer=question_data[i]["correct_answer"])
    question_bank.append(new_question)

quiz = QuizBrain(questions_list=question_bank)

while quiz.still_has_questions():
    quiz.next_question()
print("You have complete the quiz.")
print(f"Your total score was: {quiz.score}/{quiz.question_number}")