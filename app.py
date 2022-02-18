from cgitb import text
from distutils import command
from tkinter import *
from functools import partial
import password_manager

pm = password_manager.PasswordManager()


def validateLogin(email, master_password):
    # print(f'email: {email}, master_password:{master_password}')
    document_id, document = pm.login(email.get(), master_password.get())
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


def createAccount(name,email,password):
    if name.get() != "" and email.get()!= '' and password.get()!='':
        pm.create_user(email.get(),password.get(),name.get())
        create_account_window.destroy()


def submit():
    print(f'app_name:{app_name}, email:{email_id}, password:{password} ')
    if app_name.get() != "" and email_id.get() != "" and password.get() != "":
        pm.add_account(email_id.get(), password.get(), app_name.get())


def query():
    query_btn.configure(text='Hide records', command=hide)
    p_records = ''
    accounts_list = pm.get_accounts()
    for i in accounts_list:
        p_records += 'Email for '+i['platform']+' is ' + \
            i['email']+' and password is '+i['password'] + '\n'
    query_label['text'] = p_records


def hide():
    query_label['text'] = ""
    query_btn.configure(text="Show Records", command=query)


# window
tkWindow = Tk()
app_name = StringVar()
email_id = StringVar()
password = StringVar()


def create_account():
    global create_account_window
    create_account_window = Toplevel(tkWindow)
    create_account_window.geometry("400x150")
    create_account_window.title("Create Acc")

    nameLable = Label(create_account_window,text="Name").grid(row=0,column=0)
    name = StringVar()
    nameEntry = Entry(create_account_window, textvariable= name).grid(row =0,column=1)

    userEmailLabel = Label(create_account_window, text="User Name").grid(row=1, column=0)
    userEmail = StringVar()
    userEmailEntry = Entry(create_account_window, textvariable=userEmail).grid(row=1, column=1)

    # password label and password entry box
    userPasswordLabel = Label(create_account_window, text="Password").grid(row=2, column=0)
    user_master_password = StringVar()
    userPasswordEntry = Entry(create_account_window, textvariable=user_master_password,
                        show='*').grid(row=2, column=1)
    createAccountFunction = partial(createAccount,name,userEmail,user_master_password)
    createAccountButton = Button(create_account_window, text="Create Account",
                     command=createAccountFunction).grid(row=4, column=0)
    

    # print('hello there')


def open_accounts_window():
    accounts_window = Toplevel(tkWindow)
    accounts_window.title("Password Manager")
    accounts_window.geometry("500x400")
    accounts_window.minsize(600, 400)
    accounts_window.maxsize(600, 400)
    app_name_entry = Entry(accounts_window, width=30, textvariable=app_name)
    app_name_entry.grid(row=0, column=1, padx=20)
    email_id_entry = Entry(accounts_window, width=30, textvariable=email_id)
    email_id_entry.grid(row=2, column=1, padx=20)
    password_entry = Entry(accounts_window, width=30, textvariable=password)
    password_entry.grid(row=3, column=1, padx=20)

    # Create Text Box Labels
    app_name_label = Label(accounts_window, text="Application Name:")
    app_name_label.grid(row=0, column=0)
    email_id_label = Label(accounts_window, text="Email Id:")
    email_id_label.grid(row=2, column=0)
    password_label = Label(accounts_window, text="Password:")
    password_label.grid(row=3, column=0)

    submit_btn = Button(accounts_window, text="Add Record", command=submit)
    submit_btn.grid(row=5, column=0, pady=5, padx=15, ipadx=35)
    global query_btn
    query_btn = Button(accounts_window, text="Show Records", command=query)
    query_btn.grid(row=5, column=1, pady=5, padx=5, ipadx=35)
    frame = Frame(accounts_window, bg="#80c1ff", bd=5)
    frame.place(relx=0.50, rely=0.50, relwidth=0.98,
                relheight=0.45, anchor="n")
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
registerButton = Button(tkWindow, text="Create Account",
                        command=create_account).grid(row=4, column=1)

tkWindow.mainloop()
