from flask import Flask,request
import fileManipulation as fm
import cryManage as cm
server = Flask(__name__)

@server.route("/receiver", methods=['POST'])
def receiver():
    data, fileName = cm.decryptingData(request.json)
    fileName
    fm.saveFile("/data/{}.xml".format(fileName),data )
    return 'success'

@server.route("/getKey", methods=['GET'])
def getPublicKey():
    data = cm.getPublicKey()
    return data, 200

if __name__ == "__main__":
    server.run(host='0.0.0.0', debug=True)