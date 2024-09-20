from tkinter import *
window =Tk()
window.title("Mile to Km converter")
window.minsize(width=500, height=300)
window.config(padx=50, pady=50)
# Creating the Entry (which is working as a input)
input= Entry(width=20) #--> how we get hold of this input? well using get() method on that input-----> input.get()
input.insert(END, string="") # To set the default value of input description
input.grid(column=250, row=1)

# Creating label next to entry
mile_label=Label(text="Miles", font=("Arial", 15 ,"normal"))
mile_label.grid(column=280, row=1)
mile_label.config(padx=30, pady=10)

# Creating label next to entry
isequal_label=Label(text="is equal to", font=("Arial", 15 ,"normal"))
isequal_label.grid(column=0, row=150)
isequal_label.config(padx=30, pady=10)


# Creating label next to entry
km_converter_label=Label(text="0", font=("Arial", 15 ,"normal"))
km_converter_label.grid(column=250, row=150)
km_converter_label.config(padx=30, pady=10)

# Creating label next to entry
km_label=Label(text="Km", font=("Arial", 15 ,"normal"))
km_label.grid(column=280, row=150)
km_label.config(padx=30, pady=10)

def got_cicked():
    km_converter_label.configure(text=int(input.get())*1.6)
new_button=Button(text="Calculate", command=got_cicked)
new_button.grid(column=250, row=250)



window.mainloop()