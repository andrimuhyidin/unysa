from flask import request
from scrapData import *
from answerData import (
    AKREDITASI,GAGAL,
    UKT,UKT_PENGANTAR,UKTLIST,UKT1
    )
import random, json

def processRequest(req):
    # Get Dialogflow Intent and Entity
    req_dict = json.loads(request.data)
    intent = req_dict['queryResult']['intent']['displayName']
    entity_key = req_dict['queryResult']['parameters']
    entity_type = []
    entity_value = []

    for key in entity_key:
        entity_type.append(key)
        entity_value.append(entity_key[key])
        
    # Create respons for user who ask about 'akreditasi prodi' 
    if intent == "Program Studi":
        if "program_studi" in entity_type:
            scrapAkreditasi()
            for entity_value_item in entity_value:
                if entity_value_item in prodiData:
                    index = prodiData.index(entity_value_item)
                    speech = random.choice(AKREDITASI).format(
                        index=prodiData[index],
                        akreditasi=akreditasiData[index]
                    )
                else:
                    speech = random.choice(GAGAL)
    # Create respons for user who ask about 'UKT Only'
    elif intent == "UKT":
        if "biaya" in entity_type:
            if "UKT" in entity_value:
                speech = random.choice(UKT_PENGANTAR)
            else:
                speech = random.choice(GAGAL)
    # Create respons for user who ask about 'UKT on List'
    elif intent in UKTLIST:
        scrapUKT()
        if "program_studi" in entity_type:
            entity_value_split_list = []
            for entity_value_item in entity_value:
                entity_value_split = str(entity_value_item).split(' -')[0]
                entity_value_split_list.append(entity_value_split)
            
            for entity_value_split_list_item in entity_value_split_list:
                if entity_value_split_list_item in prodiUKT:
                    index = prodiUKT.index(entity_value_split_list_item)
                    # Special for UKT 1 because minus 00
                    if intent == UKTLIST[0]:
                        speech = f"yeah ini UKT 1"
                        # speech = random.choice(UKT1).format(
                        # ukt=uktData[int(intent[-1:])][index],
                        # uktIndex=intent[-1:],
                        # prodi=entity_value_item
                        # )
                    # Next UKT
                    else:
                        speech = "ini ukt 2"
                        # speech = f"yeah ini {uktData[int(intent[-1:])][index]}"
                        # speech = random.choice(UKT).format(
                        #     ukt=uktData[int(intent[-1:])][index],
                        #     uktIndex=intent[-1:],
                        #     prodi=entity_value_item
                        #     )
                else:
                    speech = f"hai {intent} ini {UKTLIST[0]}"
                    # speech = random.choice(GAGAL)
    # If you failed
    else:
        speech = f"yah {entity_type} {entity_value}"
        # speech = random.choice(GAGAL)
    res = results(speech)
    return res

# POST to dialogflow as json
def results(speech):
    return {
        "fulfillmentText": speech,
        "source":"Webhook fullfilment source"
        }