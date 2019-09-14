import json
import pyrebase

config = {
  "apiKey": "AIzaSyAn2bI9-r1lQrRdao7QQ6GUXu2ZK-f9Hvc",
  "authDomain": "htn-aydan.firebaseapp.com",
  "databaseURL": "https://htn-aydan.firebaseio.com",
  "storageBucket": "htn-aydan.appspot.com"
  }

firebase = pyrebase.initialize_app(config)

db = firebase.database()
data = {"Transcripts": {1: "Beginning of lecture"} }
db.child("Classes").child("MATH137").set(data)

def addNote(classCode, blockNumber, message):
    db.child("Classes").child(classCode).child("Transcripts").child(blockNumber).set(message)
def viewAllNotes(classCode, blockNumber):
    return(db.child("Classes").child(classCode).child("Transcripts").child(blockNumber).shallow().get())
def viewAllBlocks(classCode):
    return(db.child("Classes").child(classCode).child("Transcripts").shallow().get())
