from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToDict
from celery import Celery, Task
from celery_config import celery_app

credentials = service_account.Credentials.from_service_account_file(
    "/Users/bill/htn-aydan.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

@celery_app.task()
def createBlockData(storage_uri, data):
    print(storage_uri)

    client = speech_v1.SpeechClient(credentials=credentials)

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'

    sample_rate_hertz = 16000
    enable_word_time_offsets = True
    language_code = "en-US"
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    enable_automatic_punctuation = True

    config = {
        "enable_word_time_offsets": enable_word_time_offsets,
        "language_code": language_code,
        "encoding": encoding,
        "enable_automatic_punctuation": enable_automatic_punctuation
    }

    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print("Waiting for operation to complete...")
    result = MessageToDict(operation.result().results[0].alternatives[0]);
    print(result)

    print("words:")
    key = data['key']
    classroom = data['classroom']

    lectureData = []
    for word in result['words']:
        print(u"Word: {} - Start: {} - End {}".format
            (word['word'], word['startTime'], word['endTime'])
        )

    return lectureData
