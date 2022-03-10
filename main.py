from tkinter import *
from tkinter import messagebox
from password_genie import PasswordGenie
import pyperclip
import json


# site searcher
def search_websites():
    try:
        with open("passwords.json", "r") as sites:
            data = json.load(sites)
    except FileNotFoundError:
        messagebox.showinfo(title="File Not Found!", message="There was no data file found.")
    else:
        # data.update(new_data)
        # with open("passwords.json", "w") as passwords:
        #     json.dump(data, passwords, indent=4)
        print(type(data))
        website = website_input.get().upper()
        if website in data:
            messagebox.showinfo(title="Password Obtained",
                                message=f"Email: {data[website]['email']}\nPassword: {data[website]['password']}")
        else:
            messagebox.showinfo(title="No Data Found", message=f"No data found for {website.title()} exist.")

        # found_data = False
        # for website in data:
        #     print(website)
        #     if website_input.get().upper() == str(website).upper():
        #         print(website)
        #         messagebox.showinfo(title="Password Obtained",
        #                             message=f"Email: {website['email']}\nPassword: {website['password']}")
        #         found_data = True
        # if not found_data:

    # finally:
    #     website_input.delete(0, END)
    #     password_input.delete(0, END)
    # return True


# Pass generator
def return_generate_button():
    generate_button.config(text="Generate Password", fg="#ffc53d")


def generate_password():
    password_input.delete(0, END)
    password_input.insert(0, PasswordGenie().return_password())
    pyperclip.copy(password_input.get())
    generate_button.config(text="Copied!", fg="red", width=14)
    generate_button.after(2000, return_generate_button)


# save pass
def add_password():
    if not len(website_input.get()) or not len(username_input.get()) or not len(password_input.get()):
        messagebox.showinfo(message="Please do not leave any fields empty!", title="Uh Oh")
    else:
        confirmed = messagebox.askokcancel(title=website_input.get(),
                                           message=f"Confirm data:\n\nWebsite: {website_input.get()}\n"
                                                   f"Username: {username_input.get()}\n"
                                                   f"Password: {password_input.get()},\n\nIs it ok to save?")
        if confirmed:
            new_data = {
                website_input.get().upper(): {
                    "email": username_input.get(),
                    "password": password_input.get()
                }
            }
            # data = {}
            try:
                with open("passwords.json", "r") as passwords:
                    # passwords.write(f"{website_input.get()} | {username_input.get()} | {password_input.get()}\n")
                    data = json.load(passwords)
            except FileNotFoundError:
                with open("passwords.json", "w") as passwords:
                    json.dump(new_data, passwords, indent=4)
            else:
                data.update(new_data)
                with open("passwords.json", "w") as passwords:
                    json.dump(data, passwords, indent=4)
            finally:
                website_input.delete(0, END)
                password_input.delete(0, END)


# ui setup
window = Tk()
window.title("Magic Password")
window.config(padx=30, pady=30, bg="black")

canvas = Canvas(width=400, height=500, highlightthickness=0)
canvas.config(bg="black")
padlock_img = PhotoImage(file="padlock.png")
canvas.create_image(200, 250, image=padlock_img)
text_item = canvas.create_text(200, 50, text="Magic Password", fill="#ffc53d", font=("Courier New", 32, "bold"))
canvas.grid(row=0, column=1)

website_label = Label(text="Website:", justify="center")
website_label.grid(row=1, column=0)

username_label = Label(text="Email/Username:", justify="center")
username_label.grid(row=2, column=0)

password_label = Label(text="Password:", justify="center")
password_label.grid(row=3, column=0)

website_input = Entry(width=62)
website_input.grid(row=1, column=1, columnspan=2)
website_input.focus()

username_input = Entry(width=85)
username_input.insert(0, "")
username_input.grid(row=2, column=1, columnspan=3)

password_input = Entry(width=62, justify="left")
password_input.grid(row=3, column=1, columnspan=2)

site_search_button = Button(text="Search Websites", highlightthickness=0, borderwidth=1, padx=3, pady=3,
                         command=search_websites, width=14)
site_search_button.grid(row=1, column=3)

# This one will be the email search button
# generate_button = Button(text="Generate Password", highlightthickness=0, borderwidth=1, padx=3, pady=3,
#                          command=generate_password, width=14)
# generate_button.grid(row=3, column=3)

generate_button = Button(text="Generate Password", highlightthickness=0, borderwidth=1, padx=3, pady=3,
                         command=generate_password, width=14)
generate_button.grid(row=3, column=3)

add_button = Button(text="Add", width=72, highlightthickness=0, borderwidth=1, padx=3, pady=3, command=add_password)
add_button.grid(row=4, column=1, columnspan=3)

window.mainloop()
