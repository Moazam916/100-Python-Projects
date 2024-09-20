from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json
FONT_NAME = "Courier"
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
#-----------------------------PASSWORD SEARCH------------------------------------#
def password_search():
    website_lookup = website_entry.get()
    with open('credentials_file.json', 'r') as data_file:
        data = json.load(data_file)
        if website_lookup in data:
            Email = data[website_lookup]["email"]
            Password = data[website_lookup]["password"]
            messagebox.showinfo(title=website_lookup, message=f"Email: {Email}\nPassword: {Password}")
        else:
            messagebox.showinfo(title=website_lookup, message=f"Sorry no Record found for {website_lookup}")

# ---------------------------- PASSWORD GENERATOR --------------------------------#
def password_generator():
    password_list = []
    new_letters = [password_list.append(choice(letters)) for item in range(randint(8, 10))]
    new_symbols = [password_list.append(choice(symbols)) for item in range(randint(2, 4))]
    new_numbers = [password_list.append(choice(numbers)) for item in range(randint(2, 4))]
    shuffle(password_list)
    password = "".join(password_list)
    password_entry.insert(END, string=f"{password}")
    pyperclip.copy(f"{password}")
# ---------------------------- SAVE PASSWORD ------------------------------- #
def password_saver():
    website= website_entry.get()
    email_username= username_email_entry.get()
    password = password_entry.get()
    new_data ={
        website:{
        "email": email_username,
        "password": password
        }
    }
    if len(website) == 0 or len(password) ==0:
        messagebox.showinfo(title= "Oops", message="Please dont leave any fields empty")
    else:
        try:
            with open('credentials_file.json', 'r') as data_file:
                data = json.load(data_file)  # Reading the Data from file
                data.update(new_data)  # Updating the existing Data using new Data
        except FileNotFoundError:
            with open('credentials_file.json', 'w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            with open('credentials_file.json', 'w') as data_file:
                json.dump(data, data_file, indent=4)  # Writing updated data back to file
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
# ---------------------------- UI SETUP ------------------------------- #
window=Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)
canvas= Canvas(width=200, height=200)
logo_image=PhotoImage(file="logo.png")
canvas.create_image(100,100, image=logo_image)
canvas.grid(column=1, row=0)
# creating Password Manager labels
website_label= Label(text="Website:", font=(FONT_NAME, 10 ,"normal"))
website_label.grid(column=0, row=1)
email_username_label=Label(text="Email/Username:", font=(FONT_NAME, 10 ,"normal"))
email_username_label.grid(column=0, row=2)
password_label=Label(text="Password:", font=(FONT_NAME, 10 ,"normal"))
password_label.grid(column=0, row=3)
# Creating Password Manager Entries
website_entry=Entry(width=35)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2)
username_email_entry=Entry(width=35)
username_email_entry.insert(0, string="moazamshahzad222@gmail.com")
username_email_entry.grid(column=1, row=2, columnspan=2)
password_entry=Entry(width=17)
password_entry.insert(END, string="")
password_entry.grid(column=1, row=3)
#Creating Password Manager's Button
new_button=Button(text="Generate Password", width= 14, command=password_generator)
new_button.grid(column=2, row=3, columnspan=1)
#Creating Add Button
add_button=Button(text="Add", width= 30, command=password_saver)
add_button.grid(column=1, row=4, columnspan=2)
#Creating the search button
search_button = Button(text="Search", width=13, height=0, command = password_search)
search_button.grid(column=2, row=1)
window.mainloop()