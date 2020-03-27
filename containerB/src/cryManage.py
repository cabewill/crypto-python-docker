from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import fileManipulation as fm
from enum import Enum
import pyAesCrypt
import io
import base64

PUBLIC_KEY_PATH = '/key/public_key.pem'
PRIVATE_KEY_PATH = '/key/private_key.pem'

class KeyType(Enum):
    private = 'private'
    public = 'public'

def generatePublicKey(private_key):
    deletePublicKey()
    public_key = private_key.public_key()
    pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    saveKey(KeyType.public,pem)
    return True


def generatePrivateKey():
    if not checkKey(KeyType.private):
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        generatePublicKey(private_key)
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        saveKey(KeyType.private,pem)
        

def getPublicKey():
    if checkKey(KeyType.public) and checkKey(KeyType.private):
        return fm.getFile(PUBLIC_KEY_PATH)
    else:
        generatePrivateKey()
        return fm.getFile(PUBLIC_KEY_PATH)


def saveKey(keyType,pem):
    if keyType == KeyType.private:
        return fm.saveFile(PRIVATE_KEY_PATH,pem)
    else:
        return fm.saveFile(PUBLIC_KEY_PATH,pem)

def checkKey(keyType):
    if keyType == KeyType.private:
        return fm.checkFileExists(PRIVATE_KEY_PATH)
    else:
        return fm.checkFileExists(PUBLIC_KEY_PATH)    

def deletePublicKey():
    return fm.deleteFile(PUBLIC_KEY_PATH)

def readingKey(keyType):
    key = None
    if keyType == KeyType.private:
        keyPath = PRIVATE_KEY_PATH
    else:
        keyPath = PUBLIC_KEY_PATH

    with open(keyPath, "rb") as key_file:
        key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    return key

def decryptingData(bodyJson):

    basePassword = bodyJson['password']
    baseFileData = bodyJson['fileData']
    fileName = bodyJson['filename']

    encryptedPassword = base64.b64decode(basePassword)
    encryptedData = base64.b64decode(baseFileData)

    bufferSize = 64 * 1024
    password = decryptingPassword(encryptedPassword).decode('utf-8')
    fDec = io.BytesIO() 
    ctlen = len(encryptedData)
    encryptedIo = io.BytesIO()
    encryptedIo.write(encryptedData)
    encryptedIo.seek(0)

    pyAesCrypt.decryptStream(encryptedIo, fDec, password, bufferSize, ctlen)

    byte_str = fDec.getvalue()

    return byte_str, fileName

def decryptingPassword(encryptedData):
    private_key = readingKey(KeyType.private)
    original_message = private_key.decrypt(
        encryptedData,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_message