from tkinter import *
window =Tk()
window.title("My First GUI program")
window.minsize(width=500, height=300)
#Creating lable

Moazam_label=Label(text=" I am a Label", font=("Arial", 24 ,"bold"))
Moazam_label["text"]="This is a new label"
Moazam_label.configure(text="this is a new label 2")
Moazam_label.pack()
# How to create  Button using tkinter
def got_cicked():
    Moazam_label.configure(text= input.get())
new_button=Button(text="click me", command=got_cicked)
new_button.pack()

# How to work with inputs and listen to that input ----> concept of Entry in tkinter
input= Entry(width=30) #--> how we get hold of this input? well using get() method on that input-----> input.get()
input.insert(END, string="Please Enter your Text here") # To set the default value of input description
input.pack()

# How to add Multiline Text using TKinter
input_text=Text(height=10, width=30)
input_text.insert(END, "Example of multi line text")
print(input_text.get("1.0", END)) #--> get method helps to get hold of the text being entered  in multi line box
input_text.pack()

# How to create SpinBox using TK inter
def spin_box_got_executed():
    print(spinbox_practise.get())
spinbox_practise= Spinbox(from_=0, to=10, command=spin_box_got_executed) # to create SpinBox from SpinBox class with some arguements
spinbox_practise.pack()

#Scale
#Called with current scale value.
def scale_used(value):
    print(value)
scale = Scale(from_=0, to=100, command=scale_used)
scale.pack()

#Checkbutton
def checkbutton_used():
    #Prints 1 if On button checked, otherwise 0.
    print(checked_state.get())
#variable to hold on to checked state, 0 is off, 1 is on.
checked_state = IntVar()
checkbutton = Checkbutton(text="Is On?", variable=checked_state, command=checkbutton_used)
checked_state.get()
checkbutton.pack()

#Radiobutton
def radio_used():
    print(radio_state.get())
#Variable to hold on to which radio button value is checked.
radio_state = IntVar()
radiobutton1 = Radiobutton(text="Option1", value=1, variable=radio_state, command=radio_used)
radiobutton2 = Radiobutton(text="Option2", value=2, variable=radio_state, command=radio_used)
radiobutton1.pack()
radiobutton2.pack()

#Listbox
def listbox_used(event):
    # Gets current selection from listbox
    print(listbox.get(listbox.curselection()))

listbox = Listbox(height=4)
fruits = ["Apple", "Pear", "Orange", "Banana"]
for item in fruits:
    listbox.insert(fruits.index(item), item)
listbox.bind("<<ListboxSelect>>", listbox_used)
listbox.pack()

window.mainloop()





