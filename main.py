from flask import Flask, make_response, request
from processReq import *

app = Flask(__name__)
@app.route('/webhook', methods=['GET', 'POST'])

def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r
    
if __name__ == "__main__":
    app.run()
