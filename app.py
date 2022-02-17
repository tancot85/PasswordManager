from tkinter import *
from functools import partial
import password_manager 

pm = password_manager.PasswordManager()

def validateLogin(email, password):
    document_id,document = pm.login(email.get(),password.get())
    pm.set_document_id(document_id)
    pm.set_document(document)
    pm.set_logged_in(True)
    print(pm.get_logged_in())
    return


# window
tkWindow = Tk()
tkWindow.geometry('400x150')
tkWindow.title('Tkinter Login Form - pythonexamples.org')

# email label and text entry box
emailLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
email = StringVar()
emailEntry = Entry(tkWindow, textvariable=email).grid(row=0, column=1)

# password label and password entry box
passwordLabel = Label(tkWindow, text="Password").grid(row=1, column=0)
password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=password,
                      show='*').grid(row=1, column=1)

validateLogin = partial(validateLogin, email, password)

# login button
loginButton = Button(tkWindow, text="Login",
                     command=validateLogin).grid(row=4, column=0)

tkWindow.mainloop()
