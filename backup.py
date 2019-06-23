# import random,json
# from flask import Flask, jsonify, make_response, request
# from scrapData import *
# from answerData import (
#     AKREDITASI,GAGAL,
#     UKT,UKT_PENGANTAR,UKT1
# )

# # Global apps define
# app = Flask(__name__)

# # Route Webhook
# @app.route('/webhook', methods=['GET', 'POST'])

# # Create webhook for request and respon
# def webhook():
#     req = request.get_json(silent=True, force=True)
#     res = processRequest(req)
#     res = json.dumps(res, indent=4)
#     r = make_response(res)
#     r.headers['Content-Type'] = 'application/json'
#     return r

# # Create a process logic
# def processRequest(req):
#     req_dict = json.loads(request.data)
#     entity_type = ""
#     entity_value = ""

#     intent = req_dict['queryResult']['intent']['displayName']
#     entity_key_val = req_dict['queryResult']['parameters']

#     for key in entity_key_val:
#         entity_value = entity_key_val[key]
#         entity_type = key
    
#     # Create respons for user who ask about 'akreditasi prodi' 
#     if intent == "Program Studi":
#         if entity_type == "program_studi":

#             if entity_value in prodiData:
#                 index = prodiData.index(entity_value)
#                 speech = random.choice(AKREDITASI).format(
#                     index=prodiData[index],
#                     akreditasi=akreditasiData[index]
#                 )
#             else:
#                 speech = random.choice(GAGAL)
    
#     # Create respons for user who ask about 'UKT Only'
#     elif intent == "UKT":
#         if entity_type == "biaya":
#             if entity_value == "UKT":
#                 speech = random.choice(UKT_PENGANTAR)
#             else:
#                 speech = random.choice(GAGAL)

#     # Create respons for user who ask about 'UKT on List'
#     elif intent in UKTLIST:
#         if entity_type == "program_studi":
#             entity_value_split = str(entity_value).split(' -')[0]
#             if entity_value_split in prodiUKT:
#                 index = prodiUKT.index(entity_value_split)

#                 # Special for UKT 1 because minus 00
#                 if intent == UKTLIST[0]:
#                     speech = random.choice(UKT1).format(
#                     ukt=uktData[int(intent[-1:])][index],
#                     uktIndex=intent[-1:],
#                     prodi=entity_value_split
#                 )

#                 # Next UKT
#                 else:
#                     speech = random.choice(UKT).format(
#                         ukt=uktData[int(intent[-1:])][index],
#                         uktIndex=intent[-1:],
#                         prodi=entity_value_split
#                     )
#             else:
#                 speech = random.choice(GAGAL)
#     # If you failed
#     else:
#         speech = random.choice(GAGAL)
#     res = results(speech)
#     return res

# # POST to dialogflow as json
# def results(speech):
#     return {
#         "fulfillmentText": speech,
#         "source":"Webhook fullfilment source"
#     }

# # Flask running
# if __name__ == "__main__":
#     app.run()