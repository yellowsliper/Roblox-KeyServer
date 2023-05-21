import flask
import uuid
import json
import time
import threading

app = flask.Flask(__name__)
hwidKeys = {

}

with open('./data/hwidKeys.json', 'r') as f:
    hwidKeys = json.load(f)

def saveJson():
    try:
        hwidKeys.pop('null')
    except:
        pass
    with open('./data/hwidKeys.json', 'w') as f:
        json.dump(hwidKeys, f, indent="\t")

def whilerun(func: str, t: int):
    def run():
        while True:
            func()
            time.sleep(t)
    threading.Thread(target=run).start()

def checkHWID(HWID: str):
    if HWID in hwidKeys.keys():
        return True
    else:
        return False

@app.route('/')
def home():
    return flask.redirect(flask.url_for('error'))

@app.route('/error')
def error():
    return "Error"

@app.route('/get-key')
def getKey():
    HWID = flask.request.args.get('masterKey')
    if not HWID in hwidKeys.keys():
        hwidKeys[HWID] = [
            str(uuid.uuid4()).replace('-', ''),

        ]
    return hwidKeys[HWID]

@app.route('/check-key')
def checkKey():
    print(HWID)
    HWID = flask.request.args.get('masterKey')
    if checkHWID(HWID):
        return "true"
    else:
        return "false"

@app.route('/fakescript')
def returnscript():
    return "print(\"Hello World!\")"

whilerun(saveJson, 1)
app.run(host='0.0.0.0', port=5000, debug=False)
