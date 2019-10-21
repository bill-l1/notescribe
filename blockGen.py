from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.oauth2 import service_account
from google.protobuf.json_format import MessageToDict
from celery import Celery, Task
from celery_config import celery_app
from copy import deepcopy

credentials = service_account.Credentials.from_service_account_file(
    "/Users/bill/htn-aydan.json",
    scopes=["https://www.googleapis.com/auth/cloud-platform"],
)

PAUSE_THRESHOLD = 1
WORD_COUNT_MINIMUM = 15
EMPTY_BLOCK = {
    'text': "",
    'startTime': 0,
    'endTime': 0
}

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

    key = data['key']
    classroom = data['classroom']

    print("Generating blocks...")
    global PAUSE_THRESHOLD, WORD_COUNT_MINIMUM, EMPTY_BLOCK
    lectureBlocks = []

    for result in operation.result().results:
        result = MessageToDict(result.alternatives[0]);
        currentBlock = deepcopy(EMPTY_BLOCK)
        currentBlock['startTime'] = float(result['words'][0]['startTime'][:-1])

        for word in result['words']:
            startTime = float(word['startTime'][:-1])
            word['startTime'] = startTime
            endTime = float(word['endTime'][:-1])
            word['endTime'] = endTime
            wordStr = word['word']
            currentNumWords = 0

            currentBlock['text'] += wordStr + " "
            currentNumWords += 1

            if (((startTime - startTime) > PAUSE_THRESHOLD) or ((wordStr[-1] in ['!', '?', '.']) and (currentNumWords > WORD_COUNT_MINIMUM))):
                currentBlock['endTime'] =  endTime
                lectureBlocks.append(deepcopy(currentBlock))
                currentBlock = deepcopy(EMPTY_BLOCK)
                currentBlock['startTime'] = endTime

        currentBlock['endTime'] =  endTime
        lectureBlocks.append(deepcopy(currentBlock))

    print("Blocks created.")

    return lectureBlocks
