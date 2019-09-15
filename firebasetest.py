import json, pyrebase, requests, urllib
from flask import Flask, render_template
from celery import Celery, chain
from flask_socketio import SocketIO
from blockGen import CreateBlockDataFromWav


config = {
  "apiKey": "AIzaSyAn2bI9-r1lQrRdao7QQ6GUXu2ZK-f9Hvc",
  "authDomain": "htn-aydan.firebaseapp.com",
  "databaseURL": "https://htn-aydan.firebaseio.com",
  "storageBucket": "htn-aydan.appspot.com"
  }



firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

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

flask_app = Flask(__name__)

flask_app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery_app = Celery(
    flask_app.import_name,
    broker=flask_app.config['CELERY_BROKER_URL'],
    backend=flask_app.config['CELERY_RESULT_BACKEND']
)
celery_app.conf.update(flask_app.config)

class ContextTask(celery_app.Task):
    def __call__(self, *args, **kwargs):
        with flask_app.app_context():
            return self.run(*args, **kwargs)

celery_app.Task = ContextTask

socketio = SocketIO(flask_app)

@flask_app.route('/')
def index():
    return render_template('index.html')
    # return '<html><body><h1>Hello World</h1></body></html>'

@socketio.on('createBlockData')
def handleCreateBlockData(data):
    # print(data)
    # key = data['key']
    # print("received key: " + key)
    # print("finna look for wav:")
    # path = "data/temp/"+key+".wav"
    # result = chain(
    #     storage.child(key+".wav").download.apply_async(path),
    #     print(path + " downloaded"),
    #     CreateBlockDataFromWav(path)
    # ).delay()
    # res = result.wait();
    # print(res)


if(__name__ == '__main__'):
    socketio.run(flask_app)
