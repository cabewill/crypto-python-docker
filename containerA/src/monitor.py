import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import fileManipulation as fm
import httpRequest as hr
import cryManage as cm

# from json2xml import json2xml
# from json2xml.utils import readfromjson
# import os

class Watcher:
    DIRECTORY_TO_WATCH = "/data"
    

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            self.observer.join()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None

        filePath = event.src_path
        file_extension = fm.getFileExtension(filePath)
        fileName = fm.getFileName(filePath)
        if file_extension == '.json': 
            data = fm.concertJson2xml(filePath)
            password, encryptedData  = cm.encryptingData(data)           
            if not cm.checkKey():
                cm.getPublicKey()
            encryptedpassword = cm.encryptingPassword(password)
            
            hr.sendFile(encryptedData,encryptedpassword,fileName)


if __name__ == '__main__':
    cm.getPublicKey()
    
    w = Watcher()
    w.run()