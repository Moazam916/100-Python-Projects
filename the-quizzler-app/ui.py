from tkinter import *
from quiz_brain import QuizBrain

THEME_COLOR = "#375362"


class QuizInterface:
    def __init__(self, quiz_class_blueprint):
        self.window = Tk()
        self.window.title("Quizzer")
        self.window.config(width=500, height=700)
        self.window.config(padx=20, pady=20, bg=THEME_COLOR)
        self.canvas = Canvas(width=300, height=250)
        self.question_text = self.canvas.create_text(150,
                                                     125,
                                                     width=280,
                                                     fill=THEME_COLOR,
                                                     text="some questions",
                                                     font=("Arial", 20, "italic"))
        self.canvas.grid(column=0, row=1, columnspan=2, pady=50)
        self.score = Label(text=f"score: 0", bg=THEME_COLOR, fg="white")
        self.score.grid(column=1, row=0, padx=20, pady=20)
        self.photo_true = PhotoImage(file="images/true.png")
        self.photo_false = PhotoImage(file="images/false.png")
        self.true_button = Button(image=self.photo_true,
                                  highlightthickness=0,
                                  bg=THEME_COLOR,
                                  command=self.checking_true_answer)
        self.true_button.grid(column=0, row=2, padx=20, pady=20)
        self.false_button = Button(image=self.photo_false,
                                   highlightthickness=0,
                                   bg=THEME_COLOR,
                                   command=self.checking_false_answer)
        self.false_button.grid(column=1, row=2, padx=20, pady=20)
        self.quiz_brain = QuizBrain(quiz_class_blueprint)
        self.next_question()
        self.window.mainloop()

    def next_question(self):
        self.canvas.config(bg="white")
        if self.quiz_brain.still_has_questions():
            q_text = self.quiz_brain.next_question()
            print(q_text)
            self.canvas.itemconfig(self.question_text, text=f"{q_text}")
        else:
            self.canvas.itemconfig(self.question_text, text="You have reached the end of quiz")
            self.true_button.config(state="disabled")
            self.false_button.config(state="disabled")

    def checking_true_answer(self):
        answer_is = self.quiz_brain.check_answer(user_answer="True")
        self.user_feedback(input_answer_is=answer_is)

    def checking_false_answer(self):
        answer_is = self.quiz_brain.check_answer(user_answer="False")
        self.user_feedback(input_answer_is=answer_is)

    def user_feedback(self, input_answer_is):
        if input_answer_is:
            self.canvas.config(bg="green")
            self.score.config(text=f"score: {self.quiz_brain.score}")
        else:
            self.canvas.config(bg="red")

        self.window.after(1000, func=self.next_question)
