import os

def saveFile(filePath,data):
    with open(filePath, 'wb') as f:
        f.write(data)

def getFile(filePath):
    with open(filePath, 'r') as content_file:
        content = content_file.read()
    return content

def checkFileExists(filePath):
    return True if os.path.isfile(filePath) else False

def deleteFile(filePath):
    if checkFileExists(filePath):
        os.remove(filePath)
        return True
    else:
        return False
