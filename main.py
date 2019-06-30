# Import Flask module for request and respons to dialogflow
from flask import Flask, make_response, request

# Import local module processReq with all function
from processReq import *

# Define the place of webhook (module name)
app = Flask(__name__)
@app.route('/webhook', methods=['POST'])

# Create webhook module to POST the json type data
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

# Running main module in this file
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
