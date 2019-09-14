import json
import pyrebase
import requests


config = {
  "apiKey": "AIzaSyAn2bI9-r1lQrRdao7QQ6GUXu2ZK-f9Hvc",
  "authDomain": "htn-aydan.firebaseapp.com",
  "databaseURL": "https://htn-aydan.firebaseio.com",
  "storageBucket": "htn-aydan.appspot.com"
  }


headers = {
    'Content-Type': 'application/json',
}

params = (
    ('key', 'AIzaSyAn2bI9-r1lQrRdao7QQ6GUXu2ZK-f9Hvc'),
)

data = '{"returnSecureToken":true}'


firebase = pyrebase.initialize_app(config)

db = firebase.database()
data = {"Transcripts": {1: "Beginning of lecture"} }
db.child("Classes").child("MATH137").set(data)

def signIn(classID):
    if(classID == "password"):
        response = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp', headers=headers, params=params, data=data)
        usrId = response[idToken])
        try:
            firebase_admin.auth.verify_id_token(usrId, app=None, check_revoked=False)
            return True
        except:
            return False

def uploadNewBlock(blockArray):
    blockID = len(blockArray)-1
    db.child("Classes").child(Classcode).child("Transcripts").child(blockID).set(blockarray[-1])

def addNote(classCode, blockNumber, message):
    db.child("Classes").child(classCode).child("Transcripts").child(blockNumber).push(message)
def viewAllNotes(classCode, blockNumber):
    return(db.child("Classes").child(classCode).child("Transcripts").child(blockNumber).shallow().get())
def viewAllBlocks(classCode):
    return(db.child("Classes").child(classCode).child("Transcripts").shallow().get())
    
    
    
    
