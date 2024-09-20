from tkinter import *
import math
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 1
LONG_BREAK_MIN = 20
CHECK_MARK= "✔"
reps=0
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global CHECK_MARK
    global reps
    reps = 0
    # Cancel the timer when i hit the reset
    window.after_cancel(timer)
    # Set the label back to original once i press Reset button
    timer_label.config(text="Timer")
    # Update the Canvas text
    canvas.itemconfig(timer_text, text="00:00")
    # clearning off all the check MArk
    CHECK_MARK = ""
    checkmark_label.config(text= CHECK_MARK)
# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_countdown():
    global reps
    reps += 1
    print(f"printing reps before countdown start{reps}")
    work_in_sec = WORK_MIN * 60
    short_break_in_sec = SHORT_BREAK_MIN * 60
    long_break_in_sec = LONG_BREAK_MIN * 60
    if reps % 8 == 0:
        timer_label.config(text="Break", font=(FONT_NAME, 30, "bold"), fg=RED, bg=YELLOW, highlightthickness=0)
        count_down(long_break_in_sec)
    elif reps % 2 == 0:
        timer_label.config(text="Break", font=(FONT_NAME, 30, "bold"), fg=PINK, bg=YELLOW, highlightthickness=0)
        count_down(short_break_in_sec)
    else:
        timer_label.config(text="Work", font=(FONT_NAME, 30, "bold"), fg=GREEN, bg=YELLOW, highlightthickness=0)
        count_down(work_in_sec)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    global timer
    global reps
    count_minutes= math.floor(count / 60)
    count_seconds = count % 60
    if count_seconds == 0:
        count_seconds = "00"
    elif count_seconds < 10:
        count_seconds=f"0{count_seconds}"
    canvas.itemconfig(timer_text, text=f"{count_minutes}:{count_seconds}")
    if count > 0:
        timer=window.after(1000, count_down, count-1)
    else:
        start_countdown()
        global CHECK_MARK
        mark = ""
        print(f"the value of reps is: {reps} ")
        work_session= math.floor(reps/2)
        for _ in range(work_session):
            print("loop is coming for check Mark")
            mark += "✔"
        CHECK_MARK = mark
        checkmark_label.configure(text=mark)



# ---------------------------- UI SETUP ------------------------------- #
window=Tk()
window.title("Promodora Application")
window.minsize(width=300, height=200)
window.config(padx=50, pady=80, bg=YELLOW)
canvas=Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_image=PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_image)
timer_text=canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=100, row=130)
#creating label
timer_label=Label(text="Timer", font=(FONT_NAME, 30 ,"bold"), fg=GREEN, highlightthickness=0, bg=YELLOW)
timer_label.grid(column=100, row=1)
timer_label.config(padx=10, pady=10)
#Creating Start Button
start_button=Button(text="Start", height=1, width=10, command=start_countdown)
start_button.grid(column=30, row=200)
start_button.config(padx=5, pady=5)
#Creating End Button
end_button=Button(text="Reset", height=1, width=10, command=reset_timer)
end_button.grid(column=200, row=200)
end_button.config(padx=5, pady=5)
#Creating checKmark label
checkmark_label=Label(font=(FONT_NAME, 30 ,"bold"), fg=GREEN, highlightthickness=0, bg=YELLOW)
checkmark_label.grid(column=100, row=280)
checkmark_label.config(padx=10, pady=10)
window.mainloop()