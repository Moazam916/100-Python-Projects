from question_model import Question
from data import Data
from quiz_brain import QuizBrain
from ui import QuizInterface
OPEN_TRIVIA_URL = "https://opentdb.com/api.php"
TRIVIA_URL_PARAMETERS = {
    "amount": 10,
    "type": "boolean"
}
api_questions = Data(url=OPEN_TRIVIA_URL, parameters=TRIVIA_URL_PARAMETERS)
question_data = api_questions.questions["results"]

question_bank = []
for question in question_data:
    question_text = question["question"]
    question_answer = question["correct_answer"]
    new_question = Question(question_text, question_answer) # this line of code returning question text and question
    # answer as a input and then return class object by inheriting that class attributes
    question_bank.append(new_question) # blue print have been created which is having two attributes text and answer

quiz_ui = QuizInterface(quiz_class_blueprint=question_bank)

