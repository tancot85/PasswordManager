from base64 import encode
import hashlib
from getpass import getpass
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from cryptography.fernet import Fernet


class PasswordManager:
    _cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(
        _cred, {'databasURL': "https://passwordmanager-fb698.firebaseio.com"})
    _db = firestore.client()

    _collections = []
    _logged_in = False
    _document_id = -1
    _document = ''

    def get_collections(self):
        return self._collections

    def set_collectons(self, collections):
        self._collections = collections

    def get_logged_in(self):
        return self._logged_in

    def set_logged_in(self, logged_in):
        self._logged_in = logged_in

    def get_document_id(self):
        return self._document_id

    def set_document_id(self, document_id):
        self._document_id = document_id

    def get_document(self):
        return self._document

    def set_document(self, document):
        self._document = document

    def encrypt_user_account_password(self, password):
        key = self._document['key']
        fernet = Fernet(key)
        encoded = fernet.encrypt(password.encode())
        print('encoded')
        return encoded

    def decode_user_account_password(self, encoded):
        key = self._document['key']
        fernet = Fernet(key)
        decoded = fernet.decrypt(encoded).decode()
        return decoded

    def create_user(self, email, password, name):
        for i in self._db.collection('users').get():
            n = i.to_dict()['email']
            if n == email:
                print('account already exists to this email')
                return
        hash_pass = hashlib.sha256(password.encode()).hexdigest()
        key = Fernet.generate_key()
        data = {
            'name': name,
            'email': email,
            'password': hash_pass,
            'key': key,
        }
        self._db.collection('users').document().set(data)
        print('account successfully created')

    def login(self, email, password):
        hash_pass = hashlib.sha256(password.encode()).hexdigest()
        # doc = ''
        for i in self._db.collection('users').get():
            doc = i.to_dict()
            if doc['email'] == email and doc['password'] == hash_pass:
                logged_in = True
                print('You have successfully logged in.')
                return i.id, doc
        print('You have entered a wrong username or password')
        return -1, ''

    def logout(self,):
        self._document_id = -1
        self._logged_in = False
        self.doc = ''

    def add_account(self, email, password, platform):
        encoded_password = self.encrypt_user_account_password(password)
        account = {
            'email': email,
            'platform': platform,
            'password': encoded_password,
        }
        self._db.collection('users').document(self._document_id).collection(
            'accuonts').document().set(account)
        print('account added')
        return

    def get_account(self, platform):
        account_list = []
        for i in self._db.collection('users').document(self._document_id).collections():
            for j in i.stream():
                doc = j.to_dict()
                if doc['platform'] == platform:
                    account_list.append(doc)
        for i in account_list:
            encoded_pass = i['password']
            decoded = self.decode_user_account_password(encoded_pass)
            i['password'] = decoded
        return account_list


# while True:
#     print('1. create account \n2. login\n3. exit')
#     option = int(input('Enter your option: '))
#     if option == 3:
#         print('See you soon!')
#         break
#     if option<1 or option >3:
#         print('Enter a valid option')
#         continue
#     if option == 1:
#         name = input('Enter your name: ')
#         email = input('Enter your email: ')
#         password = input('Enter your password: ')
#         create_user(email,password,name)
#         continue
#     elif option == 2:
#         login_email = input('enter the email: ')
#         login_pass = input('enter the password: ')
#         document_id, document = login(login_email, login_pass)
#         if document_id == -1:
#             continue
#         while True:
#             print('1. add account\n2. get account\n3. logout')
#             op = int(input('Enter your choice: '))
#             if op ==3:
#                 logout()
#                 break
#             elif op <1 or op>3:
#                 print('enter a valid option')
#                 continue
#             elif op ==1:
#                 platform = input('enter the platform name: ')
#                 acc_email = input('enter the email: ')
#                 acc_pass = input('enter the account password: ')
#                 add_account(acc_email,acc_pass,platform)
#                 continue
#             elif op == 2:
#                 platform = input('enter the platform name: ')
#                 account_list = get_account(platform)
#                 print(account_list)
#                 continue
