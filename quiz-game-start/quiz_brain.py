class QuizBrain:
    def __init__(self, questions_list):
        self.question_number = 0
        self.questions_list = questions_list
        self.score = 0

    def still_has_questions(self):
        if self.question_number >= len(self.questions_list):
            return False
        else:
            return True

    def next_question(self):
        current_question = self.questions_list[self.question_number]
        self.question_number += 1
        user_answer = input(f"Q.{self.question_number}: {current_question.question} (True/False): ")
        self.check_answer(user_answer=user_answer, question_answer=current_question.correct_answer)

    def check_answer (self, user_answer, question_answer):
        if user_answer.lower() == question_answer.lower():
            self.score += 1
            print("You got it right: ")
        else:
            print("That's wrong.")
        print(f"The correct answer was: {question_answer}.")
        print(f"Your current score is: {self.score}/{self.question_number}")
        print("\n")