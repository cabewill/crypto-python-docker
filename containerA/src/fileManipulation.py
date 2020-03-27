from json2xml import json2xml
# from json2xml.utils import readfsromjson
import os
import logging
import json

logger = logging.getLogger(__name__) 

def saveFile(filePath,data):
    with open(filePath, 'wb') as f:
        f.write(data)

def convertJson2xml(filePath):
    # filePath = '/data/teste.json'
    try:
        with open(filePath) as json_file:
            data = json.load(json_file)
        logger.debug("data json :: {}".format(data))
        dataXml = json2xml.Json2xml(data).to_xml()
        logger.debug("data xml :: {}".format(dataXml))
        return dataXml
    except ValueError as e :
        logger.error(e)
        return None
    

def getFileExtension(filePath):
    filename, file_extension = os.path.splitext(filePath)
    return file_extension

def checkFileExists(filePath):
    return True if os.path.isfile(filePath) else False

def getFileName(filePath):
    return os.path.basename(filePath).split(".")[0]