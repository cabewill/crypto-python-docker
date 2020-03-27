import requests
import base64

RECEIVER_URL = "http://receive:5000/"

def sendFile(fileData,encryptedpassword,fileName):
    url = RECEIVER_URL + "/receiver"

    basePassword = base64.encodestring(encryptedpassword)
    baseFileData = base64.encodestring(fileData)    

    requests.post(url, json = {"fileData":baseFileData.decode('utf-8'), "password":basePassword.decode('utf-8'), "filename":fileName})

def getPublicKey():
    url = RECEIVER_URL + "/getKey"
    r = requests.get(url)
    if r.status_code == 200:
        return r.content
    else:
        return 'failed'