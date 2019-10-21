import json, pyrebase, requests, urllib, os
from flask import Flask, render_template, request, make_response
from celery import chain, signature
from celery_config import celery_app
from flask_socketio import SocketIO
from blockGen import createBlockData
from convertAudio import fileToWav
from firebase_api_key import API_KEY

config = {
  "apiKey": API_KEY,
  "authDomain": "htn-aydan.firebaseapp.com",
  "databaseURL": "https://htn-aydan.firebaseio.com",
  "storageBucket": "htn-aydan.appspot.com",
  "serviceAccount": "/Users/bill/htn-aydan.json"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

db = firebase.database()


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
    CELERY_RESULT_BACKEND='redis://localhost:6379',
    TEMPLATES_AUTO_RELOAD = True
)

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

@flask_app.route('/lectureupload')
def page_lecture_upload():
    r = make_response(render_template('lectureupload.html'))
    r.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'
    print(r.headers);
    return r

@flask_app.route('/lecture')
def page_lecture():
    r = make_response(render_template('lecture.html'))
    r.headers['Access-Control-Allow-Origin'] = 'http://localhost:5000'

    return r

@celery_app.task()
def handleDownloadAudio(cloudPath, localPath):
    print("Downloading " + cloudPath)
    return storage.child(cloudPath).download(localPath)

@celery_app.task()
def handleUploadAudio(newCloudPath, localPath):
    print("Uploading " + newCloudPath)
    return storage.child(newCloudPath).put(localPath)

@celery_app.task()
def handleDeleteTempAudio(localPath):
    print("Deleting " + localPath)
    return os.remove(localPath)

@celery_app.task()
def handleProcessDoneEmit(data):
    global socketio
    socketio.emit('processing_done', data)
    print("emitting: ", data['key'])

@socketio.on('createBlockData')
def handleCreateBlockData(data):
    print(data)
    key = data['key']
    classroom = data['classroom']
    downloadURL = data['downloadURL']

    audioPath = '/' + classroom + '/' + key + ".wav"
    tempPath = 'data/temp/' + key + '.wav'
    storage_uri = 'gs://' + config['storageBucket'] + audioPath

    print("received key" , key, "for classroom", classroom)
    result = chain(
        handleDownloadAudio.si(audioPath, tempPath),
        fileToWav.si(tempPath, tempPath),
        handleUploadAudio.si(audioPath, tempPath),
        handleDeleteTempAudio.si(tempPath),
        createBlockData.si(storage_uri, data)
    )()
    res = result.wait();
    print(res);
    db.child("Transcripts").child(classroom).child(key).set(res);
    handleProcessDoneEmit(data)
    print('super donezo')

@socketio.on('generateKey')
def handleKeyGen():
    socketio.emit('message', db.generate_key())

if(__name__ == '__main__'):
    socketio.run(flask_app)
