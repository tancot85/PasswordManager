import firebase_admin
from firebase_admin import credentials,db
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{'databasURL':"https://passwordmanager-fb698.firebaseio.com"})
dab = firestore.client()
# data = {
#     'platform' : "discord",
#     'email':"another@abc.com",
#     'password':"another"
# }
# dab.collection("someone").document().set(data)
# dab.collection("users").document().set(data)

# print(dab.collection("users").get())
for i in dab.collection("users").get():
    print(i.to_dict())
    col = dab.collection("users").document(i.id).collections()
    for c in col:
        for doc in c.stream():
            print(doc.to_dict())
    # print(dab.collection("users").document(i.id).collections())



