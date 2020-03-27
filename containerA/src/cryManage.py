from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import fileManipulation as fm
from enum import Enum 
import httpRequest as hr
import secrets
import string
import pyAesCrypt
import io


PUBLIC_KEY_PATH = '/key/public_key.pem'

def getPublicKey():
    pem = hr.getPublicKey()
    if not pem == 'failed':
        fm.saveFile(PUBLIC_KEY_PATH,pem)
    return True

def checkKey():
    return fm.checkFileExists(PUBLIC_KEY_PATH)    

def readingKey():
    public_key = None
    with open(PUBLIC_KEY_PATH, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key

def generatePassword():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(25))
    return password

def encryptingPassword(data):
    if isinstance(data,str):
        data = data.encode()
    public_key = readingKey()
    encrypted = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return encrypted


def encryptingData(data):
    bufferSize = 64 * 1024
    if isinstance(data,str):
        data = data.encode()
    password = generatePassword()
    fIn = io.BytesIO(data)
    fCiph = io.BytesIO()
    fCiph.seek(0)
    pyAesCrypt.encryptStream(fIn, fCiph, password, bufferSize)

    byte_str = fCiph.getvalue()

    return password, byte_str