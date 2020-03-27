import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import fileManipulation as fm
import httpRequest as hr
import cryManage as cm
from utilities.logging import setup_logging
import logging

# from json2xml import json2xml
# from json2xml.utils import readfromjson
# import os
logger = logging.getLogger(__name__) 
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
            try:
                logger.info("File to be converted :: {}".format(fileName))
                data = fm.convertJson2xml(filePath)
                if data is None:
                    return None
                password, encryptedData  = cm.encryptingData(data)           
                if not cm.checkKey():
                    cm.getPublicKey()
                encryptedpassword = cm.encryptingPassword(password)
                
                hr.sendFile(encryptedData,encryptedpassword,fileName)
            except Exception as e :
                logger.error(e)


if __name__ == '__main__':
    setup_logging()
    cm.getPublicKey()    
    w = Watcher()
    w.run()