import json
import pyrebase
import requests
import urllib



config = {
  "apiKey": "AIzaSyAn2bI9-r1lQrRdao7QQ6GUXu2ZK-f9Hvc",
  "authDomain": "htn-aydan.firebaseapp.com",
  "databaseURL": "https://htn-aydan.firebaseio.com",
  "storageBucket": "htn-aydan.appspot.com"
  }




firebase = pyrebase.initialize_app(config)

db = firebase.database()


def signIn(classID):
    if(classID == "password"):
        headers = {
        'Content-Type': 'application/json',
        }
        data = '{"returnSecureToken":true}'
        response = requests.post('https://identitytoolkit.googleapis.com/v1/accounts:signUp?key=AIzaSyAn2bI9-r1lQrRdao7QQ6GUXu2ZK-f9Hvc', data=data)
        return True
    return False

def uploadNewBlock(blockFile):
    for i in range (1,len(blockFile["blockArray"])):
        db.child("Classes").child(Classcode).child("Transcripts").child(i).set(blockFile["blockArray"][i]["text"])

def addNote(classCode, blockNumber, message):
    db.child("Classes").child(classCode).child("Transcripts").child(blockNumber).push(message)
def viewAllNotes(classCode, blockNumber):
    return(db.child("Classes").child(classCode).child("Transcripts").child(blockNumber).shallow().get())
def viewAllBlocks(classCode):
    return(db.child("Classes").child(classCode).child("Transcripts").shallow().get())
    
def upload_file(filename, classCode):
    with open(filename, 'rb') as fd:
        my_file = fd.read()
    my_url = "https://firebasestorage.googleapis.com/v0/b/htn-aydan.appspot.com/o/"+classCode+"%2F"+filename[5:]
    my_headers = {"Content-Type": "audio/wav"}
    print(my_url)
    r=requests.post(my_url, data = my_file,headers=my_headers)
"""
    my_request = urllib.request.Request(my_url, data=my_file, headers=my_headers, method="POST")

    try:
        loader = urllib.request.urlopen(my_request)
    except urllib.error.URLError as e:
        message = json.loads(e.read())
        print(message["error"]["message"])
    else:
        print(loader.read())
"""

def downloadFile(filename, classCode):
    my_url = "https://firebasestorage.googleapis.com/v0/b/htn-aydan.appspot.com/o/"+classCode+"%2F"+filename+"?alt=media"
    try:
        loader = urllib.request.urlretrieve(my_url, "data/temp/"+filename)
    except urllib.error.URLError as e:
        message = json.loads(e.read())
        print(message["error"]["message"])
    else:
        print(loader)

#upload_file("data/whatstheweatherlike.wav", "CS135")
#downloadFile("bomb_x.wav", "CS135")


