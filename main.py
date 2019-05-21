from flask import Flask, jsonify, make_response, request
from scrap import *
import json

app = Flask(__name__)
prodi = prodiGabung
akreditasi = akreditasiGabung

# Route Webhook
@app.route('/webhook', methods=['GET', 'POST'])
# Function for response
def webhook():
    req = request.get_json(silent=True, force=True)
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    # return results
    return r

def processRequest(req):
    # Parsing the POST request body into dictionary
    req_dict = json.loads(request.data)
    entity_type = ""
    entity_value = ""
    intent = req_dict['queryResult']['intent']['displayName']

    entity_key_val = req_dict['queryResult']['parameters']
    for key in entity_key_val:
        entity_value = entity_key_val[key]
        entity_type = key
    
    # speech = "Ini adalah sampel respon dari webhook dengan output intent:"+ intent + ",entity type:"+ entity_type +",entity value:"+entity_value
    
    # Menyesuaikan Intent
    if intent == "Program Studi":
        if entity_type == "program_studi":
            if entity_value in prodi:
                speech = f"Yeee... prodi {entity_value} sama dengan yang ada di web, punya akreditasi {akreditasi}"
                # speech = """
                #          Ini adalah contoh dari respon program studi PTI, belum dibuat sih ambil datanya.
                #          """
            # elif entity_value == "Pendidikan Kimia":
            #     speech = """
            #              Ini adalah program studi pendidikan kimia
            #              """
            else:
                speech = """
                         Yaahhh gagal deh.
                         """
    else:
        speech = """
                 Saat ini sementara saya baru merespon program studi
                 """
    res = results(speech)
    return res

def results(speech):
    return {
        "fulfillmentText": speech,
        "source":"Seko webhook iki!"
    }

if __name__ == "__main__":
    app.run()