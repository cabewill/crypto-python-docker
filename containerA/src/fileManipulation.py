from json2xml import json2xml
from json2xml.utils import readfromjson
import os

def saveFile(filePath,data):
    with open(filePath, 'wb') as f:
        f.write(data)

def concertJson2xml(filePath):
    # filePath = '/data/teste.json'
    data = readfromjson(filePath)
    print(data)
    return json2xml.Json2xml(data).to_xml()

def getFileExtension(filePath):
    filename, file_extension = os.path.splitext(filePath)
    return file_extension

def checkFileExists(filePath):
    return True if os.path.isfile(filePath) else False

def getFileName(filePath):
    return os.path.basename(filePath).split(".")[0]