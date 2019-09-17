import json, pyrebase, requests, urllib, os
from flask import Flask, render_template, request, make_response
from celery import chain, signature
from celery_config import celery_app
from flask_socketio import SocketIO
from blockGen import CreateBlockDataFromWav, createBlockData


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
#
# celery_app = Celery(
#     flask_app.import_name,
#     broker=flask_app.config['CELERY_BROKER_URL'],
#     backend=flask_app.config['CELERY_RESULT_BACKEND']
# )
# celery_app.conf.update(flask_app.config)
#
# class ContextTask(celery_app.Task):
#     def __call__(self, *args, **kwargs):
#         with flask_app.app_context():
#             return self.run(*args, **kwargs)
#
# celery_app.Task = ContextTask

socketio = SocketIO(flask_app)

@flask_app.route('/')
def page_index():
    r = make_response(render_template('index.html'))
    return r;
    # return '<html><body><h1>Hello World</h1></body></html>'

@flask_app.route('/classroom')
def page_classroom():
    r = make_response(render_template('classroom.html'))
    r.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
    print(r.headers);
    return r

@flask_app.route('/lecture')
def page_lecture():
    r = make_response(render_template('lecture.html'))
    r.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'

    return r

@celery_app.task()
def handleDownload(key, classroom, path):#TODO append to appropriate class later
    return storage.child(classroom+"/"+key+".wav").download(path)

@celery_app.task()
def handleUpload(key, classroom, data, path):
    print("uploading shit:")
    newData = data.copy();
    newData['key'] = key
    newData['classroom'] = classroom
    with open(path, 'w') as outfile:
        json.dump(newData, outfile)
    return storage.child(classroom+"/"+key+".json").put(path)

@celery_app.task()
def handleDeleteFile(path):
    print("deleting", path)
    os.remove(path)
    return

@celery_app.task()
def handleProcessDoneEmit(data):
    global socketio
    socketio.emit('processing_done', data)
    print("emitting", data['key'])
    return

@socketio.on('createBlockData')
def handleCreateBlockData(data):
    print(data)
    key = data['key']
    classroom = data['classroom']
    print("received key" , key, "for classroom", classroom)
    print("finna look for wav:")
    path1 = "data/temp/"+key+".wav"
    path2 = "data/temp/"+key+".json"
    #from blockGen import CreateBlockDataFromWav
    result = chain(handleDownload.s(key, classroom, path1), createBlockData.si(path1))()
    res = result.wait();
    chain(handleUpload.s(key, classroom, res, path2), handleDeleteFile.si(path1), handleDeleteFile.si(path2))()
    handleProcessDoneEmit(data) # TODO async handleProcessEmit with the main thread
    print('super donezo')

@socketio.on('generateKey')
def handleKeyGen():
    socketio.emit('message', db.generate_key())

if(__name__ == '__main__'):
    socketio.run(flask_app)
