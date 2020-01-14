from celery import Celery, Task
from celery_config import celery_app
from pydub import AudioSegment

@celery_app.task()
def fileToWav(path, newPath):
    print("Processing " + path)
    audio = AudioSegment.from_file(path)
    audio = audio.set_channels(1)
    audio.export(newPath, format="wav");
    return 0
