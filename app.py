from tkinter import *
from functools import partial
import password_manager 

pm = password_manager.PasswordManager()


query_btn = ''

def validateLogin(email, master_password):
    # print(f'email: {email}, master_password:{master_password}')
    document_id,document = pm.login(email.get(),master_password.get())
    if(document_id != -1):
        pm.set_document_id(document_id)
        pm.set_document(document)
        pm.set_logged_in(True)
        print(pm.get_logged_in())
        open_accounts_window()  
        return
    else:
        print('not logged in')
    return

def submit():
    print(f'app_name:{app_name}, email:{email_id}, password:{password} ')
    if app_name.get() !="" and email_id.get() != "" and password.get() != "":
        pm.add_account(email_id.get(), password.get(), app_name.get())

def query():
    query_btn.configure(text = 'Hide records')




# window
tkWindow = Tk()
app_name = StringVar()
email_id = StringVar()
password = StringVar()
def open_accounts_window():
    accounts_window = Toplevel(tkWindow)
    accounts_window.title("Password Manager")
    accounts_window.geometry("500x400")
    accounts_window.minsize(600, 400)
    accounts_window.maxsize(600, 400)
    app_name_entry = Entry(accounts_window, width=30,textvariable=app_name)
    app_name_entry.grid(row=0, column=1, padx=20)
    email_id_entry = Entry(accounts_window, width=30,textvariable=email_id)
    email_id_entry.grid(row=2, column=1, padx=20)
    password_entry = Entry(accounts_window, width=30,textvariable=password)
    password_entry.grid(row=3, column=1, padx=20)

    #Create Text Box Labels
    app_name_label = Label(accounts_window, text = "Application Name:")
    app_name_label.grid(row=0, column=0)
    email_id_label = Label(accounts_window, text = "Email Id:")
    email_id_label.grid(row=2, column=0)
    password_label = Label(accounts_window, text = "Password:")
    password_label.grid(row=3, column=0)
    
    submit_btn = Button(accounts_window, text = "Add Record", command = submit)
    submit_btn.grid(row = 5, column=0, pady=5, padx=15, ipadx=35)
    query_btn = Button(accounts_window, text = "Show Records", command = query)
    query_btn.grid(row=5, column=1, pady=5, padx=5, ipadx=35) 
    frame = Frame(accounts_window, bg="#80c1ff", bd=5)
    frame.place(relx=0.50, rely=0.50, relwidth=0.98, relheight=0.45, anchor = "n")
    global query_label
    query_label = Label(frame, anchor="nw", justify="left")
    query_label.place(relwidth=1, relheight=1)  

tkWindow.geometry('400x150')
tkWindow.title('Tkinter Login Form - pythonexamples.org')

# email label and text entry box
emailLabel = Label(tkWindow, text="User Name").grid(row=0, column=0)
email = StringVar()
emailEntry = Entry(tkWindow, textvariable=email).grid(row=0, column=1)

# password label and password entry box
passwordLabel = Label(tkWindow, text="Password").grid(row=1, column=0)
master_password = StringVar()
passwordEntry = Entry(tkWindow, textvariable=master_password,
                      show='*').grid(row=1, column=1)

validateLogin = partial(validateLogin, email, master_password)

# login button
loginButton = Button(tkWindow, text="Login",
                     command=validateLogin).grid(row=4, column=0)

tkWindow.mainloop()
